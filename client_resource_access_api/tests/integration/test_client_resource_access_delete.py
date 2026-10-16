from config.settings import ApiEndpoints
from pytest_check import check
import requests


def test_client_resource_access_delete_204_playwright(manage_client_resource_access_creation_playwright):
    api, client_id, resource_id = manage_client_resource_access_creation_playwright()
    #
    resp = api.delete(f"/api/v1/client-resource-access/client/{client_id}/resource/{resource_id}")
    check.is_true(resp.ok)
    check.equal(resp.status, 204)
    #
    resp = api.delete(f"/api/v1/resource/{resource_id}")
    check.is_true(resp.ok)
    check.equal(resp.status, 204)
    #
    resp = api.delete(f"/api/v1/client/{client_id}")
    check.is_true(resp.ok)
    check.equal(resp.status, 204)



def test_client_resource_access_delete_204_requests(manage_client_resource_access_creation_requests):
    client_id, resource_id = manage_client_resource_access_creation_requests()
    resp = requests.delete(f"{ApiEndpoints.client_resource_access_url()}/client/{client_id}/resource/{resource_id}")
    check.is_true(resp.ok)
    check.equal(resp.status_code, 204)
    #
    resp = requests.delete(f"{ApiEndpoints.resource_url()}/{resource_id}")
    check.is_true(resp.ok)
    check.equal(resp.status_code, 204)
    #
    resp = requests.delete(f"{ApiEndpoints.client_url()}/{client_id}")
    check.is_true(resp.ok)
    check.equal(resp.status_code, 204)




def test_client_resource_access_delete_unprocessable_422_playwright(manage_client_resource_access_creation_playwright):
    api, client_id, resource_id = manage_client_resource_access_creation_playwright()
    #
    resp = api.delete(f"/api/v1/client-resource-access/client/{client_id+client_id}/resource/{resource_id}")
    check.is_false(resp.ok)
    check.equal(resp.status, 404)
    check.is_not_none(resp.text())
    check.is_in('Not Found', resp.text())
    #
    resp = api.delete(f"/api/v1/resource/{resource_id}")
    check.is_false(resp.ok)
    check.equal(resp.status, 422)
    #
    resp = api.delete(f"/api/v1/client/{client_id}")
    check.is_false(resp.ok)
    check.equal(resp.status, 422)



def test_client_resource_access_delete_unprocessable_422_requests(manage_client_resource_access_creation_requests):
    client_id, resource_id = manage_client_resource_access_creation_requests()
    resp = requests.delete(f"{ApiEndpoints.client_resource_access_url()}/client/{client_id}/resource/{resource_id+resource_id}")
    check.is_false(resp.ok)
    check.equal(resp.status_code, 404)
    #
    resp = requests.delete(f"{ApiEndpoints.resource_url()}/{resource_id}")
    check.is_false(resp.ok)
    check.equal(resp.status_code, 422)
    #
    resp = requests.delete(f"{ApiEndpoints.client_url()}/{client_id}")
    check.is_false(resp.ok)
    check.equal(resp.status_code, 422)

