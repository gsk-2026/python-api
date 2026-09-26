import uuid
from locust import between, task, HttpUser, SequentialTaskSet, User
from config.settings import TEST_DEFAULT_HEADERS, ApiEndpoints



class NotesLifecycleLoadTest(SequentialTaskSet):

    def __init__(self, parent: User) -> None:
        super().__init__(parent)
        self.name = None
        self.email = None
        self.password = None
        self.token = None
        self.headers_login = None
        self.note_id = None


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
        with self.client.get("/health-check", headers=TEST_DEFAULT_HEADERS, catch_response=True, name="GET /health-check") as response:
            if response.status_code != 200:
                response.failure(f"Health check failed with status: {response.status_code}")
                print("Health Check Failed. Stopping all remaining tasks")
                self.interrupt()    # Immediately return if Health Check fail
                return


    @task
    def register_user(self):
        payload = {"name": self.name, "email": self.email, "password": self.password}
        with self.client.post("/users/register", json=payload, headers=TEST_DEFAULT_HEADERS, catch_response=True, name="POST /users/register") as response:
            if response.status_code != 201:
                response.failure(f"User Registration failed with status: {response.status_code}")
                print("User Registration Failed. Stopping all remaining tasks.")
                self.interrupt()        # Immediately return if User Registration fail
                return


    @task
    def login_user(self):
        payload = {"email": self.email, "password": self.password}
        with self.client.post("/users/login", json=payload, headers=TEST_DEFAULT_HEADERS, catch_response=True, name="POST /users/login") as response:
            if response.status_code == 200:
                resp_json_data = response.json()["data"]
                try:
                    self.token = resp_json_data["token"]
                    self.headers_login = {**TEST_DEFAULT_HEADERS, "x-auth-token": self.token}
                except KeyError:
                    response.failure("User login - Schema Contract Break: 'data.token' key missing")
                    self.interrupt()        # Immediately return if User Login fail
                    return
            else:
                response.failure(f"Failed user login - 'status_code': {response.status_code}")
                self.interrupt()
                return


    @task
    def authorize_user(self):
        if not self.token:
            return      # Skip as user not login
        with self.client.get("", headers=self.headers_login, catch_response=True, name="GET /") as response:
            json_data = response.json()
            if response.status_code != 200:
                response.failure(f"Failed available authorizations - 'status_code': {response.status_code}")
            elif not json_data.get("success"):
                response.failure(f"Available authorizations - 'success': {json_data.get('success')}")

    
    @task
    def get_profile(self):
        if not self.token:
            return          # Skip as user not login
        with self.client.get("/users/profile", headers=self.headers_login, catch_response=True, name="GET /users/profile") as response:
            json_data = response.json()
            if response.status_code != 200:
                response.failure(f"Failed get profile - 'status_code': {response.status_code}")
            elif not json_data.get("success"):
                response.failure(f"Get profile - 'success': {json_data.get('success')}")


    @task
    def patch_profile(self):
        if not self.token:
            return          # Skip as user not login
        new_payload = {"name": "Updated Tester QATeam"}
        with self.client.patch("/users/profile", headers=self.headers_login, json=new_payload, catch_response=True, name="PATCH /users/profile") as response:
            json_data = response.json()
            if response.status_code != 200:
                response.failure(f"Failed get profile - 'status_code': {response.status_code}")
            elif not json_data.get("success"):
                response.failure(f"Get profile - 'success': {json_data.get('success')}")


    @task
    def post_note(self):
        if not self.token:
            return      # Skip as user not login
        payload = {
            "title": "QATeam Test Task : Note Title",
            "description": "QATeam Test Task : Note Description",
            "category": "Work"      # Home, Work, Personal
        }
        with self.client.post("/notes", json=payload, headers=self.headers_login, catch_response=True, name="POST /notes") as response:
            if response.status_code in [200, 201]:
                resp_json = response.json()
                try:
                    self.note_id = resp_json["data"]["id"]
                except KeyError:
                    response.failure("Post note - Schema contract error: 'data.id' field.")
            else:
                response.failure(f"Post note Failed - HTTP Status: {response.status_code}")


    @task
    def put_note(self):
        if not self.token:
            return      # Skip as user not login
        payload = {
            "title": "PUT - QATeam Test Task : Note Title",
            "description": "PUT - QATeam Test Task : Note Description",
            "category": "Work",      # Home, Work, Personal
            "completed": True
        }
        with self.client.put(f"/notes/{self.note_id}", json=payload, headers=self.headers_login, catch_response=True, name="PUT /notes/{self.note_id}") as response:
            resp_json = response.json()
            if response.status_code == 200:
                try:
                    self.note_id = resp_json["data"]["id"]
                except KeyError:
                    response.failure("Put note - Schema contract error: 'data.id' field.")
            elif response.status_code != 200:
                response.failure(f"Put note Failed - HTTP Status: {response.status_code}")
            elif not resp_json["success"]:
                response.failure(f"Put node - 'success': {resp_json.get('success')}")


    @task
    def patch_note(self):
        if not self.token:
            return      # Skip as user not login
        payload = { "completed": True }
        with self.client.patch(f"/notes/{self.note_id}", json=payload, headers=self.headers_login, catch_response=True, name="PATCH /notes/{self.note_id}") as response:
            resp_json = response.json()
            if response.status_code == 200:
                try:
                    self.note_id = resp_json["data"]["id"]
                except KeyError:
                    response.failure("Patch note - Schema contract error: 'data.id' field.")
            elif response.status_code != 200:
                response.failure(f"Patch note Failed - HTTP Status: {response.status_code}")
            elif not resp_json["success"]:
                response.failure(f"Patch Note - 'success': {resp_json.get('success')}")


    @task
    def get_note(self):
        if not self.token:
            return      # Skip as user not login
        payload = { "completed": True }
        with self.client.get(f"/notes/{self.note_id}", json=payload, headers=self.headers_login, catch_response=True, name="GET /notes/{self.note_id}") as response:
            resp_json = response.json()
            if response.status_code == 200:
                try:
                    self.note_id = resp_json["data"]["id"]
                except KeyError:
                    response.failure("Patch note - Schema contract error: 'data.id' field.")
            elif response.status_code != 200:
                response.failure(f"Patch note Failed - HTTP Status: {response.status_code}")
            elif not resp_json["success"]:
                response.failure(f"Patch Note - 'success': {resp_json.get('success')}")



    # --------------------------------------------------------------------------
    # NEGATIVE PATHS, BOUNDARIES, AND EDGE CONSTRAINTS TESTING
    # --------------------------------------------------------------------------

    #@task
    def get_all_notes_missing_header_token(self):
        if not self.token:
            return
        with self.client.get("/notes", headers=TEST_DEFAULT_HEADERS, catch_response=True, name="EDGE: GET /notes (Missing Token)") as response:
            if response.status_code == 401:
                response.success()  # 401 is the expected design behavior
            else:
                response.failure(f"Expected 401 - Security Boundary Leak - 'status_code': {response.status_code}")

    
    #@task
    def get_all_notes_with_empty_payload(self):
        if not self.token:
            return
        malformed_payload = {}  # Empty body violations
        with self.client.post("/notes", json=malformed_payload, headers=self.headers_login, catch_response=True, name="EDGE: POST /notes (Empty Body)") as response:
            if response.status_code == 400:
                response.success()  # Validation rules applied effectively under stress
            else:
                response.failure(f"Expected 400 - Bad request protection - 'status_code': {response.status_code}")


    #@task
    def get_note_with_invalid_note_id(self):
        if not self.token:
            return
        invalid_id = "000000000000000000000000"
        with self.client.get(f"/notes/{invalid_id}", headers=self.headers_login, catch_response=True, name=f"BOUND: GET /notes/{invalid_id}") as response:
            if response.status_code == 404:
                response.success()  # System correctly returned Not Found
            else:
                response.failure(f"Expected 404 - missing parameter mapping - 'status_code': {response.status_code}")



    # --------------------------------------------------------------------------
    # TEARDOWN
    # --------------------------------------------------------------------------

    @task
    def delete_note(self):
        if not self.token or not self.note_id:
            return
        with self.client.delete(f"/notes/{self.note_id}", headers=self.headers_login, catch_response=True, name="DELETE /notes/{self.note_id}") as response:
            if response.status_code == 200:
                self.note_id = None
            else:
                response.failure(f"Delete note - cleanup failed - 'status_code': {response.status_code}")

    
    @task
    def delete_account(self):
        if not self.token:
            return
        with self.client.delete("/users/delete-account", headers=self.headers_login, catch_response=True, name="DELETE /users/delete-account") as response:
            if response.status_code == 200:
                self.token = None
            else:
                response.failure(f"Delete account - cleanup failed - 'status_code': {response.status_code}")


class LocustPerformanceUserRunner(HttpUser):
    host = ApiEndpoints.base_url()
    tasks = [NotesLifecycleLoadTest]
    wait_time = between(0.9, 1.1)
