import pytest
import requests
from pytest_check import check
from config.settings import API_NOTES_ENDPOINT


"""
Integration test for the API Endpoints: https://practice.expandtesting.com/notes/api/api-docs/#/Notes/put_notes__id_

curl -X 'PUT' \
  'https://practice.expandtesting.com/notes/api/notes/{id}' \
  -H 'accept: application/json' \
  -H 'x-auth-token: {auth_token}' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'title={title}&description={description}&completed={completed}&category={category}'
"""


def test_notes_put_success_200(manage_context_user_register_login_post_note):
    user_note_context = manage_context_user_register_login_post_note
    user_context = user_note_context.get("user_context")
    note_context = user_note_context.get("note_context")
    put_url = f"{API_NOTES_ENDPOINT}/{note_context.get('note_id')}"
    update_payload = {
        "title": "Updated : QATester Test Task : Note Title",
        "description": "Updated : Note content description",
        "category": "Work",
        "completed": True
    }
    response = requests.put(put_url, headers=user_context.get("headers_login"), json=update_payload)
    check.equal(response.status_code, 200, f"Expected 200 OK, but got {response.status_code}")

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
    check.equal(resp_json_data["title"], update_payload["title"])
    check.is_in("description", resp_json_data, msg="Expected 'description' property in resp_json_data, but it is missing")
    check.equal(resp_json_data["description"], update_payload["description"])
    check.is_in("category", resp_json_data, msg="Expected 'category' property in resp_json_data, but it is missing")
    check.equal(resp_json_data["category"], update_payload["category"])
    check.is_in("completed", resp_json_data, msg="Expected 'completed' property in resp_json_data, but it is missing")
    check.is_true(resp_json_data["completed"])
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



def test_notes_put_missing_accept_header_200(manage_context_user_register_login_post_note):
    user_note_context = manage_context_user_register_login_post_note
    user_context = user_note_context.get("user_context")
    note_context = user_note_context.get("note_context")
    put_url = f"{API_NOTES_ENDPOINT}/{note_context.get('note_id')}"
    update_payload = {
        "title": "Updated : QATester Test Task : Note Title",
        "description": "Updated : Note content description",
        "category": "Personal",
        "completed": True
    }
    headers = user_context.get("headers_login").copy()
    headers.pop("Accept", None)
    response = requests.put(put_url, headers=headers, json=update_payload)
    check.equal(response.status_code, 200, f"Expected 200 OK, but got {response.status_code}")

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
    check.equal(resp_json_data["title"], update_payload["title"])
    check.is_in("description", resp_json_data, msg="Expected 'description' property in resp_json_data, but it is missing")
    check.equal(resp_json_data["description"], update_payload["description"])
    check.is_in("category", resp_json_data, msg="Expected 'category' property in resp_json_data, but it is missing")
    check.equal(resp_json_data["category"], update_payload["category"])
    check.is_in("completed", resp_json_data, msg="Expected 'completed' property in resp_json_data, but it is missing")
    check.is_true(resp_json_data["completed"])
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



def test_notes_put_missing_content_type_header_200(manage_context_user_register_login_post_note):
    user_note_context = manage_context_user_register_login_post_note
    user_context = user_note_context.get("user_context")
    note_context = user_note_context.get("note_context")
    put_url = f"{API_NOTES_ENDPOINT}/{note_context.get('note_id')}"
    update_payload = {
        "title": "Updated : QATester Test Task : Note Title",
        "description": "Updated : Note content description",
        "category": "Personal",
        "completed": True
    }
    headers = user_context.get("headers_login").copy()
    headers.pop("Content-Type", None)
    response = requests.put(put_url, headers=headers, json=update_payload)
    check.equal(response.status_code, 200, f"Expected 200 OK, but got {response.status_code}")


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
    check.equal(resp_json_data["title"], update_payload["title"])
    check.is_in("description", resp_json_data, msg="Expected 'description' property in resp_json_data, but it is missing")
    check.equal(resp_json_data["description"], update_payload["description"])
    check.is_in("category", resp_json_data, msg="Expected 'category' property in resp_json_data, but it is missing")
    check.equal(resp_json_data["category"], update_payload["category"])
    check.is_in("completed", resp_json_data, msg="Expected 'completed' property in resp_json_data, but it is missing")
    check.is_true(resp_json_data["completed"])
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



def test_notes_put_missing_auth_token_header_401(manage_context_user_register_login_post_note):
    user_note_context = manage_context_user_register_login_post_note
    user_context = user_note_context.get("user_context")
    note_context = user_note_context.get("note_context")
    put_url = f"{API_NOTES_ENDPOINT}/{note_context.get('note_id')}"
    update_payload = {
        "title": "Updated : QATester Test Task : Note Title",
        "description": "Updated : Note content description",
        "category": "Personal",
        "completed": True
    }
    headers = user_context.get("headers_login").copy()
    headers.pop("x-auth-token", None)
    response = requests.put(put_url, headers=headers, json=update_payload)
    check.equal(response.status_code, 401, f"Expected 401 Unauthorized, but got {response.status_code}")
    note_json = response.json()
    check.equal(note_json.get("message", ""), 'No authentication token specified in x-auth-token header')



@pytest.mark.parametrize("auth_token", [
    "",
    "invalid-note-id"
])
def test_notes_put_invalid_auth_token_header_401(auth_token, manage_context_user_register_login_post_note):
    user_note_context = manage_context_user_register_login_post_note
    user_context = user_note_context.get("user_context")
    note_context = user_note_context.get("note_context")
    put_url = f"{API_NOTES_ENDPOINT}/{note_context.get('note_id')}"
    update_payload = {
        "title": "Updated : QATester Test Task : Note Title",
        "description": "Updated : Note content description",
        "category": "Personal",
        "completed": True
    }
    headers = user_context.get("headers_login").copy()
    headers["x-auth-token"] = auth_token
    response = requests.put(put_url, headers=headers, json=update_payload)
    check.equal(response.status_code, 401, f"Expected 401 Unauthorized, but got {response.status_code}")
    note_json = response.json()
    check.is_in(note_json.get("message", ""), ['No authentication token specified in x-auth-token header',
                                            'Access token is not valid or has expired, you will need to login'])



@pytest.mark.parametrize("expired_auth_token", [
    "47c0a2bf8efb41989c20993f0d9e2fdc4a941992ae6b4e3ebcb3871bfbd61bf8"
])
def test_notes_put_expired_auth_token_header_404(expired_auth_token, manage_context_user_register_login_post_note):
    user_note_context = manage_context_user_register_login_post_note
    user_context = user_note_context.get("user_context")
    note_context = user_note_context.get("note_context")
    put_url = f"{API_NOTES_ENDPOINT}/{note_context.get('note_id')}"
    update_payload = {
        "title": "Updated : QATester Test Task : Note Title",
        "description": "Updated : Note content description",
        "category": "Personal",
        "completed": True
    }
    headers = user_context.get("headers_login").copy()
    headers["x-auth-token"] = expired_auth_token
    response = requests.put(put_url, headers=headers, json=update_payload)
    check.not_equal(headers.get('x-auth-token', ""), user_context.get("headers_login").get('x-auth-token', ""))
    check.equal(headers.get('x-auth-token', ""), expired_auth_token)
    check.equal(response.status_code, 404, f"Expected 404 Not Found, but got {response.status_code}")

    note_json = response.json()
    check.is_in(note_json.get("message", ""), ['No note was found with the provided ID, Maybe it was deleted'])



@pytest.mark.parametrize("invalid_title", [
    123456,
    1234*5-1234,
    "OMG!"
])
def test_notes_put_invalid_title_200(invalid_title, manage_context_user_register_login_post_note):
    user_note_context = manage_context_user_register_login_post_note
    user_context = user_note_context.get("user_context")
    note_context = user_note_context.get("note_context")
    put_url = f"{API_NOTES_ENDPOINT}/{note_context.get('note_id')}"
    update_payload = {
        "title": f"{invalid_title}",            # Expects String type
        "description": "Updated : Note content description",
        "category": "Home",
        "completed": True
    }
    headers = user_context.get("headers_login").copy()
    response = requests.put(put_url, headers=headers, json=update_payload)
    resp_json = response.json()
    resp_data = resp_json.get("data", {})

    check.equal(response.status_code, 200, f"Expected 200 OK, but got {response.status_code}")
    check.is_true(response.json()["success"], f"Expected success to be True, but got {response.json()['success']}")
    check.equal(response.reason, "OK", f"Expected reason to be 'OK', but got {response.reason}")
    check.equal(resp_data["completed"], True, f"Expected completed to be True, but got {resp_data['completed']}")
    check.equal(resp_data["title"], str(update_payload["title"]), f"Expected title to be {str(update_payload['title'])}, but got {resp_data['title']}")
    check.equal(resp_data["category"], update_payload["category"], f"Expected category to be {update_payload['category']}, but got {resp_data['category']}")
    check.equal(resp_data["id"], note_context.get('note_id'), f"Expected id to be {note_context.get('note_id')}, but got {resp_data['id']}")



@pytest.mark.parametrize("invalid_category", [
    "Office", "WFH", "", 123             # Home, Work, Personal
])
def test_notes_put_invalid_category_enum_400( invalid_category, manage_context_user_register_login_post_note):
    user_note_context = manage_context_user_register_login_post_note
    user_context = user_note_context.get("user_context")
    note_context = user_note_context.get("note_context")
    put_url = f"{API_NOTES_ENDPOINT}/{note_context.get('note_id')}"
    bad_payload = {
        "title": "Updated : QATester Test Task : Note Title",
        "description": "Updated : Note content description",
        "category": invalid_category,
        "completed": False
    }
    response = requests.put(put_url, headers=user_context.get("headers_login"), json=bad_payload)
    check.equal(response.status_code, 400, f"Expected 400 Bad Request, but got {response.status_code}")
    check.is_false(response.json()["success"], f"Expected success to be False, but got {response.json()['success']}")
    check.equal(response.reason, "Bad Request", f"Expected reason to be 'Bad Request', but got {response.reason}")



@pytest.mark.parametrize("invalid_completed", [
    "", "Yes", "No"            # True, False
])
def test_notes_put_invalid_completed_enum_400(invalid_completed, manage_context_user_register_login_post_note):
    user_note_context = manage_context_user_register_login_post_note
    user_context = user_note_context.get("user_context")
    note_context = user_note_context.get("note_context")
    put_url = f"{API_NOTES_ENDPOINT}/{note_context.get('note_id')}"
    bad_payload = {
        "title": "Updated : QATester Test Task : Note Title",
        "description": "Updated : Note content description",
        "category": "Personal",
        "completed": invalid_completed
    }
    response = requests.put(put_url, headers=user_context.get("headers_login"), json=bad_payload)
    check.equal(response.status_code, 400, f"Expected 400 Bad Request, but got {response.status_code}")
    check.is_false(response.json()["success"], f"Expected success to be False, but got {response.json()['success']}")
    check.equal(response.reason, "Bad Request", f"Expected reason to be 'Bad Request', but got {response.reason}")



@pytest.mark.parametrize("valid_completed", [
    "1", "0", 1, 0             # True, False
])
def test_notes_put_valid_completed_enum_200(valid_completed, manage_context_user_register_login_post_note):
    user_note_context = manage_context_user_register_login_post_note
    user_context = user_note_context.get("user_context")
    note_context = user_note_context.get("note_context")
    put_url = f"{API_NOTES_ENDPOINT}/{note_context.get('note_id')}"
    update_payload = {
        "title": "Updated : QATester Test Task : Note Title",
        "description": "Updated : Note content description",
        "category": "Personal",
        "completed": valid_completed
    }
    response = requests.put(put_url, headers=user_context.get("headers_login"), json=update_payload)
    check.equal(response.status_code, 200, f"Expected 200 OK, but got {response.status_code}")
    check.is_true(response.json()["success"], f"Expected success to be True, but got {response.json()['success']}")
    resp_json = response.json()
    resp_data = resp_json.get("data", {})
    check.is_true(resp_json["success"], f"Expected success to be True, but got {resp_json['success']}")

    if valid_completed in ["1", 1]:
        check.is_true(resp_data["completed"], f"Expected completed to be True, but got {resp_data['completed']}")
    elif valid_completed in ["0", 0]:
        check.is_false(resp_data["completed"], f"Expected completed to be False, but got {resp_data['completed']}")

    check.equal(resp_data["title"], update_payload["title"], f"Expected title to be {update_payload['title']}, but got {resp_data['title']}")
    check.equal(resp_data["category"], update_payload["category"], f"Expected category to be {update_payload['category']}, but got {resp_data['category']}")
    check.equal(resp_data["id"], note_context.get("note_id"), f"Expected id to be {note_context.get('note_id')}, but got {resp_data['id']}")



@pytest.mark.parametrize("fake_id", [
    123456,
    "abcdef",
    "60b9f06a8f1b2c0015a12345" * 2
])
def test_notes_put_non_existent_id_400(fake_id, manage_context_primary_user_register_login):
    user_context = manage_context_primary_user_register_login
    put_url = f"{API_NOTES_ENDPOINT}/{fake_id}"
    update_payload = {
        "title": "Updated : QATester Test Task : Note Title",
        "description": "Updated : Note content description",
        "category": "Personal",
        "completed": True
    }
    response = requests.put(put_url, headers=user_context.get("headers_login"), json=update_payload)
    check.equal(response.status_code, 400, f"Expected 400 Bad Request, but got {response.status_code}")
    check.is_false(response.json()["success"], f"Expected success to be False, but got {response.json()['success']}")
    check.equal(response.reason, "Bad Request", f"Expected reason to be 'Bad Request', but got {response.reason}")




@pytest.mark.parametrize("fake_id", [
    "60b9f06a8f1b2c0015a12345"
])
def test_notes_put_deleted_id_404(fake_id, manage_context_primary_user_register_login):
    user_context = manage_context_primary_user_register_login
    put_url = f"{API_NOTES_ENDPOINT}/{fake_id}"
    update_payload = {
        "title": "Updated : QATester Test Task : Note Title",
        "description": "Updated : Note content description",
        "category": "Personal",
        "completed": True
    }
    response = requests.put(put_url, headers=user_context.get("headers_login"), json=update_payload)
    check.equal(response.status_code, 404, f"Expected 404 Not Found, but got {response.status_code}")
    check.is_false(response.json()["success"], f"Expected success to be False, but got {response.json()['success']}")
    check.equal(response.reason, "Not Found", f"Expected reason to be 'Not Found', but got {response.reason}")
