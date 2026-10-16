import random
from locust import events
from locust import HttpUser, task, between, SequentialTaskSet
from config.settings import ApiEndpoints
from helpers.lifecycle import start_app, stop_app


@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    try:
        start_app()
    except Exception as e:
        print(f"[locustfile_client_resource_access_api Start Error] Failed to start application: {e}")


@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    stop_app()
    print("[locustfile_client_resource_access_api Teardown] Application process successfully terminated.\n")



class ClientResourceAccessWorkflowTest(SequentialTaskSet):
    """
    End-to-end RESTful Client Resource Access Workflow:
        1. POST     /api/v1/client
        2. POST     /api/v1/resource
        3. POST     /api/v1/client-resource-access
        4. PATCH    /api/v1/client/{client_id}
        5. PATCH    /api/v1/resource/{resource_id}
        6. PATCH    /api/v1/client-resource-access/client/{client_id}/resource/{resource_id}
        7. PUT      /api/v1/client/{client_id}
        8. PUT      /api/v1/resource/{resource_id}
        9. PUT      /api/v1/client-resource-access/client/{client_id}/resource/{resource_id}
        10. GET     /api/v1/client/{client_id}
        11. GET     /api/v1/client/{client_id}/key
        12. GET     /api/v1/client/{client_id}/description
        13. GET     /api/v1/client/search
        14. GET     /api/v1/resource/{resource_id}
        15. GET     /api/v1/resource/{resource_id}/key
        16. GET     /api/v1/resource/{resource_id}/type
        17. GET     /api/v1/resource/{resource_id}/description
        18. GET     /api/v1/resource/search
        19. GET     /api/v1/client-resource-access/client/{client_id}/resource/{resource_id}
        20. GET     /api/v1/client-resource-access/client/{client_id}/resource/{resource_id}/access-code
        21. GET     /api/v1/client-resource-access/client/{client_id}/resource/{resource_id}/description
        22. GET     /api/v1/client-resource-access/search
        23. DELETE  /api/v1/client-resource-access/client/{client_id}/resource/{resource_id}
        24. DELETE  /api/v1/resource/{resource_id}
        25. DELETE  /api/v1/client/{client_id}
    """

    random_id: int
    client_id: int | None
    resource_id: int | None


    def on_start(self):
        self.random_id = random.randint(0, 999999)
        self.client_id = None
        self.resource_id = None


    # ------------------------------------------------------------------
    # HAPPY PATHS TESTING
    # ------------------------------------------------------------------

    @task
    def create_client(self):
        payload = {
            "key": f"Key_Client_Item_{self.random_id:06d}",
            "secret": f"Secret_Client_Item_{self.random_id:06d}",
            "description": f"Description Client Item {self.random_id:06d}",
        }
        with self.client.post("/api/v1/client", json=payload, catch_response=True, name="POST /api/v1/client") as response:
            if response.status_code == 201:
                self.client_id = response.json().get("id")
                response.success()
            else:
                response.failure(f"Failed to create client: {response.text}")


    @task
    def create_resource(self):
        payload = {
            "key": f"Key_Resource_Item_{self.random_id}",
            "type": f"Type_Resource_Item_{self.random_id}",
            "description": f"Description Resource Item {self.random_id}"
        }
        with self.client.post("/api/v1/resource", json=payload,
            catch_response=True, name="POST /api/v1/resource") as response:
            if response.status_code == 201:
                self.resource_id = response.json().get("id")
                response.success()
            else:
                response.failure(f"Failed to create resource: {response.text}")


    @task
    def create_client_resource_access(self):
        if self.client_id and self.resource_id:
            payload = {
                "clientId": self.client_id,
                "resourceId": self.resource_id,
                "accessCode": f"Access_Code{self.random_id}",
                "description": f"Client Resource Access Description {self.random_id}"
            }
            with self.client.post("/api/v1/client-resource-access", json=payload,
                catch_response=True, name="POST /api/v1/client-resource-access") as response:
                if response.status_code ==  201:
                    response.success()
                else:
                    response.failure(f"Failed to map access: {response.text}")


    @task
    def update_client(self):
        if self.client_id:
            payload = {
                "key": f"Updated_Key_Client_Item_{self.client_id}",
                "description": f"Updated Description Client Item {self.client_id}",
            }
            with self.client.patch(f"/api/v1/client/{self.client_id}", json=payload,
                catch_response=True, name="PATCH /api/v1/client/{client_id}") as response:
                if response.status_code == 200:
                    response.success()
                else:
                    response.failure(f"Failed to map access: {response.text}")


    @task
    def update_resource(self):
        if self.resource_id:
            payload = {
                "key": f"Updated_Key_Resource_Item_{self.resource_id}",
                "type": f"Updated_Type_Resource_Item_{self.resource_id}",
                "description": f"Updated Description Resource Item {self.resource_id}",
            }
            with self.client.patch(f"/api/v1/resource/{self.resource_id}", json=payload,
                catch_response=True, name="PATCH /api/v1/resource/{resource_id}") as response:
                if response.status_code == 200:
                    response.success()
                else:
                    response.failure(f"Failed to map access: {response.text}")


    @task
    def update_client_resource_access(self):
        if self.client_id and self.resource_id:
            payload = {
                "accessCode": f"Updated_Access_Code_{self.client_id}_{self.resource_id}",
                "description": f"Updated Client Resource Access Description {self.client_id}_{self.resource_id}",
            }
            url = f"/api/v1/client-resource-access/client/{self.client_id}/resource/{self.resource_id}"
            with self.client.patch(url, json=payload, catch_response=True,
                name="PATCH /api/v1/client-resource-access/client/{client_id}/resource/{resource_id}") as response:
                if response.status_code == 200:
                    response.success()
                else:
                    response.failure(f"Failed to map access: {response.text}")


    @task
    def replace_client(self):
        if self.client_id:
            payload = {
                "key": f"Replaced_Key_Client_Item_{self.client_id}",
                "description": f"Replaced Description Client Item {self.client_id}",
            }
            with self.client.put(f"/api/v1/client/{self.client_id}", json=payload,
                catch_response=True, name="PUT /api/v1/client/{client_id}") as response:
                if response.status_code == 200:
                    response.success()
                else:
                    response.failure(f"Failed to map access: {response.text}")


    @task
    def replace_resource(self):
        if self.resource_id:
            payload = {
                "key": f"Replaced_Key_Resource_Item_{self.resource_id}",
                "type": f"Replaced_Type_Resource_Item_{self.resource_id}",
                "description": f"Replaced Description Resource Item {self.resource_id}",
            }
            with self.client.put(f"/api/v1/resource/{self.resource_id}", json=payload,
                catch_response=True, name="PUT /api/v1/resource/{resource_id}") as response:
                if response.status_code == 200:
                    response.success()
                else:
                    response.failure(f"Failed to map access: {response.text}")


    @task
    def replace_client_resource_access(self):
        if self.client_id and self.resource_id:
            payload = {
                "accessCode": f"Replaced_Access_Code_{self.client_id}_{self.resource_id}",
                "description": f"Replaced Client Resource Access Description {self.client_id}_{self.resource_id}",
            }
            url = f"/api/v1/client-resource-access/client/{self.client_id}/resource/{self.resource_id}"
            with self.client.put(url, json=payload, catch_response=True,
                name="PUT /api/v1/client-resource-access/client/{client_id}/resource/{resource_id}") as response:
                if response.status_code == 200:
                    response.success()
                else:
                    response.failure(f"Failed to map access: {response.text}")


    @task
    def get_client_id(self):
        if self.client_id:
            with self.client.get(f"/api/v1/client/{self.client_id}", catch_response=True,
                name="GET /api/v1/client/{client_id}") as response:
                if response.status_code == 200:
                    response.success()
                else:
                    response.failure(f"Failed to map access: {response.text}")


    @task
    def get_client_key(self):
        if self.client_id:
            with self.client.get(f"/api/v1/client/{self.client_id}/key", catch_response=True,
                name="GET /api/v1/client/{client_id}/key") as response:
                if response.status_code == 200:
                    response.success()
                else:
                    response.failure(f"Failed to map access: {response.text}")


    @task
    def get_client_description(self):
        if self.client_id:
            with self.client.get(f"/api/v1/client/{self.client_id}/description", catch_response=True,
                name="GET /api/v1/client/{client_id}/description") as response:
                if response.status_code == 200:
                    response.success()
                else:
                    response.failure(f"Failed to map access: {response.text}")

    @task
    def get_client_all(self):
        with self.client.get(f"/api/v1/client/search", catch_response=True,
            name="GET /api/v1/client/search") as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Failed to map access: {response.text}")


    @task
    def get_resource_id(self):
        if self.resource_id:
            with self.client.get(f"/api/v1/resource/{self.resource_id}", catch_response=True,
                name="GET /api/v1/resource/{resource_id}") as response:
                if response.status_code == 200:
                    response.success()
                else:
                    response.failure(f"Failed to map access: {response.text}")


    @task
    def get_resource_key(self):
        if self.resource_id:
            with self.client.get(f"/api/v1/resource/{self.resource_id}/key", catch_response=True,
                name="GET /api/v1/resource/{resource_id}/key") as response:
                if response.status_code == 200:
                    response.success()
                else:
                    response.failure(f"Failed to map access: {response.text}")


    @task
    def get_resource_type(self):
        if self.resource_id:
            with self.client.get(f"/api/v1/resource/{self.resource_id}/type", catch_response=True,
                name="GET /api/v1/resource/{resource_id}/type") as response:
                if response.status_code == 200:
                    response.success()
                else:
                    response.failure(f"Failed to map access: {response.text}")


    @task
    def get_resource_description(self):
        if self.resource_id:
            with self.client.get(f"/api/v1/resource/{self.resource_id}/description", catch_response=True,
                name="GET /api/v1/resource/{resource_id}/description") as response:
                if response.status_code == 200:
                    response.success()
                else:
                    response.failure(f"Failed to map access: {response.text}")


    @task
    def get_resource_all(self):
        with self.client.get(f"/api/v1/resource/search", catch_response=True,
            name="GET /api/v1/resource/search") as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Failed to map access: {response.text}")


    @task
    def get_client_resource_access_id(self):
        if self.client_id and self.resource_id:
            url = f"/api/v1/client-resource-access/client/{self.client_id}/resource/{self.resource_id}"
            with self.client.get(url, catch_response=True,
                name="GET /api/v1/client-resource-access/client/{client_id}/resource/{resource_id}") as response:
                if response.status_code == 200:
                    response.success()
                else:
                    response.failure(f"Failed to map access: {response.text}")


    @task
    def get_client_resource_access_access_code(self):
        if self.client_id and self.resource_id:
            url = f"/api/v1/client-resource-access/client/{self.client_id}/resource/{self.resource_id}/access-code"
            with self.client.get(url, catch_response=True,
                name="GET /api/v1/client-resource-access/client/{client_id}/resource/{resource_id}/access-code") as response:
                if response.status_code == 200:
                    response.success()
                else:
                    response.failure(f"Failed to map access: {response.text}")


    @task
    def get_client_resource_access_description(self):
        if self.client_id and self.resource_id:
            url = f"/api/v1/client-resource-access/client/{self.client_id}/resource/{self.resource_id}/description"
            with self.client.get(url, catch_response=True,
                name="GET /api/v1/client-resource-access/client/{client_id}/resource/{resource_id}/description") as response:
                if response.status_code == 200:
                    response.success()
                else:
                    response.failure(f"Failed to map access: {response.text}")


    @task
    def get_client_resource_access_all(self):
        if self.client_id and self.resource_id:
            with self.client.get(f"/api/v1/client-resource-access/search", catch_response=True,
                name="GET /api/v1/client-resource-access/search") as response:
                if response.status_code == 200:
                    response.success()
                else:
                    response.failure(f"Failed to map access: {response.text}")



    # --------------------------------------------------------------------------
    # TEARDOWN
    # --------------------------------------------------------------------------

    @task
    def delete_client_resource_access(self):
        if self.client_id and self.resource_id:
            with self.client.delete(
                f"/api/v1/client-resource-access/client/{self.client_id}/resource/{self.resource_id}",
                catch_response=True,
                name="DELETE /api/v1/client-resource-access/client/{client_id}/resource/{resource_id}",
            ) as response:
                if response.status_code == 204:
                    response.success()
                else:
                    response.failure(f"Failed to map access: {response.text}")

    @task
    def delete_resource(self):
        if self.resource_id:
            with self.client.delete(f"/api/v1/resource/{self.resource_id}", catch_response=True,
                name="DELETE /api/v1/resource/{resource_id}"
            ) as response:
                if response.status_code == 204:
                    response.success()
                else:
                    response.failure(f"Failed to map access: {response.text}")


    @task
    def delete_client(self):
        if self.client_id:
            with self.client.delete(f"/api/v1/client/{self.client_id}", catch_response=True,
                name="DELETE /api/v1/client/{client_id}"
            ) as response:
                if response.status_code == 204:
                    response.success()
                else:
                    response.failure(f"Failed to map access: {response.text}")

        # --------------------------------------------------------------------------
        # Workflow completed successfully
        # Start a new workflow for this virtual user.
        # --------------------------------------------------------------------------
        self.interrupt()



class APIPerformanceUser(HttpUser):
    host = ApiEndpoints.base_url()
    tasks = [ClientResourceAccessWorkflowTest]
    wait_time = between(0.9, 1.1)
