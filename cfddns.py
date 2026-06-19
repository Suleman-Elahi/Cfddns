import json
import re
import socket
import ssl
import sys
import time
import urllib.request
import urllib.parse
import urllib.error

CF_ZONE_URL = 'https://api.cloudflare.com/client/v4/zones/'
CF_TRACE = 'https://www.cloudflare.com/cdn-cgi/trace'


def _fetch_trace(ipv6=False):
    """Fetch Cloudflare trace, forcing IPv4 or IPv6 via socket family."""
    family = socket.AF_INET6 if ipv6 else socket.AF_INET
    _orig = socket.getaddrinfo

    def _forced_getaddrinfo(host, port, family=0, type=0, proto=0, flags=0):
        return _orig(host, port, family if family else _family, type, proto, flags)

    _family = family
    socket.getaddrinfo = _forced_getaddrinfo
    try:
        ctx = ssl.create_default_context()
        with urllib.request.urlopen(CF_TRACE, context=ctx, timeout=10) as resp:
            text = resp.read().decode()
    finally:
        socket.getaddrinfo = _orig

    match = re.search(r'^ip=(.+)$', text, re.MULTILINE)
    if not match:
        raise ValueError("Could not parse IP from Cloudflare trace response")
    return match.group(1).strip()


def get_zone_id(domain, headers):
    params = {'name': domain}
    url = CF_ZONE_URL + '?' + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as response:
            if response.status == 200:
                zones = json.loads(response.read().decode())['result']
                if zones:
                    return zones[0]['id']
    except urllib.error.URLError as e:
        print(f"Error fetching zone ID: {e}")
    return None


def main():
    if len(sys.argv) != 4:
        print(f"Usage: {sys.argv[0]} <domain> <api_key> <record_type>")
        sys.exit(1)

    domain = sys.argv[1]
    api_key = sys.argv[2]
    record_type = sys.argv[3].upper()

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }

    if record_type in ('A', 'MX', 'NS'):
        ip = _fetch_trace(ipv6=False)
    else:
        try:
            ip = _fetch_trace(ipv6=True)
        except (urllib.error.URLError, OSError) as e:
            print(f"IPv6 unavailable — cannot determine public IPv6 address.")
            print(f"Use host networking: docker run --network host ...")
            sys.exit(1)

    zone_domain = re.sub(r'^.+?\.(?=[^.]+\.[^.]+$)', '', domain)
    zone_id = get_zone_id(zone_domain, headers)

    if not zone_id:
        print(f"Zone ID for {domain} not found")
        sys.exit(1)

    url = CF_ZONE_URL + f"{zone_id}/dns_records"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as response:
            if response.status != 200:
                print(f"Error fetching DNS records: {response.read().decode()}")
                sys.exit(1)
            dns_records = json.loads(response.read().decode())['result']
    except urllib.error.URLError as e:
        print(f"Error fetching DNS records: {e}")
        sys.exit(1)

    record_id = None
    existing_ip = None
    for record in dns_records:
        if record['type'] == record_type and record['name'] == domain:
            record_id = record['id']
            existing_ip = record['content']
            break

    if record_id is None:
        print(f"No {record_type} record found for {domain}")
        sys.exit(1)

    if ip == existing_ip:
        print("Nothing needs to be done.")
        sys.exit(0)

    post_data = json.dumps({
        "content": ip,
        "name": domain,
        "proxied": False,
        "type": record_type,
        "comment": "DNS Record updated using Cfddns at " + time.strftime("%H:%M:%S on %Y-%m-%d"),
        "ttl": 0,
    }).encode('utf-8')

    url = CF_ZONE_URL + f"{zone_id}/dns_records/{record_id}"
    req = urllib.request.Request(url, data=post_data, headers=headers, method='PUT')
    try:
        with urllib.request.urlopen(req) as response:
            if response.status == 200:
                print("Record updated successfully")
            else:
                print(f"Error updating record: {response.read().decode()}")
    except urllib.error.URLError as e:
        print(f"Error updating record: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
