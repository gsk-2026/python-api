import os
import time
import subprocess
import psutil
import requests
from config.settings import ApiEndpoints


PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JAR_PATH = os.path.join(PROJECT_ROOT, "data", "client-resource-access-api-0.0.1-SNAPSHOT.jar")

java_process = None


def start_app():
    global java_process
    cmd = ["java", "-Dspring.profiles.active=qatest", "-jar", JAR_PATH]

    java_process = subprocess.Popen(
        cmd,
        cwd=PROJECT_ROOT,
        stdout=None,  #subprocess.DEVNULL,
        stderr=None   #subprocess.DEVNULL
    )

    ready = False
    for _ in range(60):
        if java_process.poll() is not None:
            raise RuntimeError("Client_Resource_Access Java application exited prematurely.")

        try:
            res = requests.get(
                ApiEndpoints.health_url(),
                proxies={"http": None, "https": None},
                timeout=2
            )
            if res.status_code == 200 and res.json().get("status") == "UP":
                ready = True
                break
        except requests.exceptions.RequestException:
            time.sleep(1)

    if not ready:
        stop_app()
        raise TimeoutError(f"Client_Resource_Access Server failed to reach UP status at {ApiEndpoints.base_url()}")

    return java_process


def stop_app():
    global java_process
    if java_process:
        try:
            parent = psutil.Process(java_process.pid)
            for child in parent.children(recursive=True):
                child.kill()
            parent.kill()
        except psutil.NoSuchProcess:
            pass
        java_process = None
