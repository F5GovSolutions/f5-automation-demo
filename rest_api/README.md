# Create virtual using F5 API
The create_virtual_api.py script will take a YAML file input and will use the F5 REST API to create one https virtual.\
The script calls the username and password from environment variables.

Usage:
create_virtual_api.py <file.yaml>

Export username and password:
```
export F5_USERNAME=<username>
export F5_PASSWORD=<password>
```
Sample YAML:
```
virtual:
    lb: "10.33.88.30" # load balancer IP or host name
    app: test-app23 # app name
    description: "This is a test" # description for virtaul and pool 
    virtual-ip: "10.10.10.23" # virtuals IP address
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
Created VIP configuration for test-app23
{
  "transId": 1748453401369829,
  "state": "COMPLETED",
  "timeoutSeconds": 120,
  "asyncExecution": false,
  "validateOnly": false,
  "executionTimeout": 300,
  "executionTime": 0,
  "failureReason": "",
  "kind": "tm:transactionstate",
  "selfLink": "https://localhost/mgmt/tm/transaction/1748453401369829?ver=17.5.0"
}
```





