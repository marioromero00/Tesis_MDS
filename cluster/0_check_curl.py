import requests

# Set your variables
CF_CLIENT_ID = "5b182c9215409b8140ebd22e603b21e5.access"
CF_CLIENT_SECRET = "b53b36414bd8f2158359ffa33ba0879a0130d9bd31a9ff630f30cb1d0bf18a15"
URL = "https://ray-client.monaka.cl"

# Set the headers
headers = {
    "CF-Access-Client-Id": CF_CLIENT_ID,
    "CF-Access-Client-Secret": CF_CLIENT_SECRET,
}

# Run the test
try:
    response = requests.get(URL, headers=headers)
    print(response.status_code)
except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
