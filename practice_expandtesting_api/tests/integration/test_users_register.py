import pytest
import requests
from pytest_check import check

from config.settings import (
    API_BASE_URL,
    API_USER_REGISTER_ENDPOINT,
    UserTestStep,
    TEST_SLEEP_IN_SECOND
)


"""
Integration test for the API Endpoints: https://practice.expandtesting.com/notes/api/api-docs/#/Users/post_users_register

curl -X 'POST' \
  'https://practice.expandtesting.com/notes/api/users/register' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'name={name}&email={email}&password={password}'
"""


def test_users_register_success_201(manage_context_primary_user_register):
    context = manage_context_primary_user_register
    user_payload = context.get("user_payload")
    response = context.get("response")
    check.equal(response.status_code, 201, f"Expected 201, but got {response.status_code}")
    check.equal(manage_context_primary_user_register["user_test_step"], UserTestStep.USER_REGISTRATION)

    resp_json = response.json()
    check.is_instance(resp_json, dict, msg=f"Expected resp_json to be a JSON object, but got as {type(resp_json).__name__}.")
    check.is_in("success", resp_json, msg="Expected 'success' property in resp_json, but it is missing")
    check.is_true(resp_json["success"])
    check.is_in("status", resp_json, msg="Expected 'status' property in resp_json, but it is missing")
    check.equal(resp_json["status"], 201)
    check.is_in("message", resp_json, msg="Expected 'message' property in resp_json, but it is missing")
    check.equal(resp_json["message"], "User account created successfully")

    check.is_in("data", resp_json, msg="Expected 'data' property in resp_json, but it is missing")
    resp_json_data = resp_json["data"]
    check.is_instance(resp_json_data, dict, msg=f"Expected resp_json_data to be a JSON object, but got as {type(resp_json_data).__name__}.")
    check.is_in("name", resp_json_data, msg="Expected 'name' property in resp_json_data, but it is missing")
    check.equal(resp_json_data["name"], user_payload["name"])
    check.is_in("email", resp_json_data, msg="Expected 'email' property in resp_json_data, but it is missing")
    check.equal(resp_json_data["email"], user_payload["email"])
    check.is_in("id", resp_json_data, msg="Expected 'id' property in resp_json_data, but it is missing")
    check.is_instance(resp_json_data["id"], str)
    check.greater(len(resp_json_data["id"]), 0)

    sensitive_terms = [
        "connection_string",
        "db_password",
        "db_user",
        "db_host",
        "apikey",
        "_key",
        "kry_",
        "_id",
        "id_",
        "client",
        "username",
        "login",
        #"email",
        "phone",
        "ssn",
        "social_security",
        "birth_date",
        "dob",
        "pin",
        "pwd",
        "passwd",
        "password",
        "secret",
        "authorization",
        "token",
        "session_id",
        "bearer",
        "signature"
    ]
    body = response.text.lower()
    for term in sensitive_terms:
        check.is_not_in(term, body, "Security ERROR: user secret should NOT in response payload!")



def test_users_register_duplicate_409(manage_context_primary_user_register):
    context = manage_context_primary_user_register
    user_payload = context.get("user_payload")

    new_resp = requests.post(API_USER_REGISTER_ENDPOINT, headers={"Content-Type": "application/json"}, json=user_payload)
    check.equal(new_resp.status_code, 409, f"Expected 409, but got {new_resp.status_code}")
    check.is_false(new_resp.json()["success"], f"Expected 'False'', but got {new_resp.json()['success']}")
    check.is_in("already exists", new_resp.json()["message"].lower(), f"Expected 'already exists', but got {new_resp.json()['message']}")



@pytest.mark.parametrize("missing_field", ["name", "email", "password"])
def test_users_register_missing_required_fields_400(missing_field, manage_context_primary_user_register):
    context = manage_context_primary_user_register
    user_payload = context.get("user_payload")
    new_user_payload = user_payload.copy()
    del new_user_payload[missing_field]

    new_resp = requests.post(API_USER_REGISTER_ENDPOINT, headers={"Content-Type": "application/json"}, json=new_user_payload)
    check.equal(new_resp.status_code, 400, f"Expected 400, but got {new_resp.status_code}")

    resp_data = new_resp.json()
    check.is_false(resp_data["success"], f"Expected 'False', but got {resp_data['success']}")
    check.is_in(missing_field, resp_data["message"].lower(), f"Expected '{missing_field}' in message, but got {resp_data['message']}")



@pytest.mark.parametrize("empty_field", ["name", "email", "password"])
def test_users_register_empty_required_fields_400(empty_field, manage_context_primary_user_register):
    context = manage_context_primary_user_register
    user_payload = context.get("user_payload")
    new_user_payload = user_payload.copy()
    new_user_payload[empty_field] = "   "

    new_res = requests.post(API_USER_REGISTER_ENDPOINT, headers={"Content-Type": "application/json"}, json=new_user_payload)
    check.equal(new_res.status_code, 400, f"Expected 400, but got {new_res.status_code}")

    res_data = new_res.json()
    check.is_false(res_data["success"], f"Expected 'False', but got {res_data['success']}")
    check.is_in(empty_field, res_data["message"].lower(), f"Expected '{empty_field}' in message, but got {res_data['message']}")



@pytest.mark.parametrize("empty_field", ["name", "email", "password"])
def test_users_register_length_boundary_400(empty_field, manage_context_primary_user_register):
    context = manage_context_primary_user_register
    user_payload = context.get("user_payload")

    new_user_payload = user_payload.copy()

    if empty_field == "name":
        new_user_payload[empty_field] = "a"
    elif empty_field == "email":
        new_user_payload[empty_field] = "a@b.c"
    elif empty_field == "password":
        new_user_payload[empty_field] = "b"

    new_res = requests.post(API_USER_REGISTER_ENDPOINT, headers={"Content-Type": "application/json"}, json=new_user_payload)
    check.equal(new_res.status_code, 400, f"Expected 400, but got {new_res.status_code}")

    resp_data = new_res.json()
    check.is_false(resp_data["success"], f"Expected 'False', but got {resp_data['success']}")
    check.is_in(empty_field, resp_data["message"].lower(), f"Expected '{empty_field}' in message, but got {resp_data['message']}")



@pytest.mark.parametrize("malformed_email", [
    "qa_tester",
    "qa_tester@qateam",
    "@qateam.com",
    "qa tester@qateam.com",
    "qa_tester@.com"
])
def test_users_register_invalid_email_format_400(malformed_email):
    headers = {"Content-Type": "application/json"}
    user_payload = {
        "name": "QATester QATeam",
        "email": malformed_email,
        "password": "QATesterPSWD123!"
    }
    response = requests.post(API_USER_REGISTER_ENDPOINT, headers=headers, json=user_payload)
    check.equal(response.status_code, 400, f"Expected 400, but got {response.status_code}")
    check.is_false(response.json()["success"], f"Expected 'False', but got {response.json()['success']}")



def test_users_register_missing_content_type_header_400(manage_context_primary_user_register):
    response = requests.post(API_USER_REGISTER_ENDPOINT, data=str(manage_context_primary_user_register))
    check.is_in(response.status_code, [400, 415])
    check.is_false(response.json()["success"], f"Expected 'False', but got {response.json()['success']}")



@pytest.mark.parametrize("http_method", ["GET", "PUT", "PATCH", "DELETE"])
def test_users_register_reject_invalid_methods_404(http_method):
    response = requests.request(http_method, API_USER_REGISTER_ENDPOINT )
    status = response.status_code
    check.is_in(status, [400, 404, 405], f"Expected [400, 404, 405] for {http_method}, but got {status}")



def test_users_register_invalid_path_404():
    new_user_payload =  {
        "name": f"QATester Temp1",
        "email": f"qatester_temp1@qateam.com",
        "password": "QATesterPSWD123!"
    }
    response = requests.post(f"{API_BASE_URL}/users/registration", json=new_user_payload, timeout=TEST_SLEEP_IN_SECOND )
    check.equal(response.status_code, 404, f"Expected 404, but got {response.status_code}")
    check.is_in("Page Not Found", response.text, msg=f"Expected 'Page Not Found' in response, but got {response.text}")