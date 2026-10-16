from pytest_check import check
from random import randint
from config.settings import ApiEndpoints
import requests



def test_resource_patch_200_playwright(manage_resource_creation_playwright):
    resource_no = randint(0, 999999)
    patch_payload = {
        "key": f"KEY_RESOURCE_APP_UPDATED {resource_no}",
        "type": f"TYPE_RESOURCE_APP_UPDATED {resource_no}",
        "description": f"UPDATED Mobile App Resource {resource_no}",
    }
    api, id = manage_resource_creation_playwright()
    resp = api.patch(f"/api/v1/resource/{id}", data=patch_payload)
    check.is_true(resp.ok)
    check.equal(resp.status, 200)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(resp_json['id'], id)
    check.equal(resp_json["key"], patch_payload["key"])
    check.equal(resp_json["description"], patch_payload["description"])



def test_resource_patch_200_requests(manage_resource_creation_requests):
    resource_no = randint(0, 999999)
    patch_payload = {
        "key": f"KEY_RESOURCE_APP_UPDATED {resource_no}",
        "type": f"TYPE_RESOURCE_APP_UPDATED {resource_no}",
        "description": f"UPDATED Mobile App Resource {resource_no}",
    }
    id = manage_resource_creation_requests()
    resp = requests.patch(f"{ApiEndpoints.resource_url()}/{id}", json=patch_payload)
    check.is_true(resp.ok)
    check.equal(resp.status_code, 200)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(resp_json['id'], id)
    check.equal(resp_json["key"], patch_payload["key"])
    check.equal(resp_json["type"], patch_payload["type"])
    check.equal(resp_json["description"], patch_payload["description"])




def test_resource_patch_duplicate_key_409_playwright(manage_resource_creation_playwright):
    # first
    resource_no = randint(0, 999999)
    key_duplicate = f"KEY_RESOURCE_{resource_no}"
    patch_payload = {
        "key": f"{key_duplicate}",
        "type": f"TYPE_RESOURCE_APP_UPDATED {resource_no}-A",
        "description": f"UPDATED Mobile App Resource {resource_no}-A",
    }
    api_1, id_1 = manage_resource_creation_playwright()
    resp = api_1.patch(f"/api/v1/resource/{id_1}", data=patch_payload)
    check.is_true(resp.ok)
    check.equal(resp.status, 200)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(resp_json['id'], id_1)
    check.equal(resp_json["key"], patch_payload["key"])
    check.equal(resp_json["description"], patch_payload["description"])
    # second
    patch_payload = {
        "key": f"{key_duplicate}",
        "type": f"TYPE_RESOURCE_APP_UPDATED {resource_no}-B",
        "description": f"UPDATED Mobile App Resource {resource_no}-B",
    }
    api_2, id_2 = manage_resource_creation_playwright()
    resp = api_2.patch(f"/api/v1/resource/{id_2}", data=patch_payload)
    check.is_false(resp.ok)
    check.equal(resp.status, 409)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(resp_json['status'], 409)
    check.equal(resp_json["error"], "Conflict")
    check.equal(resp_json["path"], f"/api/v1/resource/{id_2}")



def test_resource_patch_duplicate_key_409_requests(manage_resource_creation_requests):
    resource_no = randint(0, 999999)
    key_duplicate = f"KEY_RESOURCE_{resource_no}"
    patch_payload = {
        "key": f"{key_duplicate}",
        "type": f"TYPE_RESOURCE_APP_UPDATED {resource_no}-A",
        "description": f"UPDATED Mobile App Resource {resource_no}-A",
    }
    id_1 = manage_resource_creation_requests()
    resp = requests.patch(f"{ApiEndpoints.resource_url()}/{id_1}", json=patch_payload)
    check.is_true(resp.ok)
    check.equal(resp.status_code, 200)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(resp_json['id'], id_1)
    check.equal(resp_json["key"], patch_payload["key"])
    check.equal(resp_json["type"], patch_payload["type"])
    check.equal(resp_json["description"], patch_payload["description"])
    # second resource
    patch_payload = {
        "key": f"{key_duplicate}",
        "type": f"TYPE_RESOURCE_APP_UPDATED {resource_no}-B",
        "description": f"UPDATED Mobile App Resource {resource_no}-B",
    }
    id_2 = manage_resource_creation_requests()
    resp = requests.patch(f"{ApiEndpoints.resource_url()}/{id_2}", json=patch_payload)
    check.is_false(resp.ok)
    check.equal(resp.status_code, 409)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(resp_json['status'], 409)
    check.equal(resp_json["error"], "Conflict")
    check.equal(resp_json["path"], f"/api/v1/resource/{id_2}")




def test_resource_patch_no_key_200_playwright(manage_resource_creation_playwright):
    resource_no = randint(0, 999999)
    patch_payload = {
        "description": f"Updated Mobile App Resource {resource_no}",
    }
    api, id = manage_resource_creation_playwright()
    resp = api.patch(f"/api/v1/resource/{id}", data=patch_payload)
    check.is_true(resp.ok)
    check.equal(resp.status, 200)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(resp_json['id'], id)
    check.equal(resp_json["description"], patch_payload["description"])
    check.is_not_none(resp_json["key"])



def test_resource_patch_no_key_200_requests(manage_resource_creation_requests):
    resource_no = randint(0, 999999)
    patch_payload = {
        "description": f"Updated Mobile App Resource {resource_no}",
    }
    id = manage_resource_creation_requests()
    resp = requests.patch(f"{ApiEndpoints.resource_url()}/{id}", json=patch_payload)
    check.is_true(resp.ok)
    check.equal(resp.status_code, 200)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(resp_json['id'], id)
    check.equal(resp_json["description"], patch_payload["description"])
    check.is_not_none(resp_json["key"])


def test_resource_patch_no_description_200_playwright(manage_resource_creation_playwright):
    resource_no = randint(0, 999999)
    patch_payload = {
        "key": f"RESOURCE_APP_UPDATED {resource_no}",
    }
    api, id = manage_resource_creation_playwright()
    resp = api.patch(f"/api/v1/resource/{id}", data=patch_payload)
    check.is_true(resp.ok)
    check.equal(resp.status, 200)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(resp_json['id'], id)
    check.equal(resp_json["key"], patch_payload["key"])



def test_resource_patch_no_description_200_requests(manage_resource_creation_requests):
    resource_no = randint(0, 999999)
    patch_payload = {
        "key": f"RESOURCE_APP_UPDATED {resource_no}",
    }
    id = manage_resource_creation_requests()
    resp = requests.patch(f"{ApiEndpoints.resource_url()}/{id}", json=patch_payload)
    check.is_true(resp.ok)
    check.equal(resp.status_code, 200)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(resp_json['id'], id)
    check.equal(resp_json["key"], patch_payload["key"])



def test_resource_patch_no_payload_200_playwright(manage_resource_creation_playwright):
    api, id = manage_resource_creation_playwright()
    resp = api.patch(f"/api/v1/resource/{id}", data={})
    check.is_true(resp.ok)
    check.equal(resp.status, 200)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(resp_json['id'], id)
    check.is_not_none(resp_json["key"])



def test_resource_patch_no_payload_200_requests(manage_resource_creation_requests):
    id = manage_resource_creation_requests()
    resp = requests.patch(f"{ApiEndpoints.resource_url()}/{id}", json={})
    check.is_true(resp.ok)
    check.equal(resp.status_code, 200)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(resp_json['id'], id)
    check.is_not_none(resp_json["key"])



def test_resource_patch_invalid_id_404_playwright(manage_resource_creation_playwright):
    resource_no = randint(0, 999999)
    patch_payload = {
        "key": f"RESOURCE_APP_UPDATED {resource_no}",
        "description": f"Updated Mobile App Resource {resource_no}",
    }
    api, id = manage_resource_creation_playwright()
    resp = api.patch(f"/api/v1/resource/{id+id}", data=patch_payload)
    check.is_false(resp.ok)
    check.equal(resp.status, 404)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(resp_json['status'], 404)
    check.equal(resp_json["error"], 'Not Found')


def test_resource_patch_invalid_id_404_requests(manage_resource_creation_requests):
    resource_no = randint(0, 999999)
    patch_payload = {
        "key": f"RESOURCE_APP_UPDATED {resource_no}",
        "description": f"Updated Mobile App Resource {resource_no}",
    }
    id = manage_resource_creation_requests()
    resp = requests.patch(f"{ApiEndpoints.resource_url()}/{id+id}", json=patch_payload)
    check.is_false(resp.ok)
    check.equal(resp.status_code, 404)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(resp_json['status'], 404)
    check.equal(resp_json["error"], 'Not Found')


def test_resource_patch_length_2_key_400_playwright(manage_resource_creation_playwright):
    resource_no = randint(0, 99)
    patch_payload = {
        #"key": f"KEY_RESOURCE_APP_UPDATED {resource_no}",    # @Size(min = 3, max = 128)
        "key": f"{resource_no:02d}",
        "type": f"TYPE_RESOURCE_APP_UPDATED {resource_no}",
        "description": f"UPDATED Mobile App Resource {resource_no}",
    }
    api, id = manage_resource_creation_playwright()
    resp = api.patch(f"/api/v1/resource/{id}", data=patch_payload)
    check.is_false(resp.ok)
    check.equal(resp.status, 400)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(resp_json['status'], 400)
    check.equal(resp_json['error'], 'Bad Request')



def test_resource_patch_length_4_type_400_playwright(manage_resource_creation_playwright):
    resource_no = randint(0, 9999)
    patch_payload = {
        "key": f"KEY_RESOURCE_APP_UPDATED {resource_no}",
        #"type": f"TYPE_RESOURCE_APP_UPDATED {resource_no}",       #  @Size(min = 5, max = 100)
        "type": f"{resource_no:04d}",
        "description": f"UPDATED Mobile App Resource {resource_no}",
    }
    api, id = manage_resource_creation_playwright()
    resp = api.patch(f"/api/v1/resource/{id}", data=patch_payload)
    check.is_false(resp.ok)
    check.equal(resp.status, 400)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(resp_json['status'], 400)
    check.equal(resp_json['error'], 'Bad Request')

