from random import randint

import requests
from pytest_check import check
from config.settings import ApiEndpoints



def test_resource_get_200_playwright(manage_resource_creation_playwright):
    api, id = manage_resource_creation_playwright()
    resp = api.get(f"/api/v1/resource/{id}")
    check.is_true(resp.ok)
    check.equal(resp.status, 200)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(resp_json['id'], id)
    check.is_not_none(resp_json['key'])
    check.is_not_none(resp_json['createdAt'])



def test_resource_get_200_requests(manage_resource_creation_requests):
    id = manage_resource_creation_requests()
    resp = requests.get(url=f"{ApiEndpoints.resource_url()}/{id}")
    check.is_true(resp.ok)
    check.equal(resp.status_code, 200)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(resp_json['id'], id)
    check.is_not_none(resp_json['key'])
    check.is_not_none(resp_json['createdAt'])



def test_resource_get_key_200_playwright(manage_resource_creation_playwright):
    api, id = manage_resource_creation_playwright()
    resp = api.get(f"/api/v1/resource/{id}/key")
    check.is_true(resp.ok)
    check.equal(resp.status, 200)
    check.is_not_none(resp.text())
    check.is_in("Resource_Key", resp.text())



def test_resource_get_key_200_requests(manage_resource_creation_requests):
    id = manage_resource_creation_requests()
    resp = requests.get(url=f"{ApiEndpoints.resource_url()}/{id}/key")
    check.is_true(resp.ok)
    check.equal(resp.status_code, 200)
    check.is_not_none(resp.text)
    check.is_in("Resource_Key", resp.text)



def test_resource_get_type_200_playwright(manage_resource_creation_playwright):
    api, id = manage_resource_creation_playwright()
    resp = api.get(f"/api/v1/resource/{id}/type")
    check.is_true(resp.ok)
    check.equal(resp.status, 200)
    check.is_not_none(resp.text())
    check.is_in("Resource_Type", resp.text())



def test_resource_get_type_200_requests(manage_resource_creation_requests):
    id = manage_resource_creation_requests()
    resp = requests.get(url=f"{ApiEndpoints.resource_url()}/{id}/type")
    check.is_true(resp.ok)
    check.equal(resp.status_code, 200)
    check.is_not_none(resp.text)
    check.is_in("Resource_Type", resp.text)



def test_resource_get_description_200_playwright(manage_resource_creation_playwright):
    api, id = manage_resource_creation_playwright()
    resp = api.get(f"/api/v1/resource/{id}/description")
    check.is_true(resp.ok)
    check.equal(resp.status, 200)
    check.is_not_none(resp.text())
    check.is_in("Resource Description", resp.text())



def test_resource_get_description_200_requests(manage_resource_creation_requests):
    id = manage_resource_creation_requests()
    resp = requests.get(url=f"{ApiEndpoints.resource_url()}/{id}/description")
    check.is_true(resp.ok)
    check.equal(resp.status_code, 200)
    check.is_not_none(resp.text)
    check.is_in("Resource Description", resp.text)



def test_resource_get_search_200_playwright(manage_resource_creation_playwright):
    api, id = manage_resource_creation_playwright()
    resp = api.get(f"/api/v1/resource/search")
    check.is_true(resp.ok)
    check.equal(resp.status, 200)
    check.is_not_none(resp.json())
    check.is_instance(resp.json(), list)
    check.is_true(any(resource['id'] == id for resource in resp.json()))



def test_resource_get_search_200_requests(manage_resource_creation_requests):
    id = manage_resource_creation_requests()
    resp = requests.get(url=f"{ApiEndpoints.resource_url()}/search")
    check.is_true(resp.ok)
    check.equal(resp.status_code, 200)
    check.is_not_none(resp.json())
    check.is_instance(resp.json(), list)
    check.is_true(any(resource['id'] == id for resource in resp.json()))



def test_resource_get_invalid_id_404_playwright(manage_resource_creation_playwright):
    api, id = manage_resource_creation_playwright()
    resp = api.get(f"/api/v1/resource/{id+id}")
    check.is_false(resp.ok)
    check.equal(resp.status, 404)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(resp_json['status'],404)
    check.equal(resp_json['error'], "Not Found")



def test_resource_get_invalid_id_404_requests(manage_resource_creation_requests):
    id = manage_resource_creation_requests()
    resp = requests.get(url=f"{ApiEndpoints.resource_url()}/{id+id}")
    check.is_false(resp.ok)
    check.equal(resp.status_code, 404)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(resp_json['status'],404)
    check.equal(resp_json['error'], "Not Found")




def test_resource_post_get_delete_with_null_description_201_playwright(manage_playwright_api_context):
    # post
    resource_no = randint(0, 999999)
    resource_payload = {
        "key": f"Key_Resource_Item_{resource_no:06d}",
        "type": f"Type_Resource_Item_{resource_no:06d}",
    }
    api_context = manage_playwright_api_context(base_url=ApiEndpoints.base_url())
    resp = api_context.post("/api/v1/resource", data=resource_payload)
    check.equal(resp.status, 201)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(resp_json["key"], resource_payload["key"])
    check.equal(resp_json["type"], resource_payload["type"])
    check.is_none(resp_json["description"])
    check.greater(resp_json['id'], 0)
    check.is_not_none(resp_json['createdAt'])
    check.is_not_none(resp_json['updatedAt'])
    resource_id = resp_json['id']
    # get
    resp = api_context.get(f"/api/v1/resource/{resource_id}")
    check.is_true(resp.ok)
    check.equal(resp.status, 200)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(resp_json['id'], resource_id)
    check.equal(resp_json["key"], resource_payload["key"])
    check.equal(resp_json["type"], resource_payload["type"])
    check.is_none(resp_json["description"])
    check.is_not_none(resp_json['createdAt'])
    # cleanup
    resp = api_context.delete(f"/api/v1/resource/{resource_id}")
    check.is_true(resp.ok)
    check.equal(resp.status, 204)



def test_resource_post_get_delete_with_null_description_201_requests(manage_default_headers):
    # post
    resource_no = randint(0, 999999)
    resource_payload = {
        "key": f"Key_Resource_Item_{resource_no:06d}",
        "type": f"Type_Resource_Item_{resource_no:06d}",
    }
    resp = requests.post(ApiEndpoints.resource_url(), headers=manage_default_headers, json=resource_payload)
    check.is_true(resp.ok)
    check.equal(resp.status_code, 201)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.greater(resp_json['id'], 0)
    check.equal(resp_json["key"], resource_payload["key"])
    check.equal(resp_json["type"], resource_payload["type"])
    check.is_none(resp_json["description"])
    check.is_not_none(resp_json['createdAt'])
    check.is_not_none(resp_json['updatedAt'])
    resource_id = resp_json['id']
    # get
    resp = requests.get(url=f"{ApiEndpoints.resource_url()}/{resource_id}")
    check.is_true(resp.ok)
    check.equal(resp.status_code, 200)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(resp_json['id'], resource_id)
    check.equal(resp_json["key"], resource_payload["key"])
    check.equal(resp_json["type"], resource_payload["type"])
    check.is_none(resp_json["description"])
    check.is_not_none(resp_json['createdAt'])
    # cleanup
    resp = requests.delete(f"{ApiEndpoints.resource_url()}/{resource_id}")
    check.is_true(resp.ok)
    check.equal(resp.status_code, 204)



