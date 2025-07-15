# Create virtual using Ansilble
Ansible playbook will take a YAML file input and will create one https virtual.\
The sAnsible playbook calls the username and password from environment variables.

Usage:
create vip\
ansible-playbook -i inventory playbook/playbook_create_virtual.yaml --extra-vars "@playbook/virtual_parameters.yaml"

get system info\
ansible-playbook -i inventory playbook/playbook_get_sysinfo.yaml

Export username and password:
```
export F5_USERNAME=<username>
export F5_PASSWORD=<password>
```
Sample YAML:
```
virtual:
    lb: "10.33.88.30" # load balancer IP or host name
    app: ansible_04 # app name
    description: "This is a test" # description for virtaul and pool 
    virtualip: "10.10.11.4" # virtuals IP address
    port: "443" # port the virtual will listen on 
    send_string: "GET /index.html" # send string for backend server monitoring
    recv_string: "200" # recieve string from backend servers
    members: # pool member IPs 
      - 4.4.4.4
      - 5.5.5.5

```

Output:\
If the virtual was created successful the output will look like below
```
TASK [Create pool] *************************************************************************************************************************************************************************************************
changed: [10.33.88.30 -> localhost]

TASK [Add members to pool] *****************************************************************************************************************************************************************************************
changed: [10.33.88.30 -> localhost] => (item=4.4.4.4)
changed: [10.33.88.30 -> localhost] => (item=5.5.5.5)

TASK [Create a VIP] ************************************************************************************************************************************************************************************************
changed: [10.33.88.30 -> localhost]

PLAY RECAP *********************************************************************************************************************************************************************************************************
10.33.88.30                : ok=5    changed=4    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0 
```





