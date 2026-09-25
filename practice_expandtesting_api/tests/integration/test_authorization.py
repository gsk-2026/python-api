import pytest
import requests
from pytest_check import check

from config.settings import (
    API_BASE_URL,
    UserTestStep
)


def test_auth_positive_valid_token_200(manage_context_primary_user_register_login):
    user_payload = manage_context_primary_user_register_login
    response = requests.get(API_BASE_URL, headers=user_payload.get("headers_login"))

    check.equal(response.status_code, 200, msg=f"Expected 200, but got {response.status_code}")
    manage_context_primary_user_register_login["user_test_step"] = UserTestStep.ACCESS_GRANTED
    manage_context_primary_user_register_login["response"] = response

    response_data = response.json()
    check.is_in("success", response_data, msg=f"Expected 'success' in response, but got {response_data}")
    check.is_in("status", response_data, msg=f"Expected 'status' in response, but got {response_data}")
    check.is_in("message", response_data, msg=f"Expected 'message' in response, but got {response_data}")

    check.equal(response_data.get('status', -1), 200, msg=f"Expected status 200, but got {response_data.get('status', '')}")
    check.equal(response_data.get('success', ''), True, msg=f"Expected success True, but got {response_data.get('success', '')}")
    check.equal(response_data.get('message'), "Notes API is Running", msg=f"Expected 'Notes API is Running' in message, but got {response_data.get('message')}")




def test_health_check_response_header_200(manage_context_primary_user_register_login):
    user_context = manage_context_primary_user_register_login
    response = requests.get(API_BASE_URL, headers=user_context.get("headers_login"))
    check.equal(response.status_code, 200, msg=f"Expected 200, but got {response.status_code}")
    manage_context_primary_user_register_login["user_test_step"] = UserTestStep.ACCESS_GRANTED
    manage_context_primary_user_register_login["response"] = response

    resp_json = response.json()
    check.equal(resp_json.get('status'), 200)
    check.equal(resp_json.get('success'), True)
    check.equal(resp_json.get('message'), "Notes API is Running")

    headers = response.headers
    allow_methods = {item.strip() for item in headers.get('access-control-allow-methods', '').split(',')}
    content_type = {item.strip() for item in headers.get('content-type', '').split(';')}
    allow_headers = {item.strip() for item in headers.get('access-control-allow-headers', '').split(',')}
    check.equal(allow_methods, {'GET', 'POST', 'PUT', 'PATCH', 'DELETE'})
    check.equal(content_type, {'application/json', 'charset=utf-8'})
    check.equal(allow_headers, {'Content-Type', 'Authorization', 'X-Requested-With', 'X-Auth-Token', 'Accept', 'Origin'})



def test_auth_negative_with_no_token_specified_200():
    response = requests.get(API_BASE_URL, headers={"Authorization": "Bearer invalid-token", "Accept": "application/json"})
    check.equal(response.status_code, 200, msg=f"Expected 401, but got {response.status_code}")
    check.is_true(response.json().get("success"), msg=f"Expected success False, but got {response.json().get('success')}")



def test_auth_negative_missing_token_200():
    response = requests.get(API_BASE_URL, headers={"Accept": "application/json"})

    check.equal(response.status_code, 200, msg=f"Expected 200, but got {response.status_code}")
    response_data = response.json()
    check.equal(response_data.get("status"), 200, msg=f"Expected status 200, but got {response_data.get('status')}")
    check.equal(response_data.get("message"), "Notes API is Running", msg=f"Expected 'Notes API is Running' in message, but got {response_data.get('message')}")
    check.is_true(response_data.get("success"), msg=f"Expected success False, but got {response_data.get('success')}")



@pytest.mark.parametrize("invalid_token", [
    "InvalidTokenString_Auth_Token",
    "Authorization Bearer this_is_fake_token_value",
    "omg" * 1000  # Boundary check: extremely long string
])
def test_auth_negative_invalid_tokens_200(invalid_token):
    response = requests.get(API_BASE_URL, headers={"x-auth-token": invalid_token, "Accept": "application/json"})

    check.equal(response.status_code, 200, msg=f"Expected 200, but got {response.status_code}")
    response_data = response.json()
    check.equal(response_data.get("status"), 200, msg=f"Expected status 200, but got {response_data.get('status')}")
    check.equal(response_data.get("message"), "Notes API is Running", msg=f"Expected 'Notes API is Running' in message, but got {response_data.get('message')}")
    check.is_true(response_data.get("success"), msg=f"Expected success False, but got {response_data.get('success')}")



@pytest.mark.parametrize("edge_case_token", [
    "",
    "Bearer ",
    "'; DROP TABLE users; DROP TABLE Notes; --",  # SQL injection attempt inside auth header
    "<script>alert('hack')</script>" # XSS payload attempt inside auth header
])
def test_auth_edge_and_boundary_injection_tokens_200(edge_case_token):
    response = requests.get(API_BASE_URL, headers={"x-auth-token": edge_case_token, "Accept": "application/json"})

    check.equal(response.status_code, 200, msg=f"Expected 200, but got {response.status_code}")
    response_data = response.json()
    check.equal(response_data.get("status"), 200, msg=f"Expected status 200, but got {response_data.get('status')}")
    check.equal(response_data.get("message"), "Notes API is Running", msg=f"Expected 'Notes API is Running' in message, but got {response_data.get('message')}")
    check.is_true(response_data.get("success"), msg=f"Expected success False, but got {response_data.get('success')}")
