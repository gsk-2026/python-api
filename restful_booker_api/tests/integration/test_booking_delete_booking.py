import base64
from pytest_check import check
from config.settings import ApiEndpoints



def test_booking_delete_booking_book_url_201(manage_api_context, manage_book_creation_json_context):
    # create
    req_body, book_id = manage_book_creation_json_context(user_id=1)

    # get otoken
    api = manage_api_context( base_url=ApiEndpoints.base_url() )
    resp = api.post("/auth", data = {'username': 'admin', 'password': 'password123'})
    token = resp.json().get('token')

    # delete
    api = manage_api_context(
        base_url=ApiEndpoints.booking_url()+f"/{book_id}",
        http_headers={"Cookie": f"token={token}", "Content-Type": "application/json"}
    )
    resp = api.delete("")
    check.equal(resp.status, 201)
    check.equal(resp.status_text, "Created")
    check.is_true(resp.ok)



def test_booking_delete_booking_base_url_headers_json_201(manage_api_context, manage_book_creation_json_context):
    # create
    req_body, book_id = manage_book_creation_json_context(user_id=2)

    # get otoken
    api = manage_api_context( base_url=ApiEndpoints.base_url() )
    resp = api.post("/auth", data = {'username': 'admin', 'password': 'password123'})
    token = resp.json().get('token')

    # delete
    api = manage_api_context(
        base_url=ApiEndpoints.base_url(),
        http_headers={"Cookie": f"token={token}", "Content-Type": "application/json"}
    )
    resp = api.delete(f"/booking/{book_id}")
    check.equal(resp.status, 201)
    check.equal(resp.status_text, "Created")
    check.is_true(resp.ok)



def test_booking_delete_booking_base_url_headers_xml_201(manage_api_context, manage_book_creation_json_context):
    # create
    req_body, book_id = manage_book_creation_json_context(user_id=3)

    # encode credentials
    credentials = "admin:password123"
    encoded_bytes = base64.b64encode(credentials.encode("utf-8"))
    encoded_str = encoded_bytes.decode("utf-8")

    # delete
    api = manage_api_context(
        base_url=ApiEndpoints.base_url(),
        http_headers={"Authorization": f"Basic {encoded_str}", "Content-Type": "application/json"}
    )
    resp = api.delete(f"/booking/{book_id}")
    check.equal(resp.status, 201)
    check.equal(resp.status_text, "Created")
    check.is_true(resp.ok)



def test_booking_delete_booking_base_url_double_deletion_201(manage_api_context, manage_book_creation_json_context):
    # create
    req_body, book_id = manage_book_creation_json_context(user_id=4)

    # get otoken
    api = manage_api_context( base_url=ApiEndpoints.base_url() )
    resp = api.post("/auth", data = {'username': 'admin', 'password': 'password123'})
    token = resp.json().get('token')

    # delete
    api = manage_api_context(
        base_url=ApiEndpoints.base_url(),
        http_headers={"Cookie": f"token={token}", "Content-Type": "application/json"}
    )
    resp = api.delete(f"/booking/{book_id}")
    check.equal(resp.status, 201)
    check.equal(resp.status_text, "Created")
    check.is_true(resp.ok)

    # delete replicated
    api = manage_api_context(
        base_url=ApiEndpoints.base_url(),
        http_headers={"Cookie": f"token={token}", "Content-Type": "application/json"}
    )
    resp = api.delete(f"/booking/{book_id}")
    check.equal(resp.status, 405)
    check.equal(resp.status_text, "Method Not Allowed")
    check.is_false(resp.ok)



def test_booking_delete_booking_base_url_non_existing_id_405(manage_api_context, manage_book_creation_json_context):
    # create
    req_body, book_id = manage_book_creation_json_context(user_id=5)

    # get otoken
    api = manage_api_context( base_url=ApiEndpoints.base_url() )
    resp = api.post("/auth", data = {'username': 'admin', 'password': 'password123'})
    token = resp.json().get('token')

    # delete
    api = manage_api_context(
        base_url=ApiEndpoints.base_url(),
        http_headers={"Cookie": f"token={token}", "Content-Type": "application/json"}
    )
    resp = api.delete(f"/booking/{book_id+book_id}")
    check.equal(resp.status, 405)
    check.equal(resp.status_text, "Method Not Allowed")
    check.is_false(resp.ok)

