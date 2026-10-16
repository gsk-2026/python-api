import pytest
from random import randint
from pytest_check import check
from config.settings import ApiEndpoints



class StepFailure(Exception):
    pass

def run_step(step_name, func, *args, **kwargs):
    try:
        return func(*args, **kwargs)
    except AssertionError as ae:
        raise StepFailure(f"Fatal error at step: {step_name}, exception: {str(ae)}")
    except Exception as ex:
        raise StepFailure(f"Fatal error at step: {step_name}, exception: {str(ex)}")



def test_e2e_happy_path_workflow(manage_playwright_api_context):
    random_num = randint(0, 999999)
    client_contexts = []
    resource_contexts = []
    client_resource_access_contexts = []
    api_context = manage_playwright_api_context(base_url=ApiEndpoints.base_url())

    try:
        def step_client_creation():
            client_payload = {
                "key": f"Key_Client_Item_{random_num:06d}",
                "secret": f"Secret_Client_Item_{random_num:06d}",
                "description": f"Description Client Item {random_num:06d}",
            }
            resp = api_context.post("/api/v1/client", data=client_payload)
            check.is_true(resp.ok)
            check.equal(resp.status, 201)
            check.is_not_none(resp.json())
            resp_json = resp.json()
            check.is_instance(resp_json, dict)
            check.equal(resp_json["key"], client_payload["key"])
            check.equal(resp_json["description"], client_payload["description"])
            client_contexts.append(resp_json['id'])
        run_step("E2E_Happy_Path: step_client_creation", step_client_creation)

        def step_client_get_by_id():
            client_id = client_contexts[0]
            resp = api_context.get(f"/api/v1/client/{client_id}")
            check.is_true(resp.ok)
            check.equal(resp.status, 200)
            check.is_not_none(resp.json())
            resp_json = resp.json()
            check.is_instance(resp_json, dict)
            check.equal(resp_json['id'], client_id)
        run_step("E2E_Happy_Path: step_client_get_by_id", step_client_get_by_id)

        def step_client_get_key():
            client_id = client_contexts[0]
            resp = api_context.get(f"/api/v1/client/{client_id}/key")
            check.is_true(resp.ok)
            check.equal(resp.status, 200)
            check.is_not_none(resp.text())
            check.is_in('Key_Client_Item_', resp.text())
        run_step("E2E_Happy_Path: step_client_get_key", step_client_get_key)

        def step_client_get_description():
            client_id = client_contexts[0]
            resp = api_context.get(f"/api/v1/client/{client_id}/description")
            check.is_true(resp.ok)
            check.equal(resp.status, 200)
            check.is_not_none(resp.text())
            check.is_in('Description Client Item', resp.text())
        run_step("E2E_Happy_Path: step_client_get_description", step_client_get_description)

        def step_resource_creation():
            resource_payload = {
                "key": f"Key_Resource_Item_{random_num:06d}",
                "type": f"Type_Resource_Item_{random_num:06d}",
                "description": f"Description Resource Item {random_num:06d}",
            }
            resp = api_context.post("/api/v1/resource", data=resource_payload)
            check.is_true(resp.ok)
            check.equal(resp.status, 201)
            check.is_not_none(resp.json())
            resp_json = resp.json()
            check.is_instance(resp_json, dict)
            check.equal(resp_json["key"], resource_payload["key"])
            check.equal(resp_json["type"], resource_payload["type"])
            check.equal(resp_json["description"], resource_payload["description"])
            resource_contexts.append(resp_json['id'])
        run_step("E2E_Happy_Path: step_resource_creation", step_resource_creation)

        def step_resource_get_by_id():
            resource_id = resource_contexts[0]
            resp = api_context.get(f"/api/v1/resource/{resource_id}")
            check.is_true(resp.ok)
            check.equal(resp.status, 200)
            check.is_not_none(resp.json())
            resp_json = resp.json()
            check.is_instance(resp_json, dict)
            check.equal(resp_json['id'], resource_id)
        run_step("E2E_Happy_Path: step_resource_get_by_id", step_resource_get_by_id)

        def step_resource_get_key():
            resource_id = resource_contexts[0]
            resp = api_context.get(f"/api/v1/resource/{resource_id}/key")
            check.is_true(resp.ok)
            check.equal(resp.status, 200)
            check.is_not_none(resp.text())
            check.is_in('Key_Resource_Item_', resp.text())
        run_step("E2E_Happy_Path: step_resource_get_key", step_resource_get_key)

        def step_resource_get_type():
            resource_id = resource_contexts[0]
            resp = api_context.get(f"/api/v1/resource/{resource_id}/type")
            check.is_true(resp.ok)
            check.equal(resp.status, 200)
            check.is_not_none(resp.text())
            check.is_in('Type_Resource_Item_', resp.text())
        run_step("E2E_Happy_Path: step_resource_get_type", step_resource_get_type)

        def step_resource_get_description():
            resource_id = resource_contexts[0]
            resp = api_context.get(f"/api/v1/resource/{resource_id}/description")
            check.is_true(resp.ok)
            check.equal(resp.status, 200)
            check.is_not_none(resp.text())
            check.is_in('Description Resource Item', resp.text())
        run_step("E2E_Happy_Path: step_resource_get_description", step_resource_get_description)

        def step_client_resource_access_creation():
            check.greater(len(client_contexts), 0)
            check.greater(len(resource_contexts), 0)
            client_id = client_contexts[0]
            resource_id = resource_contexts[0]
            payload = {
                "clientId": f"{client_id}",
                "resourceId": f"{resource_id}",
                "accessCode": f"Access_Code_{random_num:06d}",
                "description": f"Client Resource Access Description {random_num:06d}",
            }
            resp = api_context.post("/api/v1/client-resource-access", data=payload)
            check.is_true(resp.ok)
            check.equal(resp.status, 201)
            check.is_not_none(resp.json())
            resp_json = resp.json()
            check.is_instance(resp_json, dict)
            check.equal(resp_json['clientId'], client_id)
            check.equal(resp_json['resourceId'], resource_id)
            check.equal(resp_json['accessCode'], f"{payload['accessCode']}")
            check.equal(resp_json['description'], f"{payload['description']}")
            client_resource_access_contexts.append({'clientId': client_id, 'resourceId': resource_id})
        run_step("E2E_Happy_Path: step_client_resource_access_creation", step_client_resource_access_creation)

        def step_client_resource_access_get_by_ids():
            check.greater(len(client_contexts), 0)
            check.greater(len(resource_contexts), 0)
            client_id = client_contexts[0]
            resource_id = resource_contexts[0]
            resp = api_context.get(f"/api/v1/client-resource-access/client/{client_id}/resource/{resource_id}")
            check.is_true(resp.ok)
            check.equal(resp.status, 200)
            check.is_not_none(resp.json())
            resp_json = resp.json()
            check.is_instance(resp_json, dict)
            check.equal(resp_json['clientId'], client_id)
            check.equal(resp_json['resourceId'], resource_id)
        run_step("E2E_Happy_Path: step_client_resource_access_get_by_ids", step_client_resource_access_get_by_ids)

        def step_client_resource_access_get_access_code():
            check.greater(len(client_contexts), 0)
            check.greater(len(resource_contexts), 0)
            client_id = client_contexts[0]
            resource_id = resource_contexts[0]
            resp = api_context.get(f"/api/v1/client-resource-access/client/{client_id}/resource/{resource_id}/access-code")
            check.is_true(resp.ok)
            check.equal(resp.status, 200)
            check.is_not_none(resp.text())
            check.is_in('Access_Code_', resp.text())
        run_step("E2E_Happy_Path: step_client_resource_access_get_access_code", step_client_resource_access_get_access_code)

        def step_client_resource_access_get_description():
            check.greater(len(client_contexts), 0)
            check.greater(len(resource_contexts), 0)
            client_id = client_contexts[0]
            resource_id = resource_contexts[0]
            resp = api_context.get(f"/api/v1/client-resource-access/client/{client_id}/resource/{resource_id}/description")
            check.is_true(resp.ok)
            check.equal(resp.status, 200)
            check.is_not_none(resp.text())
            check.is_in('Client Resource Access Description', resp.text())
        run_step("E2E_Happy_Path: step_client_resource_access_get_description", step_client_resource_access_get_description)


    except StepFailure:
        pytest.fail("E2E_Happy_Path : Experienced a fatal step failure and Skipped the rest of the steps")

    finally:
        # cleanup
        for item in client_resource_access_contexts:
            resp = api_context.delete(f"/api/v1/client-resource-access/client/{item['clientId']}/resource/{item['resourceId']}")
            check.is_in(resp.status, [204, 404])
        for resource_id in resource_contexts:
            resp = api_context.delete(f"/api/v1/resource/{resource_id}")
            check.is_in(resp.status, [204, 404])
        for client_id in client_contexts:
            resp = api_context.delete(f"/api/v1/client/{client_id}")
            check.is_in(resp.status, [204, 404])




def test_e2e_comprehensive_scenarios(manage_playwright_api_context):
    random_num = randint(0, 999999)
    client_contexts = []
    resource_contexts = []
    client_resource_access_contexts = []
    api_context = manage_playwright_api_context(base_url=ApiEndpoints.base_url())

    try:
        def step_client_creation():
            client_payload = {
                "key": f"Key_Client_Item_{random_num:06d}",
                "secret": f"Secret_Client_Item_{random_num:06d}",
                "description": f"Description Client Item {random_num:06d}",
            }
            resp = api_context.post("/api/v1/client", data=client_payload)
            check.is_true(resp.ok)
            check.equal(resp.status, 201)
            check.is_not_none(resp.json())
            resp_json = resp.json()
            check.is_instance(resp_json, dict)
            check.equal(resp_json["key"], client_payload["key"])
            check.equal(resp_json["description"], client_payload["description"])
            client_contexts.append(resp_json['id'])
        run_step("E2E_Comprehensive_Case: step_client_creation", step_client_creation)

        def step_client_update():
            client_id = client_contexts[0]
            patch_payload = {
                "key": f"Updated_Key_Client_Item_{client_id}",
                "description": f"Updated Description Client Item {client_id}",
            }
            resp = api_context.patch(f"/api/v1/client/{client_id}", data=patch_payload)
            check.is_true(resp.ok)
            check.equal(resp.status, 200)
            check.is_not_none(resp.json())
            resp_json = resp.json()
            check.equal(resp_json['id'], client_id)
            check.equal(resp_json["key"], patch_payload["key"])
            check.equal(resp_json["description"], patch_payload["description"])
        run_step("E2E_Comprehensive_Case: step_client_update", step_client_update)

        def step_client_replace():
            client_id = client_contexts[0]
            put_payload = {
                "key": f"Replaced_Key_Client_Item_{client_id}",
                "description": f"Replaced Description Client Item {client_id}",
            }
            resp = api_context.patch(f"/api/v1/client/{client_id}", data=put_payload)
            check.is_true(resp.ok)
            check.equal(resp.status, 200)
            check.is_not_none(resp.json())
            resp_json = resp.json()
            check.equal(resp_json['id'], client_id)
            check.equal(resp_json["key"], put_payload["key"])
            check.equal(resp_json["description"], put_payload["description"])
        run_step("E2E_Comprehensive_Case: step_client_replace", step_client_replace)

        def step_client_get_all():
            client_id = client_contexts[0]
            resp = api_context.get(f"/api/v1/client/search")
            check.is_true(resp.ok)
            check.equal(resp.status, 200)
            check.is_not_none(resp.json())
            resp_json = resp.json()
            check.is_instance(resp_json, list)
            check.is_true(any(item['id'] == client_id for item in resp_json))
        run_step("E2E_Comprehensive_Case: step_client_get_all", step_client_get_all)

        def step_resource_creation():
            resource_payload = {
                "key": f"Key_Resource_Item_{random_num:06d}",
                "type": f"Type_Resource_Item_{random_num:06d}",
                "description": f"Description Resource Item {random_num:06d}",
            }
            resp = api_context.post("/api/v1/resource", data=resource_payload)
            check.is_true(resp.ok)
            check.equal(resp.status, 201)
            check.is_not_none(resp.json())
            resp_json = resp.json()
            check.is_instance(resp_json, dict)
            check.equal(resp_json["key"], resource_payload["key"])
            check.equal(resp_json["type"], resource_payload["type"])
            check.equal(resp_json["description"], resource_payload["description"])
            resource_contexts.append(resp_json['id'])
        run_step("E2E_Comprehensive_Case: step_resource_creation", step_resource_creation)

        def step_resource_update():
            resource_id = resource_contexts[0]
            patch_payload = {
                "key": f"Updated_Key_Resource_Item_{resource_id}",
                "type": f"Updated_Type_Resource_Item_{resource_id}",
                "description": f"Updated Description Resource Item {resource_id}",
            }
            resp = api_context.patch(f"/api/v1/resource/{resource_id}", data=patch_payload)
            check.is_true(resp.ok)
            check.equal(resp.status, 200)
            check.is_not_none(resp.json())
            resp_json = resp.json()
            check.is_instance(resp_json, dict)
            check.equal(resp_json["id"], resource_id)
            check.equal(resp_json["key"], patch_payload["key"])
            check.equal(resp_json["type"], patch_payload["type"])
            check.equal(resp_json["description"], patch_payload["description"])
        run_step("E2E_Comprehensive_Case: step_resource_update", step_resource_update)

        def step_resource_replace():
            resource_id = resource_contexts[0]
            put_payload = {
                "key": f"Replaced_Key_Resource_Item_{resource_id}",
                "type": f"Replaced_Type_Resource_Item_{resource_id}",
                "description": f"Replaced Description Resource Item {resource_id}",
            }
            resp = api_context.put(f"/api/v1/resource/{resource_id}", data=put_payload)
            check.is_true(resp.ok)
            check.equal(resp.status, 200)
            check.is_not_none(resp.json())
            resp_json = resp.json()
            check.is_instance(resp_json, dict)
            check.equal(resp_json["id"], resource_id)
            check.equal(resp_json["key"], put_payload["key"])
            check.equal(resp_json["type"], put_payload["type"])
            check.equal(resp_json["description"], put_payload["description"])
        run_step("E2E_Comprehensive_Case: step_resource_replace", step_resource_replace)

        def step_resource_get_all():
            resource_id = resource_contexts[0]
            resp = api_context.get(f"/api/v1/resource/search")
            check.is_true(resp.ok)
            check.equal(resp.status, 200)
            check.is_not_none(resp.json())
            check.is_instance(resp.json(), list)
            check.is_true(any(item['id'] == resource_id for item in resp.json()))
        run_step("E2E_Comprehensive_Case: step_resource_get_all", step_resource_get_all)

        def step_client_resource_access_creation():
            check.greater(len(client_contexts), 0)
            check.greater(len(resource_contexts), 0)
            client_id = client_contexts[0]
            resource_id = resource_contexts[0]
            payload = {
                "clientId": f"{client_id}",
                "resourceId": f"{resource_id}",
                "accessCode": f"Access_Code_{client_id}_{resource_id}",
                "description": f"Client Resource Access Description {client_id}_{resource_id}",
            }
            resp = api_context.post("/api/v1/client-resource-access", data=payload)
            check.is_true(resp.ok)
            check.equal(resp.status, 201)
            check.is_not_none(resp.json())
            resp_json = resp.json()
            check.is_instance(resp_json, dict)
            check.equal(resp_json['clientId'], client_id)
            check.equal(resp_json['resourceId'], resource_id)
            check.equal(resp_json['accessCode'], f"{payload['accessCode']}")
            check.equal(resp_json['description'], f"{payload['description']}")
            client_resource_access_contexts.append({'clientId': client_id, 'resourceId': resource_id})
        run_step("E2E_Comprehensive_Case: step_client_resource_access_creation", step_client_resource_access_creation)

        def step_client_resource_access_update():
            check.greater(len(client_contexts), 0)
            check.greater(len(resource_contexts), 0)
            client_id = client_contexts[0]
            resource_id = resource_contexts[0]
            payload = {
                "accessCode": f"Updated_Access_Code_{client_id}_{resource_id}",
                "description": f"Updated Client Resource Access Description {client_id}_{resource_id}",
            }
            resp = api_context.patch(f"/api/v1/client-resource-access/client/{client_id}/resource/{resource_id}", data=payload)
            check.is_true(resp.ok)
            check.equal(resp.status, 200)
            check.is_not_none(resp.json())
            resp_json = resp.json()
            check.is_instance(resp_json, dict)
            check.equal(resp_json['clientId'], client_id)
            check.equal(resp_json['resourceId'], resource_id)
            check.equal(resp_json['accessCode'], f"{payload['accessCode']}")
            check.equal(resp_json['description'], f"{payload['description']}")
        run_step("E2E_Comprehensive_Case: step_client_resource_access_update", step_client_resource_access_update)

        def step_client_resource_access_replace():
            check.greater(len(client_contexts), 0)
            check.greater(len(resource_contexts), 0)
            client_id = client_contexts[0]
            resource_id = resource_contexts[0]
            payload = {
                "accessCode": f"Replaced_Access_Code_{client_id}_{resource_id}",
                "description": f"Replaced Client Resource Access Description {client_id}_{resource_id}",
            }
            resp = api_context.put(f"/api/v1/client-resource-access/client/{client_id}/resource/{resource_id}", data=payload)
            check.is_true(resp.ok)
            check.equal(resp.status, 200)
            check.is_not_none(resp.json())
            resp_json = resp.json()
            check.is_instance(resp_json, dict)
            check.equal(resp_json['clientId'], client_id)
            check.equal(resp_json['resourceId'], resource_id)
            check.equal(resp_json['accessCode'], f"{payload['accessCode']}")
            check.equal(resp_json['description'], f"{payload['description']}")
        run_step("E2E_Comprehensive_Case: step_client_resource_access_replace", step_client_resource_access_replace)


        def step_client_resource_access_get_all():
            check.greater(len(client_contexts), 0)
            check.greater(len(resource_contexts), 0)
            client_id = client_contexts[0]
            resource_id = resource_contexts[0]
            resp = api_context.get(f"/api/v1/client-resource-access/search")
            check.is_true(resp.ok)
            check.equal(resp.status, 200)
            check.is_not_none(resp.json())
            check.is_instance(resp.json(), list)
            check.is_true(any(item['clientId'] == client_id and item['resourceId'] == resource_id for item in resp.json()))
        run_step("E2E_Comprehensive_Case: step_client_resource_access_get_all", step_client_resource_access_get_all)


    except StepFailure:
        pytest.fail("E2E_Comprehensive_Case : Experienced a fatal step failure and Skipped the rest of the steps")

    finally:
        # cleanup
        for item in client_resource_access_contexts:
            resp = api_context.delete(f"/api/v1/client-resource-access/client/{item['clientId']}/resource/{item['resourceId']}")
            check.is_in(resp.status, [204, 404])
        for resource_id in resource_contexts:
            resp = api_context.delete(f"/api/v1/resource/{resource_id}")
            check.is_in(resp.status, [204, 404])
        for client_id in client_contexts:
            resp = api_context.delete(f"/api/v1/client/{client_id}")
            check.is_in(resp.status, [204, 404])




def test_e2e_edge_negative_scenarios(manage_playwright_api_context):
    random_num = randint(0, 999999)
    client_contexts = []
    resource_contexts = []
    client_resource_access_contexts = []
    api_context = manage_playwright_api_context(base_url=ApiEndpoints.base_url())

    try:
        def step_client_get_invalid():
            resp = api_context.get("/api/v1/client/123456789")
            check.is_false(resp.ok)
            check.equal(resp.status, 404)
            check.is_instance(resp.json(), dict)
            resp_json = resp.json()
            check.equal(resp_json['status'], 404)
            check.equal(resp_json['error'], 'Not Found')
        run_step("E2E_Edge_Negative_Case: step_client_get_invalid", step_client_get_invalid)

        def step_resource_update_invalid():
            patch_payload = {
                "key": "Invalid_Updated_Key_Resource_Item",
                "type": "Invalid_Updated_Type_Resource_Item",
                "description": "Invalid Updated Description Resource Item",
            }
            resp = api_context.patch("/api/v1/resource/123456789", data=patch_payload)
            check.is_false(resp.ok)
            check.equal(resp.status, 404)
            check.is_instance(resp.json(), dict)
            resp_json = resp.json()
            check.equal(resp_json['status'], 404)
            check.equal(resp_json['error'], 'Not Found')
        run_step("E2E_Edge_Negative_Case: step_resource_update_invalid", step_resource_update_invalid)

        def step_client_resource_access_replace_invalid():
            payload = {
                "accessCode": f"Invalid_Replaced_Access_Code",
                "description": f"Invalid Replaced Client Resource Access Description",
            }
            resp = api_context.put(f"/api/v1/client-resource-access/client/123456/resource/654321", data=payload)
            check.is_false(resp.ok)
            check.equal(resp.status, 404)
            check.is_not_none(resp.json())
            check.is_instance(resp.json(), dict)
            resp_json = resp.json()
            check.equal(resp_json['status'], 404)                       # defect, should be 404
            check.equal(resp_json['error'], 'Not Found')
        run_step("E2E_Edge_Negative_Case: step_client_resource_access_replace_invalid", step_client_resource_access_replace_invalid)

        def step_client_post_with_xss_inputs():
            client_no = randint(0, 999999)
            client_payload = {
                "key": f'<iframe src="javascript:alert(\'XSS\')"></iframe>{client_no}',
                "secret": f'<svg onload="alert(\'XSS\')">{client_no}',
                "description": "<script>alert('xss')</script>",
            }
            resp = api_context.post("/api/v1/client", data=client_payload)
            check.is_in(resp.status, [200, 201, 400])
            if resp.status in [200, 201]:
                client_contexts.append(resp.json().get('id'))
        run_step("E2E_Edge_Negative_Case: step_client_post_with_xss_inputs", step_client_post_with_xss_inputs)

        def step_client_post_with_sql_injection():
            client_no = randint(0, 999999)
            client_payload = {

                "key": f"test_key'; DROP TABLE clients; --{client_no}",
                "secret": f"test_key'; DROP TABLE clients; --{client_no}",
                "description": "test_key'; DROP TABLE clients; --",
            }
            resp = api_context.post("/api/v1/client", data=client_payload)
            check.is_in(resp.status, [200, 201, 400])
            if resp.status in [200, 201]:
                client_contexts.append(resp.json().get('id'))
        run_step("E2E_Edge_Negative_Case: step_client_post_with_sql_injection", step_client_post_with_sql_injection)


    except StepFailure:
        pytest.fail("E2E_Comprehensive_Case : Experienced a fatal step failure and Skipped the rest of the steps")

    finally:
        # cleanup
        for item in client_resource_access_contexts:
            resp = api_context.delete(f"/api/v1/client-resource-access/client/{item['clientId']}/resource/{item['resourceId']}")
            check.is_in(resp.status, [204, 404])
        for resource_id in resource_contexts:
            resp = api_context.delete(f"/api/v1/resource/{resource_id}")
            check.is_in(resp.status, [204, 404])
        for client_id in client_contexts:
            resp = api_context.delete(f"/api/v1/client/{client_id}")
            check.is_in(resp.status, [204, 404])

