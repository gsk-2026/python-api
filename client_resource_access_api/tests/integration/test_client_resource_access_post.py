from random import randint
from config.settings import ApiEndpoints
from pytest_check import check
import requests



def test_client_resource_access_post_201_playwright(manage_playwright_api_context):
    api_context = manage_playwright_api_context(base_url=ApiEndpoints.base_url())
    random_num = randint(0, 999999)
    #
    client_payload = {
        "key": f"Client_Key_{random_num:06d}",
        "secret": f"Client_Secret_{random_num:06d}",
        "description": f"Client Description {random_num:06d}",
    }
    resp = api_context.post("/api/v1/client", data=client_payload)
    check.equal(resp.status, 201)
    client_id = resp.json()['id']
    #
    resource_payload = {
        "key": f"Key_Resource_{random_num:06d}",
        "type": f"Type_Resource_{random_num:06d}",
        "description": f"Description Resource  {random_num:06d}",
    }
    resp = api_context.post("/api/v1/resource", data=resource_payload)
    check.equal(resp.status, 201)
    resource_id = resp.json()['id']
    #
    payload = {
        "clientId": f"{client_id}",
        "resourceId": f"{resource_id}",
        "accessCode": f"Access_Code_{random_num:06d}",
        "description": f"Client resource Access Description {random_num:06d}",
    }
    resp = api_context.post("/api/v1/client-resource-access", data=payload)
    check.is_true(resp.ok)
    check.equal(resp.status, 201)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(str(resp_json['clientId']), f"{payload['clientId']}")
    check.equal(str(resp_json['resourceId']), f"{payload['resourceId']}")
    check.equal(resp_json['accessCode'], f"{payload['accessCode']}")
    check.equal(resp_json['description'], f"{payload['description']}")
    #cleanup
    resp = api_context.delete(f"/api/v1/client-resource-access/client/{client_id}/resource/{resource_id}")
    check.is_true(resp.ok)
    check.equal(resp.status, 204)
    resp = api_context.delete(f"/api/v1/resource/{resource_id}")
    check.is_true(resp.ok)
    check.equal(resp.status, 204)
    resp = api_context.delete(f"/api/v1/client/{client_id}")
    check.is_true(resp.ok)
    check.equal(resp.status, 204)




def test_client_resource_access_post_201_requests(manage_default_headers):
    dft_headers = manage_default_headers
    random_num = randint(0, 999999)
    #
    client_payload = {
        "key": f"Client_Key_{random_num:06d}",
        "secret": f"Client_Secret_{random_num:06d}",
        "description": f"Client Description {random_num:06d}",
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
        "description": f"Description Resource  {random_num:06d}",
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
        "description": f"Client resource Access Description {random_num:06d}",
    }
    resp = requests.post(ApiEndpoints.client_resource_access_url(),headers=dft_headers, json=payload)
    check.is_true(resp.ok)
    check.equal(resp.status_code, 201)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(str(resp_json['clientId']), f"{payload['clientId']}")
    check.equal(str(resp_json['resourceId']), f"{payload['resourceId']}")
    check.equal(resp_json['accessCode'], f"{payload['accessCode']}")
    check.equal(resp_json['description'], f"{payload['description']}")
    #cleanup
    resp = requests.delete(f"{ApiEndpoints.client_resource_access_url()}/client/{client_id}/resource/{resource_id}")
    check.is_true(resp.ok)
    check.equal(resp.status_code, 204)
    resp = requests.delete(f"{ApiEndpoints.resource_url()}/{resource_id}")
    check.is_true(resp.ok)
    check.equal(resp.status_code, 204)
    resp = requests.delete(f"{ApiEndpoints.client_url()}/{client_id}")
    check.is_true(resp.ok)
    check.equal(resp.status_code, 204)



def test_client_resource_access_post_duplicate_payload_409_playwright(manage_playwright_api_context):
    api_context = manage_playwright_api_context(base_url=ApiEndpoints.base_url())
    random_num = randint(0, 999999)
    #
    client_payload = {
        "key": f"Client_Key_{random_num:06d}",
        "secret": f"Client_Secret_{random_num:06d}",
        "description": f"Client Description {random_num:06d}",
    }
    resp = api_context.post("/api/v1/client", data=client_payload)
    check.equal(resp.status, 201)
    client_id = resp.json()['id']
    #
    resource_payload = {
        "key": f"Key_Resource_{random_num:06d}",
        "type": f"Type_Resource_{random_num:06d}",
        "description": f"Description Resource  {random_num:06d}",
    }
    resp = api_context.post("/api/v1/resource", data=resource_payload)
    check.equal(resp.status, 201)
    resource_id = resp.json()['id']
    #
    payload = {
        "clientId": f"{client_id}",
        "resourceId": f"{resource_id}",
        "accessCode": f"Access_Code_{random_num:06d}",
        "description": f"Client resource Access Description {random_num:06d}",
    }
    resp = api_context.post("/api/v1/client-resource-access", data=payload)
    check.is_true(resp.ok)
    check.equal(resp.status, 201)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(str(resp_json['clientId']), f"{payload['clientId']}")
    check.equal(str(resp_json['resourceId']), f"{payload['resourceId']}")
    check.equal(resp_json['accessCode'], f"{payload['accessCode']}")
    check.equal(resp_json['description'], f"{payload['description']}")
    # duplicate
    resp = api_context.post("/api/v1/client-resource-access", data=payload)
    check.is_false(resp.ok)
    check.equal(resp.status, 409)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(resp_json["status"], 409)
    check.equal(resp_json["error"], "Conflict")
    #cleanup
    resp = api_context.delete(f"/api/v1/client-resource-access/client/{client_id}/resource/{resource_id}")
    check.is_true(resp.ok)
    check.equal(resp.status, 204)
    resp = api_context.delete(f"/api/v1/resource/{resource_id}")
    check.is_true(resp.ok)
    check.equal(resp.status, 204)
    resp = api_context.delete(f"/api/v1/client/{client_id}")
    check.is_true(resp.ok)
    check.equal(resp.status, 204)




def test_client_resource_access_post_duplicate_payload_409_requests(manage_default_headers):
    dft_headers = manage_default_headers
    random_num = randint(0, 999999)
    #
    client_payload = {
        "key": f"Client_Key_{random_num:06d}",
        "secret": f"Client_Secret_{random_num:06d}",
        "description": f"Client Description {random_num:06d}",
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
        "description": f"Description Resource  {random_num:06d}",
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
        "description": f"Client resource Access Description {random_num:06d}",
    }
    resp = requests.post(ApiEndpoints.client_resource_access_url(),headers=dft_headers, json=payload)
    check.is_true(resp.ok)
    check.equal(resp.status_code, 201)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(str(resp_json['clientId']), f"{payload['clientId']}")
    check.equal(str(resp_json['resourceId']), f"{payload['resourceId']}")
    check.equal(resp_json['accessCode'], f"{payload['accessCode']}")
    check.equal(resp_json['description'], f"{payload['description']}")
    # duplicate
    resp = requests.post(ApiEndpoints.client_resource_access_url(),headers=dft_headers, json=payload)
    check.is_false(resp.ok)
    check.equal(resp.status_code, 409)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(resp_json["status"], 409)
    check.equal(resp_json["error"], "Conflict")
    #cleanup
    resp = requests.delete(f"{ApiEndpoints.client_resource_access_url()}/client/{client_id}/resource/{resource_id}")
    check.is_true(resp.ok)
    check.equal(resp.status_code, 204)
    resp = requests.delete(f"{ApiEndpoints.resource_url()}/{resource_id}")
    check.is_true(resp.ok)
    check.equal(resp.status_code, 204)
    resp = requests.delete(f"{ApiEndpoints.client_url()}/{client_id}")
    check.is_true(resp.ok)
    check.equal(resp.status_code, 204)

