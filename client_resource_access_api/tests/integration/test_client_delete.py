from config.settings import ApiEndpoints
from pytest_check import check
import requests


def test_client_delete_204_playwright(manage_client_creation_playwright):
    api, id = manage_client_creation_playwright()
    resp = api.delete(f"/api/v1/client/{id}")
    check.is_true(resp.ok)
    check.equal(resp.status, 204)



def test_client_delete_204_requests(manage_client_creation_requests):
    id = manage_client_creation_requests()
    resp = requests.delete(f"{ApiEndpoints.client_url()}/{id}")
    check.is_true(resp.ok)
    check.equal(resp.status_code, 204)



def test_client_delete_204_requests_session(manage_client_creation_requests_session):
    session, id = manage_client_creation_requests_session()
    resp = session.delete(f"{session.base_url}/{id}")
    check.is_true(resp.ok)
    check.equal(resp.status_code, 204)




def test_client_delete_invalid_id_404_playwright(manage_client_creation_playwright):
    api, id = manage_client_creation_playwright()
    resp = api.delete(f"/api/v1/client/{id+id}")
    check.is_false(resp.ok)
    check.equal(resp.status, 404)



def test_client_delete_invalid_id_404_requests(manage_client_creation_requests):
    id = manage_client_creation_requests()
    resp = requests.delete(f"{ApiEndpoints.client_url()}/{id+id}")
    check.is_false(resp.ok)
    check.equal(resp.status_code, 404)



def test_client_delete_invalid_id_404_requests_session(manage_client_creation_requests_session):
    session, id = manage_client_creation_requests_session()
    resp = session.delete(f"{session.base_url}/{id+id}")
    check.is_false(resp.ok)
    check.equal(resp.status_code, 404)



def test_client_delete_unprocessable_422_playwright(manage_client_resource_access_creation_playwright):
    api, client_id, resource_id = manage_client_resource_access_creation_playwright()
    resp = api.delete(f"/api/v1/client/{client_id}")
    check.is_false(resp.ok)
    check.equal(resp.status, 422)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(resp_json["status"], 422)
    check.equal(resp_json["error"], "Unprocessable Content")
    check.equal(resp_json["path"], f"/api/v1/client/{client_id}")



def test_client_delete_unprocessable_422_requests(manage_client_resource_access_creation_requests):
    client_id, resource_id = manage_client_resource_access_creation_requests()
    resp = requests.delete(f"{ApiEndpoints.client_url()}/{client_id}")
    check.is_false(resp.ok)
    check.equal(resp.status_code, 422)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(resp_json["status"], 422)
    check.equal(resp_json["error"], "Unprocessable Content")
    check.equal(resp_json["path"], f"/api/v1/client/{client_id}")
