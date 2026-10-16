from random import randint

from pytest_check import check
from config.settings import ApiEndpoints
import requests



def test_client_get_200_playwright(manage_client_creation_playwright):
    api, id = manage_client_creation_playwright()
    resp = api.get(f"/api/v1/client/{id}")
    check.is_true(resp.ok)
    check.equal(resp.status, 200)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(resp_json['id'], id)
    check.is_not_none(resp_json['key'])
    check.is_not_none(resp_json['createdAt'])



def test_client_get_200_requests(manage_client_creation_requests):
    id = manage_client_creation_requests()
    resp = requests.get(url=f"{ApiEndpoints.client_url()}/{id}")
    check.is_true(resp.ok)
    check.equal(resp.status_code, 200)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(resp_json['id'], id)
    check.is_not_none(resp_json['key'])
    check.is_not_none(resp_json['createdAt'])



def test_client_get_200_requests_session(manage_client_creation_requests_session):
    session, id = manage_client_creation_requests_session()
    resp = session.get(url=f"{ApiEndpoints.client_url()}/{id}")
    check.is_true(resp.ok)
    check.equal(resp.status_code, 200)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(resp_json['id'], id)
    check.is_not_none(resp_json['key'])
    check.is_not_none(resp_json['createdAt'])



def test_client_get_key_200_playwright(manage_client_creation_playwright):
    api, id = manage_client_creation_playwright()
    resp = api.get(f"/api/v1/client/{id}/key")
    check.is_true(resp.ok)
    check.equal(resp.status, 200)
    check.is_not_none(resp.text())
    check.is_in("Client_Key", resp.text())



def test_client_get_key_200_requests(manage_client_creation_requests):
    id = manage_client_creation_requests()
    resp = requests.get(url=f"{ApiEndpoints.client_url()}/{id}/key")
    check.is_true(resp.ok)
    check.equal(resp.status_code, 200)
    check.is_not_none(resp.text)
    check.is_in("Client_Key", resp.text)



def test_client_get_description_200_playwright(manage_client_creation_playwright):
    api, id = manage_client_creation_playwright()
    resp = api.get(f"/api/v1/client/{id}/description")
    check.is_true(resp.ok)
    check.equal(resp.status, 200)
    check.is_not_none(resp.text())
    check.is_in("Client Description ", resp.text())



def test_client_get_description_200_requests(manage_client_creation_requests):
    id = manage_client_creation_requests()
    resp = requests.get(url=f"{ApiEndpoints.client_url()}/{id}/description")
    check.is_true(resp.ok)
    check.equal(resp.status_code, 200)
    check.is_not_none(resp.text)
    check.is_in("Client Description", resp.text)



def test_client_get_search_200_playwright(manage_client_creation_playwright):
    api, id = manage_client_creation_playwright()
    resp = api.get(f"/api/v1/client/search")
    check.is_true(resp.ok)
    check.equal(resp.status, 200)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.is_instance(resp_json, list)
    check.is_true(any(client['id'] == id for client in resp_json))



def test_client_get_search_200_requests(manage_client_creation_requests):
    id = manage_client_creation_requests()
    resp = requests.get(url=f"{ApiEndpoints.client_url()}/search")
    check.is_true(resp.ok)
    check.equal(resp.status_code, 200)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.is_instance(resp_json, list)
    check.is_true(any(client['id'] == id for client in resp_json))



def test_client_get_404_playwright(manage_client_creation_playwright):
    api, id = manage_client_creation_playwright()
    resp = api.get(f"/api/v1/client/{id+id}")
    check.is_false(resp.ok)
    check.equal(resp.status, 404)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(resp_json['status'], 404)
    check.equal(resp_json['error'], 'Not Found')



def test_client_get_404_requests(manage_client_creation_requests):
    id = manage_client_creation_requests()
    resp = requests.get(url=f"{ApiEndpoints.client_url()}/{id+id}")
    check.is_false(resp.ok)
    check.equal(resp.status_code, 404)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(resp_json['status'], 404)
    check.equal(resp_json['error'], 'Not Found')



def test_client_get_404_requests_session(manage_client_creation_requests_session):
    session, id = manage_client_creation_requests_session()
    resp = session.get(url=f"{ApiEndpoints.client_url()}/{id+id}")
    check.is_false(resp.ok)
    check.equal(resp.status_code, 404)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(resp_json['status'], 404)
    check.equal(resp_json['error'], 'Not Found')




def test_client_post_get_delete_with_null_description_201_playwright(manage_playwright_api_context):
    # post
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
    client_key = resp_json["key"]
    client_id = resp_json['id']
    # get
    resp = api_context.get(f"/api/v1/client/{client_id}")
    check.is_true(resp.ok)
    check.equal(resp.status, 200)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(resp_json['id'], client_id)
    check.equal(resp_json['key'], client_key)
    check.is_none(resp_json["description"])
    # cleanup
    resp = api_context.delete(f"/api/v1/client/{client_id}")
    check.is_true(resp.ok)
    check.equal(resp.status, 204)



def test_client_post_get_delete_with_null_description_201_requests(manage_default_headers):
    # post
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
    client_key = resp_json["key"]
    client_id = resp_json['id']
    # get
    resp = requests.get(url=f"{ApiEndpoints.client_url()}/{client_id}")
    check.is_true(resp.ok)
    check.equal(resp.status_code, 200)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(resp_json['id'], client_id)
    check.equal(resp_json['key'], client_key)
    check.is_none(resp_json["description"])
    # cleanup
    resp = requests.delete(f"{ApiEndpoints.client_url()}/{client_id}")
    check.is_true(resp.ok)
    check.equal(resp.status_code, 204)


