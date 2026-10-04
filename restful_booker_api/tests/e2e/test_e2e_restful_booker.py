import copy
import pytest
from datetime import datetime, timedelta
from pytest_check import check
from config.settings import ApiEndpoints


class StepFailure(Exception):
    pass

def run_step(step_name, func, *args, **kwargs):
    try:
        return func(*args, **kwargs)
    except AssertionError as ae:
        raise StepFailure(f"Fatal error at step: {step_name}, exception: {str(ae)}")
    except Exception as ex:
        raise StepFailure(f"Fatal error at step: {step_name}, exception: {str(ex)}")



def test_e2e_regaular_scenario(manage_api_context, manage_book_creation_json_context):
    health_check = False
    token, req_body, book_id = None, None, None

    try:
        # health check
        def step_1():
            nonlocal health_check
            api = manage_api_context(
                base_url=ApiEndpoints.base_url(),
                http_headers={"Content-Type": "application/json"}
            )
            resp = api.get('/ping')
            check.equal(resp.status, 201)
            check.equal(resp.status_text, "Created")
            check.is_true(resp.ok)
            health_check = (resp.status == 201)
        run_step("E2E_Regular_Scenarios>Step#1. Health Check", step_1)

        # auth token
        def step_2():
            nonlocal token
            api = manage_api_context(
                base_url=ApiEndpoints.base_url(),
                http_headers={"Accept": "application/json"}
            )
            resp = api.post("/auth", data = {'username': 'admin', 'password': 'password123'})
            check.equal(resp.status, 200)
            check.equal(resp.status_text, "OK")
            check.is_true(resp.ok)
            check.is_not_none(resp.json())
            check.is_not_none(resp.json().get('token'))
            token = resp.json().get('token')
        run_step("E2E_Regular_Scenarios>Step#2. Auth Token", step_2)

        # create booking
        def step_3():
            nonlocal req_body, book_id
            req_body, book_id = manage_book_creation_json_context(user_id=1)
            check.is_not_none(req_body)
            check.greater(book_id, 0)
            check.is_instance(req_body, dict)
            check.is_not_none(req_body.get('firstname'))
            check.is_not_none(req_body.get('lastname'))
            check.is_not_none(req_body.get('totalprice'))
            check.is_not_none(req_body.get('depositpaid'))
            check.is_not_none(req_body.get('additionalneeds'))
            check.is_not_none(req_body.get('bookingdates'))
            check.is_not_none(req_body.get('bookingdates').get('checkin'))
            check.is_not_none(req_body.get('bookingdates').get('checkout'))
        run_step("E2E_Regular_Scenarios>Step#3. Create Booking", step_3)

        # get booking
        def step_4():
            nonlocal req_body, book_id
            api = manage_api_context(
                base_url=ApiEndpoints.base_url(),
                http_headers={"Accept": "application/json"}
            )
            resp = api.get(f"/booking/{book_id}")
            check.equal(resp.status, 200)
            check.equal(resp.status_text, "OK")
            check.is_true(resp.ok)
            check.is_not_none(resp.json())
            check.is_instance(resp.json(), dict)
            resp_json = resp.json()
            check.greater_equal(len(resp_json), 0)
            check.equal(resp_json.get('firstname'), req_body.get('firstname'))
            check.equal(resp_json.get('lastname'), req_body.get('lastname'))
            check.equal(resp_json.get('totalprice'), req_body.get('totalprice'))
            check.equal(resp_json.get('depositpaid'), req_body.get('depositpaid'))
            check.equal(resp_json.get('bookingdates').get('checkin'), req_body.get('bookingdates').get('checkin'))
            check.equal(resp_json.get('bookingdates').get('checkout'), req_body.get('bookingdates').get('checkout'))
            #check.is_none(resp_json.get('additionalneeds'))
        run_step("E2E_Regular_Scenarios>Step#4. Get Booking", step_4)

        # get all bookings
        def step_5():
            nonlocal req_body, book_id
            api = manage_api_context(
                base_url=ApiEndpoints.base_url(),
                http_headers={"Content-Type": "application/json"}
            )
            resp = api.get('/booking')
            check.equal(resp.status, 200)
            check.equal(resp.status_text, "OK")
            check.is_true(resp.ok)
            check.is_not_none(resp.json())
            check.is_instance(resp.json(), list)
            resp_json = resp.json()
            check.greater(len(resp_json), 0)
            check.is_true(any(book.get('bookingid') == book_id for book in resp_json))
        run_step("E2E_Regular_Scenarios>Step#5. Get All Bookings", step_5)

        # delete booking
        def step_6():
            nonlocal req_body, book_id
            api = manage_api_context(
                base_url=ApiEndpoints.base_url(),
                http_headers={"Cookie": f"token={token}", "Content-Type": "application/json"}
            )
            resp = api.delete(f"/booking/{book_id}")
            check.equal(resp.status, 201)
            check.equal(resp.status_text, "Created")
            check.is_true(resp.ok)
        run_step("E2E_Regular_Scenarios>Step#6. Delete Booking", step_6)

        # get booking
        def step_7():
            nonlocal req_body, book_id
            api = manage_api_context( base_url=ApiEndpoints.base_url() )
            resp = api.get(f'/booking/{book_id}')
            check.equal(resp.status, 404)
            check.equal(resp.status_text, "Not Found")
            check.is_false(resp.ok)
            check.is_not_none(resp.text())
        run_step("E2E_Regular_Scenarios>Step#7. Get Booking After Being Deletion", step_7)

        # get all bookings
        def step_8():
            nonlocal req_body, book_id
            api = manage_api_context(
                base_url=ApiEndpoints.base_url(),
                http_headers={"Content-Type": "application/json"}
            )
            resp = api.get('/booking')
            check.equal(resp.status, 200)
            check.equal(resp.status_text, "OK")
            check.is_true(resp.ok)
            check.is_not_none(resp.json())
            check.is_instance(resp.json(), list)
            resp_json = resp.json()
            check.greater(len(resp_json), 0)
            check.is_false(any(book.get('bookingid') == book_id for book in resp_json))
        run_step("E2E_Regular_Scenarios>Step#8. Get All Bookings After Deletion", step_8)

    except StepFailure:
        pytest.fail("E2E_Regular_Scenarios : Experienced a fatal step failure and Skipped the rest of the steps")



def test_e2e_edge_scenarios(manage_api_context, manage_book_creation_json_context):
    health_check = False
    token, req_body, book_id = None, None, None

    try:
        def step_1():
            nonlocal health_check
            api = manage_api_context(
                base_url=ApiEndpoints.base_url(),
                http_headers={"Content-Type": "application/json"}
            )
            resp = api.get('/ping')
            check.equal(resp.status, 201)
            check.equal(resp.status_text, "Created")
            check.is_true(resp.ok)
            nonlocal health_check
            health_check = (resp.status == 201)
        run_step("E2E_Edge_Scenarios>Step#1. Health Check", step_1)

        # auth token
        def step_2():
            nonlocal token
            api = manage_api_context(
                base_url=ApiEndpoints.base_url(),
                http_headers={"Accept": "application/json"}
            )
            resp = api.post("/auth", data = {'username': 'admin', 'password': 'password123'})
            check.equal(resp.status, 200)
            check.equal(resp.status_text, "OK")
            check.is_true(resp.ok)
            check.is_not_none(resp.json())
            check.is_not_none(resp.json().get('token'))
            token = resp.json().get('token')
        run_step("E2E_Edge_Scenarios>Step#2. Auth Token", step_2)

        # create booking
        def step_3():
            nonlocal req_body, book_id
            req_body, book_id = manage_book_creation_json_context(user_id=12)
            check.is_not_none(req_body)
            check.greater(book_id, 0)
            check.is_instance(req_body, dict)
            check.is_not_none(req_body.get('firstname'))
            check.is_not_none(req_body.get('lastname'))
            check.is_not_none(req_body.get('totalprice'))
            check.is_not_none(req_body.get('depositpaid'))
            check.is_not_none(req_body.get('additionalneeds'))
            check.is_not_none(req_body.get('bookingdates'))
            check.is_not_none(req_body.get('bookingdates').get('checkin'))
            check.is_not_none(req_body.get('bookingdates').get('checkout'))
        run_step("E2E_Edge_Scenarios>Step#3. Create Booking", step_3)

        # create booking - double creation
        def step_4():
            nonlocal req_body, book_id
            req_body, book_id = manage_book_creation_json_context(user_id=12)
            check.is_not_none(req_body)
            check.greater(book_id, 0)
            check.is_instance(req_body, dict)
            check.is_not_none(req_body.get('firstname'))
            check.is_not_none(req_body.get('lastname'))
            check.is_not_none(req_body.get('totalprice'))
            check.is_not_none(req_body.get('depositpaid'))
            check.is_not_none(req_body.get('additionalneeds'))
            check.is_not_none(req_body.get('bookingdates'))
            check.is_not_none(req_body.get('bookingdates').get('checkin'))
            check.is_not_none(req_body.get('bookingdates').get('checkout'))
        run_step("E2E_Edge_Scenarios>Step#4. Create Booking - Double Creation", step_4)

        # get booking
        def step_5():
            nonlocal req_body, book_id
            api = manage_api_context(
                base_url=ApiEndpoints.base_url(),
                http_headers={"Accept": "application/json"}
            )
            resp = api.get(f"/booking/{book_id}")
            check.equal(resp.status, 200)
            check.equal(resp.status_text, "OK")
            check.is_true(resp.ok)
            check.is_not_none(resp.json())
            check.is_instance(resp.json(), dict)
            resp_json = resp.json()
            check.greater_equal(len(resp_json), 0)
            check.equal(resp_json.get('firstname'), req_body.get('firstname'))
            check.equal(resp_json.get('lastname'), req_body.get('lastname'))
            check.equal(resp_json.get('totalprice'), req_body.get('totalprice'))
            check.equal(resp_json.get('depositpaid'), req_body.get('depositpaid'))
            check.equal(resp_json.get('bookingdates').get('checkin'), req_body.get('bookingdates').get('checkin'))
            check.equal(resp_json.get('bookingdates').get('checkout'), req_body.get('bookingdates').get('checkout'))
            #check.is_none(resp_json.get('additionalneeds'))
        run_step("E2E_Edge_Scenarios>Step#5. Get Booking", step_5)

        # patch - partial update
        def step_6():
            nonlocal token, req_body, book_id
            new_req_body = copy.deepcopy(req_body.copy())
            new_req_body['firstname'] = str(book_id) + "_" + req_body['firstname']
            new_req_body['lastname'] = "Updated_" + req_body['lastname'] + "_" + str(book_id)
            new_req_body['totalprice'] = req_body['totalprice'] + 100
            new_req_body['additionalneeds'] = str(book_id) + "_" + req_body['additionalneeds']
            new_req_body['bookingdates']['checkin'] = (datetime.now() - timedelta(days=3)).strftime("%Y-%m-%d")
            new_req_body['bookingdates']['checkout'] = datetime.now().strftime("%Y-%m-%d")

            api = manage_api_context(
                base_url=ApiEndpoints.base_url(),
                http_headers={"Cookie": f"token={token}"}
            )
            resp = api.patch(f"/booking/{book_id}", data=new_req_body)
            check.equal(resp.status, 200)
            check.equal(resp.status_text, "OK")
            check.is_true(resp.ok)
            check.is_not_none(resp.json())

            resp_json = resp.json()
            check.equal(resp_json.get('firstname'), new_req_body.get('firstname'))
            check.equal(resp_json.get('lastname'), new_req_body.get('lastname'))
            check.equal(resp_json.get('totalprice'), new_req_body.get('totalprice'))
            check.equal(resp_json.get('depositpaid'), new_req_body.get('depositpaid'))
            check.equal(resp_json.get('bookingdates').get('checkin'), new_req_body.get('bookingdates').get('checkin'))
            check.equal(resp_json.get('bookingdates').get('checkout'), new_req_body.get('bookingdates').get('checkout'))
            check.equal(resp_json.get('additionalneeds'), new_req_body.get('additionalneeds'))
            # update req_body
            req_body = copy.deepcopy(new_req_body.copy())
        run_step("E2E_Edge_Scenarios>Step#6. Patch - Partial Update Booking", step_6)

        # get booking after partial update
        def step_7():
            nonlocal req_body, book_id
            api = manage_api_context(
                base_url=ApiEndpoints.base_url(),
                http_headers={"Accept": "application/json"}
            )
            resp = api.get(f"/booking/{book_id}")
            check.equal(resp.status, 200)
            check.equal(resp.status_text, "OK")
            check.is_true(resp.ok)
            check.is_not_none(resp.json())
            check.is_instance(resp.json(), dict)
            resp_json = resp.json()
            check.greater_equal(len(resp_json), 0)
            check.equal(resp_json.get('firstname'), req_body.get('firstname'))
            check.equal(resp_json.get('lastname'), req_body.get('lastname'))
            check.equal(resp_json.get('totalprice'), req_body.get('totalprice'))
            check.equal(resp_json.get('depositpaid'), req_body.get('depositpaid'))
            check.equal(resp_json.get('bookingdates').get('checkin'), req_body.get('bookingdates').get('checkin'))
            check.equal(resp_json.get('bookingdates').get('checkout'), req_body.get('bookingdates').get('checkout'))
            check.equal(resp_json.get('additionalneeds'), req_body.get('additionalneeds'))
        run_step("E2E_Edge_Scenarios>Step#7. Get Booking After Patch - Partial Update Booking", step_7)

        # put - update
        def step_8():
            nonlocal token, req_body, book_id
            new_req_body = copy.deepcopy(req_body.copy())
            new_req_body['firstname'] = req_body['firstname'] + "_" + str(book_id)
            new_req_body['lastname'] = str(book_id) + "_" + req_body['lastname'] + "_Updated"
            new_req_body['totalprice'] = req_body['totalprice'] + 100
            new_req_body['additionalneeds'] = req_body['additionalneeds'] + "_" + str(book_id)
            new_req_body['bookingdates']['checkin'] = (datetime.now() - timedelta(days=5)).strftime("%Y-%m-%d")
            new_req_body['bookingdates']['checkout'] =(datetime.now() - timedelta(days=3)).strftime("%Y-%m-%d")

            api = manage_api_context( base_url=ApiEndpoints.base_url(), http_headers={"Cookie": f"token={token}"} )
            resp = api.put(f"/booking/{book_id}", data=new_req_body)
            check.equal(resp.status, 200)
            check.equal(resp.status_text, "OK")
            check.is_true(resp.ok)
            check.is_not_none(resp.json())

            resp_json = resp.json()
            check.equal(resp_json.get('firstname'), new_req_body.get('firstname'))
            check.equal(resp_json.get('lastname'), new_req_body.get('lastname'))
            check.equal(resp_json.get('totalprice'), new_req_body.get('totalprice'))
            check.equal(resp_json.get('depositpaid'), new_req_body.get('depositpaid'))
            check.equal(resp_json.get('bookingdates').get('checkin'), new_req_body.get('bookingdates').get('checkin'))
            check.equal(resp_json.get('bookingdates').get('checkout'), new_req_body.get('bookingdates').get('checkout'))
            check.equal(resp_json.get('additionalneeds'), new_req_body.get('additionalneeds'))
            # update req_body
            req_body = copy.deepcopy(new_req_body.copy())
        run_step("E2E_Edge_Scenarios>Step#8. Put - Update Booking", step_8)

        # get booking after put - update
        def step_9():
            nonlocal req_body, book_id
            api = manage_api_context(
                base_url=ApiEndpoints.base_url(),
                http_headers={"Accept": "application/json"}
            )
            resp = api.get(f"/booking/{book_id}")
            check.equal(resp.status, 200)
            check.equal(resp.status_text, "OK")
            check.is_true(resp.ok)
            check.is_not_none(resp.json())
            check.is_instance(resp.json(), dict)
            resp_json = resp.json()
            check.greater_equal(len(resp_json), 0)
            check.equal(resp_json.get('firstname'), req_body.get('firstname'))
            check.equal(resp_json.get('lastname'), req_body.get('lastname'))
            check.equal(resp_json.get('totalprice'), req_body.get('totalprice'))
            check.equal(resp_json.get('depositpaid'), req_body.get('depositpaid'))
            check.equal(resp_json.get('bookingdates').get('checkin'), req_body.get('bookingdates').get('checkin'))
            check.equal(resp_json.get('bookingdates').get('checkout'), req_body.get('bookingdates').get('checkout'))
            check.equal(resp_json.get('additionalneeds'), req_body.get('additionalneeds'))
        run_step("E2E_Edge_Scenarios>Step#9. Get Booking After Put - Update Booking", step_9)

        # delete booking
        def step_10():
            nonlocal req_body, book_id
            api = manage_api_context(
                base_url=ApiEndpoints.base_url(),
                http_headers={"Cookie": f"token={token}", "Content-Type": "application/json"}
            )
            resp = api.delete(f"/booking/{book_id}")
            check.equal(resp.status, 201)
            check.equal(resp.status_text, "Created")
            check.is_true(resp.ok)
        run_step("E2E_Edge_Scenarios>Step#10. Delete Booking", step_10)

        # get booking
        def step_11():
            nonlocal req_body, book_id
            api = manage_api_context( base_url=ApiEndpoints.base_url() )
            resp = api.get(f'/booking/{book_id}')
            check.equal(resp.status, 404)
            check.equal(resp.status_text, "Not Found")
            check.is_false(resp.ok)
            check.is_not_none(resp.text())
        run_step("E2E_Edge_Scenarios>Step#11. Get Booking After Being Deleted", step_11)

    except StepFailure:
        pytest.fail("E2E_Edge_Scenarios : Experienced a fatal step failure and Skipped the rest of the steps")

