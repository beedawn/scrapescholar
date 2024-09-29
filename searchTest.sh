#!/bin/bash

TOKEN=$(curl -X POST "http://127.0.0.1:8000/auth/login" \
-H "accept: application/json" \
-H "Content-Type: application/x-www-form-urlencoded" \
-d "username=testapi&password=secure_password" \
| jq -r '.access_token')

echo "Retrieved token: $TOKEN"

curl -X GET "http://127.0.0.1:8000/search/user/searches" \
-H "accept: application/json" \
-H "Authorization: Bearer $TOKEN"
