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
    db_url = os.getenv("APP_DB_URL", "jdbc:oracle:thin:@10.0.0.252:1521:free")
    db_user = os.getenv("APP_DB_USER", "system")
    db_pswd = os.getenv("APP_DB_PSWD", "Sankui2026")
    db_driver = os.getenv("APP_DB_DRIVER", "oracle.jdbc.OracleDriver")
    db_platform = os.getenv("APP_DB_PLATFORM", "org.hibernate.dialect.OracleDialect")
    db_ddl = os.getenv("APP_DB_DDL_AUTO", "validate")

    cmd = [
        "java",
        "-Dspring.profiles.active=qatest",
        f"-Dspring.datasource.url={db_url}",
        f"-Dspring.datasource.username={db_user}",
        f"-Dspring.datasource.password={db_pswd}",
        f"-Dspring.datasource.driver-class-name={db_driver}",
        f"-Dspring.jpa.database-platform={db_platform}",
        f"-Dspring.jpa.hibernate.ddl-auto={db_ddl}",
        f"-Dspring.jpa.properties.hibernate.dialect={db_platform}",
        "-jar",
        JAR_PATH]

    java_process = subprocess.Popen(
        cmd,
        cwd=PROJECT_ROOT,
        stdout=stdout_file,    #subprocess.PIPE,  #subprocess.DEVNULL,     #None,
        stderr=stderr_file,    #subprocess.PIPE,  #subprocess.DEVNULL,     #None,
        env=os.environ
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