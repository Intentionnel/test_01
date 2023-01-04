import requests
import json
 
APIC_HOST = "https://sandboxapicdc.cisco.com"
APIC_USERNAME = "admin"
APIC_PASSWORD = "!v3G@!4@Y"
     
def post_request(apic, cookies, uri, payload):
    url = apic + uri
    print("\n-----------------------------------------------------------------")
    print("\nExecuting API Call: POST")
    print("\nURL: {}".format(url))
    print("\nBODY: {}".format(payload))
 
    req = requests.post(url, cookies=cookies, data=payload, verify=False)
    print("\nSTATUS CODE: {}".format(req.status_code))
    print("\nRESPONSE: {}".format(req.text))
    return req
     
def get_cookies(apic):
    uri = "/api/aaaLogin.json"
    credentials = {
        "aaaUser": {"attributes": {"name": APIC_USERNAME, "pwd": APIC_PASSWORD}}
    }
    authenticate = post_request(
        apic=apic, cookies={}, uri=uri, payload=json.dumps(credentials)
    )
 
    if not authenticate.ok:
        print("\n[ERROR] Authentication failed! APIC responded with:")
        print(json.dumps(json.loads(authenticate.text), indent=4))
        exit()
 
    print("\n[OK] Authentication successful!")
    return authenticate.cookies
     
 
def main():
    cookies = get_cookies(APIC_HOST)
     
    # Create new security domain
    secdom = {
       "aaaDomain": {
          # "attributes": {"name": "SECDOM-PYTHON", "descr": "Python Managed Tenants"}
       }
    }
    path = "/api/mo/uni/userext/domain-SECDOM-PYTHON.json"
    rsp = post_request(APIC_HOST, cookies, path, json.dumps(secdom))
     
    # Create new user for security domain
    user = {
        "aaaUser": {
            "attributes": {"name": "python", "pwd": "somePassword"},
            "children": [
                {
                    "aaaUserDomain": {
                        "attributes": {"name": "all"},
                        "children": [
                            {
                                "aaaUserRole": {
                                    "attributes": {
                                        "name": "read-all",
                                        "privType": "readPriv",
                                    }
                                }
                            }
                        ],
                    }
                },
                {
                    "aaaUserDomain": {
                        "attributes": {"name": "common"},
                        "children": [
                            {
                                "aaaUserRole": {
                                    "attributes": {
                                        "name": "read-all",
                                        "privType": "readPriv",
                                    }
                                }
                            }
                        ],
                    }
                },
                {
                    "aaaUserDomain": {
                        "attributes": {"name": "SECDOM-PYTHON"},
                        "children": [
                            {
                                "aaaUserRole": {
                                    "attributes": {
                                        "name": "tenant-ext-admin",
                                        "privType": "writePriv",
                                    }
                                }
                            }
                        ],
                    }
                },
            ],
        }
    }
 
    path = "/api/mo/uni/userext/user-python.json"
    rsp = post_request(APIC_HOST, cookies, path, json.dumps(user))
         
         
if __name__ == "__main__":
    main()