import requests




def request_api():
    x = requests.get('')
    print(x.status_code)
    print(x.json())
    return {"sciencedirect":"message"}
