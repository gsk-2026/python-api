from pytest_check import check
from config.settings import ApiEndpoints
import requests



def test_resource_delete_204_playwright(manage_resource_creation_playwright):
    api, id = manage_resource_creation_playwright()
    resp = api.delete(f"/api/v1/resource/{id}")
    check.is_true(resp.ok)
    check.equal(resp.status, 204)
    check.equal(resp.text(), '')



def test_resource_delete_204_requests(manage_resource_creation_requests):
    id = manage_resource_creation_requests()
    resp = requests.delete(f"{ApiEndpoints.resource_url()}/{id}")
    check.is_true(resp.ok)
    check.equal(resp.status_code, 204)
    check.equal(resp.text, '')



def test_resource_delete_duplicate_204_404_playwright(manage_resource_creation_playwright):
    api, id = manage_resource_creation_playwright()
    resp = api.delete(f"/api/v1/resource/{id}")
    check.is_true(resp.ok)
    check.equal(resp.status, 204)
    check.equal(resp.text(), '')
    # duplicate
    resp = api.delete(f"/api/v1/resource/{id}")
    check.is_false(resp.ok)
    check.equal(resp.status, 404)
    check.is_not_none(resp.json())
    check.equal(resp.json()['status'], 404)
    check.equal(resp.json()['error'], 'Not Found')



def test_resource_delete_duplicate_204_404_requests(manage_resource_creation_requests):
    id = manage_resource_creation_requests()
    resp = requests.delete(f"{ApiEndpoints.resource_url()}/{id}")
    check.is_true(resp.ok)
    check.equal(resp.status_code, 204)
    check.equal(resp.text, '')
    # duplicate
    resp = requests.delete(f"{ApiEndpoints.resource_url()}/{id}")
    check.is_false(resp.ok)
    check.equal(resp.status_code, 404)
    check.is_not_none(resp.json())
    check.equal(resp.json()['status'], 404)
    check.equal(resp.json()['error'], 'Not Found')



def test_resource_delete_invalid_id_404_playwright(manage_resource_creation_playwright):
    api, id = manage_resource_creation_playwright()
    resp = api.delete(f"/api/v1/resource/{id+id}")
    check.is_false(resp.ok)
    check.equal(resp.status, 404)
    check.is_not_none(resp.json())
    check.equal(resp.json()['status'], 404)
    check.equal(resp.json()['error'], 'Not Found')



def test_resource_delete_invalid_id_404_requests(manage_resource_creation_requests):
    id = manage_resource_creation_requests()
    resp = requests.delete(f"{ApiEndpoints.resource_url()}/{id+id}")
    check.is_false(resp.ok)
    check.equal(resp.status_code, 404)
    check.is_not_none(resp.json())
    check.equal(resp.json()['status'], 404)
    check.equal(resp.json()['error'], 'Not Found')



def test_resource_delete_unprocessable_422_playwright(manage_client_resource_access_creation_playwright):
    api, client_id, resource_id = manage_client_resource_access_creation_playwright()
    resp = api.delete(f"/api/v1/resource/{resource_id}")
    check.is_false(resp.ok)
    check.equal(resp.status, 422)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(resp_json["status"], 422)
    check.equal(resp_json["error"], "Unprocessable Content")
    check.equal(resp_json["path"], f"/api/v1/resource/{resource_id}")



def test_resource_delete_unprocessable_422_requests(manage_client_resource_access_creation_requests):
    client_id, resource_id = manage_client_resource_access_creation_requests()
    resp = requests.delete(f"{ApiEndpoints.resource_url()}/{resource_id}")
    check.is_false(resp.ok)
    check.equal(resp.status_code, 422)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(resp_json["status"], 422)
    check.equal(resp_json["error"], "Unprocessable Content")
    check.equal(resp_json["path"], f"/api/v1/resource/{resource_id}")
