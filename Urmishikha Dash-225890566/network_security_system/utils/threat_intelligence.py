import requests

def check_threat_intelligence(ip_address):
    try:
        url = f"https://api.abuseipdb.com/api/v2/check"
        
        headers = {"Key": "d8f3b840ca4be2a12fe386abbdadae4e26ee5dc0e3b3d28798e4b8db8cb7a070fd1046282e6454f3", "Accept": "application/json"}
        params = {"ipAddress": ip_address, "maxAgeInDays": 90}
        response = requests.get(url, headers=headers, params=params)
        data = response.json()
        if data['data']['abuseConfidenceScore'] > 50:
            return True, data['data']
        return False, None
    except Exception as e:
        print(f"Error querying threat intelligence: {str(e)}")
        return False, None