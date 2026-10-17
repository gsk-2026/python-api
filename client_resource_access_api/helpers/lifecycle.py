import os
import tempfile
import time
import subprocess
import psutil
import requests
from config.settings import ApiEndpoints


PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JAR_PATH = os.path.join(PROJECT_ROOT, "data", "client-resource-access-api-0.0.1-SNAPSHOT.jar")

stdout_file = tempfile.TemporaryFile(mode="w+")
stderr_file = tempfile.TemporaryFile(mode="w+")

java_process = None


def start_app():
    global java_process
    cmd = ["java", "-Dspring.profiles.active=qatest", "-jar", JAR_PATH]

    java_process = subprocess.Popen(
        cmd,
        cwd=PROJECT_ROOT,
        stdout=stdout_file,    #subprocess.PIPE,  #subprocess.DEVNULL,     #None,
        stderr=stderr_file     #subprocess.PIPE   #subprocess.DEVNULL      #None
    )

    ready = False
    for _ in range(60):
        if java_process.poll() is not None:
            stdout_file.seek(0)
            stderr_file.seek(0)
            raise RuntimeError(f"Java app exited prematurely:\nSTDOUT: {stdout_file.read()}\nSTDERR: {stderr_file.read()}")#stdout, stderr = java_process.communicate()
            #stdout, stderr = java_process.communicate()
            #raise RuntimeError(f"Java app exited prematurely:\nSTDOUT: {stdout.decode()}\nSTDERR: {stderr.decode()}")

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
        stdout_file.seek(0)
        stderr_file.seek(0)
        logs_stdout = stdout_file.read()
        logs_stderr = stderr_file.read()
        stop_app()
        raise TimeoutError(
            f"Server failed to reach UP status.\nSTDOUT: {logs_stdout}\nSTDERR: {logs_stderr}"
        )
        #stop_app()
        #raise TimeoutError(f"Client_Resource_Access Server failed to reach UP status at {ApiEndpoints.base_url()}")

    return java_process


def stop_app():
    global java_process, stdout_file, stderr_file
    if java_process:
        try:
            parent = psutil.Process(java_process.pid)
            for child in parent.children(recursive=True):
                child.kill()
            parent.kill()
        except psutil.NoSuchProcess:
            pass
        java_process = None
    #
    if stdout_file:
        stdout_file.close()
    if stderr_file:
        stderr_file.close()