import pytest
from pytest_check import check
from config.settings import ApiEndpoints



@pytest.fixture
def manage_api_context(playwright):
    api_contexts = []

    def create_api_context(base_url, http_headers=None):
        api = playwright.request.new_context(base_url=base_url, extra_http_headers=http_headers or {})
        api_contexts.append(api)
        return api

    yield create_api_context

    for api in api_contexts:
        api.dispose()



@pytest.fixture
def manage_book_creation_json_context(playwright):
    api_contexts = []
    book_ids = []

    # booking creation
    def create_book_creation_base_url_context(user_id=None):
        api = playwright.request.new_context(base_url=ApiEndpoints.base_url())
        api_contexts.append(api)
        req_body = {
            "firstname": f"James_{user_id}",
            "lastname": f"Brown_{user_id}",
            "totalprice": int(f"{user_id}0{user_id}"),
            "depositpaid": True,
            "bookingdates": {
                "checkin": f"2025-{user_id:02d}-{user_id:02d}",
                "checkout": f"2026-{user_id:02d}-{user_id:02d}"
            },
            "additionalneeds": f"Additional Needs {user_id}"
        }
        resp = api.post('booking', data=req_body)
        check.equal(resp.status, 200)
        check.is_not_none(resp.json())

        resp_json = resp.json()
        check.is_instance(resp_json, dict)
        check.is_not_none(resp_json.get('bookingid'))
        book_id = resp.json().get('bookingid')
        book_ids.append(book_id)

        return req_body, book_id

    # pause, return, resume
    yield create_book_creation_base_url_context

    # token
    api = playwright.request.new_context( base_url=ApiEndpoints.base_url() )
    api_contexts.append(api)
    resp = api.post("/auth", data = {'username': 'admin', 'password': 'password123'})
    token = resp.json().get('token')

    # booking deletion
    for book_id in book_ids:
        api = playwright.request.new_context(
            base_url=ApiEndpoints.base_url(),
            extra_http_headers={"Accept": "application/json"}
        )
        api_contexts.append(api)
        resp = api.get(f"/booking/{book_id}")
        # check in case of been deleted
        if (
            resp.status == 200 and
            resp.json() is not None and
            isinstance(resp.json(), dict) and
            len(resp.json()) > 0
        ):
            api = playwright.request.new_context(
                base_url=ApiEndpoints.base_url(),
                extra_http_headers={"Cookie": f"token={token}", "Content-Type": "application/json"}
            )
            api_contexts.append(api)
            resp = api.delete(f"/booking/{book_id}")
            check.equal(resp.status, 201)

    # cleanup
    for api in api_contexts:
        api.dispose()



@pytest.fixture
def manage_book_creation_xml_context(playwright):
    api_contexts = []
    book_ids = []

    # booking creation
    def create_book_creation_base_url_context(user_id=None):
        api = playwright.request.new_context(
            base_url=ApiEndpoints.base_url(),
            extra_http_headers={'Content-Type': 'text/xml'}
        )
        api_contexts.append(api)
        req_body = f'''
            <booking>
                <firstname>John_{user_id}</firstname>
                <lastname>Johnson_{user_id}</lastname>
                <totalprice>{user_id}0{user_id}</totalprice>
                <depositpaid>false</depositpaid>
                <bookingdates>
                    <checkin>2025-{user_id:02d}-{user_id:02d}</checkin>
                    <checkout>2026-{user_id:02d}-{user_id:02d}</checkout>
                </bookingdates>
                <additionalneeds>Additional Needs {user_id}</additionalneeds>
            </booking>
        '''
        resp = api.post('booking', data=req_body)
        check.equal(resp.status, 200)
        check.equal(resp.status_text, "OK")
        check.is_true(resp.ok)
        check.is_not_none(resp.json())

        resp_json = resp.json()
        check.is_instance(resp_json, dict)
        check.is_not_none(resp_json.get('bookingid'))
        book_id = resp.json().get('bookingid')
        book_ids.append(book_id)

        return req_body, book_id

    # pause, return, resume
    yield create_book_creation_base_url_context

    # token
    api = playwright.request.new_context( base_url=ApiEndpoints.base_url() )
    api_contexts.append(api)
    resp = api.post("/auth", data = {'username': 'admin', 'password': 'password123'})
    token = resp.json().get('token')

    # booking deletion
    for book_id in book_ids:
        api = playwright.request.new_context(
            base_url=ApiEndpoints.base_url(),
            extra_http_headers={"Accept": "application/json"}
        )
        api_contexts.append(api)
        resp = api.get(f"/booking/{book_id}")
        # check in case of being deleted
        if (
            resp.status == 200 and
            resp.json() is not None and
            isinstance(resp.json(), dict) and
            len(resp.json()) > 0
        ):
            api = playwright.request.new_context(
                base_url=ApiEndpoints.base_url(),
                extra_http_headers={"Cookie": f"token={token}", "Content-Type": "application/json"}
            )
            api_contexts.append(api)
            resp = api.delete(f"/booking/{book_id}")
            check.equal(resp.status, 201)

    # cleanup
    for api in api_contexts:
        api.dispose()

