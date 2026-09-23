import uuid
import requests
import pytest
from pytest_check import check

from config.settings import (
    API_BASE_URL,
    API_USER_REGISTER_ENDPOINT,
    API_USER_LOGIN_ENDPOINT,
    API_USER_DELETE_ACCOUNT_ENDPOINT,
    API_NOTES_ENDPOINT,
    API_TIMEOUT,
    UserTestStep,
    TEST_DEFAULT_HEADERS
)



def manage_context_user_and_note_id_template() -> dict:
    unique_id = uuid.uuid4().hex[:8]
    user_payload = {
        "name": f"QATester {unique_id}",
        "email": f"qa_tester_{unique_id}@qateam.com",
        "password": f"QATester_PSWD@{unique_id}!"
    }
    context = {
        "user_test_step": UserTestStep.GUEST,
        "headers_default": TEST_DEFAULT_HEADERS,
        "headers_login": None,
        "credentials": {"email": user_payload["email"], "password": user_payload["password"]},
        "user_payload": user_payload,
        "token": None,
        "note_id": [],
        "response": None
    }
    return context



def manage_user_deletion(user_context) -> None:
    if user_context["user_test_step"] in [UserTestStep.GUEST, UserTestStep.ACCOUNT_DELETION]:
        return

    if user_context["user_test_step"] in [UserTestStep.USER_REGISTRATION, UserTestStep.USER_LOGOUT]:
        user_payload = user_context["user_payload"]
        user_credential = {"email": user_payload["email"], "password": user_payload["password"]}
        headers = user_context["headers_default"]
        response = requests.post(API_USER_LOGIN_ENDPOINT, json=user_credential, headers=headers)
        if response.status_code == 200:
            user_context["token"] = response.json()["data"]["token"]
            user_context["headers_login"] = {**user_context["headers_default"], "x-auth-token": user_context["token"]}
            user_context["user_test_step"] = UserTestStep.USER_LOGIN

    if user_context["user_test_step"] == UserTestStep.USER_LOGIN:
        response = requests.get(API_BASE_URL, headers={"Accept": "application/json"})
        if response.status_code == 200:
            user_context["user_test_step"] = UserTestStep.ACCESS_GRANTED

    if user_context["user_test_step"] == UserTestStep.ACCESS_GRANTED:
        for idx in range(len(user_context["note_id"])):
            headers = user_context["headers_login"]
            resp_delete = requests.delete(f"{API_NOTES_ENDPOINT}/{user_context["note_id"][idx]}", headers=headers, timeout=API_TIMEOUT)
            check.equal(resp_delete.status_code, 200, msg=f"Failed to delete note with 'status_code': {resp_delete.status_code}")

    # delete the user
    headers = user_context["headers_login"]
    response = requests.delete(API_USER_DELETE_ACCOUNT_ENDPOINT, headers=headers)
    if response.status_code == 200:
        user_context["user_test_step"] = UserTestStep.ACCOUNT_DELETION



def manage_user_context_register_and_login() -> dict:
    user_context = manage_context_user_and_note_id_template()
    user_payload = user_context.get("user_payload", {})
    resp_register = requests.post(API_USER_REGISTER_ENDPOINT, json = user_payload)
    check.is_in(resp_register.status_code, [200, 201], msg=f"User registration failed with status code {resp_register.status_code}")
    user_context["response"] = resp_register

    resp_login = requests.post(API_USER_LOGIN_ENDPOINT, json = {"email": user_payload["email"], "password": user_payload["password"]})
    check.equal(resp_login.status_code, 200, msg=f"User login failed with status code {resp_login.status_code}")
    user_context["response"] = resp_login

    user_context["token"] = resp_login.json().get("data").get("token")
    user_context["headers_login"] = {"x-auth-token": user_context["token"] , **TEST_DEFAULT_HEADERS}
    user_context["user_test_step"] = UserTestStep.USER_LOGIN

    return user_context



@pytest.fixture
def manage_context_primary_user_and_note_id_template():
    context = manage_context_user_and_note_id_template()
    yield context
    manage_user_deletion(context)



@pytest.fixture
def manage_context_secondary_user_and_note_id_template():
    context = manage_context_user_and_note_id_template()
    yield context
    manage_user_deletion(context)



@pytest.fixture
def manage_context_primary_user_register():
    user_register_context = manage_context_user_and_note_id_template()
    user_payload = user_register_context.get("user_payload")

    resp_register = requests.post(API_USER_REGISTER_ENDPOINT, headers = {"Content-Type": "application/json"}, json=user_payload)
    if resp_register.status_code == 201:
        user_register_context["user_test_step"] = UserTestStep.USER_REGISTRATION
        user_register_context["response"] = resp_register

        yield user_register_context

        manage_user_deletion(user_register_context)



@pytest.fixture
def manage_context_primary_user_register_login():
    user_context = manage_user_context_register_and_login()
    yield user_context
    manage_user_deletion(user_context)



@pytest.fixture
def manage_context_secondary_user_register_login():
    user_context = manage_user_context_register_and_login()
    yield user_context
    manage_user_deletion(user_context)



@pytest.fixture
def manage_context_user_register_login_post_note():
    user_context = manage_user_context_register_and_login()

    note_payload = {
        "title": "QATeam Test Task : Note Title",
        "description": "QATeam Test Task : Note Description",
        "category": "Work",      # Home, Work, Personal
        "completed": False
    }

    response = requests.post(
        API_NOTES_ENDPOINT,
        headers = user_context.get("headers_login"),
        json = note_payload,
        timeout = API_TIMEOUT
    )
    check.is_in(response.status_code, [200, 201], msg=f"Note creation failed with status code {response.status_code}")

    note_data = response.json().get("data", {})
    note_id = note_data.get("id")
    note_context = {
        "note_data": note_data,
        "note_id": note_id,
        "already_deleted": False
    }

    user_note_context = { "user_context": user_context,  "note_context": note_context }

    yield user_note_context

    headers = user_context.get("headers_login")

    note_deleted = note_context.get("already_deleted")
    if not note_deleted:
        resp_delete = requests.delete(f"{API_NOTES_ENDPOINT}/{user_note_context.get("note_context", {}).get("note_id")}", headers=headers, timeout=API_TIMEOUT)
        check.is_in(resp_delete.status_code, [200, 202, 204, 404, 410], msg=f"Failed to delete note with status code {resp_delete.status_code}")

    user_test_step = user_context.get("user_test_step")
    if user_test_step != UserTestStep.ACCOUNT_DELETION:
        resp_delete = requests.delete(API_USER_DELETE_ACCOUNT_ENDPOINT, headers=headers, timeout=API_TIMEOUT)
        check.is_in(resp_delete.status_code, [200, 202, 204, 404, 410], msg=f"Failed to delete user acct with status code {resp_delete.status_code}")

