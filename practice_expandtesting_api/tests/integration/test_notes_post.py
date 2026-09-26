import pytest
import requests
from pytest_check import check
from config.settings import ApiEndpoints


"""
Integration test for the API Endpoints: https://practice.expandtesting.com/notes/api/api-docs/#/Notes/post_notes

curl -X 'POST' \
  'https://practice.expandtesting.com/notes/api/notes' \
  -H 'accept: application/json' \
  -H 'x-auth-token: {auth_token}' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'title={title}&description={description}&category={category}'
"""


def test_notes_post_create_note_200(manage_context_primary_user_register_login):
    user_context = manage_context_primary_user_register_login
    payload = {
        "title": "QATeam Test Task Title",
        "description": "Verify API endpoint https://practice.expandtesting.com/notes/api/api-docs/#/Notes",
        "category": "Home"      # Home, Work, Personal
    }
    response = requests.post(ApiEndpoints.notes(), headers=user_context.get("headers_login"), json=payload)
    check.equal(response.status_code, 200) or check.equal(response.status_code, 201)

    resp_json = response.json()
    check.is_instance(resp_json, dict, msg=f"Expected resp_json to be a JSON object, but got as {type(resp_json).__name__}.")
    check.is_in("success", resp_json, msg="Expected 'success' property in resp_json, but it is missing")
    check.is_true(resp_json["success"])
    check.is_in("status", resp_json, msg="Expected 'status' property in resp_json, but it is missing")
    check.equal(resp_json["status"], 200)
    check.is_in("message", resp_json, msg="Expected 'message' property in resp_json, but it is missing")
    check.equal(resp_json["message"], "Note successfully created")

    check.is_in("data", resp_json, msg="Expected 'data' property in resp_json, but it is missing")
    resp_json_data = resp_json["data"]
    check.is_instance(resp_json_data, dict, msg=f"Expected resp_json_data to be a JSON object, but got as {type(resp_json_data).__name__}.")

    check.is_in("title", resp_json_data, msg="Expected 'title' property in resp_json_data, but it is missing")
    check.equal(resp_json_data["title"], payload["title"])
    check.is_in("description", resp_json_data, msg="Expected 'description' property in resp_json_data, but it is missing")
    check.equal(resp_json_data["description"], payload["description"])
    check.is_in("category", resp_json_data, msg="Expected 'category' property in resp_json_data, but it is missing")
    check.equal(resp_json_data["category"], payload["category"])
    check.is_in("completed", resp_json_data, msg="Expected 'completed' property in resp_json_data, but it is missing")
    check.is_false(resp_json_data["completed"])
    check.is_in("id", resp_json_data, msg="Expected 'id' property in resp_json_data, but it is missing")
    check.is_instance(resp_json_data["id"], str)
    check.greater(len(resp_json_data["id"]), 0)
    check.is_in("created_at", resp_json_data, msg="Expected 'created_at' property in resp_json_data, but it is missing")
    check.is_instance(resp_json_data["created_at"], str)
    check.greater(len(resp_json_data["created_at"]), 0)
    check.is_in("updated_at", resp_json_data, msg="Expected 'updated_at' property in resp_json_data, but it is missing")
    check.is_instance(resp_json_data["updated_at"], str)
    check.greater(len(resp_json_data["updated_at"]), 0)
    check.is_in("user_id", resp_json_data, msg="Expected 'user_id' property in resp_json_data, but it is missing")
    check.is_instance(resp_json_data["user_id"], str)
    check.greater(len(resp_json_data["user_id"]), 0)



def test_notes_post_missing_accept_header_200(manage_context_primary_user_register_login):
    user_context = manage_context_primary_user_register_login
    headers = user_context.get("headers_login").copy()
    del headers["Accept"]
    payload = {
        "title": "QATeam Test Task Title #3",
        "description": "Missing Accept headers context",
        "category": "Personal"      # Home, Work, Personal
    }
    response = requests.post(ApiEndpoints.notes(), headers=headers, json=payload)
    check.is_in(response.status_code, [200, 201]), f"Expected [200, 201], but got {response.status_code}"

    resp_json = response.json()
    check.is_instance(resp_json, dict, msg=f"Expected resp_json to be a JSON object, but got as {type(resp_json).__name__}.")
    check.is_in("success", resp_json, msg="Expected 'success' property in resp_json, but it is missing")
    check.is_true(resp_json["success"])
    check.is_in("status", resp_json, msg="Expected 'status' property in resp_json, but it is missing")
    check.equal(resp_json["status"], 200)
    check.is_in("message", resp_json, msg="Expected 'message' property in resp_json, but it is missing")
    check.equal(resp_json["message"], "Note successfully created")

    check.is_in("data", resp_json, msg="Expected 'data' property in resp_json, but it is missing")
    resp_json_data = resp_json["data"]
    check.is_instance(resp_json_data, dict, msg=f"Expected resp_json_data to be a JSON object, but got as {type(resp_json_data).__name__}.")

    check.is_in("title", resp_json_data, msg="Expected 'title' property in resp_json_data, but it is missing")
    check.equal(resp_json_data["title"], payload["title"])
    check.is_in("description", resp_json_data, msg="Expected 'description' property in resp_json_data, but it is missing")
    check.equal(resp_json_data["description"], payload["description"])
    check.is_in("category", resp_json_data, msg="Expected 'category' property in resp_json_data, but it is missing")
    check.equal(resp_json_data["category"], payload["category"])
    check.is_in("completed", resp_json_data, msg="Expected 'completed' property in resp_json_data, but it is missing")
    check.is_false(resp_json_data["completed"])
    check.is_in("id", resp_json_data, msg="Expected 'id' property in resp_json_data, but it is missing")
    check.is_instance(resp_json_data["id"], str)
    check.greater(len(resp_json_data["id"]), 0)
    check.is_in("created_at", resp_json_data, msg="Expected 'created_at' property in resp_json_data, but it is missing")
    check.is_instance(resp_json_data["created_at"], str)
    check.greater(len(resp_json_data["created_at"]), 0)
    check.is_in("updated_at", resp_json_data, msg="Expected 'updated_at' property in resp_json_data, but it is missing")
    check.is_instance(resp_json_data["updated_at"], str)
    check.greater(len(resp_json_data["updated_at"]), 0)
    check.is_in("user_id", resp_json_data, msg="Expected 'user_id' property in resp_json_data, but it is missing")
    check.is_instance(resp_json_data["user_id"], str)
    check.greater(len(resp_json_data["user_id"]), 0)



def test_notes_post_missing_content_type_header_200(manage_context_primary_user_register_login):
    user_context = manage_context_primary_user_register_login
    headers = user_context.get("headers_login").copy()
    del headers["Content-Type"]
    payload = {
        "title": "QATeam Test Task Title #3",
        "description": "Missing Accept headers context",
        "category": "Personal"      # Home, Work, Personal
    }

    response = requests.post(ApiEndpoints.notes(), headers=headers, json=payload)
    check.is_in(response.status_code, [200, 201]), f"Expected [200, 201], but got {response.status_code}"

    json_data = response.json()
    check.is_true(json_data.get("success"))

    note_data = json_data.get("data", {})
    check.is_in("id", note_data)
    check.is_in("created_at", note_data)
    check.is_in("updated_at", note_data)
    check.equal(note_data.get("title"), payload["title"])
    check.equal(note_data.get("description"), payload["description"])
    check.equal(note_data.get("category"), payload["category"])



def test_notes_post_missing_auth_token_401():
    payload = {
        "title": "QATeam Test Task Title #2",
        "description": "Missing Auth Token headers context",
        "category": "Work"      # Home, Work, Personal
    }
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    response = requests.post(ApiEndpoints.notes(), headers=headers, json=payload)
    check.equal(response.status_code, 401)
    resp_data = response.json()
    check.equal(resp_data.get("status"), 401)
    check.is_false(resp_data.get("success"))
    check.is_in("no authentication token specified in x-auth-token header", resp_data.get("message", "").lower())



@pytest.mark.parametrize(
    "scenario_name, invalid_payload",
    [
        ("TITLE_TOO_LONG", {"title": "OMG!" * 512, "description": "Valid description", "category": "Home"}),
        ("TITLE_EMPTY", {"title": "", "description": "Valid description", "category": "Home"}),
        ("TITLE_UNDER_MIN_LENGTH", {"title": "ab", "description": "Valid description"}),
        ("DESCRIPTION_MISSING", {"title": "Valid Note Structural Title"}),
        ("BLANK_FIELDS", {"title": "   ", "description": "    "}),
        ("CATEGORY_EMPTY", {"title": "Note Title", "description": "Valid description block."})
    ]
)
def test_notes_post_invalid_payload_400(scenario_name, invalid_payload, manage_context_primary_user_register_login):
    user_context = manage_context_primary_user_register_login
    response = requests.post(ApiEndpoints.notes(), headers=user_context.get("headers_login"), json=invalid_payload)
    check.equal(response.status_code, 400, f"Expected 400, but got {response.status_code}. Scenario: {scenario_name} failed")
    check.is_false(response.json().get("success"))



def test_notes_post_data_isolation_verification_200(manage_context_primary_user_register_login, manage_context_secondary_user_register_login):
    p_user_context = manage_context_primary_user_register_login
    s_user_context = manage_context_secondary_user_register_login

    # 1. Primary user creates a specific data note
    p_note_payload = {
        "title": "User A : Note Title",
        "description": "User A : Note Description.",
        "category": "Home"
    }
    creation_resp = requests.post(ApiEndpoints.notes(), headers=p_user_context.get("headers_login"), json=p_note_payload)
    check.is_in(creation_resp.status_code, [200, 201], f"Expected [200, 201], but got {creation_resp.status_code}")
    p_note_id = creation_resp.json().get("data", {}).get("id")

    # 2. Secondary user queries their global note list collection
    s_note_payload = {
        "title": "User B : Note Title",
        "description": "User B : Note Description.",
        "category": "Work"
    }
    requests.post(ApiEndpoints.notes(), headers=s_user_context.get("headers_login"), json=s_note_payload)
    s_notes_resp = requests.get(ApiEndpoints.notes(), headers=s_user_context.get("headers_login"))
    check.equal(s_notes_resp.status_code, 200)

    s_note_ids = [note.get("id") for note in s_notes_resp.json().get("data", [])]
    check.is_not_in(p_note_id, s_note_ids, msg="Critical Security Bug: Note data leaked across user contexts!")
