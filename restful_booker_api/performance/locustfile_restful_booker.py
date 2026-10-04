from random import randint
from datetime import date, timedelta
from locust import HttpUser, SequentialTaskSet, between, task
from config.settings import ApiEndpoints


class RestfulBookerWorkflowTest(SequentialTaskSet):
    """
    End-to-end RESTful Booker Workflow:
        1.  GET    /ping
        2.  POST   /auth
        3.  POST   /booking
        4.  GET    /booking
        5.  GET    /booking?firstname=&lastname=
        6.  GET    /booking?checkin=&checkout=
        7.  GET    /booking/{id}
        8.  PUT    /booking/{id}
        9.  PATCH  /booking/{id}
        10. DELETE /booking/{id}
    """

    token: str | None
    booking_id: str | None
    booking: dict

    def on_start(self):
        self.token = None
        self.booking_id = None
        self.booking = self._generate_booking_data()


    # ------------------------------------------------------------------
    # Test data - Help function
    # ------------------------------------------------------------------

    @staticmethod
    def _generate_booking_data():
        checkin = date.today() - timedelta(days=3)
        checkout = checkin + timedelta(days=6)
        lucky_no = randint(1000, 9999)
        return {
            "firstname": f"FirstName_{lucky_no}",
            "lastname": f"LastName_{lucky_no}",
            "totalprice": randint(1, 1000),
            "depositpaid": True if lucky_no % 2 == 0 else False,
            "bookingdates": {
                "checkin": checkin.isoformat(),
                "checkout": checkout.isoformat(),
            },
            "additionalneeds": ["Breakfast", "Lunch", "Dinner", "Brunch", "None"][lucky_no % 5]
        }



    # ------------------------------------------------------------------
    # HAPPY PATHS TESTING
    # ------------------------------------------------------------------

    @task
    def health_check(self):
        with self.client.get(
                "/ping",
                name="GET /ping",
                catch_response=True
        ) as response:
            if response.status_code != 201:
                response.failure(f"Health Check - Expected HTTP 201, but got HTTP {response.status_code}")
                self.interrupt()
                return


    @task
    def authenticate(self):
        payload = {"username": "admin", "password": "password123"}
        with self.client.post(
                "/auth",
                json=payload,
                name="POST /auth",
                catch_response=True
        ) as response:
            if response.status_code != 200:
                response.failure(f"Authentication - Expected HTTP 200, but got HTTP {response.status_code}")
                self.interrupt()
                return

            try:
                response_json = response.json()
                self.token = response_json.get("token")
            except (ValueError, KeyError, TypeError) as exc:
                response.failure(f"Authentication - Response is not valid JSON: {exc}")
                self.interrupt()
                return

            if not self.token:
                response.failure("Authentication - Token was not returned")
                self.interrupt()


    @task
    def create_booking(self):
        with self.client.post(
                "/booking",
                json=self.booking,
                name="POST /booking",
                catch_response=True
        ) as response:
            if response.status_code != 200:
                response.failure(f"Create Booking - Expected HTTP 200, but got HTTP {response.status_code}")
                self.interrupt()
                return

            try:
                response_json = response.json()
                self.booking_id = response_json.get("bookingid")
            except (ValueError, KeyError, TypeError) as exc:
                response.failure(f"Create Booking - Response is not valid JSON: {exc}")
                self.interrupt()
                return

            if not self.booking_id:
                response.failure("Create Booking - Booking ID was not returned")
                self.interrupt()



    @task
    def get_all_bookings(self):
        with self.client.get(
                "/booking",
                name="GET /booking",
                catch_response=True
        ) as response:
            if response.status_code != 200:
                response.failure(f"Get All Bookings - Expected HTTP 200, but got HTTP {response.status_code}")
                #self.interrupt()
                return

            try:
                response_json = response.json()
                if not isinstance(response_json, list):
                    response.failure("Get All Bookings - Expected response body to be a JSON array")
                    #self.interrupt()
                    return
                elif not any(str(book.get("bookingid")) == str(self.booking_id) for book in response_json if isinstance(book, dict)):
                    response.failure(f"Get All Bookings - Booking ID {self.booking_id} not found in response")
                    #self.interrupt()
                    return
            except (ValueError, KeyError, TypeError) as exc:
                response.failure(f"Get All Bookings - Response is not valid JSON: {exc}")
                #self.interrupt()
                return



    @task
    def get_bookings_by_name(self):
        params = {"firstname": self.booking["firstname"], "lastname": self.booking["lastname"]}

        with self.client.get(
                "/booking",
                params=params,
                name="GET /booking?firstname=&lastname=",
                catch_response=True
        ) as response:
            if response.status_code != 200:
                response.failure(f"Get Bookings by Name - Expected HTTP 200, but got HTTP {response.status_code}")
                #self.interrupt()
                return

            try:
                response_json = response.json()
                if not isinstance(response_json, list):
                    response.failure("Get Bookings by Name - Expected response body to be a JSON array")
                    #self.interrupt()
                    return
                elif not any(str(book.get("bookingid")) == str(self.booking_id) for book in response_json if isinstance(book, dict)):
                    response.failure(f"Get Bookings by Name - Booking ID {self.booking_id} not found in response")
                    #self.interrupt()
                    return
            except (ValueError, KeyError, TypeError) as exc:
                response.failure(f"Get Bookings by Name - Response is not valid JSON: {exc}")
                #self.interrupt()
                return



    @task
    def get_booking(self):
        if not self.booking_id:
            # Manually trigger a failure event in Locust stats
            self.user.environment.events.request.fire(
                request_type="GET",
                name="GET /booking/{booking_id}",
                response_time=0,
                response_length=0,
                exception=Exception("Get Booking - Failed: missing booking_id precondition"),
                context=self.user.context()
            )
            self.interrupt()
            return

        with self.client.get(
                f"/booking/{self.booking_id}",
                name="GET /booking/{booking_id}",
                catch_response=True
        ) as response:
            if response.status_code != 200:
                response.failure(f"Get Booking - Expected HTTP 200, but got HTTP {response.status_code}")
                #self.interrupt()
                return



    @task
    def put_booking(self):
        if not self.token:
            # Manually trigger a failure event in Locust stats
            self.user.environment.events.request.fire(
                request_type="PUT",
                name="PUT /booking/{booking_id}",
                response_time=0,
                response_length=0,
                exception=Exception("Update Booking - Failed: missing token precondition"),
                context=self.user.context()
            )
            self.interrupt()
            return
        elif not self.booking_id:
            # Manually trigger a failure event in Locust stats
            self.user.environment.events.request.fire(
                request_type="PUT",
                name="PUT /booking/{booking_id}",
                response_time=0,
                response_length=0,
                exception=Exception("Update Booking - Failed: missing booking_id precondition"),
                context=self.user.context()
            )
            self.interrupt()
            return

        updated_booking = {
            **self.booking,
            "totalprice": self.booking["totalprice"] + 100,
            "additionalneeds": "Breakfast and Dinner"
        }

        headers = {"Cookie": f"token={self.token}"}

        with self.client.put(
                f"/booking/{self.booking_id}",
                headers=headers,
                json=updated_booking,
                name="PUT /booking/{booking_id}",
                catch_response=True
        ) as response:
            if response.status_code != 200:
                response.failure(f"Update Booking - Expected HTTP 200, but got HTTP {response.status_code}")
                #self.interrupt()
                return



    @task
    def patch_booking(self):
        if not self.token:
            # Manually trigger a failure event in Locust stats
            self.user.environment.events.request.fire(
                request_type="PATCH",
                name="PATCH /booking/{booking_id}",
                response_time=0,
                response_length=0,
                exception=Exception("Patch Booking - Failed: missing token precondition"),
                context=self.user.context()
            )
            self.interrupt()
            return
        elif not self.booking_id:
            # Manually trigger a failure event in Locust stats
            self.user.environment.events.request.fire(
                request_type="PATCH",
                name="PATCH /booking/{booking_id}",
                response_time=0,
                response_length=0,
                exception=Exception("Patch Booking - Failed: missing booking_id precondition"),
                context=self.user.context()
            )
            self.interrupt()
            return

        headers = {"Cookie": f"token={self.token}" }
        payload = {"additionalneeds": "Breakfast, Dinner"}

        with self.client.patch(
                f"/booking/{self.booking_id}",
                headers=headers,
                json=payload,
                name="PATCH /booking/{booking_id}",
                catch_response=True
        ) as response:
            if response.status_code != 200:
                response.failure(f"Patch Booking - Expected HTTP 200, but got HTTP {response.status_code}")
                #self.interrupt()
                return



    @task
    def get_bookings_by_dates(self):
        params = {
            "checkin": str(self.booking["bookingdates"]["checkin"]),
            "checkout": str(self.booking["bookingdates"]["checkout"])
        }
        with self.client.get(
                "/booking",
                params=params,
                name="GET /booking?checkin=&checkout=",
                catch_response=True
        ) as response:
            if response.status_code != 200:
                response.failure(f"Get Bookings by Date - Expected HTTP 200, but got HTTP {response.status_code}")
                #self.interrupt()
                return

            try:
                response_json = response.json()
                if not isinstance(response_json, list):
                    response.failure("Get Bookings by Date - Expected response body to be a JSON array")
                    #self.interrupt()
                    return
                elif not any(str(book.get("bookingid")) == str(self.booking_id) for book in response_json if isinstance(book, dict)):
                    response.failure(f"Get Bookings by Date - Booking ID {self.booking_id} not found in response")
                    #self.interrupt()
                    return
            except (ValueError, KeyError, TypeError) as exc:
                response.failure(f"Get Bookings by Date - Response is not valid JSON: {exc}")
                #self.interrupt()
                return



    @task
    def get_bookings_by_check_in(self):
        params = {
            "checkin": str(self.booking["bookingdates"]["checkin"])
        }
        with self.client.get(
                "/booking",
                params=params,
                name="GET /booking?checkin=",
                catch_response=True
        ) as response:
            if response.status_code != 200:
                response.failure(f"Get Bookings by CheckIn - Expected HTTP 200, but got HTTP {response.status_code}")
                #self.interrupt()
                return

            try:
                response_json = response.json()
                if not isinstance(response_json, list):
                    response.failure("Get Bookings by CheckIn - Expected response body to be a JSON array")
                    #self.interrupt()
                    return
                elif not any(str(book.get("bookingid")) == str(self.booking_id) for book in response_json if isinstance(book, dict)):
                    response.failure(f"Get Bookings by CheckIn - Booking ID {self.booking_id} not found in response")
                    #self.interrupt()
                    return
            except (ValueError, KeyError, TypeError) as exc:
                response.failure(f"Get Bookings by CheckIn - Response is not valid JSON: {exc}")
                #self.interrupt()
                return



    @task
    def get_bookings_by_check_out(self):
        params = {
            "checkout": str(self.booking["bookingdates"]["checkout"])
        }
        with self.client.get(
                "/booking",
                params=params,
                name="GET /booking?checkout=",
                catch_response=True
        ) as response:
            if response.status_code != 200:
                response.failure(f"Get Bookings by CheckOut - Expected HTTP 200, but got HTTP {response.status_code}")
                #self.interrupt()
                return

            try:
                response_json = response.json()
                if not isinstance(response_json, list):
                    response.failure("Get Bookings by CheckOut - Expected response body to be a JSON array")
                    #self.interrupt()
                    return
                elif not any(str(book.get("bookingid")) == str(self.booking_id) for book in response_json if isinstance(book, dict)):
                    response.failure(f"Get Bookings by CheckOut - Booking ID {self.booking_id} not found in response")
                    #self.interrupt()
                    return
            except (ValueError, KeyError, TypeError) as exc:
                response.failure(f"Get Bookings by CheckOut - Response is not valid JSON: {exc}")
                #self.interrupt()
                return




    # --------------------------------------------------------------------------
    # TEARDOWN
    # --------------------------------------------------------------------------

    @task
    def delete_booking(self):
        if not self.token:
            # Manually trigger a failure event in Locust stats
            self.user.environment.events.request.fire(
                request_type="DELETE",
                name="DELETE /booking/{booking_id}",
                response_time=0,
                response_length=0,
                exception=Exception("Delete Booking - Failed: missing token precondition"),
                context=self.user.context()
            )
            self.interrupt()
            return
        elif not self.booking_id:
            # Manually trigger a failure event in Locust stats
            self.user.environment.events.request.fire(
                request_type="DELETE",
                name="DELETE /booking/{booking_id}",
                response_time=0,
                response_length=0,
                exception=Exception("Delete Booking - Failed: missing booking_id precondition"),
                context=self.user.context()
            )
            self.interrupt()
            return

        headers = {"Cookie": f"token={self.token}"}

        with self.client.delete(
                f"/booking/{self.booking_id}",
                headers=headers,
                name="DELETE /booking/{booking_id}",
                catch_response=True
        ) as response:
            if response.status_code != 201:
                response.failure(f"Delete Booking - Expected HTTP 201, but got HTTP {response.status_code}")
                self.interrupt()
                return



        # --------------------------------------------------------------------------
        # Workflow completed successfully
        # Start a new workflow for this virtual user.
        # --------------------------------------------------------------------------

        self.interrupt()



class RestfulBookerWorkflowTestUser(HttpUser):
    host = ApiEndpoints.base_url()
    tasks = [RestfulBookerWorkflowTest]
    wait_time = between(0.9, 1.1)
