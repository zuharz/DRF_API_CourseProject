import requests

# Create your tests here.
def test_LoginAsAdmin():
    url = "http://127.0.0.1:8000/token/login"

    payload = {
        "username": "admin",
        "password": "123#!"
    }
    headers = {
        "cookie": "csrftoken=bxHiqGbHH7CRBhGKOeGLsgO9YtnmQxGQ",
        "Content-Type": "application/json"
    }

    response = requests.request("POST", url, json=payload, headers=headers)

    print(response.text)
    assert True
