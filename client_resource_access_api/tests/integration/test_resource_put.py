from pytest_check import check
from random import randint
import requests
from config.settings import ApiEndpoints



def test_resource_put_200_playwright(manage_resource_creation_playwright):
    resource_no = randint(0, 999999)
    put_payload = {
        "key": f"KEY_RESOURCE_APP_REPLACED {resource_no}",
        "type": f"TYPE_RESOURCE_APP_REPLACED {resource_no}",
        "description": f"Replaced Mobile App Resource {resource_no}",
    }
    api, id = manage_resource_creation_playwright()
    resp = api.put(f"/api/v1/resource/{id}", data=put_payload)
    check.is_true(resp.ok)
    check.equal(resp.status, 200)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(resp_json['id'], id)
    check.equal(resp_json["key"], put_payload["key"])
    check.equal(resp_json["type"], put_payload["type"])
    check.equal(resp_json["description"], put_payload["description"])



def test_resource_put_200_requests(manage_resource_creation_requests):
    resource_no = randint(0, 999999)
    put_payload = {
        "key": f"KEY_RESOURCE_APP_REPLACED {resource_no}",
        "type": f"TYPE_RESOURCE_APP_REPLACED {resource_no}",
        "description": f"Replaced Mobile App Resource {resource_no}",
    }
    id = manage_resource_creation_requests()
    resp = requests.put(f"{ApiEndpoints.resource_url()}/{id}", json=put_payload)
    check.is_true(resp.ok)
    check.equal(resp.status_code, 200)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(resp_json['id'], id)
    check.equal(resp_json["key"], put_payload["key"])
    check.equal(resp_json["type"], put_payload["type"])
    check.equal(resp_json["description"], put_payload["description"])




def test_resource_put_duplicate_key_409_playwright(manage_resource_creation_playwright):
    # first resource
    resource_no = randint(0, 999999)
    key_duplicated = f"KEY_RESOURCE_{resource_no}"
    put_payload = {
        "key": f"{key_duplicated}",
        "type": f"TYPE_RESOURCE_{resource_no}-A",
        "description": f"Resource Description {resource_no}-A",
    }
    api_1, id_1 = manage_resource_creation_playwright()
    resp = api_1.put(f"/api/v1/resource/{id_1}", data=put_payload)
    check.is_true(resp.ok)
    check.equal(resp.status, 200)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(resp_json['id'], id_1)
    check.equal(resp_json["key"], put_payload["key"])
    check.equal(resp_json["type"], put_payload["type"])
    check.equal(resp_json["description"], put_payload["description"])
    # second resource
    put_payload = {
        "key": f"{key_duplicated}",
        "type": f"TYPE_RESOURCE_{resource_no}-B",
        "description": f"Resource Description {resource_no}-B",
    }
    api_2, id_2 = manage_resource_creation_playwright()
    resp = api_2.put(f"/api/v1/resource/{id_2}", data=put_payload)
    check.is_false(resp.ok)
    check.equal(resp.status, 409)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(resp_json['status'], 409)
    check.equal(resp_json['error'], 'Conflict')
    check.equal(resp_json['path'], f"/api/v1/resource/{id_2}")




def test_resource_put_duplicate_key_409_requests(manage_resource_creation_requests):
    # first resource
    resource_no = randint(0, 999999)
    key_duplicate = f"KEY_RESOURCE_{resource_no}"
    put_payload = {
        "key": f"{key_duplicate}",
        "type": f"TYPE_RESOURCE_APP_REPLACED {resource_no}-A",
        "description": f"Replaced Mobile App Resource {resource_no}-A",
    }
    id_1 = manage_resource_creation_requests()
    resp = requests.put(f"{ApiEndpoints.resource_url()}/{id_1}", json=put_payload)
    check.is_true(resp.ok)
    check.equal(resp.status_code, 200)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(resp_json['id'], id_1)
    check.equal(resp_json["key"], put_payload["key"])
    check.equal(resp_json["type"], put_payload["type"])
    check.equal(resp_json["description"], put_payload["description"])
    # second
    key_duplicate = f"KEY_RESOURCE_{resource_no}"
    put_payload = {
        "key": f"{key_duplicate}",
        "type": f"TYPE_RESOURCE_APP_REPLACED {resource_no}-B",
        "description": f"Replaced Mobile App Resource {resource_no}-B",
    }
    id_2 = manage_resource_creation_requests()
    resp = requests.put(f"{ApiEndpoints.resource_url()}/{id_2}", json=put_payload)
    check.is_false(resp.ok)
    check.equal(resp.status_code, 409)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(resp_json['status'], 409)
    check.equal(resp_json['error'], 'Conflict')
    check.equal(resp_json['path'], f"/api/v1/resource/{id_2}")




def test_resource_put_no_description_description_200_playwright(manage_resource_creation_playwright):
    resource_no = randint(0, 999999)
    put_payload = {
        "key": f"KEY_RESOURCE_APP_REPLACED {resource_no}",
        "type": f"TYPE_RESOURCE_APP_REPLACED {resource_no}",
    }
    api, id = manage_resource_creation_playwright()
    resp = api.put(f"/api/v1/resource/{id}", data=put_payload)
    check.is_true(resp.ok)
    check.equal(resp.status, 200)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(resp_json['id'], id)
    check.equal(resp_json["key"], put_payload["key"])
    check.equal(resp_json["type"], put_payload["type"])
    check.is_none(resp_json["description"])



def test_resource_put_no_description_200_requests(manage_resource_creation_requests):
    resource_no = randint(0, 999999)
    put_payload = {
        "key": f"KEY_RESOURCE_APP_REPLACED {resource_no}",
        "type": f"TYPE_RESOURCE_APP_REPLACED {resource_no}",
    }
    id = manage_resource_creation_requests()
    resp = requests.put(f"{ApiEndpoints.resource_url()}/{id}", json=put_payload)
    check.is_true(resp.ok)
    check.equal(resp.status_code, 200)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(resp_json['id'], id)
    check.equal(resp_json["key"], put_payload["key"])
    check.equal(resp_json["type"], put_payload["type"])
    check.is_none(resp_json["description"])



def test_resource_put_no_type_400_playwright(manage_resource_creation_playwright):
    resource_no = randint(0, 999999)
    put_payload = {
        "key": f"KEY_RESOURCE_APP_REPLACED {resource_no}",
        "description": f"Replaced Mobile App Resource {resource_no}",
    }
    api, id = manage_resource_creation_playwright()
    resp = api.put(f"/api/v1/resource/{id}", data=put_payload)
    check.is_false(resp.ok)
    check.equal(resp.status, 400)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(resp_json['status'], 400)
    check.equal(resp_json['error'], 'Bad Request')



def test_resource_put_no_type_400_requests(manage_resource_creation_requests):
    resource_no = randint(0, 999999)
    put_payload = {
        "key": f"KEY_RESOURCE_APP_REPLACED {resource_no}",
        "description": f"Replaced Mobile App Resource {resource_no}",
    }
    id = manage_resource_creation_requests()
    resp = requests.put(f"{ApiEndpoints.resource_url()}/{id}", json=put_payload)
    check.is_false(resp.ok)
    check.equal(resp.status_code, 400)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(resp_json['status'], 400)
    check.equal(resp_json['error'], 'Bad Request')




def test_resource_put_no_key_400_playwright(manage_resource_creation_playwright):
    resource_no = randint(0, 999999)
    put_payload = {
        "type": f"TYPE_RESOURCE_APP_REPLACED {resource_no}",
        "description": f"Replaced Mobile App Resource {resource_no}",
    }
    api, id = manage_resource_creation_playwright()
    resp = api.put(f"/api/v1/resource/{id}", data=put_payload)
    check.is_false(resp.ok)
    check.equal(resp.status, 400)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(resp_json['status'], 400)
    check.equal(resp_json['error'], 'Bad Request')



def test_resource_put_no_key_400_requests(manage_resource_creation_requests):
    resource_no = randint(0, 999999)
    put_payload = {
        "type": f"TYPE_RESOURCE_APP_REPLACED {resource_no}",
        "description": f"Replaced Mobile App Resource {resource_no}",
    }
    id = manage_resource_creation_requests()
    resp = requests.put(f"{ApiEndpoints.resource_url()}/{id}", json=put_payload)
    check.is_false(resp.ok)
    check.equal(resp.status_code, 400)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(resp_json['status'], 400)
    check.equal(resp_json['error'], 'Bad Request')



def test_resource_put_length_2_key_400_playwright(manage_resource_creation_playwright):
    resource_no = randint(0, 99)
    put_payload = {
        #"key": f"KEY_RESOURCE_APP_REPLACED {resource_no}",       # @Size(min = 3, max = 128)
        "key": f"{resource_no:02d}",
        "type": f"TYPE_RESOURCE_APP_REPLACED {resource_no}",
        "description": f"Replaced Mobile App Resource {resource_no}",
    }
    api, id = manage_resource_creation_playwright()
    resp = api.put(f"/api/v1/resource/{id}", data=put_payload)
    check.is_false(resp.ok)
    check.equal(resp.status, 400)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(resp_json["status"], 400)
    check.equal(resp_json["error"], 'Bad Request')



def test_resource_put_length_4_type_400_playwright(manage_resource_creation_playwright):
    resource_no = randint(0, 9999)
    put_payload = {
        "key": f"KEY_RESOURCE_APP_REPLACED {resource_no}",
        #"type": f"TYPE_RESOURCE_APP_REPLACED {resource_no}",            #  @Size(min = 5, max = 100)
        "type": f"{resource_no:04d}",
        "description": f"Replaced Mobile App Resource {resource_no}",
    }
    api, id = manage_resource_creation_playwright()
    resp = api.put(f"/api/v1/resource/{id}", data=put_payload)
    check.is_false(resp.ok)
    check.equal(resp.status, 400)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(resp_json["status"], 400)
    check.equal(resp_json["error"], 'Bad Request')




def test_resource_put_invalid_id_200_playwright(manage_playwright_api_context):
    resource_no = randint(0, 999999)
    put_payload = {
        "key": f"KEY_RESOURCE_APP_REPLACED {resource_no}",
        "type": f"TYPE_RESOURCE_APP_REPLACED {resource_no}",
        "description": f"Replaced Mobile App Resource {resource_no}",
    }
    api= manage_playwright_api_context(base_url=ApiEndpoints.base_url())
    resp = api.put(f"/api/v1/resource/{123456789}", data=put_payload)
    check.is_true(resp.ok)
    check.equal(resp.status, 200)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(resp_json["key"], put_payload["key"])
    check.equal(resp_json["type"], put_payload["type"])
    check.equal(resp_json["description"], put_payload["description"])
    resource_id = resp_json['id']
    # cleanup
    resp = api.delete(f"/api/v1/resource/{resource_id}")
    check.is_true(resp.ok)
    check.equal(resp.status, 204)




def test_resource_put_invalid_id_200_requests():
    resource_no = randint(0, 999999)
    put_payload = {
        "key": f"KEY_RESOURCE_APP_REPLACED {resource_no}",
        "type": f"TYPE_RESOURCE_APP_REPLACED {resource_no}",
        "description": f"Replaced Mobile App Resource {resource_no}",
    }
    resp = requests.put(f"{ApiEndpoints.resource_url()}/{987654321}", json=put_payload)
    check.is_true(resp.ok)
    check.equal(resp.status_code, 200)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(resp_json["key"], put_payload["key"])
    check.equal(resp_json["type"], put_payload["type"])
    check.equal(resp_json["description"], put_payload["description"])
    resource_id = resp_json['id']
    # cleanup
    resp = requests.delete(f"{ApiEndpoints.resource_url()}/{resource_id}")
    check.is_true(resp.ok)
    check.equal(resp.status_code, 204)

