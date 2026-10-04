import os

DEFAULT_URLS = {
    "DFT": "https://restful-booker.herokuapp.com",
    "DIT": "https://restful-booker.herokuapp.com",
    "SIT": "https://restful-booker.herokuapp.com",
    "UAT": "https://restful-booker.herokuapp.com",
}

def get_api_base_url() -> str:
    test_env = os.getenv("TEST_ENV", "DFT").upper()
    return os.getenv("API_BASE_URL", DEFAULT_URLS.get(test_env, DEFAULT_URLS["DFT"]))


class ApiEndpoints:

    @classmethod
    def base_url(cls) -> str:
        return f"{get_api_base_url()}"

    @classmethod
    def ping_url(cls) -> str:
        return f"{get_api_base_url()}/ping"

    @classmethod
    def auth_url(cls) -> str:
        return f"{get_api_base_url()}/auth"

    @classmethod
    def booking_url(cls) -> str:
        return f"{get_api_base_url()}/booking"
