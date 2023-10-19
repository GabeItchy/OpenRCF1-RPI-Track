import requests
import json

# NGINX server URL where your PHP script is hosted
nginx_server_url = "http://your_server_domain_or_ip/update_servo.php"

# Sample JSON data to send
data = {"servo_position": 90}

# Convert the data to a JSON string
data_json = json.dumps(data)

# Set the headers for the POST request
headers = {"Content-Type": "application/json"}

# Send the POST request to the NGINX server
response = requests.post(nginx_server_url, data=data_json, headers=headers)

# Check the response
if response.status_code == 200:
    print("Request was successful")
    print("Response from server:")
    print(response.text)
else:
    print(f"Request failed with status code: {response.status_code}")
    print("Response from server:")
    print(response.text)
