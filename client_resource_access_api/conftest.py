import os
import pytest
from helpers.lifecycle import start_app, stop_app


PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
JAR_PATH = os.path.join(PROJECT_ROOT, "data", "client-resource-access-api-0.0.1-SNAPSHOT.jar")


@pytest.fixture(scope="session", autouse=True)
def manage_jar_lifecycle():
    process = start_app()
    yield process
    stop_app()

'''
@pytest.fixture(scope="session", autouse=True)
def manage_jar_lifecycle():
    cmd = ["java", "-Dspring.profiles.active=qatest", "-jar", JAR_PATH]
    process = subprocess.Popen(
        cmd, cwd=PROJECT_ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )
    ready = False
    for _ in range(60):
        if process.poll() is not None:
            pytest.fail("Java application exited prematurely.")
        try:
            res = requests.get(ApiEndpoints.health_url(), proxies={"http": None, "https": None}, timeout=2)
            if res.status_code == 200 and res.json().get("status") == "UP":
                ready = True
                break
        except (requests.exceptions.RequestException):
            time.sleep(1)
    if not ready:
        process.kill()
        pytest.fail(f"Server failed to respond on {ApiEndpoints.base_url()}")

    # transfer then resume the flow
    yield process

    # teardown
    try:
        parent = psutil.Process(process.pid)
        for child in parent.children(recursive=True):
            child.kill()
        parent.kill()
    except psutil.NoSuchProcess:
        pass
'''


def pytest_addoption(parser):
    parser.addoption(
        "--test_env",
        action="store",
        default=None,  # Leave default None so settings.py or .env can act as fallbacks
        help="Target test environment: DIT, SIT, UAT"
    )


def pytest_configure(config):
    test_env = config.getoption("--test_env")

    if test_env:
        os.environ["TEST_ENV"] = test_env.upper()
