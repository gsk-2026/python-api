from pytest_check import check
from config.settings import ApiEndpoints



def test_auth_create_token_auth_uel_200(manage_api_context):
    api = manage_api_context(
        base_url=ApiEndpoints.auth_url(),
        http_headers={"Accept": "application/json"}
    )
    resp = api.post("", data = {'username': 'admin', 'password': 'password123'})
    check.equal(resp.status, 200)
    check.equal(resp.status_text, "OK")
    check.is_true(resp.ok)
    check.is_not_none(resp.json())
    check.is_not_none(resp.json().get('token'))



def test_auth_create_token_200(manage_api_context):
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



def test_auth_create_token_no_header_200(manage_api_context):
    api = manage_api_context(
        base_url=ApiEndpoints.base_url()
    )
    resp = api.post("/auth", data = {'username': 'admin', 'password': 'password123'})
    check.equal(resp.status, 200)
    check.equal(resp.status_text, "OK")
    check.is_true(resp.ok)
    check.is_not_none(resp.json())
    check.is_not_none(resp.json().get('token'))



def test_auth_create_token_invalid_username_200(manage_api_context):
    api = manage_api_context(
        base_url=ApiEndpoints.base_url(),
        http_headers={"Accept": "application/json"}
    )
    resp = api.post("/auth", data = {'username': 'Admin', 'password': 'password123'})
    check.equal(resp.status, 200)
    check.equal(resp.status_text, "OK")
    check.is_true(resp.ok)
    check.is_not_none(resp.json())
    check.is_none(resp.json().get('token'))
    check.is_not_none(resp.json().get('reason'))
    check.equal(resp.json().get('reason'), 'Bad credentials')



def test_auth_create_token_invalid_pswd_200(manage_api_context):
    api = manage_api_context(
        base_url=ApiEndpoints.base_url(),
        http_headers={"Accept": "application/json"}
    )
    resp = api.post("/auth", data = {'username': 'admin', 'password': 'pswd123'})
    check.equal(resp.status, 200)
    check.equal(resp.status_text, "OK")
    check.is_true(resp.ok)
    check.is_not_none(resp.json())
    check.is_none(resp.json().get('token'))
    check.is_not_none(resp.json().get('reason'))
    check.equal(resp.json().get('reason'), 'Bad credentials')



def test_auth_create_token_header_application_html_200(manage_api_context):
    api = manage_api_context(
        base_url=ApiEndpoints.base_url(),
        http_headers={"Content-Type": "application/html"}
    )
    resp = api.post("/auth", data = {'username': 'admin', 'password': 'password123'})
    check.equal(resp.status, 200)
    check.equal(resp.status_text, "OK")
    check.is_true(resp.ok)
    check.is_not_none(resp.json())
    check.is_none(resp.json().get('token'))
    check.is_not_none(resp.json().get('reason'))
    check.equal(resp.json().get('reason'), 'Bad credentials')



def test_auth_create_token_header_text_html_200(manage_api_context):
    api = manage_api_context(
        base_url=ApiEndpoints.base_url(),
        http_headers={"Content-Type": "text/html"}
    )
    resp = api.post("/auth", data = {'username': 'admin', 'password': 'password123'})
    check.equal(resp.status, 200)
    check.equal(resp.status_text, "OK")
    check.is_true(resp.ok)
    check.is_not_none(resp.json())
    check.is_none(resp.json().get('token'))
    check.is_not_none(resp.json().get('reason'))
    check.equal(resp.json().get('reason'), 'Bad credentials')



def test_auth_create_token_header_content_type_200(manage_api_context):
    api = manage_api_context(
        base_url=ApiEndpoints.base_url(),
        http_headers={"Content-Type": "application/json"}
    )
    resp = api.post("/auth", data = {'username': 'admin', 'password': 'password123'})
    check.equal(resp.status, 200)
    check.equal(resp.status_text, "OK")
    check.is_true(resp.ok)
    check.is_not_none(resp.json())
    check.is_not_none(resp.json().get('token'))



def test_auth_create_token_header_text_xml_400(manage_api_context):
    api = manage_api_context(
        base_url=ApiEndpoints.base_url(),
        http_headers={"Content-Type": "text/xml"}
    )
    resp = api.post("/auth", data = {'username': 'admin', 'password': 'password123'})
    check.equal(resp.status, 400)
    check.equal(resp.status_text, "Bad Request")
    check.is_false(resp.ok)



def test_auth_create_token_header_application_xml_400(manage_api_context):
    api = manage_api_context(
        base_url=ApiEndpoints.base_url(),
        http_headers={"Content-Type": "application/xml"}
    )
    resp = api.post("/auth", data = {'username': 'admin', 'password': 'password123'})
    check.equal(resp.status, 400)
    check.equal(resp.status_text, "Bad Request")
    check.is_false(resp.ok)

