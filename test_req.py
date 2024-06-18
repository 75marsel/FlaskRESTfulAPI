import requests

BASE_URL = "http://127.0.0.1:5000/"

headers = {"Content-Type": "application/json; charset=utf-8"}
data = [
    {"likes": 7_000, "name": "Lily Jin Morrow NMIXX", "views": 9_999},
    {"likes": 469, "name": "mayakashi deck", "views": 5_001},
    {"likes": 10_000, "name": "Firefly HSR Leak E6", "views": 50_000},
]

# as per 
# https://stackoverflow.com/questions/72893180/flask-restful-error-request-content-type-was-not-application-json
# json, args and form

for i in range(len(data)):
    response = requests.put(BASE_URL + f"video/{i}", json=data[i], headers=headers)
    print(response.json())

for i in range(len(data)):
    response = requests.get(BASE_URL + f"video/{i}")
    print(response.json())
    
response = requests.get(BASE_URL + "video/9")
print(response.json())

response = requests.patch(BASE_URL + "video/1", json={"name": "KYUJINN"})
print(response.json())

#response = requests.delete(BASE_URL + "video/1")