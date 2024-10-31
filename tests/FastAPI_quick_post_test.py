import requests

url = "http://127.0.0.1:8000/log"
data = {
    "message": "Test log entry",
    "log_level": "INFO"
}
print 
response = requests.post(url, json=data)
print(response.json())