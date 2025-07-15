#!/usr/bin/env python3
"""
Simplified F5 VIP creation script - consolidated into single file
"""
import argparse
import yaml
import json
import requests
from datetime import date
import os
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Configuration
F5_USERNAME = os.getenv("F5_USERNAME")
F5_PASSWORD = os.getenv("F5_PASSWORD")
PREFIXES = {"virtual": "vs_", "pool": "p_", "monitor": "m_"}


class F5Manager:
    def __init__(self, lb_host):
        self.lb_host = lb_host
        self.base_url = f"https://{lb_host}/mgmt/tm"
        self.session = self._authenticate()

    def _authenticate(self):
        # Get token and authenticated session
        session = requests.Session()
        auth_url = f"https://{self.lb_host}/mgmt/shared/authn/login"
        payload = {
            "username": F5_USERNAME,
            "password": F5_PASSWORD,
            "loginProviderName": "tmos",
        }

        try:
            response = session.post(auth_url, json=payload, verify=False, timeout=30)
            response.raise_for_status()
            token = response.json()["token"]["token"]
            session.headers.update(
                {"Content-Type": "application/json", "X-F5-Auth-Token": token}
            )
            return session
        except requests.RequestException as e:
            raise Exception(f"F5 authentication failed for {self.lb_host}: {e}")

    def _execute_transaction(self, virtual_config):
        # Execute multiple virtual configurations in a single transaction∏
        # Create transaction
        transaction_response = self.session.post(
            f"https://{self.lb_host}/mgmt/tm/transaction", json={}, verify=False
        )
        transaction_response.raise_for_status()
        transaction_id = str(transaction_response.json()["transId"])

        # Add transaction header
        headers = {"X-F5-REST-Coordination-Id": transaction_id}

        # Execute virtual configuration
        for config in virtual_config:
            response = self.session.post(
                f"{self.base_url}/{config['endpoint']}",
                json=config["payload"],
                headers=headers,
                verify=False,
                timeout=30,
            )
            response.raise_for_status()

        # Commit transaction
        commit_response = self.session.put(
            f"https://{self.lb_host}/mgmt/tm/transaction/{transaction_id}",
            json={"state": "VALIDATING"},
            verify=False,
        )
        response = json.loads(commit_response.content)
        return response

    def create_vip_config(self, config_file):
        # Create VIP configuration from YAML file
        with open(config_file) as f:
            input_config = yaml.safe_load(f)["virtual"]

        # Generate names
        app_name = input_config["app"]
        virtual_name = f"{PREFIXES['virtual']}{app_name}"
        pool_name = f"{PREFIXES['pool']}{app_name}"
        monitor_name = f"{PREFIXES['monitor']}{app_name}"

        # Build member list
        port = input_config["port"]
        members = [f"{ip}:{port}" for ip in input_config["members"]]

        # Create description
        description = (
            f"appname: {app_name}; {date.today()}; {input_config['description']}"
        )

        # Define virtual, pool and monitor configuration
        virtual_config = [
            {
                "endpoint": "ltm/monitor/https",
                "payload": {
                    "name": monitor_name,
                    "description": description,
                    "send": f"{input_config['send_string']}",
                    "recv": f"{input_config['recv_string']}",
                },
            },
            {
                "endpoint": "ltm/pool",
                "payload": {
                    "name": pool_name,
                    "description": description,
                    "monitor": monitor_name,
                    "members": members,
                },
            },
            {
                "endpoint": "ltm/virtual",
                "payload": {
                    "name": virtual_name,
                    "description": description,
                    "destination": f"{input_config['virtual-ip']}:{port}",
                    "mask": "255.255.255.255",
                    "ipProtocol": "tcp",
                    "pool": pool_name,
                },
            },
        ]

        # Execute all operations in transaction
        result = self._execute_transaction(virtual_config)
        print(f"Created VIP configuration for {app_name}")
        return result


def main():
    parser = argparse.ArgumentParser(description="Create F5 VIP configuration")
    parser.add_argument("yaml_file", help="Path to YAML configuration file")
    args = parser.parse_args()

    # Load config to get F5 host or IP
    with open(args.yaml_file) as f:
        lb_host = yaml.safe_load(f)["virtual"]["lb"]

    # Create and execute configuration
    f5_manager = F5Manager(lb_host)
    result = f5_manager.create_vip_config(args.yaml_file)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
