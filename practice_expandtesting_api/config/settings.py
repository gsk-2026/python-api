import os
from enum import Enum
from dotenv import load_dotenv


# Load local .env file if it exists
load_dotenv()


#####################################################################
# API Configuration
#####################################################################

API_TIMEOUT = int(os.getenv("API_TIMEOUT", "5"))   # second



#####################################################################
# Test Configuration
#####################################################################

TEST_SLEEP_IN_SECOND = 5
TEST_PERFORMANCE_LOOP = 10
TEST_DEFAULT_HEADERS = {"Accept": "application/json", "Content-Type": "application/json"}



#####################################################################
# User Test Step on the API workflow
#####################################################################

class UserTestSteps(Enum):
    GUEST = 0
    HEALTH_CHECK = 1
    USER_REGISTRATION = 2
    USER_LOGIN = 3
    ACCESS_GRANTED = 4
    USER_LOGOUT = 5
    ACCOUNT_DELETION = 6



#####################################################################
# API Endpoints
#####################################################################

DEFAULT_URLS = {
    "DFT": "https://practice.expandtesting.com/notes/api",
    "DIT": "https://practice.expandtesting.com/notes/api",
    "SIT": "https://practice.expandtesting.com/notes/api",
    "UAT": "https://practice.expandtesting.com/notes/api",
}

def get_api_base_url() -> str:
    test_env = os.getenv("TEST_ENV", "DFT").upper()
    return os.getenv("API_BASE_URL", DEFAULT_URLS.get(test_env, DEFAULT_URLS["DFT"]))


class ApiEndpoints:

    @classmethod
    def base_url(cls) -> str:
        return f"{get_api_base_url()}"

    @classmethod
    def health_check(cls) -> str:
        return f"{get_api_base_url()}/health-check"

    @classmethod
    def user_register(cls) -> str:
        return f"{get_api_base_url()}/users/register"

    @classmethod
    def user_login(cls) -> str:
        return f"{get_api_base_url()}/users/login"

    @classmethod
    def user_profile(cls) -> str:
        return f"{get_api_base_url()}/users/profile"

    @classmethod
    def user_change_password(cls) -> str:
        return f"{get_api_base_url()}/users/change-password"

    @classmethod
    def user_logout(cls) -> str:
        return f"{get_api_base_url()}/users/logout"

    @classmethod
    def user_delete_account(cls) -> str:
        return f"{get_api_base_url()}/users/delete-account"

    @classmethod
    def notes(cls) -> str:
        return f"{get_api_base_url()}/notes"
