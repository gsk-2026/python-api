import pytest
import requests
from pytest_check import check

from config.settings import (
    ApiEndpoints,
    UserTestSteps
)


class StepFailure(Exception):
    pass


def run_step(step_name, func, *args, **kwargs):
    try:
        return func(*args, **kwargs)
    except AssertionError as ae:
        raise StepFailure(f"Fatal error at step: {step_name}, exception: {str(ae)}")
    except Exception as ex:
        raise StepFailure(f"Fatal error at step: {step_name}, exception: {str(ex)}")
    

def test_e2e_a_happy_path_lifecycle(manage_context_primary_user_and_note_id_template):
    try:
        context = manage_context_primary_user_and_note_id_template
        headers_default = context["headers_default"]
        def step_1():
            resp = requests.get(f"{ApiEndpoints.health_check()}", headers=headers_default)
            check.equal(resp.status_code, 200, msg=f"Expected 200, but got {resp.status_code}")
            check.is_true(resp.json().get("success"))
        run_step("E2E_A>Step#1. Health Check", step_1)

        def step_2():
            user_payload = context["user_payload"]
            resp = requests.post(f"{ApiEndpoints.user_register()}", json=user_payload, headers=headers_default)
            check.equal(resp.status_code, 201, msg=f"Expected 201, but got {resp.status_code}")
            check.is_true(resp.json().get("success"))
            manage_context_primary_user_and_note_id_template["user_test_step"] = UserTestSteps.USER_REGISTRATION
        run_step("E2E_A>Step#2. User Registration", step_2)

        def step_3():
            user_payload = context["user_payload"]
            payload = {"email": user_payload["email"], "password": user_payload["password"]}
            resp = requests.post(f"{ApiEndpoints.user_login()}", json=payload, headers=context["headers_default"])
            check.equal(resp.status_code, 200, msg=f"Expected 200, but got {resp.status_code}")
            data = resp.json()
            check.is_true("token" in data["data"], msg="Token missing for User Login")
            manage_context_primary_user_and_note_id_template["token"] = data["data"]["token"]
            manage_context_primary_user_and_note_id_template["headers_login"] = {**context["headers_default"], "x-auth-token": data["data"]["token"]}
            manage_context_primary_user_and_note_id_template["user_test_step"] = UserTestSteps.USER_LOGIN
        run_step("E2E_A>Step#3. User Login", step_3)

        def step_4():
            headers = {**context["headers_login"], "x-auth-token": context["token"]}
            payload = {"title": "E2E Test Note #1", "description": "Verified sequential testing.", "category": "Work"}
            resp = requests.post(f"{ApiEndpoints.notes()}", json=payload, headers=headers)
            check.equal(resp.status_code, 200, msg=f"Expected success, but got {resp.status_code}")
            context["note_id"].append(resp.json()["data"]["id"])
        run_step("E2E_A>Step#4. Note Creation #1", step_4)

        def step_5():
            headers = {**context["headers_login"], "x-auth-token": context["token"]}
            resp = requests.get(f"{ApiEndpoints.notes()}/{context['note_id'][0]}", headers=headers)
            check.equal(resp.status_code, 200, msg=f"Expected 200, but got {resp.status_code}")
            check.equal(resp.json()["data"]["title"], "E2E Test Note #1")
            check.equal(resp.json()["data"]["id"], context["note_id"][0])
        run_step("E2E_A>Step#5. Verify Note #1", step_5)

        def step_6():
            headers = {**context["headers_login"], "x-auth-token": context["token"]}
            resp = requests.delete(f"{ApiEndpoints.notes()}/{context['note_id'][0]}", headers=headers)
            check.equal(resp.status_code, 200, msg=f"Expected 200, but got {resp.status_code}")
            get_res = requests.get(f"{ApiEndpoints.notes()}/{context['note_id'][0]}", headers=headers)
            check.equal(get_res.status_code, 404, msg=f"Expected 404, but got {get_res.status_code}")
            context['note_id'].pop(0)
        run_step("E2E_A>Step#6. Note Deletion #1 and Verification", step_6)

        def step_7():
            headers = {**context["headers_login"], "x-auth-token": context["token"]}
            payload = {"title": "E2E Test Note #2", "description": "Verified sequential testing #2", "category": "Work"}
            resp = requests.post(f"{ApiEndpoints.notes()}", json=payload, headers=headers)
            check.equal(resp.status_code, 200, msg=f"Expected 200, but got {resp.status_code}")
            context["note_id"].append(resp.json()["data"]["id"])
            payload = {"title": "E2E Test Note #3", "description": "Verified sequential testing #3", "category": "Personal"}
            resp = requests.post(f"{ApiEndpoints.notes()}", json=payload, headers=headers)
            check.equal(resp.status_code, 200, msg=f"Expected 200, but got {resp.status_code}")
            context["note_id"].append(resp.json()["data"]["id"])
            payload = {"title": "E2E Test Note #4", "description": "Verified sequential testing #4", "category": "Home"}
            resp = requests.post(f"{ApiEndpoints.notes()}", json=payload, headers=headers)
            check.equal(resp.status_code, 200, msg=f"Expected 200, but got {resp.status_code}")
            context["note_id"].append(resp.json()["data"]["id"])
            payload = {"title": "E2E Test Note #5", "description": "Verified sequential testing #5", "category": "Work"}
            resp = requests.post(f"{ApiEndpoints.notes()}", json=payload, headers=headers)
            check.equal(resp.status_code, 200, msg=f"Expected 200, but got {resp.status_code}")
            context["note_id"].append(resp.json()["data"]["id"])
        run_step("E2E_A>Step#7. Note Creation: #2, #3, #4, #5", step_7)

        def step_8():
            headers = {**context["headers_login"], "x-auth-token": context["token"]}
            resp = requests.get(f"{ApiEndpoints.notes()}", headers=headers)
            check.equal(resp.status_code, 200, msg=f"Expected 200, but got {resp.status_code}")
            check.equal(len(resp.json()["data"]), 4)
            title_set = {"E2E Test Note #2", "E2E Test Note #3", "E2E Test Note #4", "E2E Test Note #5"}
            desc_set= {"Verified sequential testing #2", "Verified sequential testing #3", "Verified sequential testing #4", "Verified sequential testing #5"}
            category_lset = {"Home",  "Work", "Personal"}
            for i in range(len(resp.json()["data"])):
                check.is_in(resp.json()["data"][i]["title"], title_set)
                check.is_in(resp.json()["data"][i]["description"], desc_set)
                check.is_in(resp.json()["data"][i]["category"], category_lset)
        run_step("E2E_A>Step#8. Note Verification #2, #3, #4, #5", step_8)

    except StepFailure:
        pytest.fail("E2E_A : Experienced a fatal step failure and Skipped the rest of the steps")



def test_e2e_b_change_password_logout_relogin(manage_context_primary_user_and_note_id_template):
    try:
        context = manage_context_primary_user_and_note_id_template
        headers_default = context["headers_default"]
        def step_1():
            user_payload = context["user_payload"]
            resp = requests.post(f"{ApiEndpoints.user_register()}", json=user_payload, headers=headers_default)
            check.equal(resp.status_code, 201, msg=f"Expected 201, but got {resp.status_code}")
            check.is_true(resp.json().get("success"))
            manage_context_primary_user_and_note_id_template["user_test_step"] = UserTestSteps.USER_REGISTRATION
        run_step("E2E_B>Step#1. User Register", step_1)

        def step_2():
            user_payload = context["user_payload"]
            resp = requests.post(f"{ApiEndpoints.user_login()}", json=user_payload, headers=context["headers_login"])
            check.equal(resp.status_code, 200, msg=f"Expected 200, but got {resp.status_code}")
            data = resp.json()
            check.is_true("token" in data["data"], msg="Authentication token missing from response structure")
            manage_context_primary_user_and_note_id_template["token"] = data["data"]["token"]
            manage_context_primary_user_and_note_id_template["headers_login"] = {**context["headers_default"], "x-auth-token": data["data"]["token"]}
            manage_context_primary_user_and_note_id_template["user_test_step"] = UserTestSteps.USER_LOGIN
        run_step("E2E_B>Step#2. Initial User Login", step_2)

        def step_3():
            headers = {**context["headers_login"], "x-auth-token": context["token"]}
            user_payload = context["user_payload"]
            password = user_payload["password"]
            new_password = "NEW_" + user_payload["password"]
            payload = {"currentPassword": password, "newPassword": new_password}
            resp = requests.post(f"{ApiEndpoints.user_change_password()}", json=payload, headers=headers)
            check.equal(resp.status_code, 200, msg=f"Expected 200, but got {resp.status_code}")
            check.is_true(resp.json().get("success"))
            manage_context_primary_user_and_note_id_template["user_payload"]["password"] = new_password
            manage_context_primary_user_and_note_id_template["credentials"]["password"] = new_password
        run_step("E2E_B>Step#3. Change User Password", step_3)

        def step_4():
            headers = {**context["headers_login"], "x-auth-token": context["token"]}
            resp = requests.delete(f"{ApiEndpoints.user_logout()}", headers=headers)
            check.equal(resp.status_code, 200, msg=f"Expected 200, but got {resp.status_code}")
            check.is_true(resp.json().get("success"))
            manage_context_primary_user_and_note_id_template["user_test_step"] = UserTestSteps.USER_LOGOUT
        run_step("E2E_B>Step#4. User Logout", step_4)

        def step_5():
            # Attempt to reach a protected profile route with the old token
            headers = {**context["headers_login"], "x-auth-token": context["token"]}
            resp = requests.get(f"{ApiEndpoints.user_profile()}", headers=headers)
            check.equal(resp.status_code, 401, msg=f"Expected 401, but got {resp.status_code}")
        run_step("E2E_B>Step#5. Revoked Session Access Denied after Logout", step_5)

        def step_6():
            user_payload = context["user_payload"]
            payload = {"email": user_payload["email"], "password": user_payload["password"]}
            resp = requests.post(f"{ApiEndpoints.user_login()}", json=payload, headers=context["headers_login"])
            check.equal(resp.status_code, 200, msg=f"Expected 200, but got {resp.status_code}")
            data = resp.json()
            check.is_in("token", data["data"], msg="Token missing For Authentication/Authorization after re-login")
            manage_context_primary_user_and_note_id_template["token"] = data["data"]["token"]
            manage_context_primary_user_and_note_id_template["headers_login"] = {**context["headers_default"], "x-auth-token": data["data"]["token"]}
            manage_context_primary_user_and_note_id_template["user_test_step"] = UserTestSteps.USER_LOGIN
        run_step("E2E_B>Step#6. Re-Login with Changed Password", step_6)

        def step_7():
            user_payload = context["user_payload"]
            headers = {**context["headers_login"], "x-auth-token": context["token"]}
            resp = requests.get(f"{ApiEndpoints.user_profile()}", headers=headers)
            check.equal(resp.status_code, 200, msg=f"Expected 200, but got {resp.status_code}")
            check.equal(resp.json()["data"]["email"], user_payload["email"], msg="Email mismatch found in user profile")
        run_step("E2E_B>Step#7. Validate New Session Access", step_7)

    except StepFailure:
        pytest.fail("E2E_B : Experienced a fatal step failure and Skipped the rest of the steps")



def test_e2e_c_security_check(manage_context_primary_user_and_note_id_template, manage_context_secondary_user_and_note_id_template):
    try:
        context_primary = manage_context_primary_user_and_note_id_template
        context_secondary = manage_context_secondary_user_and_note_id_template
        headers_default = context_secondary.get("headers_default")
        def step_1():
            payload_primary = context_primary["user_payload"]
            resp = requests.post(f"{ApiEndpoints.user_register()}", json=payload_primary, headers=headers_default)
            check.equal(resp.status_code, 201, msg=f"Expected 201, got {resp.status_code}")
            manage_context_primary_user_and_note_id_template["user_test_step"] = UserTestSteps.USER_REGISTRATION
        run_step("E2E_C>Step#1. Register User Account", step_1)

        def step_2():
            check.equal(context_primary["user_test_step"], UserTestSteps.USER_REGISTRATION)
            payload_primary = context_primary["user_payload"]
            resp = requests.post(f"{ApiEndpoints.user_register()}", json=payload_primary, headers=headers_default)
            check.equal(resp.status_code, 409, msg=f"Expected 409, got {resp.status_code}")
            check.is_false(resp.json().get("success"))
            check.equal(resp.json().get("message"), "An account already exists with the same email address")
            manage_context_primary_user_and_note_id_template["user_test_step"] = UserTestSteps.USER_REGISTRATION
        run_step("E2E_C>Step#2. Register User Account with Same Email should be Blocked", step_2)

        def step_3():
            payload = context_primary["user_payload"].copy()
            payload["password"] = f"Invalid_QATesterPSWD@unique_id!"
            resp = requests.post(f"{ApiEndpoints.user_login()}", json=payload, headers=headers_default)
            check.equal(resp.status_code, 400, msg=f"Expected 400, but got {resp.status_code}")
            check.equal(resp.json().get("message"), "Password must be between 6 and 30 characters")
            check.is_false(resp.json().get("success"))
        run_step("E2E_C>Step#3. Verify Login with Invalid Password", step_3)

        def step_4():
            resp = requests.get(f"{ApiEndpoints.notes()}", headers=context_primary["headers_login"])
            assert resp.status_code == 401, f"Expected 401, but got {resp.status_code}"
            check.equal(resp.json().get("message"), "No authentication token specified in x-auth-token header")
        run_step("E2E_C>Step#4. Access Note before login without Token should be Blocked", step_4)

        def step_5():
            ###
            # primary user login
            payload_primary = context_primary["user_payload"]
            resp_login_primary = requests.post(f"{ApiEndpoints.user_login()}", json=payload_primary, headers=headers_default)
            check.equal(resp_login_primary.status_code, 200, msg=f"Expected 200, but got {resp_login_primary.status_code}")
            data_primary= resp_login_primary.json()
            check.is_true("token" in data_primary["data"], msg="Authentication token missing from response structure")
            headers_login_primary = {**headers_default, "x-auth-token": data_primary["data"]["token"]}
            manage_context_primary_user_and_note_id_template["token"] = data_primary["data"]["token"]
            manage_context_primary_user_and_note_id_template["headers_login"] = headers_login_primary
            manage_context_primary_user_and_note_id_template["user_test_step"] = UserTestSteps.USER_LOGIN
            # primary user create note
            payload_note = {
                "title": "QATeam Test Task Title",
                "description": "Verify API endpoint https://practice.expandtesting.com/notes/api/api-docs/#/Notes",
                "category": "Home"      # Home, Work, Personal
            }
            resp_note_primary = requests.post(ApiEndpoints.notes(), headers=headers_login_primary, json=payload_note)
            check.equal(resp_note_primary.status_code, 200) or check.equal(resp_note_primary.status_code, 201)
            # primary user get notes (only one note)
            resp_notes_primary = requests.get(ApiEndpoints.notes(), headers=headers_login_primary)
            check.equal(resp_notes_primary.status_code, 200, msg=f"Expected 200, but got: {resp_notes_primary.status_code}")
            json_data_primary = resp_notes_primary.json()
            check.is_true(json_data_primary.get("success"), msg="Expected success to be True")
            check.is_instance(json_data_primary.get("data"), list, msg="Node data error: expected a array collection list")
            note_details_primary = json_data_primary.get("data", {})
            notes_titles_primary = [note.get("title") for note in note_details_primary]
            notes_descriptions_primary = [note.get("description") for note in note_details_primary]
            notes_categories_primary = [note.get("category") for note in note_details_primary]
            check.greater(len(notes_titles_primary), 0)
            check.equal(len(notes_descriptions_primary), 1)
            check.less(len(notes_categories_primary), 2)
            ###
            # secondary user register
            payload_secondary = context_secondary["user_payload"]
            resp_login_secondary = requests.post(f"{ApiEndpoints.user_register()}", json=payload_secondary, headers=headers_default)
            check.equal(resp_login_secondary.status_code, 201, msg=f"Expected 201, got {resp_login_secondary.status_code}")
            manage_context_primary_user_and_note_id_template["user_test_step"] = UserTestSteps.USER_REGISTRATION
            # secondary user login
            resp_login_secondary = requests.post(f"{ApiEndpoints.user_login()}", json=payload_secondary, headers=headers_default)
            check.equal(resp_login_secondary.status_code, 200, msg=f"Expected 200, but got {resp_login_secondary.status_code}")
            data_secondary = resp_login_secondary.json()
            check.is_true("token" in data_secondary["data"], msg="Authentication token missing from response structure")
            headers_login_secondary = {**headers_default, "x-auth-token": data_secondary ["data"]["token"]}
            manage_context_secondary_user_and_note_id_template["token"] = data_secondary ["data"]["token"]
            manage_context_secondary_user_and_note_id_template["headers_login"] = headers_login_secondary
            manage_context_primary_user_and_note_id_template["user_test_step"] = UserTestSteps.USER_LOGIN
            # secondary user get note (has no note)
            resp_notes_secondary = requests.get(ApiEndpoints.notes(), headers=headers_login_secondary)
            check.equal(resp_notes_secondary.status_code, 200, msg=f"Expected 200, but got: {resp_notes_secondary.status_code}")
            json_data_secondary = resp_notes_secondary.json()
            check.is_true(json_data_secondary.get("success"), msg="Expected success to be True")
            check.is_instance(json_data_secondary.get("data"), list, msg="Node data error: expected a array collection list")
            note_details_secondary = json_data_secondary.get("data", {})
            notes_titles_secondary = [note.get("title") for note in note_details_secondary]
            notes_descriptions_secondary = [note.get("description") for note in note_details_secondary]
            notes_categories_secondary = [note.get("category") for note in note_details_secondary]
            check.greater(len(notes_titles_secondary), -1)
            check.equal(len(notes_descriptions_secondary), 0)
            check.less(len(notes_categories_secondary), 1)
        run_step("E2E_C>Step#5. Access Note before login without Token should be Blocked", step_5)

    except StepFailure:
        pytest.fail("E2E_C : Experienced a fatal step failure and Skipped the rest of the steps.")
