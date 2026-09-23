import time
import pytest
import requests
from pytest_check import check

from config.settings import (
    API_NOTES_ENDPOINT,
    TEST_SLEEP_IN_SECOND
)


"""
Integration test for the API Endpoint: https://practice.expandtesting.com/notes/api/api-docs/#/Notes/delete_notes__id_ 

curl -X 'DELETE' \
  'https://practice.expandtesting.com/notes/api/notes/{id}}' \
  -H 'accept: application/json' \
  -H 'x-auth-token: {auth_token}'
"""


def test_notes_delete_success_200(manage_context_user_register_login_post_note):
    user_note_context = manage_context_user_register_login_post_note
    time.sleep(TEST_SLEEP_IN_SECOND)  # Ensure the note is fully created before deletion
    user_context = user_note_context.get("user_context")
    note_context = user_note_context.get("note_context")
    url = f"{API_NOTES_ENDPOINT}/{note_context.get("note_id")}"
    response = requests.delete(url, headers=user_context.get("headers_login"))
    check.equal(response.status_code, 200, msg=f"Expected 200, but got {response.status_code}")
    user_note_context["note_context"]["already_deleted"] = True

    resp_json = response.json()
    check.is_instance(resp_json, dict, msg=f"Expected resp_json to be a JSON object, but got as {type(resp_json).__name__}.")
    check.is_in("success", resp_json, msg="Expected 'success' property in resp_json, but it is missing")
    check.is_true(resp_json["success"])
    check.is_in("status", resp_json, msg="Expected 'status' property in resp_json, but it is missing")
    check.equal(resp_json["status"], 200)
    check.is_in("message", resp_json, msg="Expected 'message' property in resp_json, but it is missing")
    check.equal(resp_json["message"], "Note successfully deleted")




def test_notes_delete_duplicate_200_404(manage_context_user_register_login_post_note):
    user_note_context = manage_context_user_register_login_post_note
    time.sleep(TEST_SLEEP_IN_SECOND)  # Ensure the note is fully created before deletion
    user_context = user_note_context.get("user_context")
    note_context = user_note_context.get("note_context")
    url = f"{API_NOTES_ENDPOINT}/{note_context.get("note_id")}"
    first_resp = requests.delete(url, headers=user_context.get("headers_login"))
    user_note_context["note_context"]["already_deleted"] = True

    first_json = first_resp.json()
    check.equal(first_resp.status_code, 200)
    check.is_true(first_json["success"])
    check.is_in("Note successfully deleted", first_json["message"])

    second_resp = requests.delete(url, headers=user_context.get("headers_login"))
    second_json = second_resp.json()
    check.equal(second_resp.status_code, 404)
    check.is_false(second_json["success"])
    check.equal(second_json["message"], "No note was found with the provided ID, Maybe it was deleted")




def test_notes_delete_missing_accept_200(manage_context_user_register_login_post_note):
    user_note_context = manage_context_user_register_login_post_note
    user_context = user_note_context.get("user_context")
    note_context = user_note_context.get("note_context")
    time.sleep(TEST_SLEEP_IN_SECOND)  # Ensure the note is fully created before deletion
    url = f"{API_NOTES_ENDPOINT}/{note_context.get("note_id")}"
    headers = user_context["headers_login"].copy()
    headers.pop("Accept", None)

    response = requests.delete(url, headers=headers)
    user_note_context["note_context"]["already_deleted"] = True
    resp_json = response.json()
    check.equal(response.status_code, 200)
    check.is_in("Note successfully deleted", resp_json["message"])



def test_notes_delete_missing_content_type_200(manage_context_user_register_login_post_note):
    user_note_context = manage_context_user_register_login_post_note
    user_context = user_note_context.get("user_context")
    note_context = user_note_context.get("note_context")
    time.sleep(TEST_SLEEP_IN_SECOND)  # Ensure the note is fully created before deletion
    url = f"{API_NOTES_ENDPOINT}/{note_context.get("note_id")}"
    headers = user_context["headers_login"].copy()
    headers.pop("Content-Type", None)

    response = requests.delete(url, headers=headers)
    user_note_context["note_context"]["already_deleted"] = True
    resp_json = response.json()
    check.equal(response.status_code, 200)
    check.is_in("Note successfully deleted", resp_json["message"])



def test_notes_delete_missing_accept_and_content_type_200(manage_context_user_register_login_post_note):
    user_note_context = manage_context_user_register_login_post_note
    user_context = user_note_context.get("user_context")
    note_context = user_note_context.get("note_context")
    time.sleep(TEST_SLEEP_IN_SECOND)  # Ensure the note is fully created before deletion
    url = f"{API_NOTES_ENDPOINT}/{note_context.get("note_id")}"
    headers = user_context["headers_login"].copy()
    headers.pop("Accept", None)
    headers.pop("Content-Type", None)

    response = requests.delete(url, headers=headers)
    user_note_context["note_context"]["already_deleted"] = True
    resp_json = response.json()
    check.equal(response.status_code, 200)
    check.is_in("Note successfully deleted", resp_json["message"])



def test_notes_delete_missing_token_401(manage_context_user_register_login_post_note):
    user_note_context = manage_context_user_register_login_post_note
    user_context = user_note_context.get("user_context")
    note_context = user_note_context.get("note_context")
    time.sleep(TEST_SLEEP_IN_SECOND)  # Ensure the note is fully created before deletion
    url = f"{API_NOTES_ENDPOINT}/{note_context.get("note_id")}"
    headers = user_context["headers_login"].copy()
    headers.pop("x-auth-token", None)

    response = requests.delete(url, headers=headers)
    resp_json = response.json()
    check.equal(response.status_code, 401)
    check.is_in("No authentication token specified in x-auth-token header", resp_json["message"])



@pytest.mark.parametrize("new_token", [
    "",
    "invalid-token",
    "49c42d1403384cf6a37e1b71dd3abec582f06687a32b47a5842bcef90bc30bbe",
    "49c42d1403384cf6a37e1b71dd3abec582f06687a32b47a5842bcef90bc30bbe" * 2
])
def test_notes_delete_note_invalid_token_401(new_token, manage_context_user_register_login_post_note):
    user_note_context = manage_context_user_register_login_post_note
    user_context = user_note_context.get("user_context")
    note_context = user_note_context.get("note_context")
    time.sleep(TEST_SLEEP_IN_SECOND)  # Ensure the note is fully created before deletion
    url = f"{API_NOTES_ENDPOINT}/{note_context.get("note_id")}"
    headers = user_context["headers_login"].copy()
    headers["x-auth-token"] = new_token
    response = requests.delete(url, headers=headers)

    resp_json = response.json()
    check.equal(response.status_code, 401)
    check.is_in(resp_json["message"],[
        "No authentication token specified in x-auth-token header",
        "Access token is not valid or has expired, you will need to login"
    ])



@pytest.mark.parametrize("malformed_id", [
    "non_existent_id_123",
    "~!@#$%^&*()_+-=",
    "507f1f77bcf86cd799439011_extra_characters",
    "'1'='1",
    "'; DROP TABLE Notes; TRUNCATE TABLE Users; --"
])
def test_notes_delete_note_invalid_id_400(malformed_id, manage_context_user_register_login_post_note):
    user_note_context = manage_context_user_register_login_post_note
    user_context = user_note_context.get("user_context")
    time.sleep(TEST_SLEEP_IN_SECOND)  # Ensure the note is fully created before deletion
    url = f"{API_NOTES_ENDPOINT}/{malformed_id}"
    headers = user_context["headers_login"].copy()
    response = requests.delete(url, headers=headers)
    resp_json = response.json()

    check.equal(response.status_code, 400)
    check.equal(response.reason, "Bad Request")
    check.is_false(resp_json["success"])
    check.equal(resp_json["message"], "Note ID must be a valid ID")
