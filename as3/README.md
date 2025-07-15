# Create virtual using F5 AS3
The create_virtual_as3.py script will take a YAML file input and will use the F5 REST API to create one https virtual.\
The script calls the username and password from environment variables.

Usage:
create_virtual_as3.py <file.yaml>

Export username and password:
```
export F5_USERNAME=<username>
export F5_PASSWORD=<password>
```
Sample YAML:
```
virtual:
    lb: "10.33.88.30" # load balancer IP or host name
    app: test-app01 # app name
    description: "This is a test" # description for virtaul and pool 
    virtual-ip: "10.10.10.1" # virtuals IP address
    port: "443" # port the virtual will listen on 
    send_string: "GET /index.html" # send string for backend server monitoring
    recv_string: "200" # recieve string from backend servers
    members: # pool member IPs 
      - 1.1.1.1
      - 2.2.2.2
      - 3.3.3.3

```

Output:\
If the virtual was created successful the output will look like below
```
{
    "results": [
        {
            "code": 200,
            "message": "success",
            "lineCount": 24,
            "host": "localhost",
            "tenant": "vs_test-app01",
            "runTime": 734,
            "declarationId": "vs_test-app01"
        }
    ],
    "declaration": {
        "class": "ADC",
        "schemaVersion": "3.5.0",
        "id": "vs_test-app01",
        "label": "vs_test-app01",
        "remark": "appname: test-app01; 2025-05-28; This is a test",
        "vs_test-app01": {
            "class": "Tenant",
            "A1": {
                "class": "Application",
                "vs_test-app01": {
                    "class": "Service_HTTP",
                    "virtualAddresses": [
                        "10.10.10.1"
                    ],
                    "remark": "appname: test-app01; 2025-05-28; This is a test",
                    "pool": "p_test-app01"
                },
                "p_test-app01": {
                    "class": "Pool",
                    "remark": "appname: test-app01; 2025-05-28; This is a test",
                    "monitors": [
                        {
                            "use": "m_test-app01"
                        }
                    ],
                    "members": [
                        {
                            "servicePort": 443,
                            "serverAddresses": [
                                "1.1.1.1",
                                "2.2.2.2",
                                "3.3.3.3"
                            ]
                        }
                    ]
                },
                "m_test-app01": {
                    "class": "Monitor",
                    "remark": "appname: test-app01; 2025-05-28; This is a test",
                    "monitorType": "https",
                    "send": "GET /index.html",
                    "receive": "200"
                }
            }
        },
        "updateMode": "selective",
        "controls": {
            "archiveTimestamp": "2025-05-28T22:17:14.718Z"
        }
    }
}
```





