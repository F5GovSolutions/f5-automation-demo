import os
import json
import requests
import yaml
import argparse
from jinja2 import Environment, FileSystemLoader
from datetime import date

requests.packages.urllib3.disable_warnings()


def create_virtual(lb, config):
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

    # Deploy configuration
    response = session.post(f"https://{lb}/mgmt/shared/appsvcs/declare", json=config)
    response_json = response.json()
    print(json.dumps(response_json, indent=4))


def build_as3_config(input_config):
    # Build AS3 configuration from input parameters
    app = input_config["app"]
    names = {
        k: f"{v}{app}"
        for k, v in {"virtual": "vs_", "pool": "p_", "monitor": "m_"}.items()
    }
    description = f"appname: {app}; {date.today()}; {input_config['description']}"

    env = Environment(
        loader=FileSystemLoader("templates"), trim_blocks=True, lstrip_blocks=True
    )
    as3_config = env.get_template("https.j2").render(
        virtual_name=names["virtual"],
        description=description,
        virtual_ip=input_config["virtual-ip"],
        pool_name=names["pool"],
        members=input_config["members"],
        monitor_name=names["monitor"],
        send_string=input_config["send_string"],
        receive_string=input_config["recv_string"],
    )
    return as3_config


def main():
    parser = argparse.ArgumentParser(description="Create F5 VIP configuration")
    parser.add_argument("yaml_file", help="Path to YAML configuration file")

    with open(parser.parse_args().yaml_file) as f:
        input_config = yaml.safe_load(f)["virtual"]

    create_virtual(input_config["lb"], build_as3_config(input_config))
    as3_config = build_as3_config(input_config)
    #print(as3_config)


if __name__ == "__main__":
    main()
