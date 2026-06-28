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

def get_domain_records(api_token: str, zone_id: int):
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    } 

    response = requests.get(url=f"{base_url}/zones/{zone_id}/dns_records", headers=headers)
    data = response.json()
    return data

def delete_domain_record(api_token: str, zone_id: int, dns_record_id: int):
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    } 

    response = requests.delete(url=f"{base_url}/zones/{zone_id}/dns_records/{dns_record_id}", headers=headers)
    data = response.json()
    return data
    
def create_domain_record(api_token: str, zone_id: int, record_name: str, record_type: str, record_target: str):
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    } 
    payload = {
        "name" : record_name,
        "ttl" : 3600,
        "type" : record_type,
        "comment" : "Created by Gaia",
        "content" : record_target,
        "private_routing" : False,
        "proxied" : False
    }

    response = requests.post(url=f"{base_url}/zones/{zone_id}/dns_records", json=payload, headers=headers)
    data = response.json()
    return data