import time
import pytest
import requests
from pytest_check import check

from config.settings import (
    API_HEALTH_CHECK_ENDPOINT,
    API_TIMEOUT,
    TEST_PERFORMANCE_LOOP
)


"""
Integration test for the API Endpoint: https://practice.expandtesting.com/notes/api/api-docs/#/Health/get_health_check

curl -X 'GET' \
  'https://practice.expandtesting.com/notes/api/health-check' \
  -H 'accept: application/json'
"""


def test_health_check_happy_path_200():
    response = requests.get(API_HEALTH_CHECK_ENDPOINT, timeout=API_TIMEOUT)
    check.equal(response.status_code, 200, msg=f"Expected 200, but got {response.status_code}")

    content_type = response.headers.get("Content-Type", "")
    check.is_in("application/json", content_type, msg=f"Expected JSON format, but got {content_type}")

    resp_data = response.json()
    check.is_instance(resp_data, dict, msg=f"Expected resp_data to be a JSON object, but got as {type(resp_data).__name__}.")
    check.is_in("success", resp_data, msg="Expected 'success' property in resp_data, but it is missing")
    check.is_true(resp_data["success"])
    check.is_in("status", resp_data, msg="Expected 'status' property in resp_data, but it is missing")
    check.equal(resp_data["status"], 200)
    check.is_in("message", resp_data, msg="Expected 'message' property in resp_data, but it is missing")
    check.equal(resp_data["message"], "Notes API is Running")



def test_health_check_accept_content_type_xml_200():
    custom_headers = {"Accept": "application/xml"}
    response = requests.get(
        API_HEALTH_CHECK_ENDPOINT,
        headers=custom_headers,
        timeout=API_TIMEOUT
    )

    if response.status_code == 200:
        content_type = response.headers.get("Content-Type", "")
        check.is_in("application/xml", content_type, msg=f"Expected XML format, but got {content_type}")
    else:
        check.equal(response.status_code, 406, msg=f"Expected 406 for application/xml, got {response.status_code}")



def test_health_check_accept_content_type_json_200():
    custom_headers = {"Accept": "application/json"}
    response = requests.get(
        API_HEALTH_CHECK_ENDPOINT,
        headers=custom_headers,
        timeout=API_TIMEOUT
    )
    check.equal(response.status_code, 200, msg=f"Expected 200, but got {response.status_code}")

    content_type = response.headers.get("Content-Type", "")
    check.is_in("application/json", content_type, msg=f"Expected JSON format, but got {content_type}")



def test_health_check_invalid_parameters_200():
    payload_params = {"invalid_key": "invalid_value", "id": 9999999}
    response = requests.get(
        API_HEALTH_CHECK_ENDPOINT,
        params=payload_params,
        timeout=API_TIMEOUT
    )
    check.equal(response.status_code, 200, msg=f"Expected 200, but got {response.status_code}")
    check.is_in("application/json", response.headers.get("Content-Type", ""),  msg=f"Expected JSON format, but got {response.headers.get('Content-Type', '')}")
    check.equal(response.headers.get("Accept"), None, msg=f"Expected Accept header to be None, but got {response.headers.get('Accept', '')}")



def test_health_check_performance_200():
    duration_ms = 0.0
    for _ in range(TEST_PERFORMANCE_LOOP):
        start_time = time.time()
        response = requests.get(
            API_HEALTH_CHECK_ENDPOINT,
            timeout = API_TIMEOUT
        )
        duration_ms += (time.time() - start_time)
        check.equal(response.status_code, 200, msg=f"Expected 200, but got {response.status_code}")

    # Performance Threshold Validation
    duration_ms *= 1000
    duration_ms /= TEST_PERFORMANCE_LOOP
    check.less(duration_ms, API_TIMEOUT * 1000, msg=f"Expected response time < {API_TIMEOUT * 1000}ms: but took {duration_ms:.2f}ms")



def test_health_check_sensitive_information_200():
    response = requests.get(
        API_HEALTH_CHECK_ENDPOINT,
        timeout = API_TIMEOUT
    )
    check.equal(response.status_code, 200, msg=f"Expected 200, but got {response.status_code}")

    sensitive_terms = [
        "passwd",
        "pwd",
        "username",
        "login",
        "pin",
        "connection_string",
        "db_password",
        "db_user",
        "db_host",
        "key_id",
        "email",
        "phone",
        "ssn",
        "social_security",
        "birth_date",
        "dob",
        "first_name",
        "last_name",
        "password",
        "secret",
        "access",
        "authorization",
        "access_token",
        "private_key",
        "token",
        "api_key",
        "apikey",
        "session_id",
        "session_token",
        "refresh_token",
        "bearer",
        "client",
        "signature"
    ]

    body = response.text.lower()

    for term in sensitive_terms:
        check.is_not_in(term, body, msg=f"Sensitive term '{term}' found in response body")



def test_health_check_response_header_200():
    custom_headers = {"Accept": "application/json", "Content-Type": "application/json"}
    response = requests.get(
        API_HEALTH_CHECK_ENDPOINT,
        headers=custom_headers,
        timeout=API_TIMEOUT
    )

    resp_json = response.json()
    check.equal(response.status_code, 200, msg=f"Expected 200, but got {response.status_code}")
    check.equal(resp_json.get('status'), 200, msg=f"Expected status 200, but got {resp_json.get('status')}")
    check.is_true(resp_json.get('success'), msg=f"Expected success True, but got {resp_json.get('success')}")
    check.equal(resp_json.get('message'), "Notes API is Running", msg=f"Expected message 'Notes API is Running', but got {resp_json.get('message')}")

    headers = response.headers
    allow_methods = {item.strip() for item in headers.get('access-control-allow-methods', '').split(',')}
    content_type = {item.strip() for item in headers.get('content-type', '').split(';')}
    allow_headers = {item.strip() for item in headers.get('access-control-allow-headers', '').split(',')}
    check.equal(allow_methods, {'GET', 'POST', 'PUT', 'PATCH', 'DELETE'}, msg=f"Expected allow methods {{'GET', 'POST', 'PUT', 'PATCH', 'DELETE'}}, but got {allow_methods}")
    check.equal(content_type, {'application/json', 'charset=utf-8'}, msg=f"Expected content type {{'application/json', 'charset=utf-8'}}, but got {content_type}")
    check.equal(allow_headers, {'Content-Type', 'Authorization', 'X-Requested-With', 'X-Auth-Token', 'Accept', 'Origin'}, msg=f"Expected allow headers {{'Content-Type', 'Authorization', 'X-Requested-With', 'X-Auth-Token', 'Accept', 'Origin'}}, but got {allow_headers}")



@pytest.mark.parametrize("http_method", ["POST", "PUT", "PATCH", "DELETE"])
def test_health_check_reject_invalid_methods_404(http_method):
    response = requests.request(http_method, API_HEALTH_CHECK_ENDPOINT)
    check.is_in(response.status_code, [400, 404, 405], msg=f"Expected [400, 404, 405] for {http_method}, but got {response.status_code}")



def test_health_check_return_500():
    pass
