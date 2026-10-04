from pytest_check import check
import json
import xml.etree.ElementTree as ET
from config.settings import ApiEndpoints


def test_booking_create_booking_book_url_dft_headers_200(manage_api_context):
    api = manage_api_context(base_url=ApiEndpoints.booking_url())
    req_body = {
        "firstname": "John",
        "lastname": "Doe",
        "totalprice": 101,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2023-01-01",
            "checkout": "2023-01-02"
        },
        "additionalneeds" : "Breakfast"
    }
    resp = api.post('', data=req_body)
    check.equal(resp.status, 200)
    check.equal(resp.status_text, "OK")
    check.is_true(resp.ok)
    check.is_not_none(resp.json())

    resp_json = resp.json()
    check.is_instance(resp_json, dict)
    check.is_not_none(resp_json.get('bookingid'))
    check.is_not_none(resp_json.get('booking'))
    check.equal(resp_json.get('booking').get('firstname'), req_body.get('firstname'))
    check.equal(resp_json.get('booking').get('lastname'), req_body.get('lastname'))
    check.equal(resp_json.get('booking').get('totalprice'), req_body.get('totalprice'))
    check.equal(resp_json.get('booking').get('depositpaid'), req_body.get('depositpaid'))
    check.equal(resp_json.get('booking').get('additionalneeds'), req_body.get('additionalneeds'))
    check.equal(resp_json.get('booking').get('bookingdates').get('checkin'), req_body.get('bookingdates').get('checkin'))
    check.equal(resp_json.get('booking').get('bookingdates').get('checkout'), req_body.get('bookingdates').get('checkout'))




def test_booking_create_booking_base_url_dft_headers_200(manage_api_context):
    api = manage_api_context(base_url=ApiEndpoints.base_url())
    req_body = {
        "firstname": "John",
        "lastname": "Doe",
        "totalprice": 202,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2023-02-01",
            "checkout": "2023-02-02"
        },
        "additionalneeds" : "Breakfast"
    }
    resp = api.post('booking', data=req_body)
    check.equal(resp.status, 200)
    check.equal(resp.status_text, "OK")
    check.is_true(resp.ok)
    check.is_not_none(resp.json())

    resp_json = resp.json()
    check.is_instance(resp_json, dict)
    check.is_not_none(resp_json.get('bookingid'))
    check.is_not_none(resp_json.get('booking'))
    check.equal(resp_json.get('booking').get('firstname'), req_body.get('firstname'))
    check.equal(resp_json.get('booking').get('lastname'), req_body.get('lastname'))
    check.equal(resp_json.get('booking').get('totalprice'), req_body.get('totalprice'))
    check.equal(resp_json.get('booking').get('depositpaid'), req_body.get('depositpaid'))
    check.equal(resp_json.get('booking').get('additionalneeds'), req_body.get('additionalneeds'))

    resp_bookingdates = resp_json.get('booking').get('bookingdates')
    req_bookingdates = req_body.get('bookingdates')
    check.is_instance(resp_bookingdates, dict)
    check.is_instance(req_bookingdates, dict)
    check.equal(resp_bookingdates.get('checkin'), req_bookingdates.get('checkin'))
    check.equal(resp_bookingdates.get('checkout'), req_bookingdates.get('checkout'))




def test_booking_create_booking_base_url_headers_json_200(manage_api_context):
    api = manage_api_context(
        base_url=ApiEndpoints.base_url(),
        http_headers={'Content-Type': 'application/json'}
    )
    req_body = {
        "firstname": "John",
        "lastname": "Doe",
        "totalprice": 303,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2023-03-01",
            "checkout": "2023-03-02"
        },
        "additionalneeds" : "Lunch"
    }
    resp = api.post('/booking', data=req_body)
    check.equal(resp.status, 200)
    check.equal(resp.status_text, "OK")
    check.is_true(resp.ok)
    check.is_not_none(resp.json())

    resp_json = resp.json()
    check.is_instance(resp_json, dict)
    check.is_not_none(resp_json.get('bookingid'))
    check.is_not_none(resp_json.get('booking'))
    check.equal(resp_json.get('booking').get('firstname'), req_body.get('firstname'))
    check.equal(resp_json.get('booking').get('lastname'), req_body.get('lastname'))
    check.equal(resp_json.get('booking').get('totalprice'), req_body.get('totalprice'))
    check.equal(resp_json.get('booking').get('depositpaid'), req_body.get('depositpaid'))
    check.equal(resp_json.get('booking').get('additionalneeds'), req_body.get('additionalneeds'))

    resp_bookingdates = resp_json.get('booking').get('bookingdates')
    req_bookingdates = req_body.get('bookingdates')
    check.is_instance(resp_bookingdates, dict)
    check.is_instance(req_bookingdates, dict)
    check.equal(resp_bookingdates.get('checkin'), req_bookingdates.get('checkin'))
    check.equal(resp_bookingdates.get('checkout'), req_bookingdates.get('checkout'))




def test_booking_create_booking_base_url_headers_xml_200(manage_api_context):
    api = manage_api_context(
        base_url=ApiEndpoints.base_url(),
        http_headers={'Content-Type': 'text/xml'}
    )
    req_body = '''
        <booking>
            <firstname>John</firstname>
            <lastname>Doe</lastname>
            <totalprice>404</totalprice>
            <depositpaid>true</depositpaid>
            <bookingdates>
                <checkin>2023-04-01</checkin>
                <checkout>2023-04-02</checkout>
            </bookingdates>
            <additionalneeds>Dinner</additionalneeds>
        </booking>
    '''
    resp = api.post('/booking', data=req_body)
    check.equal(resp.status, 200)
    check.equal(resp.status_text, "OK")
    check.is_true(resp.ok)
    check.is_not_none(resp.text())

    req_xml_root = ET.fromstring(req_body)
    resp_json_root = json.loads(resp.text())
    check.is_not_none(resp_json_root.get("bookingid"))
    check.is_not_none(resp_json_root.get("booking"))
    check.equal(resp_json_root.get("booking").get("firstname"), req_xml_root.find("firstname").text)
    check.equal(resp_json_root.get("booking").get("lastname"), req_xml_root.find("lastname").text)
    check.equal(str(resp_json_root.get("booking").get("totalprice")), req_xml_root.find("totalprice").text)
    check.equal(resp_json_root.get("booking").get("depositpaid"), req_xml_root.find("depositpaid").text.lower()=='true')    # defect here
    check.equal(resp_json_root.get("booking").get("additionalneeds"), req_xml_root.find("additionalneeds").text)
    check.equal(resp_json_root.get("booking").get("bookingdates").get("checkin"), req_xml_root.find("bookingdates/checkin").text)
    check.equal(resp_json_root.get("booking").get("bookingdates").get("checkout"), req_xml_root.find("bookingdates/checkout").text)



def test_booking_create_booking_base_url_headers_application_xml_500(manage_api_context):
    api = manage_api_context(
        base_url=ApiEndpoints.base_url(),
        http_headers={'Content-Type': 'application/xml'}
    )
    req_body = '''
        <booking>
            <firstname>John</firstname>
            <lastname>Doe</lastname>
            <totalprice>505</totalprice>
            <depositpaid>true</depositpaid>
            <bookingdates>
                <checkin>2023-05-01</checkin>
                <checkout>2023-05-02</checkout>
            </bookingdates>
            <additionalneeds>Dinner</additionalneeds>
        </booking>
    '''
    resp = api.post('/booking', data=req_body)
    check.equal(resp.status, 500)
    check.equal(resp.status_text, "Internal Server Error")
    check.equal(resp.text(), "Internal Server Error")
    check.is_false(resp.ok)

