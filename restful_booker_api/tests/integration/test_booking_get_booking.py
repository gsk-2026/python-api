from pytest_check import check
import xml.etree.ElementTree as ET
from config.settings import ApiEndpoints



def test_booking_get_booking_booking_url_200(manage_api_context, manage_book_creation_json_context):
    # create
    req_body, book_id = manage_book_creation_json_context(user_id=1)

    # get
    api = manage_api_context(
        base_url=ApiEndpoints.booking_url()+f"/{book_id}",
        http_headers={"Accept": "application/json"}
    )
    resp = api.get("")
    check.equal(resp.status, 200)
    check.equal(resp.status_text, "OK")
    check.is_true(resp.ok)
    check.is_not_none(resp.json())
    check.is_instance(resp.json(), dict)

    resp_json = resp.json()
    check.is_not_none(resp_json.get('firstname'))
    check.is_not_none(resp_json.get('lastname'))
    check.is_not_none(resp_json.get('totalprice'))
    check.is_not_none(resp_json.get('depositpaid'))
    check.is_not_none(resp_json.get('bookingdates'))
    check.is_not_none(resp_json.get('bookingdates').get('checkin'))
    check.is_not_none(resp_json.get('bookingdates').get('checkout'))
    #check.is_none(resp_json.get('additionalneeds'))



def test_booking_get_booking_base_url_200(manage_api_context, manage_book_creation_json_context):
    # create
    req_body, book_id = manage_book_creation_json_context(user_id=2)

    # get
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
    check.is_not_none(resp_json.get('firstname'))
    check.is_not_none(resp_json.get('lastname'))
    check.is_not_none(resp_json.get('totalprice'))
    check.is_not_none(resp_json.get('depositpaid'))
    check.is_not_none(resp_json.get('bookingdates'))
    check.is_not_none(resp_json.get('bookingdates').get('checkin'))
    check.is_not_none(resp_json.get('bookingdates').get('checkout'))
    #check.is_none(resp_json.get('additionalneeds'))



def test_booking_get_booking_base_url_headers_application_xml_200(manage_api_context, manage_book_creation_json_context):
    # create
    req_body, book_id = manage_book_creation_json_context(user_id=3)

    # get
    api = manage_api_context(
        base_url=ApiEndpoints.base_url(),
        http_headers={"Accept": "application/xml", "Content-Type": "application/xml"}
    )
    resp = api.get(f"/booking/{book_id}")
    check.equal(resp.status, 200)
    check.equal(resp.status_text, "OK")
    check.is_true(resp.ok)
    check.is_not_none(resp.text())
    check.is_instance(resp.text(), str)

    root = ET.fromstring(resp.text())
    check.is_not_none(root.find("firstname").text)
    check.is_not_none(root.find("lastname").text)
    check.greater(int(root.find("totalprice").text),0)
    check.is_not_none(root.find("depositpaid").text)
    check.is_not_none(root.find("bookingdates/checkin").text)
    check.is_not_none(root.find("bookingdates/checkout").text)



def test_booking_get_booking_base_url_headers_application_json_200(manage_api_context, manage_book_creation_json_context):
    # create
    req_body, book_id = manage_book_creation_json_context(user_id=4)

    # get
    api = manage_api_context(
        base_url=ApiEndpoints.base_url(),
        http_headers={"Accept": "application/json"}
    )
    resp = api.get(f"/booking/{book_id}")
    check.equal(resp.status, 200)
    check.equal(resp.status_text, "OK")

    resp_json = resp.json()
    check.is_not_none(resp_json.get('firstname'))
    check.is_not_none(resp_json.get('lastname'))
    check.is_not_none(resp_json.get('totalprice'))
    check.is_not_none(resp_json.get('depositpaid'))
    check.is_not_none(resp_json.get('bookingdates'))
    check.is_not_none(resp_json.get('bookingdates').get('checkin'))
    check.is_not_none(resp_json.get('bookingdates').get('checkout'))
    #check.is_none(resp_json.get('additionalneeds'))



def test_booking_get_booking_base_url_headers_application_html_418(manage_api_context, manage_book_creation_json_context):
    # create
    req_body, book_id = manage_book_creation_json_context(user_id=5)

    # get
    api = manage_api_context(
        base_url=ApiEndpoints.base_url(),
        http_headers={"Accept": "text/html"}
    )
    resp = api.get(f"/booking/{book_id}")
    check.equal(resp.status, 418)
    check.equal(resp.status_text, "I'm a teapot")



def test_booking_get_booking_base_url_no_existing_id_404(manage_api_context, manage_book_creation_json_context):
    # create
    req_body, book_id = manage_book_creation_json_context(user_id=6)

    # get
    api = manage_api_context(
        base_url=ApiEndpoints.base_url(),
        http_headers={"Accept": "application/json"}
    )
    resp = api.get(f"/booking/{book_id+book_id}")
    check.equal(resp.status, 404)
    check.equal(resp.status_text, "Not Found")
    check.is_false(resp.ok)



def test_booking_get_booking_base_url_append_invalid_200(manage_api_context, manage_book_creation_json_context):
    # create
    req_body, book_id = manage_book_creation_json_context(user_id=7)

    # get
    api = manage_api_context(
        base_url=ApiEndpoints.base_url(),
        http_headers={"Accept": "application/json"}
    )
    resp = api.get(f"/booking/{book_id}abcdef")         # source defect ?
    check.equal(resp.status, 200)
    check.equal(resp.status_text, "OK")

    resp_json = resp.json()
    check.is_not_none(resp_json.get('firstname'))
    check.is_not_none(resp_json.get('lastname'))
    check.is_not_none(resp_json.get('totalprice'))
    check.is_not_none(resp_json.get('depositpaid'))
    check.is_not_none(resp_json.get('bookingdates'))
    check.is_not_none(resp_json.get('bookingdates').get('checkin'))
    check.is_not_none(resp_json.get('bookingdates').get('checkout'))
    #check.is_none(resp_json.get('additionalneeds'))




def test_booking_get_booking_base_url_prepend_invalid_404(manage_api_context, manage_book_creation_json_context):
    # create
    req_body, book_id = manage_book_creation_json_context(user_id=8)

    # get
    api = manage_api_context(
        base_url=ApiEndpoints.base_url(),
        http_headers={"Accept": "application/json"}
    )
    resp = api.get(f"/booking/a{book_id}")
    check.equal(resp.status, 404)
    check.equal(resp.status_text, "Not Found")
    check.is_false(resp.ok)

