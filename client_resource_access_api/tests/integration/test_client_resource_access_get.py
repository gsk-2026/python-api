from random import randint

from config.settings import ApiEndpoints
from pytest_check import check
import requests



def test_client_resource_access_get_by_id_200_playwright(manage_client_resource_access_creation_playwright):
    api, client_id, resource_id = manage_client_resource_access_creation_playwright()
    resp = api.get(f"/api/v1/client-resource-access/client/{client_id}/resource/{resource_id}")
    check.is_true(resp.ok)
    check.equal(resp.status, 200)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.is_true(isinstance(resp_json, dict))
    check.equal(resp_json['clientId'], client_id)
    check.equal(resp_json['resourceId'], resource_id)



def test_client_resource_access_get_by_id_200_requests(manage_client_resource_access_creation_requests):
    client_id, resource_id = manage_client_resource_access_creation_requests()
    resp = requests.get(f"{ApiEndpoints.client_resource_access_url()}/client/{client_id}/resource/{resource_id}")
    check.is_true(resp.ok)
    check.equal(resp.status_code, 200)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.is_true(isinstance(resp_json, dict))
    check.equal(resp_json['clientId'], client_id)
    check.equal(resp_json['resourceId'], resource_id)



def test_client_resource_access_get_access_code_200_playwright(manage_client_resource_access_creation_playwright):
    api, client_id, resource_id = manage_client_resource_access_creation_playwright()
    resp = api.get(f"/api/v1/client-resource-access/client/{client_id}/resource/{resource_id}/access-code")
    check.is_true(resp.ok)
    check.equal(resp.status, 200)
    check.is_not_none(resp.text())
    check.is_in('Access_Code_', resp.text())



def test_client_resource_access_get_access_code_200_requests(manage_client_resource_access_creation_requests):
    client_id, resource_id = manage_client_resource_access_creation_requests()
    resp = requests.get(f"{ApiEndpoints.client_resource_access_url()}/client/{client_id}/resource/{resource_id}/access-code")
    check.is_true(resp.ok)
    check.equal(resp.status_code, 200)
    check.is_not_none(resp.text)
    check.is_in('Access_Code_', resp.text)



def test_client_resource_access_get_description_200_playwright(manage_client_resource_access_creation_playwright):
    api, client_id, resource_id = manage_client_resource_access_creation_playwright()
    resp = api.get(f"/api/v1/client-resource-access/client/{client_id}/resource/{resource_id}/description")
    check.is_true(resp.ok)
    check.equal(resp.status, 200)
    check.is_not_none(resp.text())
    check.is_in('Client Resource Access Description', resp.text())



def test_client_resource_access_get_description_200_requests(manage_client_resource_access_creation_requests):
    client_id, resource_id = manage_client_resource_access_creation_requests()
    resp = requests.get(f"{ApiEndpoints.client_resource_access_url()}/client/{client_id}/resource/{resource_id}/description")
    check.is_true(resp.ok)
    check.equal(resp.status_code, 200)
    check.is_not_none(resp.text)
    check.is_in('Client Resource Access Description', resp.text)



def test_client_resource_access_get_search_200_playwright(manage_client_resource_access_creation_playwright):
    api, client_id, resource_id = manage_client_resource_access_creation_playwright()
    resp = api.get(f"/api/v1/client-resource-access/search")
    check.is_true(resp.ok)
    check.equal(resp.status, 200)
    check.is_not_none(resp.json())
    check.is_instance(resp.json(), list)
    check.greater_equal(len(resp.json()), 1)
    check.is_true(any(item['clientId'] == client_id and item['resourceId'] == resource_id for item in resp.json()))



def test_client_resource_access_get_search_200_requests(manage_client_resource_access_creation_requests):
    client_id_1, resource_id_1 = manage_client_resource_access_creation_requests()
    client_id_2, resource_id_2 = manage_client_resource_access_creation_requests()
    resp = requests.get(f"{ApiEndpoints.client_resource_access_url()}/search")
    check.is_true(resp.ok)
    check.equal(resp.status_code, 200)
    check.is_not_none(resp.json())
    check.is_instance(resp.json(), list)
    check.greater_equal(len(resp.json()), 2)
    check.is_true(any(item['clientId'] == client_id_1 and item['resourceId'] == resource_id_1 for item in resp.json()))
    check.is_true(any(item['clientId'] == client_id_2 and item['resourceId'] == resource_id_2 for item in resp.json()))




def test_client_resource_access_get_invalid_client_id_404_playwright(manage_client_resource_access_creation_playwright):
    api, client_id, resource_id = manage_client_resource_access_creation_playwright()
    resp = api.get(f"/api/v1/client-resource-access/client/{client_id+client_id}/resource/{resource_id}")
    check.is_false(resp.ok)
    check.equal(resp.status, 404)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.is_true(isinstance(resp_json, dict))
    check.equal(resp_json['status'], 404)
    check.equal(resp_json['error'], 'Not Found')



def test_client_resource_access_get_invalid_resource_id_404_requests(manage_client_resource_access_creation_requests):
    client_id, resource_id = manage_client_resource_access_creation_requests()
    resp = requests.get(f"{ApiEndpoints.client_resource_access_url()}/client/{client_id}/resource/{resource_id+resource_id}")
    check.is_false(resp.ok)
    check.equal(resp.status_code, 404)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.is_true(isinstance(resp_json, dict))
    check.equal(resp_json['status'], 404)
    check.equal(resp_json['error'], 'Not Found')




def test_client_resource_access_get_delete_with_null_description_201_playwright(manage_playwright_api_context):
    api_context = manage_playwright_api_context(base_url=ApiEndpoints.base_url())
    random_num = randint(0, 999999)
    # post
    client_payload = {
        "key": f"Client_Key_{random_num:06d}",
        "secret": f"Client_Secret_{random_num:06d}",
    }
    resp = api_context.post("/api/v1/client", data=client_payload)
    check.equal(resp.status, 201)
    client_id = resp.json()['id']
    #
    resource_payload = {
        "key": f"Resource_Key_{random_num:06d}",
        "type": f"Resource_Type_{random_num:06d}",
    }
    resp = api_context.post("/api/v1/resource", data=resource_payload)
    check.equal(resp.status, 201)
    resource_id = resp.json()['id']
    #
    payload = {
        "clientId": f"{client_id}",
        "resourceId": f"{resource_id}",
        "accessCode": f"Access_Code_{random_num:06d}",
    }
    resp = api_context.post("/api/v1/client-resource-access", data=payload)
    check.is_true(resp.ok)
    check.equal(resp.status, 201)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(str(resp_json['clientId']), f"{payload['clientId']}")
    check.equal(str(resp_json['resourceId']), f"{payload['resourceId']}")
    check.equal(resp_json['accessCode'], f"{payload['accessCode']}")
    check.is_none(resp_json['description'])
    # get
    resp = api_context.get(f"/api/v1/client-resource-access/client/{client_id}/resource/{resource_id}")
    check.is_true(resp.ok)
    check.equal(resp.status, 200)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(str(resp_json['clientId']), f"{client_id}")
    check.equal(str(resp_json['resourceId']), f"{resource_id}")
    check.equal(resp_json['accessCode'], f"{payload['accessCode']}")
    check.is_none(resp_json['description'])
    # cleanup
    resp = api_context.delete(f"/api/v1/client-resource-access/client/{client_id}/resource/{resource_id}")
    check.is_true(resp.ok)
    check.equal(resp.status, 204)
    resp = api_context.delete(f"/api/v1/resource/{resource_id}")
    check.is_true(resp.ok)
    check.equal(resp.status, 204)
    resp = api_context.delete(f"/api/v1/client/{client_id}")
    check.is_true(resp.ok)
    check.equal(resp.status, 204)




def test_client_resource_access_post_get_delete_with_null_description_201_requests(manage_default_headers):
    dft_headers = manage_default_headers
    random_num = randint(0, 999999)
    # post
    client_payload = {
        "key": f"Client_Key_{random_num:06d}",
        "secret": f"Client_Secret_{random_num:06d}",
    }
    resp = requests.post(ApiEndpoints.client_url(), headers=dft_headers, json=client_payload)
    check.is_true(resp.ok)
    check.equal(resp.status_code, 201)
    check.is_not_none(resp.json())
    client_id = resp.json()['id']
    #
    resource_payload = {
        "key": f"Key_Resource_{random_num:06d}",
        "type": f"Type_Resource_{random_num:06d}",
    }
    resp = requests.post(ApiEndpoints.resource_url(), headers=dft_headers, json=resource_payload)
    check.is_true(resp.ok)
    check.equal(resp.status_code, 201)
    check.is_not_none(resp.json())
    resource_id = resp.json()['id']
    #
    payload = {
        "clientId": f"{client_id}",
        "resourceId": f"{resource_id}",
        "accessCode": f"Access_Code_{random_num:06d}",
    }
    resp = requests.post(ApiEndpoints.client_resource_access_url(),headers=dft_headers, json=payload)
    check.is_true(resp.ok)
    check.equal(resp.status_code, 201)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(str(resp_json['clientId']), f"{client_id}")
    check.equal(str(resp_json['resourceId']), f"{resource_id}")
    check.equal(resp_json['accessCode'], f"{payload['accessCode']}")
    check.is_none(resp_json['description'])
    # get
    resp = requests.get(f"{ApiEndpoints.client_resource_access_url()}/client/{client_id}/resource/{resource_id}")
    check.is_true(resp.ok)
    check.equal(resp.status_code, 200)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.is_true(isinstance(resp_json, dict))
    check.equal(resp_json['clientId'], client_id)
    check.equal(resp_json['resourceId'], resource_id)
    check.equal(resp_json['accessCode'], f"{payload['accessCode']}")
    check.is_none(resp_json['description'])
    # cleanup
    resp = requests.delete(f"{ApiEndpoints.client_resource_access_url()}/client/{client_id}/resource/{resource_id}")
    check.is_true(resp.ok)
    check.equal(resp.status_code, 204)
    resp = requests.delete(f"{ApiEndpoints.resource_url()}/{resource_id}")
    check.is_true(resp.ok)
    check.equal(resp.status_code, 204)
    resp = requests.delete(f"{ApiEndpoints.client_url()}/{client_id}")
    check.is_true(resp.ok)
    check.equal(resp.status_code, 204)


