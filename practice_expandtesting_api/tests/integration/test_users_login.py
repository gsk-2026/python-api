import pytest
import requests
from pytest_check import check

from config.settings import (
    API_USER_LOGIN_ENDPOINT,
    UserTestStep
)


"""
Integration test for the API Endpoints: https://practice.expandtesting.com/notes/api/api-docs/#/Users/post_users_login

curl -X 'POST' \
  'https://practice.expandtesting.com/notes/api/users/login' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'email={email}&password={password}'
"""



def test_users_login_success_200(manage_context_primary_user_register):
    context = manage_context_primary_user_register
    user_payload = context.get("user_payload")
    user_credential = {"email": user_payload["email"], "password": user_payload["password"]}

    response = requests.post(API_USER_LOGIN_ENDPOINT, headers={"Content-Type": "application/json"}, json=user_credential)
    check.equal(response.status_code, 200, f"Expected 200, got {response.status_code}")
    manage_context_primary_user_register["token"] = response.json()["data"]["token"]
    manage_context_primary_user_register["headers_login"] = {**context["headers_default"], "x-auth-token": response.json()["data"]["token"]}
    manage_context_primary_user_register["user_test_step"] = UserTestStep.USER_LOGIN
    manage_context_primary_user_register["response"] = response

    resp_json = response.json()
    check.is_instance(resp_json, dict, msg=f"Expected resp_json to be a JSON object, but got as {type(resp_json).__name__}.")
    check.is_in("success", resp_json, msg="Expected 'success' property in resp_json, but it is missing")
    check.is_true(resp_json["success"])
    check.is_in("status", resp_json, msg="Expected 'status' property in resp_json, but it is missing")
    check.equal(resp_json["status"], 200)
    check.is_in("message", resp_json, msg="Expected 'message' property in resp_json, but it is missing")
    check.equal(resp_json["message"], "Login successful")

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
    check.is_in("token", resp_json_data, msg="Expected 'token' property in resp_json_data, but it is missing")
    check.is_instance(resp_json_data["token"], str)
    check.greater(len(resp_json_data["token"]), 0)



def test_users_login_invalid_password_400(manage_context_primary_user_register):
    context = manage_context_primary_user_register
    user_payload = context.get("user_payload")
    response = requests.post(
        API_USER_LOGIN_ENDPOINT,
        headers={"Content-Type": "application/json"},
        data={"email": user_payload["email"], "password": "WrongPassword!"}
    )
    check.equal(response.status_code, 400)
    response_data = response.json()
    check.is_false(response_data["success"])
    check.is_in("message", response_data)


def test_users_login_invalid_email_400(manage_context_primary_user_register):
    context = manage_context_primary_user_register
    user_payload = context.get("user_payload")
    response = requests.post(
        API_USER_LOGIN_ENDPOINT,
        headers={"Content-Type": "application/json"},
        data={"email": "InvalidEmail@qateam.com", "password": user_payload["password"]}
    )
    check.equal(response.status_code, 400)
    response_data = response.json()
    check.is_false(response_data["success"])
    check.is_in("message", response_data)



@pytest.mark.parametrize("missing_field", ["email", "password"])
def test_users_login_missing_required_fields_400(missing_field, manage_context_primary_user_register):
    context = manage_context_primary_user_register
    user_payload = context.get("user_payload")
    payload = user_payload.copy()
    payload.pop(missing_field)

    response = requests.post(API_USER_LOGIN_ENDPOINT, headers={"Content-Type": "application/json"}, data=payload)
    check.equal(response.status_code, 400)
    check.is_false(response.json()["success"])



@pytest.mark.parametrize("invalid_email", [
    "QATester",
    "~!@#$%^&*$().com",
    "@qateam.com",
    "qateam.com"
])
def test_users_login_invalid_email_format_400(invalid_email, manage_context_primary_user_register):
    context = manage_context_primary_user_register
    user_payload = context.get("user_payload")
    payload = {"email": invalid_email,"password": user_payload["password"]}
    response = requests.post(API_USER_LOGIN_ENDPOINT, headers={"Content-Type": "application/json"}, data=payload)
    check.equal(response.status_code, 400)
    check.is_false(response.json()["success"])


def test_users_login_empty_password_400(manage_context_primary_user_register):
    context = manage_context_primary_user_register
    user_payload = context.get("user_payload")
    payload = {"email": user_payload["email"], "password": ""}
    response = requests.post(API_USER_LOGIN_ENDPOINT, headers={"Content-Type": "application/json"}, data=payload)
    check.equal(response.status_code, 400)
    check.is_false(response.json()["success"])



def test_users_login_payload_json_200(manage_context_primary_user_register):
    context = manage_context_primary_user_register
    user_payload = context.get("user_payload")
    headers = { "Content-Type": "application/json", "Accept": "application/json"}
    response = requests.post(API_USER_LOGIN_ENDPOINT, headers=headers, json=user_payload )
    check.equal(response.status_code, 200)
    manage_context_primary_user_register["token"] = response.json()["data"]["token"]
    manage_context_primary_user_register["headers_login"] = {**context["headers_default"], "x-auth-token": response.json()["data"]["token"]}
    manage_context_primary_user_register["user_test_step"] = UserTestStep.USER_LOGIN
    manage_context_primary_user_register["response"] = response



def test_users_login_payload_data_400(manage_context_primary_user_register):
    context = manage_context_primary_user_register
    user_payload = context.get("user_payload")
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    response = requests.post(API_USER_LOGIN_ENDPOINT, headers=headers, data=user_payload)
    check.equal(response.status_code, 400)



def test_users_login_content_type_text_plain_400(manage_context_primary_user_register):
    context = manage_context_primary_user_register
    user_payload = context.get("user_payload")
    bad_headers = {"Content-Type": "text/plain", "Accept": "application/json" }
    response = requests.post(API_USER_LOGIN_ENDPOINT, headers=bad_headers, json=user_payload)
    check.equal(response.status_code, 400)



def test_users_login_unregistered_401():
    response = requests.post(
        API_USER_LOGIN_ENDPOINT,
        headers={"Content-Type": "application/json"},
        json={"email": "InvalidEmail@qateam.com", "password": "InvalidUserName"}
    )
    check.equal(response.status_code, 401)
    response_data = response.json()
    check.is_false(response_data["success"])
    check.is_in("message", response_data)



@pytest.mark.parametrize("http_method", ["GET", "PUT", "PATCH", "DELETE"])
def test_users_login_reject_invalid_methods_404(http_method):
    response = requests.request(
        http_method,
        API_USER_LOGIN_ENDPOINT
    )
    status = response.status_code
    check.is_in(status, [400, 404, 405], f"Expected [400, 404, 405] for {http_method}, but got {status}"
)