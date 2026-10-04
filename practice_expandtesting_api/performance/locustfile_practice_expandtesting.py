import uuid
from locust import between, task, HttpUser, SequentialTaskSet
from config.settings import TEST_DEFAULT_HEADERS, ApiEndpoints



class NotesLifecycleTest(SequentialTaskSet):

    """
    End-to-end Expand Testing Users Notes Lifecycle:
        1. GET /health-check
        2. POST /users/register
        3. POST /users/login
        4. GET  (Authorize)
        5. GET /users/profile
        6. PATCH /users/profile
        7. POST /notes
        8. PUT /notes/{note_id}
        9. PATCH /notes/{note_id}
        10. GET /notes/{note_id}
        11. GET /notes
        12. DELETE /notes/{note_id}
        13. DELETE /users/delete-account
    """

    name: str
    email: str
    password: str
    token: str | None
    headers_login: dict[str, str] | None
    note_id: str | None

    def on_start(self):
        unique_id = uuid.uuid4().hex[:8]
        self.name = f"QATester {unique_id}"
        self.email = f"qa_tester_{unique_id}@qateam.com"
        self.password = f"QATester_PSWD@{unique_id}!"
        self.token = None
        self.headers_login = None
        self.note_id = None



    # --------------------------------------------------------------------------
    # HAPPY PATHS TESTING
    # --------------------------------------------------------------------------

    @task
    def check_health(self):
        with self.client.get(
                "/health-check",
                headers=TEST_DEFAULT_HEADERS,
                catch_response=True,
                name="GET /health-check"
        ) as response:
            if response.status_code != 200:
                response.failure(f"Health check failed with status: {response.status_code}")
                self.interrupt()
                return


    @task
    def register_user(self):
        payload = {"name": self.name, "email": self.email, "password": self.password}
        with self.client.post(
                "/users/register",
                json=payload,
                headers=TEST_DEFAULT_HEADERS,
                catch_response=True,
                name="POST /users/register"
        ) as response:
            if response.status_code != 201:
                response.failure(f"User Registration failed with status: {response.status_code}")
                self.interrupt()
                return


    @task
    def login_user(self):
        payload = {"email": self.email, "password": self.password}
        with self.client.post(
                "/users/login",
                json=payload,
                headers=TEST_DEFAULT_HEADERS,
                catch_response=True,
                name="POST /users/login"
        ) as response:
            if response.status_code != 200:
                response.failure(f"Failed user login - 'status_code': {response.status_code}")
                #self.interrupt()
                return
            else:
                try:
                    resp_json = response.json()
                    resp_json_data = resp_json["data"]
                    token = resp_json_data["token"]
                    if not isinstance(token, str) or not token:
                        response.failure("Login failed - invalid or missing token")
                        #self.interrupt()
                        return

                    self.token = token
                    self.headers_login = {**TEST_DEFAULT_HEADERS, "x-auth-token": token}
                except (ValueError, KeyError, TypeError) as exc:
                    response.failure(f"Post User login - Unexpected error: {exc}")
                    #self.interrupt()
                    return


    @task
    def authorize_user(self):
        if not self.token:
            return

        with self.client.get(
                "/",
                headers=self.headers_login,
                catch_response=True,
                name="GET /"
        ) as response:
            if response.status_code != 200:
                response.failure(f"Authorizations Failed - 'status_code': {response.status_code}")
                #self.interrupt()
                return


    @task
    def get_profile(self):
        if not self.token:
            return

        with self.client.get(
                "/users/profile",
                headers=self.headers_login,
                catch_response=True,
                name="GET /users/profile"
        ) as response:
            if response.status_code != 200:
                response.failure(f"Failed get profile - 'status_code': {response.status_code}")
                #self.interrupt()
                return


    @task
    def patch_profile(self):
        if not self.token:
            return

        new_payload = {"name": "Updated Tester QATeam"}
        with self.client.patch(
                "/users/profile",
                headers=self.headers_login,
                json=new_payload,
                catch_response=True,
                name="PATCH /users/profile"
        ) as response:
            if response.status_code != 200:
                response.failure(f"Failed patch profile - 'status_code': {response.status_code}")
                #self.interrupt()
                return


    @task
    def post_note(self):
        if not self.token:
            return

        payload = {
            "title": "QATeam Test Task : Note Title",
            "description": "QATeam Test Task : Note Description",
            "category": "Work"      # Home, Work, Personal
        }
        with self.client.post(
                "/notes",
                json=payload,
                headers=self.headers_login,
                catch_response=True,
                name="POST /notes"
        ) as response:
            if response.status_code in [200, 201]:
                try:
                    resp_json = response.json()
                    resp_json_data = resp_json["data"]
                    self.note_id = str(resp_json_data["id"])
                except (ValueError, KeyError, TypeError) as exc:
                    response.failure(f"Post note - Unexpected error: {exc}")
                    #self.interrupt()
                    return
            else:
                response.failure(f"Post note Failed - HTTP Status: {response.status_code}")
                #self.interrupt()
                return


    @task
    def put_note(self):
        if not self.token or not self.note_id:
            return

        payload = {
            "title": "PUT - QATeam Test Task : Note Title",
            "description": "PUT - QATeam Test Task : Note Description",
            "category": "Work",      # Home, Work, Personal
            "completed": True
        }
        with self.client.put(
                f"/notes/{self.note_id}",
                json=payload,
                headers=self.headers_login,
                catch_response=True,
                name="PUT /notes/{note_id}"
        ) as response:
            if response.status_code == 200:
                try:
                    resp_json = response.json()
                    resp_json_data = resp_json["data"]
                    self.note_id = str(resp_json_data["id"])
                except (ValueError, KeyError, TypeError) as exc:
                    response.failure(f"Put note - Unexpected error: {exc}")
                    #self.interrupt()
                    return
            else:
                response.failure(f"Put note Failed - HTTP Status: {response.status_code}")
                #self.interrupt()
                return


    @task
    def patch_note(self):
        if not self.token or not self.note_id:
            return

        payload = { "completed": True }
        with self.client.patch(
                f"/notes/{self.note_id}",
                json=payload,
                headers=self.headers_login,
                catch_response=True,
                name="PATCH /notes/{note_id}"
        ) as response:
            if response.status_code == 200:
                try:
                    resp_json = response.json()
                    resp_json_data = resp_json["data"]
                    self.note_id = str(resp_json_data["id"])
                except (ValueError, KeyError, TypeError) as exc:
                    response.failure(f"Patch note - Unexpected error: {exc}")
                    #self.interrupt()
                    return
            else:
                response.failure(f"Patch note Failed - HTTP Status: {response.status_code}")
                #self.interrupt()
                return


    @task
    def get_note(self):
        if not self.token or not self.note_id:
            return

        with self.client.get(
                f"/notes/{self.note_id}",
                headers=self.headers_login,
                catch_response=True,
                name="GET /notes/{note_id}"
        ) as response:
            if response.status_code == 200:
                try:
                    resp_json = response.json()
                    resp_json_data = resp_json["data"]
                    if self.note_id != str(resp_json_data["id"]):
                        response.failure(f"Get note - ID mismatch: {self.note_id} != {resp_json_data['id']}")
                        #self.interrupt()
                        return
                except (ValueError, KeyError, TypeError) as exc:
                    response.failure(f"Get note - Unexpected error: {exc}")
                    #self.interrupt()
                    return
            else:
                response.failure(f"Get note Failed - HTTP Status: {response.status_code}")
                #self.interrupt()
                return



    @task
    def get_all_note(self):
        if not self.token or not self.note_id:
            return

        with self.client.get(
                "/notes",
                headers=self.headers_login,
                catch_response=True,
                name="GET /notes"
        ) as response:
            if response.status_code == 200:
                try:
                    resp_json = response.json()
                    resp_json_data = resp_json["data"]
                    if not isinstance(resp_json_data, list):
                        response.failure(f"Get all notes - Expected list, got {type(resp_json_data)}")
                        #self.interrupt()
                        return
                    elif not any(str(note["id"]) == self.note_id for note in resp_json_data):
                        response.failure(f"Get all notes - Note ID {self.note_id} not found in response")
                        #self.interrupt()
                        return
                except (ValueError, KeyError, TypeError) as exc:
                    response.failure(f"Get all note - Unexpected error: {exc}")
                    #self.interrupt()
                    return
            else:
                response.failure(f"Get all note - Failed with HTTP Status: {response.status_code}")
                #self.interrupt()
                return



    # -------------------------------a-------------------------------------------
    # NEGATIVE PATHS, BOUNDARIES, AND EDGE CONSTRAINTS TESTING
    # --------------------------------------------------------------------------

    @task
    def get_all_notes_missing_header_token(self):
        if  not self.token:
            return

        with self.client.get(
                "/notes",
                headers=TEST_DEFAULT_HEADERS,
                catch_response=True,
                name="EDGE: GET /notes (Missing Token)"
        ) as response:
            if response.status_code == 401:
                response.success()  # 401 is the expected design behavior
            else:
                response.failure(f"Expected 401 - Security Boundary Leak - 'status_code': {response.status_code}")
                #self.interrupt()
                return

    @task
    def get_all_notes_with_empty_payload(self):
        if  not self.token:
            return

        malformed_payload = {}  # Empty body violations
        with self.client.post(
                "/notes",
                json=malformed_payload,
                headers=self.headers_login,
                catch_response=True,
                name="EDGE: POST /notes (Empty Body)"
        ) as response:
            if response.status_code == 400:
                response.success()  # Validation rules applied effectively under stress
            else:
                response.failure(f"Expected 400 - Bad request protection - 'status_code': {response.status_code}")
                #self.interrupt()
                return


    @task
    def get_note_with_invalid_note_id(self):
        if not self.token:
            return

        invalid_id = "000000000000000000000000"
        with self.client.get(
                f"/notes/{invalid_id}",
                headers=self.headers_login,
                catch_response=True,
                name="BOUND: GET /notes/{invalid_id}"
        ) as response:
            if response.status_code == 404:
                response.success()  # System correctly returned Not Found
            else:
                response.failure(f"Expected 404 - missing parameter mapping - 'status_code': {response.status_code}")
                #self.interrupt()
                return



    # --------------------------------------------------------------------------
    # TEARDOWN
    # --------------------------------------------------------------------------

    @task
    def delete_note(self):
        if not self.token or not self.note_id:
            return
        with self.client.delete(
                f"/notes/{self.note_id}",
                headers=self.headers_login,
                catch_response=True,
                name="DELETE /notes/{note_id}"
        ) as response:
            if response.status_code == 200:
                self.note_id = None
            else:
                response.failure(f"Delete note - cleanup failed - 'status_code': {response.status_code}")

    
    @task
    def delete_account(self):
        if not self.token:
            return
        with self.client.delete(
                "/users/delete-account",
                headers=self.headers_login,
                catch_response=True,
                name="DELETE /users/delete-account"
        ) as response:
            if response.status_code == 200:
                self.token = None
            else:
                response.failure(f"Delete account - cleanup failed - 'status_code': {response.status_code}")



        # --------------------------------------------------------------------------
        # Workflow completed successfully
        # Start a new workflow for this virtual user.
        # --------------------------------------------------------------------------

        self.interrupt()



class NotesLifecycleTestUser(HttpUser):
    host = ApiEndpoints.base_url()
    tasks = [NotesLifecycleTest]
    wait_time = between(0.9, 1.1)
