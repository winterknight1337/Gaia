from cloudflare import Cloudflare

def cloudflare_get_dns_zones(env: str):
    cf_client = Cloudflare(api_token=env["CLOUDFLARE_API_TOKEN"])

    zones = cf_client.zones.list()
    results = zones.result
    print(zones.result)