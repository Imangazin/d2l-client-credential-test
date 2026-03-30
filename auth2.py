import os
import time
import uuid
import requests
import jwt  # pip install pyjwt cryptography

# =========================
# CONFIG
# =========================
BRIGHTSPACE_BASE_URL = ""
CLIENT_ID = ""
KID = ""  # must match the "kid" in your JWKS
SCOPES = ""


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PRIVATE_KEY_FILE = os.path.join(BASE_DIR, "private.key")

with open(PRIVATE_KEY_FILE, "r") as f:
    PRIVATE_KEY_PEM = f.read()

TOKEN_URL = "https://auth.brightspace.com/core/connect/token"


def build_client_assertion() -> str:
    now = int(time.time())

    payload = {
        "iss": CLIENT_ID,
        "sub": CLIENT_ID,
        "aud": TOKEN_URL,
        "jti": str(uuid.uuid4()),
        "iat": now,
        "exp": now + 300,  # 5 minutes
    }

    headers = {
        "kid": KID,
        "typ": "JWT",
        "alg": "RS256",
    }

    token = jwt.encode(
        payload,
        PRIVATE_KEY_PEM,
        algorithm="RS256",
        headers=headers,
    )
    return token


def get_access_token() -> dict:
    client_assertion = build_client_assertion()

    # Debug: decode JWT without verification
    decoded = jwt.decode(
        client_assertion,
        options={"verify_signature": False, "verify_aud": False},
        algorithms=["RS256"],
    )
    print("Decoded JWT payload:", decoded)

    data = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "scope": SCOPES,
        "client_assertion_type": "urn:ietf:params:oauth:client-assertion-type:jwt-bearer",
        "client_assertion": client_assertion,
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json",
    }

    response = requests.post(
        TOKEN_URL,
        data=data,
        headers=headers,
        timeout=30,
        allow_redirects=False,
    )
    print("Status:", response.status_code)
    print("Headers:", dict(response.headers))
    print("Response:", response.text)
    response.raise_for_status()
    return response.json()


def get_users(access_token: str) -> None:
    # Example API call after token retrieval.
    # You can replace this with another endpoint allowed by your scopes/permissions.
    url = f"{BRIGHTSPACE_BASE_URL}/d2l/api/lp/1.43/users/"
    headers = {
        "Authorization": f"Bearer {access_token}",
    }

    response = requests.get(url, headers=headers, timeout=30)
    print("\nWhoAmI status:", response.status_code)
    print("WhoAmI response:", response.text)


def api_headers(access_token: str) -> dict:
    return {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }


def add_user(access_token: str, user_data: dict):
    url = f"{BRIGHTSPACE_BASE_URL}/d2l/api/lp/1.43/users/"
    response = requests.post(
        url,
        headers=api_headers(access_token),
        json=user_data,
        timeout=30,
    )
    print("\nAdd user status:", response.status_code)
    print("Add user response:", response.text)
    return response


def update_user(access_token: str, user_id: int, user_data: dict):
    url = f"{BRIGHTSPACE_BASE_URL}/d2l/api/lp/1.43/users/{user_id}"
    response = requests.put(
        url,
        headers=api_headers(access_token),
        json=user_data,
        timeout=30,
    )
    print("\nUpdate user status:", response.status_code)
    print("Update user response:", response.text)
    return response


def activate_user(access_token: str, user_id: int, is_active: bool):
    url = f"{BRIGHTSPACE_BASE_URL}/d2l/api/lp/1.43/users/{user_id}/activation"
    payload = {"IsActive": is_active}
    response = requests.put(
        url,
        headers=api_headers(access_token),
        json=payload,
        timeout=30,
    )
    print("\nActivate user status:", response.status_code)
    print("Activate user response:", response.text)
    return response


if __name__ == "__main__":
    token_response = get_access_token()
    access_token = token_response["access_token"]
    print("\nAccess token acquired.")
    print("Expires in:", token_response.get("expires_in"))
    get_users(access_token)

    #Example usage (update values before running)
    # new_user = {
    #     "OrgDefinedId": "9999966666",
    #     "FirstName": "TestFirstName",
    #     "MiddleName": None,
    #     "LastName": "TestLastName",
    #     "ExternalEmail": "testemail@localhost.local",
    #     "UserName": "testusername",
    #     "RoleId": 122,
    #     "IsActive": True,
    #     "SendCreationEmail": False
    # }
    # created = add_user(access_token, new_user)
    # print(created.json())

    # activate_user(access_token, user_id, False)