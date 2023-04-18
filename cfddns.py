import requests
import json
import re
import sys

################--CONFIG--#############################################################
requests.packages.urllib3.util.connection.HAS_IPV6 = False

record_id = ''
domain = sys.argv[1]
api_key = sys.argv[2]
existing_IP = ''

CF_ZONE_URL = 'https://api.cloudflare.com/client/v4/zones/'
CF_TRACE = 'https://cloudflare.com/cdn-cgi/trace' 
#######################################################################################

headers = {
    'Content-Type': 'application/json',
	'Authorization': f'Bearer {api_key}',
}

def get_zone_id(domain, api_key, headers):
    params = {'name': domain}
    response = requests.get(CF_ZONE_URL, headers=headers, params=params)
    if response.status_code == 200:
        zones = response.json()['result']
        if len(zones) > 0:
            return zones[0]['id']
    return None
    
def get_public_ip():
   response = requests.get(CF_TRACE)
   match = re.search(r'^ip=([\d\.]+)', response.text, re.MULTILINE)
   return match.group(1).strip()
   
ip = get_public_ip()

zone_id = get_zone_id(re.sub(r'^.+?\.(?=[^\.]+\.[^\.]+$)', '', domain), api_key, headers)

if not zone_id:
    print(f"Zone ID for {domain} not found")

response = requests.get(CF_ZONE_URL + f"{zone_id}/dns_records", headers=headers)

if response.status_code == 200:
    # find the record ID for the first A record for the supplied domain name
    dns_records = json.loads(response.text)['result']
    for record in dns_records:
        if record['type'] == 'A' and record['name'] == domain:
            record_id = record['id']
            existing_IP = record['content']
            break
else:
    print('Error fetching DNS records:', response.text)

if ip == existing_IP:
    print("Nothign needs to be done..")
    sys.exit(0)
	
# Set the JSON data to update record value
new_data = {
  "content": ip,
  "name": domain,
  "proxied": False,
  "type": "A",
  "comment": "DDNS Record from Docker",
  "ttl": 0
}

# Update the record via PUT request
response = requests.put(CF_ZONE_URL + f"{zone_id}/dns_records/{record_id}", headers=headers, data=json.dumps(new_data))

if response.status_code == 200:
    print('Record updated successfully')
else:
    print('Error updating record:', response.text)