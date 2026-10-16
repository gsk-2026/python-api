from pytest_check import check
from random import randint
import requests

from config.settings import ApiEndpoints



def test_client_put_key_description_200_playwright(manage_client_creation_playwright):
    client_no = randint(0, 999999)
    put_payload = {
        "key": f"CLIENT_APP_REPLACED {client_no}",
        "description": f"Replaced Mobile App Client {client_no}",
    }
    api, id = manage_client_creation_playwright()
    resp = api.put(f"/api/v1/client/{id}", data=put_payload)
    check.is_true(resp.ok)
    check.equal(resp.status, 200)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(resp_json['id'], id)
    check.equal(resp_json["key"], put_payload["key"])
    check.equal(resp_json["description"], put_payload["description"])



def test_client_put_key_description_200_requests(manage_client_creation_requests):
    client_no = randint(0, 999999)
    put_payload = {
        "key": f"CLIENT_APP_REPLACED {client_no}",
        "description": f"Replaced Mobile App Client {client_no}",
    }
    id = manage_client_creation_requests()
    resp = requests.put(f"{ApiEndpoints.client_url()}/{id}", json=put_payload)
    check.is_true(resp.ok)
    check.equal(resp.status_code, 200)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(resp_json['id'], id)
    check.equal(resp_json["key"], put_payload["key"])
    check.equal(resp_json["description"], put_payload["description"])



def test_client_put_no_description_200_playwright(manage_client_creation_playwright):
    client_no = randint(0, 999999)
    put_payload = {
        "key": f"CLIENT_APP_REPLACED {client_no}",
    }
    api, id = manage_client_creation_playwright()
    resp = api.put(f"/api/v1/client/{id}", data=put_payload)
    check.is_true(resp.ok)
    check.equal(resp.status, 200)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(resp_json['id'], id)
    check.equal(resp_json["key"], put_payload["key"])
    check.is_none(resp_json["description"])



def test_client_put_no_description_200_requests(manage_client_creation_requests):
    client_no = randint(0, 999999)
    put_payload = {
        "key": f"CLIENT_APP_REPLACED {client_no}",
    }
    id = manage_client_creation_requests()
    resp = requests.put(f"{ApiEndpoints.client_url()}/{id}", json=put_payload)
    check.is_true(resp.ok)
    check.equal(resp.status_code, 200)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(resp_json['id'], id)
    check.equal(resp_json["key"], put_payload["key"])
    check.is_none(resp_json["description"])



def test_client_put_no_key_400_playwright(manage_client_creation_playwright):
    client_no = randint(0, 999999)
    put_payload = {
        "description": f"Replaced Mobile App Client {client_no}",
    }
    api, id = manage_client_creation_playwright()
    resp = api.put(f"/api/v1/client/{id}", data=put_payload)
    check.is_false(resp.ok)
    check.equal(resp.status, 400)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(resp_json['status'], 400)
    check.equal(resp_json['error'], 'Bad Request')



def test_client_put_no_key_400_requests(manage_client_creation_requests):
    client_no = randint(0, 999999)
    put_payload = {
        "description": f"Replaced Mobile App Client {client_no}",
    }
    id = manage_client_creation_requests()
    resp = requests.put(f"{ApiEndpoints.client_url()}/{id}", json=put_payload)
    check.is_false(resp.ok)
    check.equal(resp.status_code, 400)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(resp_json['status'], 400)
    check.equal(resp_json['error'], 'Bad Request')



def test_client_put_no_payload_400_playwright(manage_client_creation_playwright):
    api, id = manage_client_creation_playwright()
    resp = api.put(f"/api/v1/client/{id}", data={})
    check.is_false(resp.ok)
    check.equal(resp.status, 400)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(resp_json['status'], 400)
    check.equal(resp_json['error'], 'Bad Request')



def test_client_put_no_payload_400_requests(manage_client_creation_requests):
    id = manage_client_creation_requests()
    resp = requests.put(f"{ApiEndpoints.client_url()}/{id}", json={})
    check.is_false(resp.ok)
    check.equal(resp.status_code, 400)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(resp_json['status'], 400)
    check.equal(resp_json['error'], 'Bad Request')



def test_client_put_invalid_id_200_playwright(manage_client_creation_playwright):
    client_no = randint(0, 999999)
    put_payload = {
        "key": f"CLIENT_APP_REPLACED {client_no}",
        "description": f"Replaced Mobile App Client {client_no}",
    }
    api, id = manage_client_creation_playwright()
    resp = api.put(f"/api/v1/client/{id+id}", data=put_payload)
    check.is_true(resp.ok)
    check.equal(resp.status, 200)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.is_not_none(resp_json['id'])
    check.greater(resp_json['id'], id)
    check.equal(resp_json["key"], put_payload["key"])
    check.equal(resp_json["description"], put_payload["description"])
    client_id = resp_json['id']
    # cleanup
    resp = api.delete(f"/api/v1/client/{client_id}")
    check.is_true(resp.ok)
    check.equal(resp.status, 204)




def test_client_put_invalid_id_200_requests(manage_client_creation_requests):
    client_no = randint(0, 999999)
    put_payload = {
        "key": f"CLIENT_APP_REPLACED {client_no}",
        "description": f"Replaced Mobile App Client {client_no}",
    }
    id = manage_client_creation_requests()
    resp = requests.put(f"{ApiEndpoints.client_url()}/{id+id}", json=put_payload)
    check.is_true(resp.ok)
    check.equal(resp.status_code, 200)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.is_not_none(resp_json['id'])
    check.greater(resp_json['id'], id)
    check.equal(resp_json["key"], put_payload["key"])
    check.equal(resp_json["description"], put_payload["description"])
    client_id = resp_json['id']
    # cleanup
    resp = requests.delete(f"{ApiEndpoints.client_url()}/{client_id}")
    check.is_true(resp.ok)
    check.equal(resp.status_code, 204)




def test_client_put_length_1_key_400_playwright(manage_client_creation_playwright):
    client_no = randint(0, 9)
    put_payload = {
        "key": f"{client_no:01d}",      # @Size(min = 3, max = 100)
        "description": f"Replaced Mobile App Client {client_no}",
    }
    api, id = manage_client_creation_playwright()
    resp = api.put(f"/api/v1/client/{id}", data=put_payload)
    check.is_false(resp.ok)
    check.equal(resp.status, 400)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(resp_json['status'], 400)
    check.equal(resp_json['error'], 'Bad Request')



def test_client_put_length_2_key_400_playwright(manage_client_creation_playwright):
    client_no = randint(0, 99)
    put_payload = {
        "key": f"{client_no:02d}",      # @Size(min = 3, max = 100)
        "description": f"Replaced Mobile App Client {client_no}",
    }
    api, id = manage_client_creation_playwright()
    resp = api.put(f"/api/v1/client/{id}", data=put_payload)
    check.is_false(resp.ok)
    check.equal(resp.status, 400)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(resp_json['status'], 400)
    check.equal(resp_json['error'], 'Bad Request')



def test_client_put_length_3_key_200_playwright(manage_client_creation_playwright):
    client_no = randint(0, 999)
    put_payload = {
        "key": f"CLIENT_APP_REPLACED {client_no:03d}",      # @Size(min = 3, max = 100)
        "description": f"Replaced Mobile App Client {client_no}",
    }
    api, id = manage_client_creation_playwright()
    resp = api.put(f"/api/v1/client/{id}", data=put_payload)
    check.is_true(resp.ok)
    check.equal(resp.status, 200)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(resp_json['id'], id)
    check.equal(resp_json["key"], put_payload["key"])
    check.equal(resp_json["description"], put_payload["description"])




def test_client_put_duplicate_key_409_playwright(manage_client_creation_playwright):
    # first client
    client_no = randint(0, 999999)
    put_payload = {
        "key": f"Client-Key-{client_no}",
        "description": f"Client Description {client_no}"
    }
    api_1, id_1 = manage_client_creation_playwright()
    resp = api_1.put(f"/api/v1/client/{id_1}", data=put_payload)
    check.is_true(resp.ok)
    check.equal(resp.status, 200)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(resp_json['id'], id_1)
    check.equal(resp_json["key"], put_payload["key"])
    check.equal(resp_json["description"], put_payload["description"])
    key_1 = resp_json["key"]
    # second client
    put_payload = {
        "key": f"{key_1}",
        "description": f"Replaced Client Description {client_no}",
    }
    api_2, id_2 = manage_client_creation_playwright()
    resp = api_1.put(f"/api/v1/client/{id_2}", data=put_payload)
    check.is_false(resp.ok)
    check.equal(resp.status, 409)
    resp_json = resp.json()
    check.equal(resp_json["status"], 409)
    check.equal(resp_json["error"], "Conflict")
    check.equal(resp_json["path"], f"/api/v1/client/{id_2}")




def test_client_put_duplicate_key_409_requests(manage_client_creation_requests):
    # first client
    client_no = randint(0, 999999)
    put_payload = {
        "key": f"Client-Key-{client_no}",
        "description": f"Client Description {client_no}"
    }
    id_1 = manage_client_creation_requests()
    resp = requests.put(f"{ApiEndpoints.client_url()}/{id_1}", json=put_payload)
    check.is_true(resp.ok)
    check.equal(resp.status_code, 200)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(resp_json['id'], id_1)
    check.equal(resp_json["key"], put_payload["key"])
    check.equal(resp_json["description"], put_payload["description"])
    key_1 = resp_json["key"]
    # second client
    put_payload = {
        "key": f"{key_1}",
        "description": f"Replaced Client Description {client_no}",
    }
    id_2 = manage_client_creation_requests()
    resp = requests.put(f"{ApiEndpoints.client_url()}/{id_2}", json=put_payload)
    check.is_false(resp.ok)
    check.equal(resp.status_code, 409)
    resp_json = resp.json()
    check.equal(resp_json["status"], 409)
    check.equal(resp_json["error"], "Conflict")
    check.equal(resp_json["path"], f"/api/v1/client/{id_2}")

