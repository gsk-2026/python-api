import pytest
import requests
from random import randint
from pytest_check import check
from config.settings import ApiEndpoints


def _get_default_headers():
    return {"Content-Type": "application/json", "Accept": "application/json"}


def _get_client_context(client_num=None):
    num = randint(0, 999999) if client_num is None else client_num
    return {
        "key": f"Client_Key_{num:06d}",
        "secret": f"Client_Secret_{num:06d}",
        "description": f"Client Description {num:06d}",
    }


def _get_resource_context(resource_num=None):
    num = randint(0, 999999) if resource_num is None else resource_num
    return {
        "key": f"Resource_Key_{num:06d}",
        "type": f"Resource_Type_{num:06d}",
        "description": f"Resource Description {num:06d}",
    }



@pytest.fixture
def manage_default_headers():
    return _get_default_headers()


@pytest.fixture
def manage_playwright_api_context(playwright):
    api_contexts = []

    def create_api_context(base_url, http_headers=None):
        merged_headers = _get_default_headers().copy()
        if http_headers: merged_headers.update(http_headers)

        api_ctxt = playwright.request.new_context(
            base_url=base_url,
            extra_http_headers=merged_headers
        )
        api_contexts.append(api_ctxt)
        return api_ctxt

    yield create_api_context

    for api in api_contexts:
        api.dispose()



@pytest.fixture(scope="session")
def manage_requests_api_session_context():
    session_contexts = []

    def create_session(base_url, headers=None):
        session_ctxt = requests.Session()
        session_ctxt.base_url = base_url.rstrip("/")

        merged_headers = _get_default_headers().copy()
        if headers: merged_headers.update(headers)

        session_ctxt.headers.update(merged_headers)
        session_contexts.append(session_ctxt)
        return session_ctxt

    yield create_session

    for session in session_contexts:
        session.close()

    session_contexts.clear()



@pytest.fixture
def manage_client_context(playwright):
    api_contexts = []

    def create_api_context(base_url=None, http_headers=None):
        merged_url = ApiEndpoints.base_url()
        merged_headers = _get_default_headers().copy()
        if base_url: merged_url = base_url.rstrip("/")
        if http_headers: merged_headers.update(http_headers)

        api_ctxt = playwright.request.new_context(base_url=merged_url, extra_http_headers=merged_headers)
        api_contexts.append(api_ctxt)
        return api_ctxt

    yield create_api_context

    for api in api_contexts:
        api.dispose()



@pytest.fixture
def manage_client_creation_playwright(playwright):
    api_contexts = []
    client_contexts = []

    def create_api_client_context(base_url=None, http_headers=None):
        merged_url = ApiEndpoints.client_url()
        merged_headers = _get_default_headers().copy()
        if base_url: merged_url = base_url.rstrip("/")
        if http_headers: merged_headers.update(http_headers)

        api = playwright.request.new_context(base_url=merged_url, extra_http_headers=merged_headers)
        api_contexts.append(api)

        client_payload = _get_client_context().copy()
        resp = api.post("/api/v1/client", data=client_payload)
        check.is_true(resp.ok)
        check.equal(resp.status, 201)
        check.is_not_none(resp.json())
        client_id = resp.json()['id']
        client_contexts.append(client_id)

        return api, client_id

    yield create_api_client_context

    for api, client_id in zip(api_contexts, client_contexts):
        resp = api.delete(f"/api/v1/client/{client_id}")
        check.is_in(resp.status, [204, 404])
        api.dispose()



@pytest.fixture
def manage_client_creation_requests():
    client_contexts = []

    def create_api_client_context(base_url=None, http_headers=None):
        client_payload = _get_client_context().copy()
        merged_url = ApiEndpoints.client_url()
        merged_headers = _get_default_headers().copy()
        if base_url: merged_url = base_url.rstrip("/")
        if http_headers: merged_headers.update(http_headers)

        resp = requests.post(merged_url, headers=merged_headers, json=client_payload)
        check.is_true(resp.ok)
        check.equal(resp.status_code, 201)
        check.is_not_none(resp.json())
        client_id = resp.json()['id']
        client_contexts.append(client_id)

        return client_id

    yield create_api_client_context

    for client_id in client_contexts:
        resp = requests.delete(f"{ApiEndpoints.client_url()}/{client_id}")
        check.is_in(resp.status_code, [204, 404])



@pytest.fixture(scope="session")
def manage_client_creation_requests_session():
    session_contexts = []
    client_contexts = []

    def create_api_client_context(base_url=None, http_headers=None):
        merged_url = ApiEndpoints.client_url()
        merged_headers = _get_default_headers().copy()
        if base_url: merged_url = base_url
        if http_headers: merged_headers.update(http_headers)

        session = requests.Session()
        session.base_url = merged_url.rstrip("/")
        session.headers.update(merged_headers)
        session_contexts.append(session)

        client_payload = _get_client_context().copy()

        resp = session.post(f"{session.base_url}", json=client_payload)
        check.is_true(resp.ok)
        check.equal(resp.status_code, 201)
        check.is_not_none(resp.json())
        client_id = resp.json()['id']
        client_contexts.append(client_id)

        return session, client_id

    yield create_api_client_context

    for session, client_id in zip(session_contexts, client_contexts):
        resp = session.delete(f"{session.base_url}/{client_id}")
        check.is_in(resp.status_code, [204, 404])
        session.close()



@pytest.fixture
def manage_resource_creation_playwright(playwright):
    api_contexts = []
    resource_contexts = []

    def create_api_resource_context(base_url=None, http_headers=None):
        merged_url = ApiEndpoints.resource_url()
        merged_headers = _get_default_headers().copy()
        if base_url: merged_url = base_url.rstrip("/")
        if http_headers: merged_headers.update(http_headers)

        api = playwright.request.new_context(base_url=merged_url, extra_http_headers=merged_headers)
        api_contexts.append(api)

        resource_payload = _get_resource_context().copy()
        resp = api.post("/api/v1/resource", data=resource_payload)
        check.is_true(resp.ok)
        check.equal(resp.status, 201)
        check.is_not_none(resp.json())
        resource_id = resp.json()['id']
        resource_contexts.append(resource_id)

        return api, resource_id

    yield create_api_resource_context

    for api, resource_id in zip(api_contexts, resource_contexts):
        resp = api.delete(f"/api/v1/resource/{resource_id}")
        check.is_in(resp.status, [204, 404])
        api.dispose()



@pytest.fixture
def manage_resource_creation_requests():
    resource_contexts = []

    def create_api_resource_context(base_url=None, http_headers=None):
        resource_payload = _get_resource_context().copy()
        merged_url = ApiEndpoints.resource_url()
        merged_headers = _get_default_headers().copy()
        if base_url: merged_url = base_url.rstrip("/")
        if http_headers: merged_headers.update(http_headers)

        resp = requests.post(merged_url, headers=merged_headers, json=resource_payload)
        check.is_true(resp.ok)
        check.equal(resp.status_code, 201)
        check.is_not_none(resp.json())
        resource_id = resp.json()['id']
        resource_contexts.append(resource_id)

        return resource_id

    yield create_api_resource_context

    for resource_id in resource_contexts:
        resp = requests.delete(f"{ApiEndpoints.resource_url()}/{resource_id}")
        check.is_in(resp.status_code, [204, 404])




@pytest.fixture
def manage_client_resource_access_creation_playwright(playwright):
    api_contexts = []
    client_contexts = []
    resource_contexts = []
    #
    def create_client_resource_access_context(base_url=None, http_headers=None, random_num=None):
        merged_url = ApiEndpoints.resource_url()
        merged_headers = _get_default_headers().copy()
        merged_random_num = randint(0, 999999)
        if base_url: merged_url = base_url.rstrip("/")
        if http_headers: merged_headers.update(http_headers)
        #
        api = playwright.request.new_context(base_url=merged_url, extra_http_headers=merged_headers)
        api_contexts.append(api)
        #
        client_payload = _get_client_context(merged_random_num).copy()
        resp = api.post("/api/v1/client", data=client_payload)
        check.is_true(resp.ok)
        check.equal(resp.status, 201)
        check.is_not_none(resp.json())
        client_id = resp.json()['id']
        client_contexts.append(client_id)
        #
        resource_payload = _get_resource_context(merged_random_num).copy()
        resp = api.post("/api/v1/resource", data=resource_payload)
        check.is_true(resp.ok)
        check.equal(resp.status, 201)
        check.is_not_none(resp.json())
        resource_id = resp.json()['id']
        resource_contexts.append(resource_id)
        #
        client_resource_access_payload =  {
            "clientId": f"{client_id}",
            "resourceId": f"{resource_id}",
            "accessCode": f"Access_Code_{merged_random_num:06d}",
            "description": f"Client Resource Access Description {merged_random_num:06d}",
        }
        resp = api.post("/api/v1/client-resource-access", data=client_resource_access_payload)
        check.is_true(resp.ok)
        check.equal(resp.status, 201)
        check.is_not_none(resp.json())
        resp_json = resp.json()
        check.equal(str(resp_json['clientId']), f"{client_resource_access_payload['clientId']}")
        check.equal(str(resp_json['resourceId']), f"{client_resource_access_payload['resourceId']}")
        check.equal(resp_json['accessCode'], f"{client_resource_access_payload['accessCode']}")
        check.equal(resp_json['description'], f"{client_resource_access_payload['description']}")
        #
        return api, client_id, resource_id
    #
    yield create_client_resource_access_context
    #
    for api, client_id, resource_id in zip(api_contexts, client_contexts, resource_contexts):
        resp = api.delete(f"/api/v1/client-resource-access/client/{client_id}/resource/{resource_id}")
        check.is_in(resp.status, [204, 404])
        resp = api.delete(f"/api/v1/resource/{resource_id}")
        check.is_in(resp.status, [204, 404])
        resp = api.delete(f"/api/v1/client/{client_id}")
        check.is_in(resp.status, [204, 404])
        api.dispose()




@pytest.fixture
def manage_client_resource_access_creation_requests():
    client_contexts = []
    resource_contexts = []

    def create_client_resource_access_context(base_url=None, http_headers=None, random_num=None):
        merged_url = ApiEndpoints.base_url()
        merged_headers = _get_default_headers().copy()
        merged_random_num = randint(0, 999999)
        if base_url: merged_url = base_url.rstrip("/")
        if http_headers: merged_headers.update(http_headers)
        if random_num: merged_random_num = random_num
        #
        client_payload = _get_client_context(merged_random_num).copy()
        resp = requests.post(f"{merged_url}/api/v1/client", headers=merged_headers, json=client_payload)
        check.is_true(resp.ok)
        check.equal(resp.status_code, 201)
        check.is_not_none(resp.json())
        client_id = resp.json()['id']
        client_contexts.append(client_id)
        #
        resource_payload = _get_resource_context(merged_random_num).copy()
        resp = requests.post(f"{merged_url}/api/v1/resource", headers=merged_headers, json=resource_payload)
        check.is_true(resp.ok)
        check.equal(resp.status_code, 201)
        check.is_not_none(resp.json())
        resource_id = resp.json()['id']
        resource_contexts.append(resource_id)
        #
        client_resource_access_payload =  {
            "clientId": f"{client_id}",
            "resourceId": f"{resource_id}",
            "accessCode": f"Access_Code_{merged_random_num:06d}",
            "description": f"Client Resource Access Description {merged_random_num:06d}",
        }
        resp = requests.post(f"{merged_url}/api/v1/client-resource-access", headers=merged_headers, json=client_resource_access_payload)
        check.is_true(resp.ok)
        check.equal(resp.status_code, 201)
        check.is_not_none(resp.json())
        resp_json = resp.json()
        check.equal(str(resp_json['clientId']), f"{client_resource_access_payload['clientId']}")
        check.equal(str(resp_json['resourceId']), f"{client_resource_access_payload['resourceId']}")
        check.equal(resp_json['accessCode'], f"{client_resource_access_payload['accessCode']}")
        check.equal(resp_json['description'], f"{client_resource_access_payload['description']}")
        #
        return client_id, resource_id
    #
    yield create_client_resource_access_context
    #
    for client_id, resource_id in zip(client_contexts, resource_contexts):
        resp = requests.delete(f"{ApiEndpoints.client_resource_access_url()}/client/{client_id}/resource/{resource_id}")
        check.is_in(resp.status_code, [204, 404])
        resp = requests.delete(f"{ApiEndpoints.resource_url()}/{resource_id}")
        check.is_in(resp.status_code, [204, 404])
        resp = requests.delete(f"{ApiEndpoints.client_url()}/{client_id}")
        check.is_in(resp.status_code, [204, 404])

