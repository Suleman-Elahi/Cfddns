schtasks /create /sc hourly /mo 1 /tn "Cloudflare DDNS Script" /tr "C:\python\python.exe D:\cfddns\cfddns.py YourDomainHere APIKeyHere"
