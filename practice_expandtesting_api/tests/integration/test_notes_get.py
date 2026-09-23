import uuid
import pytest
import requests
from pytest_check import check

from config.settings import (
    API_NOTES_ENDPOINT
)


"""
Integration test for the API Endpoints: 
    https://practice.expandtesting.com/notes/api/api-docs/#/Notes/get_notes
    https://practice.expandtesting.com/notes/api/api-docs/#/Notes/get_notes__id_
    
curl -X 'GET' \
  'https://practice.expandtesting.com/notes/api/notes' \
  -H 'accept: application/json' \
  -H 'x-auth-token: {auth_token}'
  
curl -X 'GET' \
  'https://practice.expandtesting.com/notes/api/notes/{id}' \
  -H 'accept: application/json' \
  -H 'x-auth-token: {auth_token}'
"""


def test_notes_get_all_notes_200(manage_context_user_register_login_post_note):
    user_note_context = manage_context_user_register_login_post_note
    user_context = user_note_context.get("user_context")
    note_context = user_note_context.get("note_context")
    note_context_data = note_context.get("note_data")

    response = requests.get(API_NOTES_ENDPOINT, headers=user_context.get("headers_login"))
    check.equal(response.status_code, 200, msg=f"Expected 200, but got: {response.status_code}")

    resp_json = response.json()
    check.is_instance(resp_json, dict, msg=f"Expected resp_json to be a JSON object, but got as {type(resp_json).__name__}.")
    check.is_in("success", resp_json, msg="Expected 'success' property in resp_json, but it is missing")
    check.is_true(resp_json["success"])
    check.is_in("status", resp_json, msg="Expected 'status' property in resp_json, but it is missing")
    check.equal(resp_json["status"], 200)
    check.is_in("message", resp_json, msg="Expected 'message' property in resp_json, but it is missing")
    check.equal(resp_json["message"], "Notes successfully retrieved")

    check.is_in("data", resp_json, msg="Expected 'data' property in resp_json, but it is missing")
    note_details = resp_json["data"]
    check.is_instance(note_details, list, msg=f"Expected resp_json_data to be a LIST object, but got as {type(note_details).__name__}.")

    notes_ids = [note.get("id") for note in note_details]
    notes_titles = [note.get("title") for note in note_details]
    notes_descriptions = [note.get("description") for note in note_details]
    notes_categories = [note.get("category") for note in note_details]
    notes_completes = [note.get("completed") for note in note_details]
    notes_created_ats = [note.get("created_at") for note in note_details]
    notes_updated_ats = [note.get("updated_at") for note in note_details]
    notes_user_ids = [note.get("user_id") for note in note_details]

    check.is_in(note_context_data.get("id"), notes_ids)
    check.is_in(note_context_data.get("title"), notes_titles)
    check.is_in(note_context_data.get("description"), notes_descriptions)
    check.is_in(note_context_data.get("category"), notes_categories)
    check.is_in(note_context_data.get("completed"), notes_completes)
    check.is_in(note_context_data.get("created_at"), notes_created_ats)
    check.is_in(note_context_data.get("updated_at"), notes_updated_ats)
    check.is_in(note_context_data.get("user_id"), notes_user_ids)




def test_notes_get_note_by_id_200(manage_context_user_register_login_post_note):
    user_note_context = manage_context_user_register_login_post_note
    user_context = user_note_context.get("user_context")
    note_context = user_note_context.get("note_context")
    note_context_data = note_context.get("note_data")
    target_url = f"{API_NOTES_ENDPOINT}/{note_context.get("note_id")}"

    response = requests.get(target_url, headers=user_context.get("headers_login"))
    check.equal(response.status_code, 200, msg=f"Expected 200, but got: {response.status_code}")

    json_data = response.json()
    check.is_true(json_data.get("success"))

    note_details = json_data.get("data", {})
    check.equal(note_details.get("id"), note_context.get("note_id"))
    check.is_in("title", note_details)
    check.is_in("description", note_details)
    check.is_in("category", note_details)

    resp_json = response.json()
    check.is_instance(resp_json, dict, msg=f"Expected resp_json to be a JSON object, but got as {type(resp_json).__name__}.")
    check.is_in("success", resp_json, msg="Expected 'success' property in resp_json, but it is missing")
    check.is_true(resp_json["success"])
    check.is_in("status", resp_json, msg="Expected 'status' property in resp_json, but it is missing")
    check.equal(resp_json["status"], 200)
    check.is_in("message", resp_json, msg="Expected 'message' property in resp_json, but it is missing")
    check.equal(resp_json["message"], "Note successfully retrieved")

    check.is_in("data", resp_json, msg="Expected 'data' property in resp_json, but it is missing")
    resp_json_data = resp_json["data"]
    check.is_instance(resp_json_data, dict, msg=f"Expected resp_json_data to be a LIST object, but got as {type(resp_json_data).__name__}.")

    check.is_in(note_context_data.get("id"), resp_json_data.get("id"))
    check.is_in(note_context_data.get("title"), resp_json_data.get("title"))
    check.is_in(note_context_data.get("description"), resp_json_data.get("description"))
    check.is_in(note_context_data.get("category"), resp_json_data.get("category"))
    #check.is_in(note_context_data.get("completed"), resp_json_data.get("completed"))
    check.is_in(note_context_data.get("created_at"), resp_json_data.get("created_at"))
    check.is_in(note_context_data.get("updated_at"), resp_json_data.get("updated_at"))
    check.is_in(note_context_data.get("user_id"), resp_json_data.get("user_id"))




@pytest.mark.parametrize("path", ["../notes"])
def test_notes_get_path_traversal_without_notes_200(path, manage_context_primary_user_register_login):
    user_context = manage_context_primary_user_register_login 
    target_url = f"{API_NOTES_ENDPOINT}/{path}"

    response = requests.get(target_url, headers=user_context.get("headers_login"))
    check.equal(response.status_code, 200)

    json_data = response.json()
    check.is_true(json_data.get("success"))

    note_details = json_data.get("data", {})
    check.equal(len(note_details), 0)



@pytest.mark.parametrize("path", ["../notes"])
def test_notes_get_path_traversal_with_notes_200(path, manage_context_user_register_login_post_note):
    user_note_context = manage_context_user_register_login_post_note
    user_context = user_note_context.get("user_context")
    target_url = f"{API_NOTES_ENDPOINT}/{path}"
    response = requests.get(target_url, headers=user_context.get("headers_login"))

    check.equal(response.status_code, 200)
    json_data = response.json()
    check.is_true(json_data.get("success"))

    note_details = json_data.get("data", {})
    check.greater(len(note_details), 0)



def test_notes_get_missing_auth_token_401():
    headers = {"Accept": "application/json"}
    response = requests.get(API_NOTES_ENDPOINT, headers=headers)
    check.equal(response.status_code, 401)
    check.is_in("no authentication token specified in x-auth-token header", response.json().get("message", "").lower())



@pytest.mark.parametrize("note_id", ["invalid-note-id", "{id}"])
def test_notes_get_invalid_note_id_400(note_id, manage_context_primary_user_register_login):
    user_context = manage_context_primary_user_register_login
    target_url = f"{API_NOTES_ENDPOINT}/{note_id}"
    response = requests.get(target_url, headers=user_context.get("headers_login"))

    check.equal(response.status_code, 400)
    check.is_in("bad request", response.reason.lower())
    check.is_in("note id must be a valid id", response.json().get("message", "").lower())



def test_notes_get_valid_but_nonexistent_note_id_404(manage_context_primary_user_register_login):
    user_context = manage_context_primary_user_register_login
    non_existent_hex_id = uuid.uuid4().hex[:24]
    target_url = f"{API_NOTES_ENDPOINT}/{non_existent_hex_id}"
    response = requests.get(target_url, headers=user_context.get("headers_login"))
    check.equal(response.status_code, 404)
    check.is_false(response.json().get("success"))
    check.equal(response.content, b'{"success":false,"status":404,"message":"No note was found with the provided ID, Maybe it was deleted"}')



@pytest.mark.parametrize("endpoint_path", ["/getnode/id"])
def test_notes_get_invalid_path_404(endpoint_path, manage_context_primary_user_register_login):
    user_context = manage_context_primary_user_register_login
    target_url = f"{API_NOTES_ENDPOINT}{endpoint_path}"
    response = requests.get(target_url, headers=user_context.get("headers_login"))

    check.equal(response.status_code, 404)
    check.is_in("not found", response.reason.lower())
    check.is_in("not found", response.json().get("message", "").lower())



@pytest.mark.parametrize("corrupt_id", [
        " ",
        "shortID",
        "'; DROP TABLE notes; TRUNCATE TABLE users; --",    # SQL Injection query payload entry test
        "' OR '1'='1"
])
def test_notes_get_path_parameter_anomalies_400(corrupt_id, manage_context_primary_user_register_login):
    user_context = manage_context_primary_user_register_login
    target_url = f"{API_NOTES_ENDPOINT}/{corrupt_id}"
    response = requests.get(target_url, headers=user_context.get("headers_login"))
    check.equal(response.status_code, 400)
    check.not_equal(response.status_code, 500)



@pytest.mark.parametrize("corrupt_path", [
        "../config",            # Path traversal attack vector string mutation
        "../configure",
        "../admin"
])
def test_notes_get_path_anomalies_404(corrupt_path, manage_context_primary_user_register_login):
    user_context = manage_context_primary_user_register_login
    target_url = f"{API_NOTES_ENDPOINT}/{corrupt_path}"
    response = requests.get(target_url, headers=user_context.get("headers_login"))
    check.equal(response.status_code, 404)
    check.not_equal(response.status_code, 500)



def test_notes_get_security_cross_tenant_isolation_breach_404(manage_context_secondary_user_register_login, manage_context_user_register_login_post_note):
    s_user_context = manage_context_secondary_user_register_login

    p_user_note_context = manage_context_user_register_login_post_note
    p_note_context = p_user_note_context.get("note_context")

    target_url = f"{API_NOTES_ENDPOINT}/{p_note_context.get('note_id')}"

    # Secondary User attempts to access Primary User's generated resource note ID
    response = requests.get(target_url, headers=s_user_context.get("headers_login"))
    check.equal(response.status_code, 404)
    check.is_in('not found', response.reason.lower())
    check.equal(response.text, '{"success":false,"status":404,"message":"No note was found with the provided ID, Maybe it was deleted"}')

    if response.status_code == 200:
        pytest.fail("Critical Security Vulnerability: Vertical privilege escalation detected leading to unauthorized data access")
