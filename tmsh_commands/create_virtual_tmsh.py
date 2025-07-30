#!/usr/bin/env python3
import argparse
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
import yaml
from datetime import date


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("yaml_file", type=Path)
    args = parser.parse_args()

    # Load data and setup
    with args.yaml_file.open() as f:
        virtual_config = yaml.safe_load(f)["virtual"]

    env = Environment(
        loader=FileSystemLoader("."), trim_blocks=True, lstrip_blocks=True
    )

    # Build config directly in template call
    print(
        env.get_template("virtual_template.j2").render(
            virtual_name=f"vs_{virtual_config['app']}",
            pool_name=f"p_{virtual_config['app']}",
            monitor_name=f"m_{virtual_config['app']}",
            clientssl_name=f"clientssl_{virtual_config['app']}",
            description=f"appname: {virtual_config['app']}; {date.today()}; {virtual_config.get('description', '')}",
            vip_port=f"{virtual_config['virtual-ip']}:{virtual_config['port']}",
            members_ip_port=[
                f"{ip}:{virtual_config['member_port']}"
                for ip in virtual_config.get("members", [])
            ],
            send_string=virtual_config.get("send_string", ""),
            recv_string=virtual_config.get("recv_string", ""),
        )
    )


if __name__ == "__main__":
    main()
