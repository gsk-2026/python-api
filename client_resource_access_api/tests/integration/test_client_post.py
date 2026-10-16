from config.settings import ApiEndpoints
from pytest_check import check
from random import randint
import requests

from tests.conftest import manage_playwright_api_context



def test_client_post_201_playwright(manage_playwright_api_context):
    client_no = randint(0, 999999)
    client_payload = {
        "key": f"Client_App_{client_no:06d}",
        "secret": f"validSecret_{client_no:06d}",
        "description": f"Client App {client_no:06d}",
    }
    api_context = manage_playwright_api_context(base_url=ApiEndpoints.base_url())
    resp = api_context.post("/api/v1/client", data=client_payload)
    check.equal(resp.status, 201)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(resp_json["key"], client_payload["key"])
    check.equal(resp_json["description"], client_payload["description"])
    check.greater(resp_json['id'], 0)
    check.is_not_none(resp_json['createdAt'])
    check.is_not_none(resp_json['updatedAt'])
    # cleanup
    resp = api_context.delete(f"/api/v1/client/{resp_json['id']}")
    check.is_true(resp.ok)
    check.equal(resp.status, 204)



def test_client_post_201_requests(manage_default_headers):
    client_no = randint(0, 999999)
    client_payload = {
        "key": f"Client_App_{client_no:06d}",
        "secret": f"validSecret_{client_no:06d}",
        "description": f"Client App {client_no:06d}",
    }
    resp = requests.post(ApiEndpoints.client_url(), headers=manage_default_headers, json=client_payload)
    check.is_true(resp.ok)
    check.equal(resp.status_code, 201)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(resp_json["key"], client_payload["key"])
    check.equal(resp_json["description"], client_payload["description"])
    check.greater(resp_json['id'], 0)
    check.is_not_none(resp_json['createdAt'])
    check.is_not_none(resp_json['updatedAt'])
    # cleanup
    resp = requests.delete(f"{ApiEndpoints.client_url()}/{resp_json['id']}")
    check.is_true(resp.ok)
    check.equal(resp.status_code, 204)



def test_client_post_201_requests_session(manage_requests_api_session_context):
    client_no = randint(0, 999999)
    client_payload = {
        "key": f"Client_App_{client_no:06d}",
        "secret": f"validSecret_{client_no:06d}",
        "description": f"Client App {client_no:06d}",
    }
    api_session_context = manage_requests_api_session_context(base_url=ApiEndpoints.client_url())
    resp = api_session_context.post(f"{api_session_context.base_url}", json=client_payload)
    check.is_true(resp.ok)
    check.equal(resp.status_code, 201)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(resp_json["key"], client_payload["key"])
    check.equal(resp_json["description"], client_payload["description"])
    check.greater(resp_json['id'], 0)
    check.is_not_none(resp_json['createdAt'])
    check.is_not_none(resp_json['updatedAt'])
    # cleanup
    resp = api_session_context.delete(f"{api_session_context.base_url}/{resp_json['id']}")
    check.is_true(resp.ok)
    check.equal(resp.status_code, 204)



def test_client_post_no_secret_201_playwright(manage_playwright_api_context):
    client_no = randint(0, 999999)
    client_payload = {
        "key": f"Client_App_{client_no:06d}",
        "description": f"Client App {client_no:06d}",
    }
    api_context = manage_playwright_api_context(base_url=ApiEndpoints.base_url())
    resp = api_context.post("/api/v1/client", data=client_payload)
    check.equal(resp.status, 201)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(resp_json["key"], client_payload["key"])
    check.equal(resp_json["description"], client_payload["description"])
    check.greater(resp_json['id'], 0)
    check.is_not_none(resp_json['createdAt'])
    check.is_not_none(resp_json['updatedAt'])
    # cleanup
    resp = api_context.delete(f"/api/v1/client/{resp_json['id']}")
    check.is_true(resp.ok)
    check.equal(resp.status, 204)



def test_client_post_no_secret_201_requests(manage_default_headers):
    client_no = randint(0, 999999)
    client_payload = {
        "key": f"Client_App_{client_no:06d}",
        "description": f"Client App {client_no:06d}",
    }
    resp = requests.post(ApiEndpoints.client_url(), headers=manage_default_headers, json=client_payload)
    check.is_true(resp.ok)
    check.equal(resp.status_code, 201)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(resp_json["key"], client_payload["key"])
    check.equal(resp_json["description"], client_payload["description"])
    check.greater(resp_json['id'], 0)
    check.is_not_none(resp_json['createdAt'])
    check.is_not_none(resp_json['updatedAt'])
    # cleanup
    resp = requests.delete(f"{ApiEndpoints.client_url()}/{resp_json['id']}")
    check.is_true(resp.ok)
    check.equal(resp.status_code, 204)



def test_client_post_no_description_201_playwright(manage_playwright_api_context):
    client_no = randint(0, 999999)
    client_payload = {
        "key": f"Client_App_{client_no:06d}",
        "secret": f"validSecret_{client_no:06d}",
    }
    api_context = manage_playwright_api_context(base_url=ApiEndpoints.base_url())
    resp = api_context.post("/api/v1/client", data=client_payload)
    check.equal(resp.status, 201)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(resp_json["key"], client_payload["key"])
    check.is_none(resp_json["description"])
    check.greater(resp_json['id'], 0)
    check.is_not_none(resp_json['createdAt'])
    check.is_not_none(resp_json['updatedAt'])
    # cleanup
    resp = api_context.delete(f"/api/v1/client/{resp_json['id']}")
    check.is_true(resp.ok)
    check.equal(resp.status, 204)


def test_client_post_no_description_201_requests(manage_default_headers):
    client_no = randint(0, 999999)
    client_payload = {
        "key": f"Client_App_{client_no:06d}",
        "secret": f"validSecret_{client_no:06d}",
    }
    resp = requests.post(ApiEndpoints.client_url(), headers=manage_default_headers, json=client_payload)
    check.is_true(resp.ok)
    check.equal(resp.status_code, 201)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(resp_json["key"], client_payload["key"])
    check.is_none(resp_json["description"])
    check.greater(resp_json['id'], 0)
    check.is_not_none(resp_json['createdAt'])
    check.is_not_none(resp_json['updatedAt'])
    # cleanup
    resp = requests.delete(f"{ApiEndpoints.client_url()}/{resp_json['id']}")
    check.is_true(resp.ok)
    check.equal(resp.status_code, 204)



def test_client_post_duplicate_key_409_playwright(manage_playwright_api_context):
    # first client
    client_no = randint(0, 999999)
    client_payload = {
        "key": f"Client_App_{client_no:06d}",
        "secret": f"validSecret_{client_no:06d}",
        "description": f"Client App {client_no:06d}",
    }
    api_context = manage_playwright_api_context(base_url=ApiEndpoints.base_url())
    resp = api_context.post("/api/v1/client", data=client_payload)
    check.is_true(resp.ok)
    check.equal(resp.status, 201)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(resp_json["key"], client_payload["key"])
    check.equal(resp_json["description"], client_payload["description"])
    # second client
    client_payload_2 = {
        "key": f"{client_payload['key']}",
        "secret": f"{client_payload['secret']}-2",
        "description": f"{client_payload['description']}-2",
    }
    resp = api_context.post("/api/v1/client", data=client_payload_2)
    check.is_false(resp.ok)
    check.equal(resp.status, 409)
    resp_json = resp.json()
    check.equal(resp_json["status"], 409)
    check.equal(resp_json["error"], "Conflict")
    check.equal(resp_json["path"], "/api/v1/client")



def test_client_post_duplicate_key_409_requests(manage_default_headers):
    client_no = randint(0, 999999)
    client_payload = {
        "key": f"Client_App_{client_no:06d}",
        "secret": f"validSecret_{client_no:06d}",
        "description": f"Client App {client_no:06d}",
    }
    resp = requests.post(ApiEndpoints.client_url(), headers=manage_default_headers, json=client_payload)
    check.is_true(resp.ok)
    check.equal(resp.status_code, 201)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(resp_json["key"], client_payload["key"])

    client_payload_2 = {
        "key": f"{client_payload['key']}",
        "secret": f"{client_payload['secret']}-2",
        "description": f"{client_payload['description']}-2",
    }
    resp = requests.post(ApiEndpoints.client_url(), headers=manage_default_headers, json=client_payload_2)
    check.is_false(resp.ok)
    check.equal(resp.status_code, 409)
    resp_json = resp.json()
    check.equal(resp_json["status"], 409)
    check.equal(resp_json["error"], "Conflict")
    check.equal(resp_json["path"], "/api/v1/client")



def test_client_post_no_key_400_playwright(manage_playwright_api_context):
    client_no = randint(0, 999999)
    client_payload = {
        "secret": f"validSecret_{client_no:06d}",
        "description": f"Client App {client_no:06d}",
    }
    api_context = manage_playwright_api_context(base_url=ApiEndpoints.base_url())
    resp = api_context.post("/api/v1/client", data=client_payload)
    check.is_false(resp.ok)
    check.equal(resp.status, 400)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(resp_json["status"], 400)
    check.equal(resp_json["error"], "Bad Request")



def test_client_post_no_key_400_requests(manage_default_headers):
    client_no = randint(0, 999999)
    client_payload = {
        "secret": f"validSecret_{client_no:06d}",
        "description": f"Client App {client_no:06d}",
    }
    resp = requests.post(ApiEndpoints.client_url(), headers=manage_default_headers, json=client_payload)

    check.is_false(resp.ok)
    check.equal(resp.status_code, 400)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(resp_json["status"], 400)
    check.equal(resp_json["error"], "Bad Request")



def test_client_post_no_payload_400_playwright(manage_playwright_api_context):
    api_context = manage_playwright_api_context(base_url=ApiEndpoints.base_url())
    resp = api_context.post("/api/v1/client", data={})
    check.is_false(resp.ok)
    check.equal(resp.status, 400)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(resp_json["status"], 400)
    check.equal(resp_json["error"], "Bad Request")



def test_client_post_no_payload_400_requests(manage_default_headers):
    resp = requests.post(ApiEndpoints.client_url(), headers=manage_default_headers, json={})
    check.is_false(resp.ok)
    check.equal(resp.status_code, 400)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(resp_json["status"], 400)
    check.equal(resp_json["error"], "Bad Request")




def test_client_post_invalid_url_404_playwright(manage_playwright_api_context):
    client_no = randint(0, 999999)
    client_payload = {
        "key": f"Client_App_{client_no:06d}",
        "secret": f"validSecret_{client_no:06d}",
        "description": f"Client App {client_no:06d}",
    }
    api_context = manage_playwright_api_context(base_url=ApiEndpoints.base_url())
    resp = api_context.post("/api/v2/client", data=client_payload)
    check.is_false(resp.ok)
    check.equal(resp.status, 404)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(resp_json["status"], 404)
    check.equal(resp_json["error"], "Not Found")



def test_client_post_invalid_url_404_requests(manage_default_headers):
    client_no = randint(0, 999999)
    client_payload = {
        "key": f"Client_App_{client_no:06d}",
        "secret": f"validSecret_{client_no:06d}",
        "description": f"Client App {client_no:06d}",
    }
    resp = requests.post(ApiEndpoints.base_url(), headers=manage_default_headers, json=client_payload)
    check.is_false(resp.ok)
    check.equal(resp.status_code, 404)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(resp_json["status"], 404)
    check.equal(resp_json["error"], "Not Found")



def test_client_post_duplicate_payload_201_409_playwright(manage_playwright_api_context):
    client_no = randint(0, 999999)
    client_payload = {
        "key": f"Client_App_{client_no:06d}",
        "secret": f"validSecret_{client_no:06d}",
        "description": f"Client App {client_no:06d}",
    }
    # first time
    api_context = manage_playwright_api_context(base_url=ApiEndpoints.base_url())
    resp = api_context.post("/api/v1/client", data=client_payload)
    check.equal(resp.status, 201)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(resp_json["key"], client_payload["key"])
    check.equal(resp_json["description"], client_payload["description"])
    check.greater(resp_json['id'], 0)
    check.is_not_none(resp_json['createdAt'])
    check.is_not_none(resp_json['updatedAt'])
    client_id = resp_json['id']
    # duplicated
    resp = api_context.post("/api/v1/client", data=client_payload)
    check.equal(resp.status, 409)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(resp_json["status"], 409)
    check.equal(resp_json["error"], "Conflict")
    # cleanup
    resp = api_context.delete(f"/api/v1/client/{client_id}")
    check.is_true(resp.ok)
    check.equal(resp.status, 204)



def test_client_post_duplicate_payload_201_409_requests(manage_default_headers):
    client_no = randint(0, 999999)
    client_payload = {
        "key": f"Client_App_{client_no:06d}",
        "secret": f"validSecret_{client_no:06d}",
        "description": f"Client App {client_no:06d}",
    }
    # first time
    resp = requests.post(ApiEndpoints.client_url(), headers=manage_default_headers, json=client_payload)
    check.is_true(resp.ok)
    check.equal(resp.status_code, 201)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(resp_json["key"], client_payload["key"])
    check.equal(resp_json["description"], client_payload["description"])
    check.greater(resp_json['id'], 0)
    check.is_not_none(resp_json['createdAt'])
    check.is_not_none(resp_json['updatedAt'])
    client_id = resp_json['id']
    # duplicated
    resp = requests.post(ApiEndpoints.client_url(), headers=manage_default_headers, json=client_payload)
    check.is_false(resp.ok)
    check.equal(resp.status_code, 409)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(resp_json["status"], 409)
    check.equal(resp_json["error"], "Conflict")
    # cleanup
    resp = requests.delete(f"{ApiEndpoints.client_url()}/{client_id}")
    check.is_true(resp.ok)
    check.equal(resp.status_code, 204)



def test_client_post_min_length_key_400_playwright(manage_playwright_api_context):
    client_no = randint(0, 99)
    client_payload = {
        #"key": f"Client_App_{client_no:06d}",          # @Size(min = 3, max = 100)
        "key": f"{client_no:02d}",
        "secret": f"validSecret_{client_no:06d}",
        "description": f"Client App {client_no:06d}",
    }
    api_context = manage_playwright_api_context(base_url=ApiEndpoints.base_url())
    resp = api_context.post("/api/v1/client", data=client_payload)
    check.is_false(resp.ok)
    check.equal(resp.status, 400)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(resp_json['status'], 400)
    check.equal(resp_json['error'], 'Bad Request')



def test_client_post_min_length_secret_400_requests(manage_default_headers):
    client_no = randint(0, 999999)
    client_payload = {
        "key": f"Client_App_{client_no:06d}",
        #"secret": f"validSecret_{client_no:06d}",      # @Size(min = 16, max = 128)
        "secret": f"Secret_A_{client_no:06d}",
        "description": f"Client App {client_no:06d}",
    }
    resp = requests.post(ApiEndpoints.client_url(), headers=manage_default_headers, json=client_payload)
    check.is_false(resp.ok)
    check.equal(resp.status_code, 400)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(resp_json['status'], 400)
    check.equal(resp_json['error'], 'Bad Request')


