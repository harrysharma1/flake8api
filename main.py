import argparse
import requests
import json

parser = argparse.ArgumentParser(
    prog="Flake8 API",
    description="Return pretty print of Flake8 rules",
)

parser.add_argument("api", type=str, metavar="E", help="Flake8 code usually prefixed with E following a number e.g. E501")  # noqa: E501

args = parser.parse_args()

id = args.api
response = requests.get(f"https://www.flake8rules.com/api/rules/{id}/")

if response.status_code != 200:
    print(f"Incorrect code:{id}")
else:
    j = response.json()
    print(json.dumps(j, indent=2))
