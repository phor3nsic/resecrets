import re
import os
import json
import sys
import argparse

from pathlib import Path

RED='\033[0;31m'
WHITE='\033[0;37m'
GREEN='\033[0;32m'
NC='\033[0m'

BANNER = f"""{WHITE}

┬─┐┌─┐┌─┐┌─┐┌─┐┬─┐┌─┐┌┬┐┌┼┐
├┬┘├┤ └─┐├┤ │  ├┬┘├┤  │ └┼┐
┴└─└─┘└─┘└─┘└─┘┴└─└─┘ ┴ └┼┘

{NC}"""

def search_in_files(directory, regex_pattern):
    regex = re.compile(regex_pattern)
    matches = []

    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    match = regex.findall(content)
                    if match:
                        matches.append((file_path, match))
            except Exception as e:
                print(f"[!] Could not read file {file_path}")

    return matches

def matche_filter(name, filter, directory):
    matches = search_in_files(directory, filter)
    for file_path, match in matches:
        print(f"[+] {RED}{name.replace('_',' ')}{NC} in {GREEN}{file_path}{NC}")


def main():

    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument("directory", help="Directory to search secrets")
    parser.add_argument("-r", "--regex", help="Json file with custom regex pattern")
    parser.add_argument("-silent", action="store_true", help="Not show banner")
    args = parser.parse_args()

    if not args.silent:
        print(BANNER)

    directory = args.directory
    main_dir = os.path.dirname(os.path.realpath(__file__))
    pathern = os.path.join(str(Path(main_dir).parent), "config", "regexes.json") if args.regex is None else args.regex

    with open(pathern) as f:
        regex_data = json.load(f)
        for name, filter in regex_data.items():
            if isinstance(filter, list):
                for f in filter:
                    matche_filter(name, f, directory)
            else:
                matche_filter(name, filter, directory)

if __name__ == "__main__":
    main()