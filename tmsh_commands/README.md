# TMSH command generator
The create_virtual_tmsh.py script will take a YAML file input and output the TMSH commands to create one https virtual.

Usage:
create_virtual_tmsh.py <file.yaml>

Sample YAML:
```
virtual:
    app: test-app # app name
    description: "This is a test" # description for virtaul and pool 
    virtual-ip: "10.10.10.10" # virtuals IP address
    port: "443" # port the virtual will listen on 
    send_string: "GET /index.html" # send string for backend server monitoring
    recv_string: "200" # recieve string from backend servers
    members: # pool member IPs 
      - 1.1.1.1
      - 2.2.2.2
      - 3.3.3.3
```

Output:
```
run util bash
tmsh
create cli transaction
create ltm profile client-ssl clientssl_test-app  cert default.crt description 'appname: test-app;2025-05-22 ;This is a test' key default.key
create ltm monitor https m_test-app description 'appname: test-app;2025-05-22 ;This is a test' send 'GET GET /index.html\r\nHost: \r\nUser-Agent: F5-healthcheck\r\nConnection: Close\r\n\r\n' recv '200'
create ltm pool p_test-app description 'appname: test-app;2025-05-22 ;This is a test' load-balancing-mode round-robin members add {  1.1.1.1:443  2.2.2.2:443  3.3.3.3:443  } monitor m_test-app
create ltm virtual vs_test-app description 'appname: test-app;2025-05-22 ;This is a test' destination 10.10.10.10:443 pool p_test-app profiles add { clientssl_test-app { context clientside } tcp } source-address-translation { type automap}
submit cli transaction
save sys config
quit
exit
```





