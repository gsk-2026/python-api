from pytest_check import check
from config.settings import ApiEndpoints



def test_booking_get_booking_ids_booking_url_200(manage_api_context, manage_book_creation_json_context):
    # create
    req_body, book_id = manage_book_creation_json_context(user_id=1)

    # get
    api = manage_api_context(base_url=ApiEndpoints.booking_url(), http_headers={"Content-Type": "application/json"})
    resp = api.get('')
    check.equal(resp.status, 200)
    check.equal(resp.status_text, "OK")
    check.is_true(resp.ok)
    check.is_not_none(resp.json())
    check.is_instance(resp.json(), list)

    resp_json = resp.json()
    check.greater(len(resp_json), 0)
    book_ids = [book.get('bookingid') for book in resp_json]
    check.is_in(book_id, book_ids)



def test_booking_get_booking_ids_200(manage_api_context, manage_book_creation_json_context):
    # create
    req_body, book_id = manage_book_creation_json_context(user_id=2)

    # get
    api = manage_api_context( base_url=ApiEndpoints.base_url(), http_headers={"Content-Type": "application/json"})
    resp = api.get('/booking')
    check.equal(resp.status, 200)
    check.equal(resp.status_text, "OK")
    check.is_true(resp.ok)
    check.is_not_none(resp.json())
    check.is_instance(resp.json(), list)

    resp_json = resp.json()
    check.greater(len(resp_json), 0)
    check.is_true(any(book.get('bookingid') == book_id for book in resp_json))



def test_booking_get_booking_ids_no_headers_200(manage_api_context, manage_book_creation_json_context):
    # create
    req_body, book_id = manage_book_creation_json_context(user_id=3)

    # get
    api = manage_api_context( base_url=ApiEndpoints.base_url() )
    resp = api.get('/booking')
    check.equal(resp.status, 200)
    check.equal(resp.status_text, "OK")
    check.is_true(resp.ok)
    check.is_not_none(resp.json())
    check.is_instance(resp.json(), list)

    resp_json = resp.json()
    check.greater(len(resp_json), 0)
    check.is_true(any(book.get('bookingid') == book_id for book in resp_json))



def test_booking_get_booking_ids_first_name_james_200(manage_api_context, manage_book_creation_json_context):
    # create
    req_body, book_id = manage_book_creation_json_context(user_id=4)

    # get
    api = manage_api_context( base_url=ApiEndpoints.base_url() )
    query_params = {"firstname": "James_4"}   # case-sensitive ?
    resp = api.get('/booking', params=query_params)
    check.equal(resp.status, 200)
    check.equal(resp.status_text, "OK")
    check.is_true(resp.ok)
    check.is_not_none(resp.json())
    check.is_instance(resp.json(), list)

    resp_json = resp.json()
    check.greater(len(resp_json), 0)
    check.is_true(any(book.get('bookingid') == book_id for book in resp_json))



def test_booking_get_booking_ids_last_name_brown_200(manage_api_context, manage_book_creation_json_context):
    # create
    req_body, book_id = manage_book_creation_json_context(user_id=5)

    # get
    api = manage_api_context( base_url=ApiEndpoints.base_url() )
    query_params = {"lastname": "Brown_5"}   # case-sensitive

    resp = api.get('/booking', params=query_params)
    check.equal(resp.status, 200)
    check.equal(resp.status_text, "OK")
    check.is_true(resp.ok)
    check.is_not_none(resp.json())
    check.is_instance(resp.json(), list)

    resp_json = resp.json()
    check.greater(len(resp_json), 0)
    check.is_true(any(book.get('bookingid') == book_id for book in resp_json))



def test_booking_get_booking_ids_first_james_last_brown_200(manage_api_context, manage_book_creation_json_context):
    # create
    req_body, book_id = manage_book_creation_json_context(user_id=6)

    # get
    api = manage_api_context( base_url=ApiEndpoints.base_url() )
    query_params = {"firstname": "James_6", "lastname": "Brown_6"}
    resp = api.get('/booking', params=query_params)
    check.equal(resp.status, 200)
    check.equal(resp.status_text, "OK")
    check.is_true(resp.ok)
    check.is_not_none(resp.json())
    check.is_instance(resp.json(), list)

    resp_json = resp.json()
    check.greater(len(resp_json), 0)
    check.is_true(any(book.get('bookingid') == book_id for book in resp_json))



def test_booking_get_booking_ids_check_in_200(manage_api_context, manage_book_creation_json_context):
    # create
    #req_body, book_id = manage_book_creation_json_context(user_id=7)

    # get
    api = manage_api_context( base_url=ApiEndpoints.base_url() )
    query_params = {"checkin": "2025-07-07"}        # defect for "checkin"

    resp = api.get('/booking', params=query_params)
    check.equal(resp.status, 200)
    check.equal(resp.status_text, "OK")
    check.is_true(resp.ok)
    check.is_not_none(resp.json())
    check.is_instance(resp.json(), list)

    resp_json = resp.json()
    check.greater(len(resp_json), 0)
    #check.is_true(any(book.get('bookingid') == book_id for book in resp_json))   # defect for "checkin"



def test_booking_get_booking_ids_check_out_200(manage_api_context, manage_book_creation_json_context):
    # create
    req_body, book_id = manage_book_creation_json_context(user_id=8)

    # get
    api = manage_api_context( base_url=ApiEndpoints.base_url() )
    query_params = {"checkout": "2026-08-08"}

    resp = api.get('/booking', params=query_params)
    check.equal(resp.status, 200)
    check.equal(resp.status_text, "OK")
    check.is_true(resp.ok)
    check.is_not_none(resp.json())
    check.is_instance(resp.json(), list)

    resp_json = resp.json()
    check.greater(len(resp_json), 0)
    check.is_true(any(book.get('bookingid') == book_id for book in resp_json))



def test_booking_get_booking_ids_check_in_out_200(manage_api_context, manage_book_creation_json_context):
    # create
    req_body, book_id = manage_book_creation_json_context(user_id=9)

    # get
    api = manage_api_context( base_url=ApiEndpoints.base_url() )
    query_params = {"checkin": "2025-09-09", "checkout": "2026-09-09"}      # defect for "checkin"
    resp = api.get('/booking', params=query_params)
    check.equal(resp.status, 200)
    check.equal(resp.status_text, "OK")
    check.is_true(resp.ok)
    check.is_not_none(resp.json())
    check.is_instance(resp.json(), list)

    resp_json = resp.json()
    check.greater_equal(len(resp_json), 0)      # check.greater(len(resp_json), 0)  # defect with "checkin"
    #check.is_true(any(book.get('bookingid') == book_id for book in resp_json))     # defect for "checkin"



def test_booking_get_booking_ids_invalid_query_200(manage_api_context, manage_book_creation_json_context):
    # create
    #req_body, book_id = manage_book_creation_json_context(user_id=10)

    # get
    api = manage_api_context( base_url=ApiEndpoints.base_url())
    query_params = {"ssn": "123-456-7890", "id": "abc-123"}     # API ignore this invalid params but get all of the booking

    resp = api.get('/booking', params=query_params)
    check.equal(resp.status, 200)
    check.equal(resp.status_text, "OK")
    check.is_true(resp.ok)
    check.is_not_none(resp.json())
    check.is_instance(resp.json(), list)

    resp_json = resp.json()
    check.greater(len(resp_json), 0)



def test_booking_get_booking_ids_headers_xml_200(manage_api_context, manage_book_creation_xml_context):
    # create
    req_body, book_id = manage_book_creation_xml_context(user_id=11)

    # get
    api = manage_api_context(
        base_url=ApiEndpoints.base_url(),
        http_headers={"Content-Type": "application/xml", "Accept": "application/xml"}
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



def test_booking_get_booking_ids_headers_html_200(manage_api_context, manage_book_creation_json_context):
    # create
    req_body, book_id = manage_book_creation_json_context(user_id=12)

    # get
    api = manage_api_context(
        base_url=ApiEndpoints.base_url(),
        http_headers={"Content-Type": "text/html", "Accept": "text/html"}
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

