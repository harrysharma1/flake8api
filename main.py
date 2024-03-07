import argparse
import requests
import json
from rich import print
from markdownify import markdownify
from rich.console import Console
from rich.markdown import Markdown

parser = argparse.ArgumentParser(
    prog="Flake8 API",
    description="Return pretty print of Flake8 rules",
)

parser.add_argument("--single-json", type=str, metavar="E", help="Flake8 code usually prefixed with E following a number e.g. E501")  # noqa: E501
parser.add_argument("--single-pretty", type=str, metavar="EP", help="Pretty printing Flake8 response")  # noqa: E501
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


def single_pretty_print() -> None:
    id = args.single_pretty
    upper_id = id.upper()
    response = requests.get(f"https://www.flake8rules.com/api/rules/{upper_id}/")  # noqa: E501
    if response.status_code != 200:
        print(f"ERROR_INCORRECT_CODE: {id}")
        return
    console = Console()
    data = json.loads(response.text)
    code = data["code"]
    message = data["message"]
    content_html = data["content"]
    rules = markdownify(content_html)
    links = data["links"]
    header = Markdown(f"# {code}")
    console.print(header)
    text = Markdown(f"{message}")
    console.print(text)
    example = Markdown(f"{rules}")
    console.print(example)
    for i in links:
        further_reading = i.split("#")
        title = further_reading[-1]
        title = title.title()
        title = title.replace("-", " ")
        link = Markdown(f"[{title}]({i})")
        console.print(link)


if args.single_json:
    single_json()
elif args.all_json:
    all_json()
elif args.single_pretty:
    single_pretty_print()
