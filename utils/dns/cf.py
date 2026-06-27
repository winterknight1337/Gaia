import requests

base_url = "https://api.cloudflare.com/client/v4"

def get_domains(api_token: str):
    headers = {
    "Authorization": f"Bearer {api_token}",
    "Content-Type": "application/json"
    } 
    
    response = requests.get(f"{base_url}/zones", headers=headers)
    data = response.json()
    return data