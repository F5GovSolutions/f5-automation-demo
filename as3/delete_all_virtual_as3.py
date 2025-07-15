import os
import json
import requests
import yaml
import argparse
from jinja2 import Environment, FileSystemLoader
from datetime import date

requests.packages.urllib3.disable_warnings()


def delete_virtual(lb):
    # Create F5 virtual server with AS3 configuration
    session = requests.Session()
    session.verify = False

    # Authenticate
    auth_response = session.post(
        f"https://{lb}/mgmt/shared/authn/login",
        json={
            "username": os.getenv("F5_USERNAME"),
            "password": os.getenv("F5_PASSWORD"),
            "loginProviderName": "tmos",
        },
        timeout=30,
    )
    auth_response.raise_for_status()

    # Update session headers with token
    session.headers.update(
        {
            "Content-Type": "application/json",
            "X-F5-Auth-Token": auth_response.json()["token"]["token"],
        }
    )
    url = f"https://{lb}/mgmt/shared/appsvcs/declare/"
    print(url)
    # Delete configuration
    response = session.delete(f"https://{lb}/mgmt/shared/appsvcs/declare")
    response_json = response.json()
    print(response_json)


def main():
    parser = argparse.ArgumentParser(description="Create F5 VIP configuration")
    parser.add_argument("yaml_file", help="Path to YAML configuration file")

    with open(parser.parse_args().yaml_file) as f:
        input_config = yaml.safe_load(f)["virtual"]

    delete_virtual(input_config["lb"])
    print(input_config["app"])


if __name__ == "__main__":
    main()
