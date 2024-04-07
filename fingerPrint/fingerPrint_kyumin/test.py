import requests

res = requests.get("http://localhost:8080/restaurants")
print(res.content)