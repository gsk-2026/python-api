import time
import pytest
import requests
from pytest_check import check

from config.settings import (
    API_USER_LOGIN_ENDPOINT,
    API_USER_CHANGE_PASSWORD_ENDPOINT,
    TEST_SLEEP_IN_SECOND
)


"""
Integration test for the API Endpoints: https://practice.expandtesting.com/notes/api/api-docs/#/Users/post_users_change_password

curl -X 'POST' \
  'https://practice.expandtesting.com/notes/api/users/change-password' \
  -H 'accept: application/json' \
  -H 'x-auth-token: {auth_token}' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'currentPassword={currentPassword}&newPassword={newpassword}'
"""



def test_users_change_password_success_200(manage_context_primary_user_register_login):
    new_password = "New_QATesterPSWD789!"
    payload = {
        "currentPassword": manage_context_primary_user_register_login["credentials"]["password"],
        "newPassword": new_password
    }
    response = requests.post(API_USER_CHANGE_PASSWORD_ENDPOINT, headers=manage_context_primary_user_register_login["headers_login"], json=payload)
    check.equal(response.status_code, 200, f"Expected 200 OK, got {response.status_code}")
    manage_context_primary_user_register_login["user_payload"]["password"] = new_password
    manage_context_primary_user_register_login["credentials"]["password"] = new_password

    resp_json = response.json()
    check.is_instance(resp_json, dict, msg=f"Expected resp_json to be a JSON object, but got as {type(resp_json).__name__}.")
    check.is_in("success", resp_json, msg="Expected 'success' property in resp_json, but it is missing")
    check.is_true(resp_json["success"])
    check.is_in("status", resp_json, msg="Expected 'status' property in resp_json, but it is missing")
    check.equal(resp_json["status"], 200)
    check.is_in("message", resp_json, msg="Expected 'message' property in resp_json, but it is missing")
    check.equal(resp_json["message"], "The password was successfully updated")




def test_users_change_password_missing_token_401(manage_context_primary_user_register_login):
    new_password = "New_QATesterPSWD789!"
    payload = {
        "currentPassword": manage_context_primary_user_register_login["credentials"]["password"],
        "newPassword": new_password
    }
    headers = manage_context_primary_user_register_login["headers_login"].copy()
    headers.pop("x-auth-token", None)

    response = requests.post(API_USER_CHANGE_PASSWORD_ENDPOINT, headers=headers, json=payload)
    check.equal(response.status_code, 401, f"Expected 401 Unauthorized, got {response.status_code}")
    check.is_in("Unauthorized", str(response.reason), "Expected Unauthorized reason not found")
    check.is_in("no authentication token specified in x-auth-token header", response.json().get("message", "").lower(), "Expected unauthorized message not found")



def test_users_change_password_wrong_current_password_400(manage_context_primary_user_register_login):
    wrong_new_password = "Wrong_" + manage_context_primary_user_register_login["credentials"]["password"]
    payload = { "currentPassword": wrong_new_password, "newPassword": "New_QATesterPSWD789!" }

    response = requests.post(API_USER_CHANGE_PASSWORD_ENDPOINT, headers=manage_context_primary_user_register_login["headers_login"], json=payload)
    check.equal(response.status_code, 400, f"Expected 400 Bad Request, got {response.status_code}")
    check.is_in("bad request", response.reason.lower(), "Expected bad request reason not found")

    resp_data = response.json()
    check.is_true(resp_data.get("success") is False, "Expected success to be False")
    check.is_in("the current password is incorrect", str(resp_data.get("message")).lower(), "Expected incorrect password message not found")



@pytest.mark.parametrize(
    "scenario_name, invalid_payload",
    [
        ("NEW_PASSWORD_TOO_SHORT", {"currentPassword": "QATesterPSWD123!", "newPassword": "123"}),
        ("NEW_PASSWORD_TOO_LONG", {"currentPassword": "QATesterPSWD123!", "newPassword": "omg!" * 256}),
        ("NEW_PASSWORD_MISSING", {"currentPassword": "QATesterPSWD123!"}),
        ("BOTH_PASSWORD_EMPTY", {"currentPassword": "", "newPassword": ""})
    ]
)
def test_users_change_password_invalid_new_password_400(scenario_name, invalid_payload, manage_context_primary_user_register_login):
    if "currentPassword" in invalid_payload and invalid_payload["currentPassword"] != "":
        invalid_payload["currentPassword"] = manage_context_primary_user_register_login["credentials"]["password"]

    response = requests.post(API_USER_CHANGE_PASSWORD_ENDPOINT, headers=manage_context_primary_user_register_login["headers_login"], json=invalid_payload)
    assert response.status_code == 400, f"Expected 400, but got: {response.status_code}. Scenario '{scenario_name}' failed"

    json_data = response.json()
    check.is_false(json_data.get("success"), "Expected success to be False")
    check.is_in("message", json_data, "Expected message not found")



def test_users_change_password_credential_lifecycle_401(manage_context_primary_user_register_login):
    current_password = manage_context_primary_user_register_login["credentials"]["password"]
    new_password = "New_" + current_password
    payload = {"currentPassword": current_password, "newPassword": new_password}
    change_resp = requests.post(API_USER_CHANGE_PASSWORD_ENDPOINT, json=payload, headers=manage_context_primary_user_register_login["headers_login"])
    check.equal(change_resp.status_code, 200, f"Expected 200 OK, got {change_resp.status_code}")
    check.is_true(change_resp.json().get("success"), "Expected success to be True")
    check.is_in("The password was successfully updated", change_resp.json().get("message"), "Expected success message not found")
    manage_context_primary_user_register_login["user_payload"]["password"] = new_password
    manage_context_primary_user_register_login["credentials"]["password"] = new_password

    time.sleep(TEST_SLEEP_IN_SECOND)

    payload_with_old_password = {
        "email": manage_context_primary_user_register_login["credentials"]["email"],
        "password": current_password
    }
    login_resp = requests.post(API_USER_LOGIN_ENDPOINT, json=payload_with_old_password)
    check.equal(login_resp.status_code, 401, f"Expected 401 Unauthorized, got {login_resp.status_code}")
    check.is_false(login_resp.json().get("success"), "Expected success to be False")
    check.is_in("Incorrect email address or password", login_resp.json().get("message"), "Expected incorrect credentials message not found")



@pytest.mark.parametrize("http_method", ["GET", "PUT", "PATCH", "DELETE"])
def test_users_change_password_reject_invalid_methods_404(http_method):
    response = requests.request(
        http_method,
        API_USER_CHANGE_PASSWORD_ENDPOINT
    )
    status = response.status_code
    check.equal(status, 404, f"Expected 404 Not Found for {http_method}, but got {status}")
    check.is_in("not found", response.reason.lower(), f"Expected 'not found' in reason for {http_method}, but got {response.reason}")
