from random import randint
from pytest_check import check
import requests
from config.settings import ApiEndpoints



def test_client_resource_access_patch_200_playwright(manage_client_resource_access_creation_playwright):
    random_num   = randint(0, 999999)
    patch_payload = {
        "accessCode": f"Updated_Client_Resource_Access_AccessCode_{random_num}",
        "description": f"Updated Client Resource Access Description {random_num}",
    }
    api, client_id, resource_id = manage_client_resource_access_creation_playwright()
    resp = api.patch(f"/api/v1/client-resource-access/client/{client_id}/resource/{resource_id}", data=patch_payload)
    check.is_true(resp.ok)
    check.equal(resp.status, 200)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(resp_json['clientId'], client_id)
    check.equal(resp_json['resourceId'], resource_id)
    check.equal(resp_json["accessCode"], patch_payload["accessCode"])
    check.equal(resp_json["description"], patch_payload["description"])



def test_client_resource_access_patch_200_requests(manage_client_resource_access_creation_requests):
    random_num = randint(0, 999999)
    patch_payload = {
        "accessCode": f"Updated_Client_Resource_Access_AccessCode_{random_num}",
        "description": f"Updated Client Resource Access Description {random_num}",
    }
    client_id, resource_id = manage_client_resource_access_creation_requests()
    resp = requests.patch(f"{ApiEndpoints.client_resource_access_url()}/client/{client_id}/resource/{resource_id}", json=patch_payload)
    check.is_true(resp.ok)
    check.equal(resp.status_code, 200)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(resp_json['clientId'], client_id)
    check.equal(resp_json['resourceId'], resource_id)
    check.equal(resp_json["accessCode"], patch_payload["accessCode"])
    check.equal(resp_json["description"], patch_payload["description"])



def test_client_resource_access_patch_invaid_client_404_playwright(manage_client_resource_access_creation_playwright):
    random_num   = randint(0, 999999)
    patch_payload = {
        "accessCode": f"Updated_Client_Resource_Access_AccessCode_{random_num}",
        "description": f"Updated Client Resource Access Description {random_num}",
    }
    api, client_id, resource_id = manage_client_resource_access_creation_playwright()
    resp = api.patch(f"/api/v1/client-resource-access/client/{client_id+client_id}/resource/{resource_id}", data=patch_payload)
    check.is_false(resp.ok)
    check.equal(resp.status, 404)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(resp_json['status'], 404)
    check.equal(resp_json['error'], 'Not Found')



def test_client_resource_access_patch_invalid_resource_404_requests(manage_client_resource_access_creation_requests):
    random_num = randint(0, 999999)
    patch_payload = {
        "accessCode": f"Updated_Client_Resource_Access_AccessCode_{random_num}",
        "description": f"Updated Client Resource Access Description {random_num}",
    }
    client_id, resource_id = manage_client_resource_access_creation_requests()
    resp = requests.patch(f"{ApiEndpoints.client_resource_access_url()}/client/{client_id}/resource/{resource_id+resource_id}", json=patch_payload)
    check.is_false(resp.ok)
    check.equal(resp.status_code, 404)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(resp_json['status'], 404)
    check.equal(resp_json['error'], 'Not Found')




def test_client_resource_access_patch_duplicate_payload_200_playwright(manage_client_resource_access_creation_playwright):
    random_num   = randint(0, 999999)
    patch_payload = {
        "accessCode": f"Updated_Client_Resource_Access_AccessCode_{random_num}",
        "description": f"Updated Client Resource Access Description {random_num}",
    }
    api, client_id, resource_id = manage_client_resource_access_creation_playwright()
    resp = api.patch(f"/api/v1/client-resource-access/client/{client_id}/resource/{resource_id}", data=patch_payload)
    check.is_true(resp.ok)
    check.equal(resp.status, 200)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(resp_json['clientId'], client_id)
    check.equal(resp_json['resourceId'], resource_id)
    check.equal(resp_json["accessCode"], patch_payload["accessCode"])
    check.equal(resp_json["description"], patch_payload["description"])
    # duplicate
    resp = api.patch(f"/api/v1/client-resource-access/client/{client_id}/resource/{resource_id}", data=patch_payload)
    check.is_true(resp.ok)
    check.equal(resp.status, 200)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(resp_json['clientId'], client_id)
    check.equal(resp_json['resourceId'], resource_id)
    check.equal(resp_json["accessCode"], patch_payload["accessCode"])
    check.equal(resp_json["description"], patch_payload["description"])



def test_client_resource_access_patch_duplicate_payload_200_requests(manage_client_resource_access_creation_requests):
    random_num = randint(0, 999999)
    patch_payload = {
        "accessCode": f"Updated_Client_Resource_Access_AccessCode_{random_num}",
        "description": f"Updated Client Resource Access Description {random_num}",
    }
    client_id, resource_id = manage_client_resource_access_creation_requests()
    resp = requests.patch(f"{ApiEndpoints.client_resource_access_url()}/client/{client_id}/resource/{resource_id}", json=patch_payload)
    check.is_true(resp.ok)
    check.equal(resp.status_code, 200)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(resp_json['clientId'], client_id)
    check.equal(resp_json['resourceId'], resource_id)
    check.equal(resp_json["accessCode"], patch_payload["accessCode"])
    check.equal(resp_json["description"], patch_payload["description"])
    # duplicate
    resp = requests.patch(f"{ApiEndpoints.client_resource_access_url()}/client/{client_id}/resource/{resource_id}", json=patch_payload)
    check.is_true(resp.ok)
    check.equal(resp.status_code, 200)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(resp_json['clientId'], client_id)
    check.equal(resp_json['resourceId'], resource_id)
    check.equal(resp_json["accessCode"], patch_payload["accessCode"])
    check.equal(resp_json["description"], patch_payload["description"])

