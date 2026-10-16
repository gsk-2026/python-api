from random import randint
from pytest_check import check
import requests
from config.settings import ApiEndpoints



def test_resource_post_201_playwright(manage_playwright_api_context):
    resource_no = randint(0, 999999)
    resource_payload = {
        "key": f"Key_Resource_Item_{resource_no:06d}",
        "type": f"Type_Resource_Item_{resource_no:06d}",
        "description": f"Description Resource Item {resource_no:06d}",
    }
    api_context = manage_playwright_api_context(base_url=ApiEndpoints.base_url())
    resp = api_context.post("/api/v1/resource", data=resource_payload)
    check.equal(resp.status, 201)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(resp_json["key"], resource_payload["key"])
    check.equal(resp_json["type"], resource_payload["type"])
    check.equal(resp_json["description"], resource_payload["description"])
    check.greater(resp_json['id'], 0)
    check.is_not_none(resp_json['createdAt'])
    check.is_not_none(resp_json['updatedAt'])
    # cleanup
    resp = api_context.delete(f"/api/v1/resource/{resp_json['id']}")
    check.is_true(resp.ok)
    check.equal(resp.status, 204)



def test_resource_post_201_requests(manage_default_headers):
    resource_no = randint(0, 999999)
    resource_payload = {
        "key": f"Key_Resource_Item_{resource_no:06d}",
        "type": f"Type_Resource_Item_{resource_no:06d}",
        "description": f"Description Resource Item {resource_no:06d}",
    }
    resp = requests.post(ApiEndpoints.resource_url(), headers=manage_default_headers, json=resource_payload)
    check.is_true(resp.ok)
    check.equal(resp.status_code, 201)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(resp_json["key"], resource_payload["key"])
    check.equal(resp_json["type"], resource_payload["type"])
    check.equal(resp_json["description"], resource_payload["description"])
    check.greater(resp_json['id'], 0)
    check.is_not_none(resp_json['createdAt'])
    check.is_not_none(resp_json['updatedAt'])
    # cleanup
    resp = requests.delete(f"{ApiEndpoints.resource_url()}/{resp_json['id']}")
    check.is_true(resp.ok)
    check.equal(resp.status_code, 204)





def test_resource_post_201_requests_session(manage_requests_api_session_context):
    resource_no = randint(0, 999999)
    resource_payload = {
        "key": f"Key_Resource_Item_{resource_no:06d}",
        "type": f"Type_Resource_Item_{resource_no:06d}",
        "description": f"Description Resource Item {resource_no:06d}",
    }
    api_session_context = manage_requests_api_session_context(base_url=ApiEndpoints.resource_url())
    resp = api_session_context.post(f"{api_session_context.base_url}", json=resource_payload)
    check.is_true(resp.ok)
    check.equal(resp.status_code, 201)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(resp_json["key"], resource_payload["key"])
    check.equal(resp_json["type"], resource_payload["type"])
    check.equal(resp_json["description"], resource_payload["description"])
    check.greater(resp_json['id'], 0)
    check.is_not_none(resp_json['createdAt'])
    check.is_not_none(resp_json['updatedAt'])
    # cleanup
    resp = api_session_context.delete(f"{api_session_context.base_url}/{resp_json['id']}")
    check.is_true(resp.ok)
    check.equal(resp.status_code, 204)



def test_resource_post_no_description_201_playwright(manage_playwright_api_context):
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
    # cleanup
    resp = api_context.delete(f"/api/v1/resource/{resp_json['id']}")
    check.is_true(resp.ok)
    check.equal(resp.status, 204)




def test_resource_post_no_description_201_requests(manage_default_headers):
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
    check.equal(resp_json["key"], resource_payload["key"])
    check.equal(resp_json["type"], resource_payload["type"])
    check.is_none(resp_json["description"])
    check.greater(resp_json['id'], 0)
    check.is_not_none(resp_json['createdAt'])
    check.is_not_none(resp_json['updatedAt'])
    # cleanup
    resp = requests.delete(f"{ApiEndpoints.resource_url()}/{resp_json['id']}", headers=manage_default_headers)
    check.is_true(resp.ok)
    check.equal(resp.status_code, 204)



def test_resource_post_no_description_201_requests_session(manage_requests_api_session_context):
    resource_no = randint(0, 999999)
    resource_payload = {
        "key": f"Key_Resource_Item_{resource_no:06d}",
        "type": f"Type_Resource_Item_{resource_no:06d}",
    }
    api_session_context = manage_requests_api_session_context(base_url=ApiEndpoints.resource_url())
    resp = api_session_context.post(f"{api_session_context.base_url}", json=resource_payload)
    check.is_true(resp.ok)
    check.equal(resp.status_code, 201)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(resp_json["key"], resource_payload["key"])
    check.equal(resp_json["type"], resource_payload["type"])
    check.is_none(resp_json["description"])
    check.greater(resp_json['id'], 0)
    check.is_not_none(resp_json['createdAt'])
    check.is_not_none(resp_json['updatedAt'])
    # cleanup
    resp = api_session_context.delete(f"{api_session_context.base_url}/{resp_json['id']}")
    check.is_true(resp.ok)
    check.equal(resp.status_code, 204)



def test_resource_post_no_type_400_playwright(manage_playwright_api_context):
    resource_no = randint(0, 999999)
    resource_payload = {
        "key": f"Key_Resource_Item_{resource_no:06d}",
        "description": f"Description Resource Item {resource_no:06d}",
    }
    api_context = manage_playwright_api_context(base_url=ApiEndpoints.base_url())
    resp = api_context.post("/api/v1/resource", data=resource_payload)
    check.is_false(resp.ok)
    check.equal(resp.status, 400)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(resp_json["status"], 400)
    check.equal(resp_json["error"], "Bad Request")



def test_resource_post_no_type_400_requests(manage_default_headers):
    resource_no = randint(0, 999999)
    resource_payload = {
        "key": f"Key_Resource_Item_{resource_no:06d}",
        "description": f"Description Resource Item {resource_no:06d}",
    }
    resp = requests.post(ApiEndpoints.resource_url(), headers=manage_default_headers, json=resource_payload)
    check.is_false(resp.ok)
    check.equal(resp.status_code, 400)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(resp_json["status"], 400)
    check.equal(resp_json["error"], "Bad Request")



def test_resource_post_no_type_400_requests_session(manage_requests_api_session_context):
    resource_no = randint(0, 999999)
    resource_payload = {
        "key": f"Key_Resource_Item_{resource_no:06d}",
        "description": f"Description Resource Item {resource_no:06d}",
    }
    api_session_context = manage_requests_api_session_context(base_url=ApiEndpoints.resource_url())
    resp = api_session_context.post(f"{api_session_context.base_url}", json=resource_payload)
    check.is_false(resp.ok)
    check.equal(resp.status_code, 400)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(resp_json["status"], 400)
    check.equal(resp_json["error"], "Bad Request")



def test_resource_post_no_key_400_playwright(manage_playwright_api_context):
    resource_no = randint(0, 999999)
    resource_payload = {
        "type": f"Type_Resource_Item_{resource_no:06d}",
        "description": f"Description Resource Item {resource_no:06d}",
    }
    api_context = manage_playwright_api_context(base_url=ApiEndpoints.base_url())
    resp = api_context.post("/api/v1/resource", data=resource_payload)
    check.equal(resp.status, 400)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(resp_json["status"], 400)
    check.equal(resp_json["error"], "Bad Request")



def test_resource_post_no_key_400_requests(manage_default_headers):
    resource_no = randint(0, 999999)
    resource_payload = {
        "type": f"Type_Resource_Item_{resource_no:06d}",
        "description": f"Description Resource Item {resource_no:06d}",
    }
    resp = requests.post(ApiEndpoints.resource_url(), headers=manage_default_headers, json=resource_payload)
    check.is_false(resp.ok)
    check.equal(resp.status_code, 400)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(resp_json["status"], 400)
    check.equal(resp_json["error"], "Bad Request")



def test_resource_post_no_key_400_requests_session(manage_requests_api_session_context):
    resource_no = randint(0, 999999)
    resource_payload = {
        "type": f"Type_Resource_Item_{resource_no:06d}",
        "description": f"Resource Item {resource_no:06d}",
    }
    api_session_context = manage_requests_api_session_context(base_url=ApiEndpoints.resource_url())
    resp = api_session_context.post(f"{api_session_context.base_url}", json=resource_payload)
    check.is_false(resp.ok)
    check.equal(resp.status_code, 400)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(resp_json["status"], 400)
    check.equal(resp_json["error"], "Bad Request")



def test_resource_post_no_payload_400_playwright(manage_playwright_api_context):
    api_context = manage_playwright_api_context(base_url=ApiEndpoints.base_url())
    resp = api_context.post("/api/v1/resource", data={})
    check.equal(resp.status, 400)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(resp_json["status"], 400)
    check.equal(resp_json["error"], "Bad Request")



def test_resource_post_no_payload_400_requests(manage_default_headers):
    resp = requests.post(ApiEndpoints.resource_url(), headers=manage_default_headers, json={})
    check.is_false(resp.ok)
    check.equal(resp.status_code, 400)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(resp_json["status"], 400)
    check.equal(resp_json["error"], "Bad Request")



def test_resource_post_no_payload_400_requests_session(manage_requests_api_session_context):
    api_session_context = manage_requests_api_session_context(base_url=ApiEndpoints.resource_url())
    resp = api_session_context.post(f"{api_session_context.base_url}", json={})
    check.is_false(resp.ok)
    check.equal(resp.status_code, 400)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(resp_json["status"], 400)
    check.equal(resp_json["error"], "Bad Request")



def test_resource_post_duplicate_key_201_409_playwright(manage_playwright_api_context):
    resource_no = randint(0, 999999)
    key_duplicated = f"Key_Resource_Item_{resource_no:06d}"
    resource_payload = {
        "key": f"{key_duplicated}",
        "type": f"Type_Resource_Item_{resource_no:06d}-A",
        "description": f"Description Resource Item {resource_no:06d}-A",
    }
    api_context = manage_playwright_api_context(base_url=ApiEndpoints.base_url())
    # first
    resp = api_context.post("/api/v1/resource", data=resource_payload)
    check.equal(resp.status, 201)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(resp_json["key"], resource_payload["key"])
    check.equal(resp_json["type"], resource_payload["type"])
    check.equal(resp_json["description"], resource_payload["description"])
    check.greater(resp_json['id'], 0)
    check.is_not_none(resp_json['createdAt'])
    check.is_not_none(resp_json['updatedAt'])
    resource_id = resp_json['id']
    # duplicate
    resource_payload = {
        "key": f"{key_duplicated}",
        "type": f"Type_Resource_Item_{resource_no:06d}-B",
        "description": f"Description Resource Item {resource_no:06d}-B",
    }
    resp = api_context.post("/api/v1/resource", data=resource_payload)
    check.is_false(resp.ok)
    check.is_not_none(resp.json())
    check.equal(resp.status, 409)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(resp_json["status"], 409)
    check.equal(resp_json["error"], "Conflict")
    # cleanup
    resp = api_context.delete(f"/api/v1/resource/{resource_id}")
    check.is_true(resp.ok)
    check.equal(resp.status, 204)



def test_resource_post_duplicate_key_201_409_requests(manage_default_headers):
    resource_no = randint(0, 999999)
    key_duplicated = f"Key_Resource_Item_{resource_no:06d}"
    resource_payload = {
        "key": f"{key_duplicated}",
        "type": f"Type_Resource_Item_{resource_no:06d}-A",
        "description": f"Description Resource Item {resource_no:06d}-A",
    }
    # first resource
    resp = requests.post(ApiEndpoints.resource_url(), headers=manage_default_headers, json=resource_payload)
    check.is_true(resp.ok)
    check.equal(resp.status_code, 201)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(resp_json["key"], resource_payload["key"])
    check.equal(resp_json["type"], resource_payload["type"])
    check.equal(resp_json["description"], resource_payload["description"])
    check.greater(resp_json['id'], 0)
    check.is_not_none(resp_json['createdAt'])
    check.is_not_none(resp_json['updatedAt'])
    resource_id = resp_json['id']
    # duplicate resource
    resource_payload = {
        "key": f"{key_duplicated}",
        "type": f"Type_Resource_Item_{resource_no:06d}-B",
        "description": f"Description Resource Item {resource_no:06d}-B",
    }
    resp = requests.post(ApiEndpoints.resource_url(), headers=manage_default_headers, json=resource_payload)
    check.is_false(resp.ok)
    check.equal(resp.status_code, 409)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(resp_json["status"], 409)
    check.equal(resp_json["error"], "Conflict")
    # cleanup
    resp = requests.delete(f"{ApiEndpoints.resource_url()}/{resource_id}", headers=manage_default_headers)
    check.is_true(resp.ok)
    check.equal(resp.status_code, 204)



def test_resource_post_duplicate_payload_201_409_playwright(manage_playwright_api_context):
    resource_no = randint(0, 999999)
    resource_payload = {
        "key": f"Key_Resource_Item_{resource_no:06d}",
        "type": f"Type_Resource_Item_{resource_no:06d}",
        "description": f"Description Resource Item {resource_no:06d}",
    }
    api_context = manage_playwright_api_context(base_url=ApiEndpoints.base_url())
    # first
    resp = api_context.post("/api/v1/resource", data=resource_payload)
    check.equal(resp.status, 201)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(resp_json["key"], resource_payload["key"])
    check.equal(resp_json["type"], resource_payload["type"])
    check.equal(resp_json["description"], resource_payload["description"])
    check.greater(resp_json['id'], 0)
    check.is_not_none(resp_json['createdAt'])
    check.is_not_none(resp_json['updatedAt'])
    resource_id = resp_json['id']
    # duplicate
    resp = api_context.post("/api/v1/resource", data=resource_payload)
    check.is_false(resp.ok)
    check.is_not_none(resp.json())
    check.equal(resp.status, 409)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(resp_json["status"], 409)
    check.equal(resp_json["error"], "Conflict")
    # cleanup
    resp = api_context.delete(f"/api/v1/resource/{resource_id}")
    check.is_true(resp.ok)
    check.equal(resp.status, 204)



def test_resource_post_duplicate_payload_201_409_requests(manage_default_headers):
    resource_no = randint(0, 999999)
    resource_payload = {
        "key": f"Key_Resource_Item_{resource_no:06d}",
        "type": f"Type_Resource_Item_{resource_no:06d}",
        "description": f"Description Resource Item {resource_no:06d}",
    }
    # first
    resp = requests.post(ApiEndpoints.resource_url(), headers=manage_default_headers, json=resource_payload)
    check.is_true(resp.ok)
    check.equal(resp.status_code, 201)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(resp_json["key"], resource_payload["key"])
    check.equal(resp_json["type"], resource_payload["type"])
    check.equal(resp_json["description"], resource_payload["description"])
    check.greater(resp_json['id'], 0)
    check.is_not_none(resp_json['createdAt'])
    check.is_not_none(resp_json['updatedAt'])
    resource_id = resp_json['id']
    # duplicate
    resp = requests.post(ApiEndpoints.resource_url(), headers=manage_default_headers, json=resource_payload)
    check.is_false(resp.ok)
    check.equal(resp.status_code, 409)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(resp_json["status"], 409)
    check.equal(resp_json["error"], "Conflict")
    # cleanup
    resp = requests.delete(f"{ApiEndpoints.resource_url()}/{resource_id}", headers=manage_default_headers)
    check.is_true(resp.ok)
    check.equal(resp.status_code, 204)



def test_resource_post_duplicate_payload_201_409_requests_session(manage_requests_api_session_context):
    resource_no = randint(0, 999999)
    resource_payload = {
        "key": f"Key_Resource_Item_{resource_no:06d}",
        "type": f"Type_Resource_Item_{resource_no:06d}",
        "description": f"Description Resource Item {resource_no:06d}",
    }
    api_session_context = manage_requests_api_session_context(base_url=ApiEndpoints.resource_url())
    # first
    resp = api_session_context.post(f"{api_session_context.base_url}", json=resource_payload)
    check.is_true(resp.ok)
    check.equal(resp.status_code, 201)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(resp_json["key"], resource_payload["key"])
    check.equal(resp_json["type"], resource_payload["type"])
    check.equal(resp_json["description"], resource_payload["description"])
    check.greater(resp_json['id'], 0)
    check.is_not_none(resp_json['createdAt'])
    check.is_not_none(resp_json['updatedAt'])
    resource_id = resp_json['id']
    # duplicate
    resp = api_session_context.post(f"{api_session_context.base_url}", json=resource_payload)
    check.is_false(resp.ok)
    check.equal(resp.status_code, 409)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(resp_json["status"], 409)
    check.equal(resp_json["error"], "Conflict")
    # cleanup
    resp = api_session_context.delete(f"{api_session_context.base_url}/{resource_id}")
    check.is_true(resp.ok)
    check.equal(resp.status_code, 204)



def test_resource_post_length_2_key_400_playwright(manage_playwright_api_context):
    resource_no = randint(0, 99)
    resource_payload = {
        #"key": f"Key_Resource_Item_{resource_no:06d}",          # @Size(min = 3, max = 128)
        "key": f"{resource_no:02d}",
        "type": f"Type_Resource_Item_{resource_no:06d}",
        "description": f"Description Resource Item {resource_no:06d}",
    }
    api_context = manage_playwright_api_context(base_url=ApiEndpoints.base_url())
    resp = api_context.post("/api/v1/resource", data=resource_payload)
    check.is_false(resp.ok)
    check.equal(resp.status, 400)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(resp_json['status'], 400)
    check.equal(resp_json['error'], 'Bad Request')



def test_resource_post_length_4_type_400_requests(manage_default_headers):
    resource_no = randint(0, 9999)
    resource_payload = {
        "key": f"Key_Resource_Item_{resource_no:06d}",
        #"type": f"Type_Resource_Item_{resource_no:06d}",        #  @Size(min = 5, max = 100)
        "type": f"{resource_no:04d}",
        "description": f"Description Resource Item {resource_no:06d}",
    }
    resp = requests.post(ApiEndpoints.resource_url(), headers=manage_default_headers, json=resource_payload)
    check.is_false(resp.ok)
    check.equal(resp.status_code, 400)
    check.is_not_none(resp.json())
    resp_json = resp.json()
    check.equal(resp_json['status'], 400)
    check.equal(resp_json['error'], 'Bad Request')

