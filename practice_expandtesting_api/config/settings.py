import os
from enum import Enum
from dotenv import load_dotenv


load_dotenv()


#####################################################################
# API Endpoints
#####################################################################

API_BASE_URL = os.getenv(
    "API_BASE_URL", "https://practice.expandtesting.com/notes/api"
)

API_HEALTH_CHECK_ENDPOINT = f"{API_BASE_URL}/health-check"

API_USER_REGISTER_ENDPOINT = f"{API_BASE_URL}/users/register"
API_USER_LOGIN_ENDPOINT = f"{API_BASE_URL}/users/login"
API_USER_PROFILE_ENDPOINT = f"{API_BASE_URL}/users/profile"
API_USER_CHANGE_PASSWORD_ENDPOINT = f"{API_BASE_URL}/users/change-password"
API_USER_LOGOUT_ENDPOINT = f"{API_BASE_URL}/users/logout"
API_USER_DELETE_ACCOUNT_ENDPOINT = f"{API_BASE_URL}/users/delete-account"

API_NOTES_ENDPOINT = f"{API_BASE_URL}/notes"



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

class UserTestStep(Enum):
    GUEST = 0
    HEALTH_CHECK = 1
    USER_REGISTRATION = 2
    USER_LOGIN = 3
    ACCESS_GRANTED = 4
    USER_LOGOUT = 5
    ACCOUNT_DELETION = 6