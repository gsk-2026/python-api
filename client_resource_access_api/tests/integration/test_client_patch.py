from pytest_check import check
from random import randint
from config.settings import ApiEndpoints
import requests



def test_client_patch_200_playwright(manage_client_creation_playwright):
    client_no = randint(0, 999999)
    patch_payload = {
        "key": f"CLIENT_APP_UPDATED {client_no}",
        "description": f"Updated Mobile App Client {client_no}",
    }
    api, id = manage_client_creation_playwright()
    resp = api.patch(f"/api/v1/client/{id}", data=patch_payload)
    check.is_true(resp.ok)
    check.equal(resp.status, 200)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(resp_json['id'], id)
    check.equal(resp_json["key"], patch_payload["key"])
    check.equal(resp_json["description"], patch_payload["description"])



def test_client_patch_200_requests(manage_client_creation_requests):
    client_no = randint(0, 999999)
    patch_payload = {
        "key": f"CLIENT_APP_UPDATED {client_no}",
        "description": f"Updated Mobile App Client {client_no}",
    }
    id = manage_client_creation_requests()
    resp = requests.patch(f"{ApiEndpoints.client_url()}/{id}", json=patch_payload)
    check.is_true(resp.ok)
    check.equal(resp.status_code, 200)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(resp_json['id'], id)
    check.equal(resp_json["key"], patch_payload["key"])
    check.equal(resp_json["description"], patch_payload["description"])



def test_client_patch_blank_description_200_playwright(manage_client_creation_playwright):
    client_no = randint(0, 999999)
    patch_payload = {
        "key": f"CLIENT_APP_UPDATED {client_no}",
        "description": ""
    }
    api, id = manage_client_creation_playwright()
    resp = api.patch(f"/api/v1/client/{id}", data=patch_payload)
    check.is_true(resp.ok)
    check.equal(resp.status, 200)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(resp_json['id'], id)
    check.equal(resp_json["key"], patch_payload["key"])
    check.equal(resp_json["description"], "")



def test_client_patch_blank_description_200_requests(manage_client_creation_requests):
    client_no = randint(0, 999999)
    patch_payload = {
        "key": f"CLIENT_APP_UPDATED {client_no}",
        "description": ""
    }
    id = manage_client_creation_requests()
    resp = requests.patch(f"{ApiEndpoints.client_url()}/{id}", json=patch_payload)
    check.is_true(resp.ok)
    check.equal(resp.status_code, 200)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(resp_json['id'], id)
    check.equal(resp_json["key"], patch_payload["key"])
    check.equal(resp_json["description"], "")




def test_client_patch_secret_200_playwright(manage_playwright_api_context):
    client_no = randint(0, 999999)
    client_payload = {
        "key": f"Client_App_{client_no:06d}",
        "secret": f"validSecret_{client_no:06d}",
        "description": f"Client App {client_no:06d}",
    }
    # post
    api = manage_playwright_api_context(base_url=ApiEndpoints.base_url())
    resp = api.post("/api/v1/client", data=client_payload)
    check.equal(resp.status, 201)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(resp_json["key"], client_payload["key"])
    check.equal(resp_json["description"], client_payload["description"])
    check.greater(resp_json['id'], 0)
    check.is_not_none(resp_json['createdAt'])
    # patch
    client_id = resp_json['id']
    secret_payload = {"currentSecret": f"{client_payload['secret']}", "newSecret": f"new_updated_secret_{client_no:06d}"}
    resp = api.patch(f"/api/v1/client/{client_id}/secret", data=secret_payload)
    check.is_true(resp.ok)
    check.equal(resp.status, 204)
    check.is_not_none(resp.text())
    check.equal(resp.text(), '')
    # delete
    resp = api.delete(f"/api/v1/client/{client_id}")
    check.is_true(resp.ok)
    check.equal(resp.status, 204)




def test_client_patch_secret_200_requests(manage_default_headers):
    client_no = randint(0, 999999)
    client_payload = {
        "key": f"Client_App_{client_no:06d}",
        "secret": f"validSecret_{client_no:06d}",
        "description": f"Client App {client_no:06d}",
    }
    # post
    resp = requests.post(ApiEndpoints.client_url(), headers=manage_default_headers, json=client_payload)
    check.is_true(resp.ok)
    check.equal(resp.status_code, 201)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(resp_json["key"], client_payload["key"])
    check.equal(resp_json["description"], client_payload["description"])
    check.greater(resp_json['id'], 0)
    check.is_not_none(resp_json['createdAt'])
    check.is_not_none(resp_json['updatedAt'])
    # patch
    client_id = resp_json['id']
    secret_payload = {"currentSecret": f"{client_payload['secret']}", "newSecret": f"new_updated_secret_{client_no:06d}"}
    resp = requests.patch(f"{ApiEndpoints.client_url()}/{client_id}/secret", json=secret_payload)
    check.is_true(resp.ok)
    check.equal(resp.status_code, 204)
    # delete
    resp = requests.delete(f"{ApiEndpoints.client_url()}/{client_id}")
    check.is_true(resp.ok)
    check.equal(resp.status_code, 204)




def test_client_patch_no_key_200_playwright(manage_client_creation_playwright):
    client_no = randint(0, 999999)
    patch_payload = {
        "description": f"Updated Mobile App Client {client_no}",
    }
    api, id = manage_client_creation_playwright()
    resp = api.patch(f"/api/v1/client/{id}", data=patch_payload)
    check.is_true(resp.ok)
    check.equal(resp.status, 200)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(resp_json['id'], id)
    check.equal(resp_json["description"], patch_payload["description"])
    check.is_not_none(resp_json["key"])



def test_client_patch_no_key_200_requests(manage_client_creation_requests):
    client_no = randint(0, 999999)
    patch_payload = {
        "description": f"Updated Mobile App Client {client_no}",
    }
    id = manage_client_creation_requests()
    resp = requests.patch(f"{ApiEndpoints.client_url()}/{id}", json=patch_payload)
    check.is_true(resp.ok)
    check.equal(resp.status_code, 200)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(resp_json['id'], id)
    check.equal(resp_json["description"], patch_payload["description"])
    check.is_not_none(resp_json["key"])



def test_client_patch_no_description_200_playwright(manage_client_creation_playwright):
    client_no = randint(0, 999999)
    patch_payload = {
        "key": f"CLIENT_APP_UPDATED {client_no}",
    }
    api, id = manage_client_creation_playwright()
    resp = api.patch(f"/api/v1/client/{id}", data=patch_payload)
    check.is_true(resp.ok)
    check.equal(resp.status, 200)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(resp_json['id'], id)
    check.equal(resp_json["key"], patch_payload["key"])



def test_client_patch_no_description_200_requests(manage_client_creation_requests):
    client_no = randint(0, 999999)
    patch_payload = {
        "key": f"CLIENT_APP_UPDATED {client_no}",
    }
    id = manage_client_creation_requests()
    resp = requests.patch(f"{ApiEndpoints.client_url()}/{id}", json=patch_payload)
    check.is_true(resp.ok)
    check.equal(resp.status_code, 200)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(resp_json['id'], id)
    check.equal(resp_json["key"], patch_payload["key"])



def test_client_patch_no_payload_200_playwright(manage_client_creation_playwright):
    api, id = manage_client_creation_playwright()
    resp = api.patch(f"/api/v1/client/{id}", data={})
    check.is_true(resp.ok)
    check.equal(resp.status, 200)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(resp_json['id'], id)
    check.is_not_none(resp_json["key"])



def test_client_patch_no_payload_200_requests(manage_client_creation_requests):
    id = manage_client_creation_requests()
    resp = requests.patch(f"{ApiEndpoints.client_url()}/{id}", json={})
    check.is_true(resp.ok)
    check.equal(resp.status_code, 200)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(resp_json['id'], id)
    check.is_not_none(resp_json["key"])



def test_client_patch_invalid_id_404_playwright(manage_client_creation_playwright):
    client_no = randint(0, 999999)
    patch_payload = {
        "key": f"CLIENT_APP_UPDATED {client_no}",
        "description": f"Updated Mobile App Client {client_no}",
    }
    api, id = manage_client_creation_playwright()
    resp = api.patch(f"/api/v1/client/{id+id}", data=patch_payload)
    check.is_false(resp.ok)
    check.equal(resp.status, 404)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(resp_json['status'], 404)
    check.equal(resp_json["error"], 'Not Found')


def test_client_patch_invalid_id_404_requests(manage_client_creation_requests):
    client_no = randint(0, 999999)
    patch_payload = {
        "key": f"CLIENT_APP_UPDATED {client_no}",
        "description": f"Updated Mobile App Client {client_no}",
    }
    id = manage_client_creation_requests()
    resp = requests.patch(f"{ApiEndpoints.client_url()}/{id+id}", json=patch_payload)
    check.is_false(resp.ok)
    check.equal(resp.status_code, 404)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(resp_json['status'], 404)
    check.equal(resp_json["error"], 'Not Found')


"""
# The feature is out of the current scope, to be implemented in future
"""
def test_client_patch_invalid_secret_200_playwright(manage_playwright_api_context):
    client_no = randint(0, 999999)
    client_payload = {
        "key": f"Client_App_{client_no:06d}",
        "secret": f"validSecret_{client_no:06d}",
        "description": f"Client App {client_no:06d}",
    }
    # post
    api = manage_playwright_api_context(base_url=ApiEndpoints.base_url())
    resp = api.post("/api/v1/client", data=client_payload)
    check.equal(resp.status, 201)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(resp_json["key"], client_payload["key"])
    check.equal(resp_json["description"], client_payload["description"])
    check.greater(resp_json['id'], 0)
    check.is_not_none(resp_json['createdAt'])
    # patch
    client_id = resp_json['id']
    secret_payload = {"currentSecret": f"Invalid_{client_payload['secret']}", "newSecret": f"new_updated_secret_{client_no:06d}"}
    resp = api.patch(f"/api/v1/client/{client_id}/secret", data=secret_payload)
    check.is_true(resp.ok)
    check.equal(resp.status, 204)
    check.is_not_none(resp.text())
    check.equal(resp.text(), '')
    # delete
    resp = api.delete(f"/api/v1/client/{client_id}")
    check.is_true(resp.ok)
    check.equal(resp.status, 204)



"""
# The feature is out of the current scope, to be implemented in future
"""
def test_client_patch_invalid_secret_200_requests(manage_default_headers):
    client_no = randint(0, 999999)
    client_payload = {
        "key": f"Client_App_{client_no:06d}",
        "secret": f"validSecret_{client_no:06d}",
        "description": f"Client App {client_no:06d}",
    }
    # post
    resp = requests.post(ApiEndpoints.client_url(), headers=manage_default_headers, json=client_payload)
    check.is_true(resp.ok)
    check.equal(resp.status_code, 201)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(resp_json["key"], client_payload["key"])
    check.equal(resp_json["description"], client_payload["description"])
    check.greater(resp_json['id'], 0)
    check.is_not_none(resp_json['createdAt'])
    check.is_not_none(resp_json['updatedAt'])
    # patch
    client_id = resp_json['id']
    secret_payload = {"currentSecret": f"Invalid_{client_payload['secret']}", "newSecret": f"new_updated_secret_{client_no:06d}"}
    resp = requests.patch(f"{ApiEndpoints.client_url()}/{client_id}/secret", json=secret_payload)
    check.is_true(resp.ok)
    check.equal(resp.status_code, 204)
    # delete
    resp = requests.delete(f"{ApiEndpoints.client_url()}/{client_id}")
    check.is_true(resp.ok)
    check.equal(resp.status_code, 204)



def test_client_patch_length_1_key_400_playwright(manage_client_creation_playwright):
    client_no = randint(0, 9)
    patch_payload = {
        "key": f"{client_no}",       # @Size(min = 3, max = 100)
        "description": f"Updated Mobile App Client {client_no}",
    }
    api, id = manage_client_creation_playwright()
    resp = api.patch(f"/api/v1/client/{id}", data=patch_payload)
    check.is_false(resp.ok)
    check.equal(resp.status, 400)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(resp_json['status'], 400)
    check.equal(resp_json['error'], 'Bad Request')



def test_client_patch_length_2_key_400_playwright(manage_client_creation_playwright):
    client_no = randint(0, 99)
    patch_payload = {
        "key": f"{client_no:02d}",       # @Size(min = 3, max = 100)
        "description": f"Updated Mobile App Client {client_no}",
    }
    api, id = manage_client_creation_playwright()
    resp = api.patch(f"/api/v1/client/{id}", data=patch_payload)
    check.is_false(resp.ok)
    check.equal(resp.status, 400)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(resp_json['status'], 400)
    check.equal(resp_json['error'], 'Bad Request')



def test_client_patch_length_3_key_200_requests(manage_client_creation_requests):
    client_no = randint(0, 999)
    patch_payload = {
        "key": f"{client_no:03d}",       # @Size(min = 3, max = 100)
        "description": f"Updated Mobile App Client {client_no}",
    }
    id = manage_client_creation_requests()
    resp = requests.patch(f"{ApiEndpoints.client_url()}/{id}", json=patch_payload)
    check.is_true(resp.ok)
    check.equal(resp.status_code, 200)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(resp_json['id'], id)
    check.equal(resp_json["key"], patch_payload["key"])
    check.equal(resp_json["description"], patch_payload["description"])




def test_client_patch_duplicate_key_409_playwright(manage_client_creation_playwright):
    # first client
    client_no = randint(0, 999999)
    patch_payload = {
        "description": f"Client Description {client_no}",
    }
    api_1, id_1 = manage_client_creation_playwright()
    resp = api_1.patch(f"/api/v1/client/{id_1}", data=patch_payload)
    check.is_true(resp.ok)
    check.equal(resp.status, 200)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(resp_json['id'], id_1)
    check.equal(resp_json["description"], patch_payload["description"])
    key_1 = resp_json["key"]
    # second client
    patch_payload = {
        "key": f"{key_1}",
        "description": f"Updated Client Description {client_no}",
    }
    api_2, id_2 = manage_client_creation_playwright()
    resp = api_2.patch(f"/api/v1/client/{id_2}", data=patch_payload)
    check.is_false(resp.ok)
    check.equal(resp.status, 409)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(resp_json['status'], 409)
    check.equal(resp_json['error'], 'Conflict')
    check.equal(resp_json['path'], f'/api/v1/client/{id_2}')




def test_client_patch_duplicate_key_409_requests(manage_client_creation_requests):
    # first client
    client_no = randint(0, 999999)
    patch_payload = {
        "description": f"Client Description {client_no}",
    }
    id_1 = manage_client_creation_requests()
    resp = requests.patch(f"{ApiEndpoints.client_url()}/{id_1}", json=patch_payload)
    check.is_true(resp.ok)
    check.equal(resp.status_code, 200)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(resp_json['id'], id_1)
    check.equal(resp_json["description"], patch_payload["description"])
    key_1 = resp_json["key"]
    # second client
    patch_payload = {
        "key": f"{key_1}",
        "description": f"Updated Client Description {client_no}",
    }
    id_2 = manage_client_creation_requests()
    resp = requests.patch(f"{ApiEndpoints.client_url()}/{id_2}", json=patch_payload)
    check.is_false(resp.ok)
    check.equal(resp.status_code, 409)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(resp_json['status'], 409)
    check.equal(resp_json['error'], 'Conflict')
    check.equal(resp_json['path'], f'/api/v1/client/{id_2}')


