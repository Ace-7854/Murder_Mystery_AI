import requests

API_KEY = "<insert API key here>"
BASE_URL = "https://api.bland.ai"

headers = {
    "Authorization": f"{API_KEY}",
    "Content-Type": "application/json"
}

# Check current org_rate_limit
def get_org_rate_limit():
    response = requests.get(f"{BASE_URL}/v1/orgs", headers=headers)
    if response.status_code == 200:
        return response.json()['data']['org_rate_limit']
    else:
        return f"Error: {response.status_code}, {response.text}"

# Change org_rate_limit
def update_org_rate_limit(new_limit):
    data = {"org_rate_limit": new_limit}
    response = requests.patch(f"{BASE_URL}/v1/org_properties", headers=headers, json=data)
    if response.status_code == 200:
        return response.json()['data']['org_rate_limit']
    else:
        return f"Error: {response.status_code}, {response.text}"

# Usage
print(f"Current rate limit: {get_org_rate_limit()}")
new_limit = 10  # Example new limit
print(f"Updated rate limit: {update_org_rate_limit(new_limit)}")