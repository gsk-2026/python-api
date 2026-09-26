import pytest
import requests
from pytest_check import check
from config.settings import ApiEndpoints


"""
Integration test for the API Endpoints: https://practice.expandtesting.com/notes/api/api-docs/#/Notes/patch_notes__id_

curl -X 'PATCH' \
  'https://practice.expandtesting.com/notes/api/notes/{id}' \
  -H 'accept: application/json' \
  -H 'x-auth-token: {auth_token}' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'completed={completed}'
"""


def test_notes_patch_required_completed_success_200(manage_context_user_register_login_post_note):
    user_note_context = manage_context_user_register_login_post_note
    user_context = user_note_context.get("user_context")
    note_context = user_note_context.get("note_context")
    note_context_data = note_context.get("note_data")
    patch_url = f"{ApiEndpoints.notes()}/{note_context.get('note_id')}"
    completed = False if note_context.get("note_data").get("completed") is True else True
    patch_payload = { "completed": completed }

    response = requests.patch(patch_url, headers=user_context.get("headers_login"), json=patch_payload)
    check.equal(response.status_code, 200, msg=f"Expected 200, but got {response.status_code}")

    resp_json = response.json()
    check.is_instance(resp_json, dict, msg=f"Expected resp_json to be a JSON object, but got as {type(resp_json).__name__}.")
    check.is_in("success", resp_json, msg="Expected 'success' property in resp_json, but it is missing")
    check.is_true(resp_json["success"])
    check.is_in("status", resp_json, msg="Expected 'status' property in resp_json, but it is missing")
    check.equal(resp_json["status"], 200)
    check.is_in("message", resp_json, msg="Expected 'message' property in resp_json, but it is missing")
    check.equal(resp_json["message"], "Note successfully Updated")

    check.is_in("data", resp_json, msg="Expected 'data' property in resp_json, but it is missing")
    resp_json_data = resp_json["data"]
    check.is_instance(resp_json_data, dict, msg=f"Expected resp_json_data to be a JSON object, but got as {type(resp_json_data).__name__}.")

    check.is_in("title", resp_json_data, msg="Expected 'title' property in resp_json_data, but it is missing")
    check.equal(resp_json_data["title"], note_context_data["title"])
    check.is_in("description", resp_json_data, msg="Expected 'description' property in resp_json_data, but it is missing")
    check.equal(resp_json_data["description"], note_context_data["description"])
    check.is_in("category", resp_json_data, msg="Expected 'category' property in resp_json_data, but it is missing")
    check.equal(resp_json_data["category"], note_context_data["category"])
    check.is_in("completed", resp_json_data, msg="Expected 'completed' property in resp_json_data, but it is missing")
    check.equal(resp_json_data["completed"], patch_payload["completed"])
    check.is_in("id", resp_json_data, msg="Expected 'id' property in resp_json_data, but it is missing")
    check.equal(resp_json_data["id"], note_context.get("note_id"))
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





def test_notes_patch_required_completed_and_non_required_title_200(manage_context_user_register_login_post_note):
    user_note_context = manage_context_user_register_login_post_note
    user_context = user_note_context.get("user_context")
    note_context = user_note_context.get("note_context")
    note_context_data = note_context.get("note_data")
    patch_url = f"{ApiEndpoints.notes()}/{note_context.get('note_id')}"
    title = "Updated : " + note_context.get("note_data").get("title")
    completed = False if note_context.get("note_data").get("completed") is True else True
    patch_payload = {"title": f"{title}", "completed": completed}

    response = requests.patch(patch_url, headers=user_context.get("headers_login"), json=patch_payload)
    check.equal(response.status_code, 200, msg=f"Expected 200, but got {response.status_code}")

    resp_json = response.json()
    check.is_instance(resp_json, dict, msg=f"Expected resp_json to be a JSON object, but got as {type(resp_json).__name__}.")
    check.is_in("success", resp_json, msg="Expected 'success' property in resp_json, but it is missing")
    check.is_true(resp_json["success"])
    check.is_in("status", resp_json, msg="Expected 'status' property in resp_json, but it is missing")
    check.equal(resp_json["status"], 200)
    check.is_in("message", resp_json, msg="Expected 'message' property in resp_json, but it is missing")
    check.equal(resp_json["message"], "Note successfully Updated")

    check.is_in("data", resp_json, msg="Expected 'data' property in resp_json, but it is missing")
    resp_json_data = resp_json["data"]
    check.is_instance(resp_json_data, dict, msg=f"Expected resp_json_data to be a JSON object, but got as {type(resp_json_data).__name__}.")

    check.is_in("title", resp_json_data, msg="Expected 'title' property in resp_json_data, but it is missing")
    check.equal(resp_json_data["title"], note_context_data["title"])
    check.is_in("description", resp_json_data, msg="Expected 'description' property in resp_json_data, but it is missing")
    check.equal(resp_json_data["description"], note_context_data["description"])
    check.is_in("category", resp_json_data, msg="Expected 'category' property in resp_json_data, but it is missing")
    check.equal(resp_json_data["category"], note_context_data["category"])
    check.is_in("completed", resp_json_data, msg="Expected 'completed' property in resp_json_data, but it is missing")
    check.equal(resp_json_data["completed"], patch_payload["completed"])
    check.is_in("id", resp_json_data, msg="Expected 'id' property in resp_json_data, but it is missing")
    check.equal(resp_json_data["id"], note_context.get("note_id"))
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





def test_notes_patch_non_required_title_400(manage_context_user_register_login_post_note):
    user_note_context = manage_context_user_register_login_post_note
    user_context = user_note_context.get("user_context")
    note_context = user_note_context.get("note_context")
    patch_url = f"{ApiEndpoints.notes()}/{note_context.get('note_id')}"
    title = "Updated : " + note_context.get("note_data").get("title")
    patch_payload = {"title": f"{title}"}

    response = requests.patch(patch_url, headers=user_context.get("headers_login"), json=patch_payload)
    check.equal(response.status_code, 400)
    check.equal(response.reason, "Bad Request")
    resp_json = response.json()
    check.equal(resp_json.get("message"), 'Note completed status must be boolean')



@pytest.mark.parametrize("new_category", ["Home", "Work", "Personal"])
def test_notes_patch_non_required_category_400(new_category, manage_context_user_register_login_post_note):
    user_note_context = manage_context_user_register_login_post_note
    user_context = user_note_context.get("user_context")
    note_context = user_note_context.get("note_context")
    patch_url = f"{ApiEndpoints.notes()}/{note_context.get('note_id')}"
    patch_payload = {"category": new_category}

    response = requests.patch(patch_url, headers=user_context.get("headers_login"), json=patch_payload)
    check.equal(response.status_code, 400)
    check.equal(response.reason, "Bad Request")

    resp_json = response.json()
    check.equal(resp_json.get("message"), 'Note completed status must be boolean')



def test_notes_patch_empty_object_payload_400(manage_context_user_register_login_post_note):
    user_note_context = manage_context_user_register_login_post_note
    user_context = user_note_context.get("user_context")
    note_context = user_note_context.get("note_context")
    patch_url = f"{ApiEndpoints.notes()}/{note_context.get('note_id')}"
    response = requests.patch(patch_url, headers=user_context.get("headers_login"), json={})

    check.equal(response.status_code, 400)
    check.equal(response.reason, "Bad Request")
    resp_json = response.json()
    check.equal(resp_json.get("message"), 'Note completed status must be boolean')



def test_notes_patch_missing_auth_token_401(manage_context_user_register_login_post_note):
    user_note_context = manage_context_user_register_login_post_note
    user_context = user_note_context.get("user_context")
    note_context = user_note_context.get("note_context")
    patch_url = f"{ApiEndpoints.notes()}/{note_context.get('note_id')}"
    headers = user_context.get("headers_login").copy()
    headers.pop("x-auth-token")

    response = requests.patch(patch_url, headers=headers, json={"completed": True})
    check.equal(response.status_code, 401)
    check.equal(response.reason, "Unauthorized")



def test_notes_patch_missing_accept_200(manage_context_user_register_login_post_note):
    user_note_context = manage_context_user_register_login_post_note
    user_context = user_note_context.get("user_context")
    note_context = user_note_context.get("note_context")
    patch_url = f"{ApiEndpoints.notes()}/{note_context.get('note_id')}"
    headers = user_context.get("headers_login").copy()
    headers.pop("Accept")
    completed = False if note_context.get("note_data").get("completed") is True else True
    patch_payload = { "completed": completed}

    response = requests.patch(patch_url, headers=headers, json={"completed": True})
    check.equal(response.status_code, 200)

    resp_data = response.json().get("data", {})
    check.equal(resp_data["id"], note_context.get("note_data").get("id"))
    check.equal(resp_data["title"], note_context.get("note_data").get("title"))  # Confirm unchanged, and PATCH is ignored on title
    check.equal(resp_data["description"], note_context.get("note_data").get("description"))
    check.equal(resp_data["category"], note_context.get("note_data").get("category"))
    check.equal(resp_data["completed"], patch_payload["completed"])



def test_notes_patch_missing_content_type_200(manage_context_user_register_login_post_note):
    user_note_context = manage_context_user_register_login_post_note
    user_context = user_note_context.get("user_context")
    note_context = user_note_context.get("note_context")
    patch_url = f"{ApiEndpoints.notes()}/{note_context.get('note_id')}"
    headers = user_context.get("headers_login").copy()
    headers.pop("Content-Type")
    completed = False if note_context.get("note_data").get("completed") is True else True
    patch_payload = { "completed": completed}

    response = requests.patch(patch_url, headers=headers, json={"completed": True})
    check.equal(response.status_code, 200)

    resp_data = response.json().get("data", {})
    check.equal(resp_data["id"], note_context.get("note_data").get("id"))
    check.equal(resp_data["title"], note_context.get("note_data").get("title"))  # Confirm unchanged, and PATCH is ignored on title
    check.equal(resp_data["description"], note_context.get("note_data").get("description"))
    check.equal(resp_data["category"], note_context.get("note_data").get("category"))
    check.equal(resp_data["completed"], patch_payload["completed"])



@pytest.mark.parametrize("new_completed", [ "True", "False", "Yes", "No", '2', 2 ])
def test_notes_patch_required_completed_invalid_datatype_400(new_completed, manage_context_user_register_login_post_note):
    user_note_context = manage_context_user_register_login_post_note
    user_context = user_note_context.get("user_context")
    note_context = user_note_context.get("note_context")
    patch_url = f"{ApiEndpoints.notes()}/{note_context.get('note_id')}"
    patch_payload = {"completed": new_completed}

    response = requests.patch(patch_url, headers=user_context.get("headers_login"), json=patch_payload)
    check.equal(response.status_code, 400)
    check.equal(response.reason, "Bad Request")



@pytest.mark.parametrize("new_completed", [ '1', '0', 1, 0 ])
def test_notes_patch_required_completed_valid_datatype_400(new_completed, manage_context_user_register_login_post_note):
    user_note_context = manage_context_user_register_login_post_note
    user_context = user_note_context.get("user_context")
    note_context = user_note_context.get("note_context")
    patch_url = f"{ApiEndpoints.notes()}/{note_context.get('note_id')}"
    patch_payload = {"completed": new_completed}

    response = requests.patch(patch_url, headers=user_context.get("headers_login"), json=patch_payload)
    check.equal(response.status_code, 200)
    check.equal(response.reason, "OK")

    resp_data = response.json().get("data", {})
    check.equal(resp_data["id"], note_context.get("note_data").get("id"))
    check.equal(resp_data["title"], note_context.get("note_data").get("title"))  # Confirm unchanged, and PATCH is ignored on title
    check.equal(resp_data["description"], note_context.get("note_data").get("description"))
    check.equal(resp_data["category"], note_context.get("note_data").get("category"))
    check.equal(resp_data["completed"], bool(int(patch_payload["completed"])))
