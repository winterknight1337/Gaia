import requests
from prettytable import PrettyTable

base_url = "https://api.porkbun.com/api/json/v3"

def get_domains(api_key: str, secret_key: str):
    headers = {
        "Content-Type" : "application/json"
    }

    data = {
        "apikey" : f"{api_key}",
        "secretapikey" : f"{secret_key}",
        }

    response = requests.post(f"{base_url}/domain/listAll", headers=headers, json=data)
    data = response.json()
    return data

def get_domain_records(api_key: str, secret_key: str, domain: str):
    headers = {
        "X-API-KEY" : f"{api_key}",
        "X-Secret-API-KEY" : f"{secret_key}",
        "Content-Type" : "application/json"
    }
        
    response = requests.get(f"{base_url}/dns/retrieve/{domain}", headers=headers)
    data = response.json()
    return data

def delete_domain_record_by_id(api_key: str, secret_key: str, domain: str, record_id: str):
    headers = {
        "Content-Type" : "application/json"
    }

    data = {
        "apikey" : f"{api_key}",
        "secretapikey" : f"{secret_key}",
        "domain" : f"{domain}", 
        "id" : f"{record_id}",
        }

    response = requests.post(f"{base_url}/dns/delete/{domain}/{record_id}", headers=headers, json=data)
    data = response.json()
    return data

def create_domain_record(api_key: str, secret_key: str, domain: str, record_name: str, record_type: str, record_target):
    headers = {
        "Content-Type" : "application/json"
    }

    data = {
        "apikey" : f"{api_key}",
        "secretapikey" : f"{secret_key}",
        "name" : f"{record_name}", 
        "type" : f"{record_type}",
        "content" : f"{record_target}",
        "notes" : "Created by Gaia"
    }

    response = requests.post(f"{base_url}/dns/create/{domain}", headers=headers, json=data)
    data = response.json()
    return data

def print_domains(domains:dict):
    table = PrettyTable(["Domain Name", "Domain Status", "Domain ID"])

    for i in domains["domains"]:
        domain_name = i["domain"]
        domain_status = i["status"]
        domain_api = i["apiAccess"]

        table.add_row([domain_name, domain_status, domain_api])

    print(table)

def print_domain_records(domain_records:dict):

    table = PrettyTable(["Record Name", "Record Type", "Record Value", "Record ID"])

    for i in domain_records:
        record_name = i["name"]
        record_type = i["type"]
        record_value = i["content"]
        record_id = i["id"]

        table.add_row([record_name, record_type, record_value, record_id])

    print(table)
