import argparse
import requests
import json


parser = argparse.ArgumentParser(
    prog="Flake8 API",
    description="Return pretty print of Flake8 rules",
)

parser.add_argument("--single-json", type=str, metavar="E", help="Flake8 code usually prefixed with E following a number e.g. E501")  # noqa: E501
parser.add_argument("--all-json", help="Example optional argument", action="store_true")  # noqa: E501

args = parser.parse_args()


def single_json() -> None:
    id = args.single_json
    uppder_id = id.upper()
    response = requests.get(f"https://www.flake8rules.com/api/rules/{uppder_id}/")  # noqa: E501
    if response.status_code != 200:
        print(f"ERROR_INCORRECT_CODE: {id}")
        return
    data = json.loads(response.text)
    print(json.dumps(data, indent=2))


def all_json() -> None:
    response = requests.get("https://www.flake8rules.com/api/rules.json")
    if response.status_code != 200:
        print(f"ERROR_UNKOWN_RESPONSE_STATUS: {response.status_code}")
        return
    data = json.loads(response.text)
    print(json.dumps(data, indent=2))


if args.single_json:
    single_json()
elif args.all_json:
    all_json()
