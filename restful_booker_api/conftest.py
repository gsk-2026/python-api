import os


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

