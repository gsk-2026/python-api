import pytest
import requests
from pytest_check import check

from config.settings import (
    ApiEndpoints
)


"""
Integration test for the API Endpoints: https://practice.expandtesting.com/notes/api/api-docs/#/Users/patch_users_profile

curl -X 'PATCH' \
        'https://practice.expandtesting.com/notes/api/users/profile' \
        -H 'accept: application/json' \
           -H 'x-auth-token: {auth_token}' \
              -H 'Content-Type: application/x-www-form-urlencoded' \
                 -d 'name={name}&phone={phone}&company={company}'
"""


def test_users_get_profile_data_contract_200(manage_context_primary_user_register_login):
    response = requests.get(ApiEndpoints.user_profile(), headers=manage_context_primary_user_register_login["headers_login"])
    check.equal(response.status_code, 200, f"Expected 200 OK, got {response.status_code}")

    resp_json = response.json()
    check.is_instance(resp_json, dict, msg=f"Expected resp_json to be a JSON object, but got as {type(resp_json).__name__}.")
    check.is_in("success", resp_json, msg="Expected 'success' property in resp_json, but it is missing")
    check.is_true(resp_json["success"])
    check.is_in("status", resp_json, msg="Expected 'status' property in resp_json, but it is missing")
    check.equal(resp_json["status"], 200)
    check.is_in("message", resp_json, msg="Expected 'message' property in resp_json, but it is missing")
    check.equal(resp_json["message"], "Profile successful")

    check.is_in("data", resp_json, msg="Expected 'data' property in resp_json, but it is missing")
    resp_json_data = resp_json["data"]
    check.is_instance(resp_json_data, dict, msg=f"Expected resp_json_data to be a JSON object, but got as {type(resp_json_data).__name__}.")
    check.is_in("name", resp_json_data, msg="Expected 'name' property in resp_json_data, but it is missing")
    check.equal(resp_json_data["name"], manage_context_primary_user_register_login["user_payload"]["name"])
    check.is_in("email", resp_json_data, msg="Expected 'email' property in resp_json_data, but it is missing")
    check.equal(resp_json_data["email"], manage_context_primary_user_register_login["user_payload"]["email"])
    check.is_in("id", resp_json_data, msg="Expected 'id' property in resp_json_data, but it is missing")
    check.is_instance(resp_json_data["id"], str)
    check.greater(len(resp_json_data["id"]), 0)
    '''
    check.is_in("phone", resp_json_data, msg="Expected 'phone' property in resp_json_data, but it is missing")
    check.is_instance(resp_json_data["phone"], str)
    check.greater(len(resp_json_data["phone"]), 0) 
    check.is_in("company", resp_json_data, msg="Expected 'company' property in resp_json_data, but it is missing")
    check.is_instance(resp_json_data["company"], str)
    check.greater(len(resp_json_data["company"]), 0)
    '''



@pytest.mark.parametrize(
    "malformed_token, expected_msg",
    [
        ("", "no authentication token specified in x-auth-token header"),
        ("invalid_token_string", "token is not valid or has expired"),
        ("OMG!" * 512, "token is not valid or has expired")
    ]
)
def test_users_get_profile_malformed_token_401(malformed_token, expected_msg):
    headers = {"x-auth-token": malformed_token,"Accept": "application/json"}
    response = requests.get(ApiEndpoints.user_profile(), headers=headers)

    assert response.status_code == 401
    assert response.reason == "Unauthorized"

    resp_data = response.json()
    assert resp_data.get("status") == 401
    assert expected_msg in resp_data.get("message", "").lower()



def test_users_get_profile_bad_request_400():
    pass



def test_users_patch_profile_update_name_200(manage_context_primary_user_register_login):
    new_name = "Updated Tester QATeam"
    new_payload = {"name": new_name}

    response = requests.patch(ApiEndpoints.user_profile(), headers=manage_context_primary_user_register_login.get("headers_login"), json=new_payload)
    check.equal(response.status_code, 200, f"Expected 200 OK, but got {response.status_code}")

    resp_json = response.json()
    check.is_instance(resp_json, dict, msg=f"Expected resp_json to be a JSON object, but got as {type(resp_json).__name__}.")
    check.is_in("success", resp_json, msg="Expected 'success' property in resp_json, but it is missing")
    check.is_true(resp_json["success"])
    check.is_in("status", resp_json, msg="Expected 'status' property in resp_json, but it is missing")
    check.equal(resp_json["status"], 200)
    check.is_in("message", resp_json, msg="Expected 'message' property in resp_json, but it is missing")
    check.equal(resp_json["message"], "Profile updated successful")

    check.is_in("data", resp_json, msg="Expected 'data' property in resp_json, but it is missing")
    resp_json_data = resp_json["data"]
    check.is_instance(resp_json_data, dict, msg=f"Expected resp_json_data to be a JSON object, but got as {type(resp_json_data).__name__}.")
    check.is_in("name", resp_json_data, msg="Expected 'name' property in resp_json_data, but it is missing")
    check.equal(resp_json_data["name"], new_name)
    check.is_in("email", resp_json_data, msg="Expected 'email' property in resp_json_data, but it is missing")
    check.equal(resp_json_data["email"], manage_context_primary_user_register_login["user_payload"]["email"])
    check.is_in("id", resp_json_data, msg="Expected 'id' property in resp_json_data, but it is missing")
    check.is_instance(resp_json_data["id"], str)
    check.greater(len(resp_json_data["id"]), 0)
    '''
    check.is_in("phone", resp_json_data, msg="Expected 'phone' property in resp_json_data, but it is missing")
    check.is_instance(resp_json_data["phone"], str)
    check.greater(len(resp_json_data["phone"]), 0) 
    check.is_in("company", resp_json_data, msg="Expected 'company' property in resp_json_data, but it is missing")
    check.is_instance(resp_json_data["company"], str)
    check.greater(len(resp_json_data["company"]), 0)
    '''



def test_users_patch_profile_update_name_phone_200(manage_context_primary_user_register_login):
    new_name = "Updated Tester QATeam"
    new_phone = "8883697531"
    new_payload = {"name": new_name, "phone": new_phone}

    response = requests.patch(ApiEndpoints.user_profile(), headers=manage_context_primary_user_register_login.get("headers_login"), json=new_payload)
    check.equal(response.status_code, 200, f"Expected 200 OK, but got {response.status_code}")

    json_data = response.json()
    check.is_true(json_data.get("success"), "Expected success flag to be True")
    check.equal(json_data.get("status"), 200, "Expected status to be 200")
    check.is_in("profile updated successful", json_data.get("message", "").lower())

    user_data = json_data.get("data", {})
    check.equal(user_data.get("name"), new_name, "Expected name mismatch")
    check.equal(user_data.get("phone"), new_phone, "Expected phone mismatch")
    check.equal(user_data.get("email"), manage_context_primary_user_register_login["user_payload"]["email"], "Expected email mismatch")




def test_users_patch_profile_update_name_phone_company_200(manage_context_primary_user_register_login):
    new_name = "Updated Tester QATeam"
    new_phone = "8883697531"
    new_company = "Dream Tech Product Inc."
    new_payload = {"name": new_name, "phone": new_phone, "company": new_company}

    response = requests.patch(ApiEndpoints.user_profile(), headers=manage_context_primary_user_register_login["headers_login"], json=new_payload)
    check.equal(response.status_code, 200, f"Expected 200 OK, but got {response.status_code}")

    json_data = response.json()
    check.is_true(json_data.get("success"))
    check.equal(json_data.get("status"), 200)
    check.is_in("profile updated successful", json_data.get("message", "").lower())

    user_data = json_data.get("data", {})
    check.equal(user_data.get("name"), new_name)
    check.equal(user_data.get("phone"), new_phone)
    check.equal(user_data.get("company"), new_company)
    check.equal(user_data.get("email"), manage_context_primary_user_register_login["user_payload"]["email"], "Expected email mismatch")



@pytest.mark.parametrize(
    "scenario_name, invalid_payload, expected_status",
    [
        ("NAME_EMPTY", {"name": ""}, 400),
        ("NAME_NOT_STRING", {"name": 12345}, 400),
        ("NAME_INVALID_DATATYPE", {"name": ["Not", "A", "String"]}, 400),
        ("PHONE_INVALID", {"phone": "abc-def-ghij"}, 400),
        ("PAYLOAD_EMPTY", {}, 400)
    ]
)
def test_users_patch_profile_bad_request_400(scenario_name, invalid_payload, expected_status, manage_context_primary_user_register_login):
    response = requests.patch(ApiEndpoints.user_profile(), json=invalid_payload, headers=manage_context_primary_user_register_login["headers_login"])

    assert response.status_code == expected_status, f"Expected {expected_status}, but got {response.status_code}. Scenario '{scenario_name}' failed."
    assert "bad request" in response.reason.lower()
    json_data = response.json()
    assert json_data.get("success") is False
    assert "message" in json_data



@pytest.mark.parametrize("http_method", ["POST", "PUT", "DELETE"])
def test_users_profile_reject_invalid_methods_404(http_method):
    response = requests.request(
        http_method,
        ApiEndpoints.user_profile()
    )
    status = response.status_code
    assert status == 404, f"Expected 404 for {http_method}, but got {status}"
