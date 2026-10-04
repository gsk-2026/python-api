from pytest_check import check
from config.settings import ApiEndpoints



def test_ping_health_check_ping_url_201(manage_api_context):
    api = manage_api_context(
        base_url=ApiEndpoints.ping_url(),
        http_headers={"Content-Type": "application/json"}
    )
    resp = api.get('')
    check.equal(resp.status, 201)
    check.equal(resp.status_text, "Created")
    check.is_true(resp.ok)


def test_ping_health_check_headers_context_type_201(manage_api_context):
    api = manage_api_context(
        base_url=ApiEndpoints.base_url(),
        http_headers={"Content-Type": "application/json"}
    )
    resp = api.get('/ping')
    check.equal(resp.status, 201)
    check.equal(resp.status_text, "Created")
    check.is_true(resp.ok)


def test_ping_health_check_headers_accept_201(manage_api_context):
    api = manage_api_context(
        base_url=ApiEndpoints.base_url(),
        http_headers={"Accept": "application/json"}
    )
    resp = api.get('/ping')
    check.equal(resp.status, 201)
    check.equal(resp.status_text, "Created")
    check.is_true(resp.ok)


def test_ping_health_check_headers_201(manage_api_context):
    api = manage_api_context(
        base_url=ApiEndpoints.base_url(),
        http_headers={"Content-Type": "application/json", "Accept": "application/json"}
    )
    resp = api.get('/ping')
    check.equal(resp.status, 201)
    check.equal(resp.status_text, "Created")
    check.is_true(resp.ok)


def test_ping_health_check_no_headers_201(manage_api_context):
    api = manage_api_context(
        base_url=ApiEndpoints.base_url()
    )
    resp = api.get('/ping')
    check.equal(resp.status, 201)
    check.equal(resp.status_text, "Created")
    check.is_true(resp.ok)


def test_ping_health_check_headers_text_html_201(manage_api_context):
    api = manage_api_context(
        base_url=ApiEndpoints.base_url(),
        http_headers={"Content-Type": "text/html"}
    )
    resp = api.get('/ping')
    check.equal(resp.status, 201)
    check.equal(resp.status_text, "Created")
    check.is_true(resp.ok)


def test_ping_health_check_headers_application_html_201(manage_api_context):
    api = manage_api_context(
        base_url=ApiEndpoints.base_url(),
        http_headers={"Content-Type": "application/html"}
    )
    resp = api.get('/ping')
    check.equal(resp.status, 201)
    check.equal(resp.status_text, "Created")
    check.is_true(resp.ok)


def test_ping_health_check_headers_text_xml_201(manage_api_context):
    api = manage_api_context(
        base_url=ApiEndpoints.base_url(),
        http_headers={"Content-Type": "text/xml"}
    )
    resp = api.get('/ping')
    check.equal(resp.status, 201)
    check.equal(resp.status_text, "Created")
    check.is_true(resp.ok)



def test_ping_health_check_headers_application_xml_201(manage_api_context):
    api = manage_api_context(
        base_url=ApiEndpoints.base_url(),
        http_headers={"Content-Type": "application/xml"}
    )
    resp = api.get('/ping')
    check.equal(resp.status, 201)
    check.equal(resp.status_text, "Created")
    check.is_true(resp.ok)



def test_ping_health_check_wrong_url_404(manage_api_context):
    api = manage_api_context(
        base_url=ApiEndpoints.booking_url(),
        http_headers={"Content-Type": "application/json"}
    )
    resp = api.get('/PINGS')
    check.equal(resp.status, 404)
    check.equal(resp.status_text, "Not Found")
    check.is_false(resp.ok)
