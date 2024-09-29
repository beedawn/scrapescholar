import jwt

SECRET = "your_secret_key"

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyIiwiZXhwIjoxNzI3NTg4ODU0fQ.dZdvwJ-5iL9uSo_IygYWf9fXHvEr-kygV8sIUky0OYY"

payload = jwt.decode(token, SECRET, algorithms=["HS256"])

print(payload)