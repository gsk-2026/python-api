import pytest
import requests
from pytest_check import check

from config.settings import (
    API_USER_LOGOUT_ENDPOINT,
    API_NOTES_ENDPOINT, UserTestStep
)


'''
Integration test for the API Endpoint: https://practice.expandtesting.com/notes/api/api-docs/#/Users/delete_users_logout 

curl -X 'DELETE' \
  'https://practice.expandtesting.com/notes/api/users/logout' \
  -H 'accept: application/json' \
  -H 'x-auth-token: {auth_token}'
'''



def test_users_logout_positive_logout_200(manage_context_primary_user_register_login):
    user_context = manage_context_primary_user_register_login
    response = requests.delete(API_USER_LOGOUT_ENDPOINT, headers=user_context.get("headers_login"))
    check.equal(response.status_code, 200, msg=f"Expected 200, but got {response.status_code}")
    manage_context_primary_user_register_login["user_test_step"] = UserTestStep.USER_LOGOUT
    manage_context_primary_user_register_login["response"] = response

    resp_json = response.json()
    check.is_instance(resp_json, dict, msg=f"Expected resp_json to be a JSON object, but got as {type(resp_json).__name__}.")
    check.is_in("success", resp_json, msg="Expected 'success' property in resp_json, but it is missing")
    check.is_true(resp_json["success"])
    check.is_in("status", resp_json, msg="Expected 'status' property in resp_json, but it is missing")
    check.equal(resp_json["status"], 200)
    check.is_in("message", resp_json, msg="Expected 'message' property in resp_json, but it is missing")
    check.equal(resp_json["message"], "User has been successfully logged out")



def test_users_logout_missing_accept_header_200(manage_context_primary_user_register_login):
    user_context = manage_context_primary_user_register_login
    headers = user_context["headers_login"].copy()
    del headers["Accept"]
    response = requests.delete(API_USER_LOGOUT_ENDPOINT, headers=headers)
    check.equal(response.status_code, 200, msg=f"Expected 200, but got {response.status_code}")
    manage_context_primary_user_register_login["user_test_step"] = UserTestStep.USER_LOGOUT
    manage_context_primary_user_register_login["response"] = response

    resp_data = response.json()
    check.equal(resp_data.get("status"), 200, msg=f"Expected 200, but got {resp_data.get('status')}")
    check.is_true(resp_data.get("success"), msg=f"Expected True, but got {resp_data.get('success')}")
    check.is_in("successfully logged out", resp_data.get("message").lower(), msg=f"Expected 'successfully logged out' in message, but got {resp_data.get('message')}")




def test_users_logout_double_logout_200_401(manage_context_primary_user_register_login):
    user_context = manage_context_primary_user_register_login

    resp_1 = requests.delete(API_USER_LOGOUT_ENDPOINT, headers=user_context.get("headers_login"))
    check.equal(resp_1.status_code, 200, msg=f"Expected 200 OK, but got {resp_1.status_code}")
    manage_context_primary_user_register_login["user_test_step"] = UserTestStep.USER_LOGOUT
    manage_context_primary_user_register_login["response"] = resp_1

    resp_2 = requests.delete(API_USER_LOGOUT_ENDPOINT, headers=user_context.get("headers_login"))
    check.equal(resp_2.status_code, 401, msg=f"Expected 401 Unauthorized, but got {resp_2.status_code}")



def test_users_logout_data_integrity_post_logout_401(manage_context_primary_user_register_login):
    user_context = manage_context_primary_user_register_login

    logout_resp = requests.delete(API_USER_LOGOUT_ENDPOINT, headers=user_context.get("headers_login"))
    check.equal(logout_resp.status_code, 200, msg=f"Expected 200 OK, but got {logout_resp.status_code}")
    manage_context_primary_user_register_login["user_test_step"] = UserTestStep.USER_LOGOUT
    manage_context_primary_user_register_login["response"] = logout_resp

    notes_resp = requests.get(API_NOTES_ENDPOINT, headers=user_context.get("headers_login"))
    check.equal(notes_resp.status_code, 401, msg=f"Expected 401 Unauthorized, but got {notes_resp.status_code}")
    resp_data = notes_resp.json()
    check.is_in("access token is not valid or has expired", resp_data.get("message").lower(), msg=f"Expected 'access token is not valid or has expired' in message, but got {resp_data.get('message')}")



def test_users_logout_missing_token_401():
    headers = {"Accept": "application/json"}
    response = requests.delete(API_USER_LOGOUT_ENDPOINT, headers=headers)

    assert response.status_code == 401
    resp_data = response.json()
    assert resp_data.get("status") == 401
    assert resp_data.get("success") is False
    assert "no authentication token" in resp_data.get("message").lower()



@pytest.mark.parametrize(
    "malformed_token, expected_msg",
    [
        ("", "no authentication token specified in x-auth-token header"),
        ("invalid_token_string", "access token is not valid or has expired"),
        ("x" * 500, "access token is not valid or has expired")
    ]
)
def test_users_logout_malformed_token_401(malformed_token, expected_msg):
    headers = {"x-auth-token": malformed_token, "Accept": "application/json"}
    response = requests.delete(API_USER_LOGOUT_ENDPOINT, headers=headers)

    assert response.status_code == 401
    resp_data = response.json()
    assert resp_data.get("status") == 401
    assert resp_data.get("success") is False
    assert expected_msg in resp_data.get("message", "").lower()



@pytest.mark.parametrize("http_method", ["GET", "POST", "PUT", "PATCH"])
def test_users_logout_reject_invalid_methods_404(http_method):
    response = requests.request(http_method, API_USER_LOGOUT_ENDPOINT)
    status = response.status_code
    assert status in [400, 404, 405], f"Expected [400, 404, 405] for {http_method}, but got {status}"



def test_users_logout_bad_request_400():
    pass