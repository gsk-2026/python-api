import os


DEFAULT_URLS = {
    "DFT": "http://localhost:8181",
    "DIT": "http://localhost:8181",
    "SIT": "http://localhost:8181",
    "UAT": "http://localhost:8181",
}


def get_api_base_url() -> str:
    test_env = os.getenv("TEST_ENV", "DFT").upper()
    return os.getenv("API_BASE_URL", DEFAULT_URLS.get(test_env, DEFAULT_URLS["DFT"]))



class ApiEndpoints:

    @classmethod
    def base_url(cls) -> str:
        return f"{get_api_base_url()}"

    @classmethod
    def health_url(cls) -> str:
        return f"{get_api_base_url()}/actuator/health"

    @classmethod
    def client_url(cls) -> str:
        return f"{get_api_base_url()}/api/v1/client"

    @classmethod
    def resource_url(cls) -> str:
        return f"{get_api_base_url()}/api/v1/resource"

    @classmethod
    def client_resource_access_url(cls) -> str:
        return f"{get_api_base_url()}/api/v1/client-resource-access"


