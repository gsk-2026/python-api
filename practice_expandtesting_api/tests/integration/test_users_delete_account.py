import time
import pytest
import requests
from pytest_check import check

from config.settings import (
    ApiEndpoints,
    UserTestSteps,
    TEST_SLEEP_IN_SECOND
)


"""
Integration test for the API Endpoint: 
    https://practice.expandtesting.com/notes/api/api-docs/#/Users/delete_users_logout
    https://practice.expandtesting.com/notes/api/api-docs/#/Users/delete_users_delete_account
    
curl -X 'DELETE' \
  'https://practice.expandtesting.com/notes/api/users/logout' \
  -H 'accept: application/json' \
  -H 'x-auth-token: {auth_token}'
  
curl -X 'DELETE' \
  'https://practice.expandtesting.com/notes/api/users/delete-account' \
  -H 'accept: application/json' 
"""


def test_users_delete_acct_normal_positive_200(manage_context_primary_user_register_login):
    headers = manage_context_primary_user_register_login.get("headers_login")
    response = requests.delete(ApiEndpoints.user_delete_account(), headers=headers)
    manage_context_primary_user_register_login["user_test_step"] = UserTestSteps.ACCOUNT_DELETION
    manage_context_primary_user_register_login["response"] = response

    resp_json = response.json()
    check.is_instance(resp_json, dict, msg=f"Expected resp_json to be a JSON object, but got as {type(resp_json).__name__}.")
    check.is_in("success", resp_json, msg="Expected 'success' property in resp_json, but it is missing")
    check.is_true(resp_json["success"])
    check.is_in("status", resp_json, msg="Expected 'status' property in resp_json, but it is missing")
    check.equal(resp_json["status"], 200)
    check.is_in("message", resp_json, msg="Expected 'message' property in resp_json, but it is missing")
    check.equal(resp_json["message"], "Account successfully deleted")




def test_users_delete_acct_missing_header_accept_200(manage_context_primary_user_register_login):
    headers = manage_context_primary_user_register_login.get("headers_login").copy()
    del headers["Accept"]
    response = requests.delete(ApiEndpoints.user_delete_account(), headers=headers)
    check.equal(response.status_code, 200, msg=f"Expected 200, but got {response.status_code}")
    manage_context_primary_user_register_login["user_test_step"] = UserTestSteps.ACCOUNT_DELETION
    manage_context_primary_user_register_login["response"] = response

    resp_json = response.json()
    check.is_instance(resp_json, dict, msg=f"Expected resp_json to be a JSON object, but got as {type(resp_json).__name__}.")
    check.is_in("success", resp_json, msg="Expected 'success' property in resp_json, but it is missing")
    check.is_true(resp_json["success"])
    check.is_in("status", resp_json, msg="Expected 'status' property in resp_json, but it is missing")
    check.equal(resp_json["status"], 200)
    check.is_in("message", resp_json, msg="Expected 'message' property in resp_json, but it is missing")
    check.equal(resp_json["message"], "Account successfully deleted")



def test_users_delete_acct_missing_token_401():
    response = requests.delete(ApiEndpoints.user_delete_account(), headers={"Accept": "application/json"})
    check.equal(response.status_code, 401)
    response_data = response.json()
    check.equal(response_data.get("status"), 401)
    check.is_false(response_data.get("success"))
    check.is_in("no authentication token", response_data.get("message").lower())



@pytest.mark.parametrize("blank_token", [
    ""
])
def test_users_delete_acct_blank_token_401(blank_token):
    response = requests.delete(ApiEndpoints.user_delete_account(), headers={"x-auth-token": blank_token, "Accept": "application/json"})
    check.equal(response.status_code, 401)

    response_data = response.json()
    check.equal(response_data.get("status"), 401)
    check.is_false(response_data.get("success"))
    check.is_in("no authentication token specified in x-auth-token header", response_data.get("message").lower())



@pytest.mark.parametrize("malformed_token", [
    "not.a.validtoken",
    "invalid_jwt_1234567890",
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjY0MmI0In0.fake_signature",
    "OMG!" * 256
])
def test_users_delete_acct_malformed_token_401(malformed_token):
    response = requests.delete(ApiEndpoints.user_delete_account(), headers={"x-auth-token": malformed_token, "Accept": "application/json"})
    check.equal(response.status_code, 401)

    response_data = response.json()
    check.equal(response_data.get("status"), 401)
    check.is_false(response_data.get("success"))
    check.is_in("access token is not valid or has expired", response_data.get("message").lower())




def test_users_delete_acct_duplicate_deletion_200_401(manage_context_primary_user_register_login):
    headers = manage_context_primary_user_register_login.get("headers_login")
    first_resp = requests.delete(ApiEndpoints.user_delete_account(), headers=headers)
    check.equal(first_resp.status_code, 200)
    manage_context_primary_user_register_login["user_test_step"] = UserTestSteps.ACCOUNT_DELETION
    manage_context_primary_user_register_login["response"] = first_resp

    first_data = first_resp.json()
    check.equal(first_data.get("status"), 200)
    check.is_true(first_data.get("success"))
    check.is_in("successful", first_data.get("message").lower())

    second_resp = requests.delete(ApiEndpoints.user_delete_account(), headers=headers)
    check.equal(second_resp.status_code, 401)
    second_data = second_resp.json()
    check.equal(second_data.get("status"), 401)
    check.is_false(second_data.get("success"))
    check.is_in("access token is not valid", second_data.get("message").lower())



def test_users_delete_acct_deletion_then_login_401(manage_context_primary_user_register_login):
    headers = manage_context_primary_user_register_login.get("headers_login")
    delete_resp = requests.delete(ApiEndpoints.user_delete_account(), headers=headers)
    check.equal(delete_resp.status_code, 200)
    manage_context_primary_user_register_login["user_test_step"] = UserTestSteps.ACCOUNT_DELETION

    delete_data = delete_resp.json()
    check.equal(delete_data.get("status"), 200)
    check.is_true(delete_data.get("success"))
    check.is_in("successful", delete_data.get("message").lower())

    time.sleep(TEST_SLEEP_IN_SECOND)

    login_resp = requests.post(ApiEndpoints.user_login(), json=manage_context_primary_user_register_login["credentials"])
    check.equal(login_resp.status_code, 401)

    login_data = login_resp.json()
    check.equal(login_data.get("status"), 401)
    check.is_false(login_data.get("success"))
    check.is_in("incorrect email address or password", login_data.get("message").lower())




@pytest.mark.parametrize("http_method", ["GET", "POST", "PUT", "PATCH"])
def test_users_delete_acct_reject_invalid_methods(http_method):
    response = requests.request(
        http_method,
        ApiEndpoints.user_delete_account()
    )
    status = response.status_code
    check.is_in(status, [400, 404, 405], f"Expected [400, 404, 405] for {http_method}, but got {status}")



def test_users_delete_acct_page_not_found_404(manage_context_primary_user_register_login):
    headers = manage_context_primary_user_register_login.get("headers_login")
    del_url = ApiEndpoints.user_delete_account().replace("-","")
    response = requests.delete(del_url, headers=headers)

    check.equal(response.status_code, 404)
    check.is_in("404 page not found", response.text.lower())


def test_users_delete_acct_bad_request_400(manage_context_primary_user_register_login):
    pass
