import requests, utils.env


cloudflare_api_token = utils.env.get_dns_api_token()
base_url = "https://api.cloudflare.com/client/V4"

headers = {
    "Authorization": f"Bearer {cloudflare_api_token}",
    "Content-Type": "application/json"
}

def cf_get_domains():
    response = requests.get(f"{base_url}/zones", headers=headers)
    data = response.json()
    print(data)