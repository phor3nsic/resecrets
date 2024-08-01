import re
import os
import json
import sys
import argparse

from pathlib import Path

MAIN_DIR = os.path.dirname(os.path.realpath(__file__))
RED='\033[0;31m'
WHITE='\033[0;37m'
GREEN='\033[0;32m'
NC='\033[0m'
SILENT = False

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
                    for match in regex.finditer(content):
                        full_match = match.group()
                        matches.append((file_path, full_match))
            except UnicodeDecodeError:
                pass
            except Exception as e:
                print(f"[!] An unexpected error occurred: {e}")
                raise

    return matches

def matche_filter(name, filter, directory):
    matches = search_in_files(directory, filter)
    for file_path, match in matches:
        if SILENT == False:
            print(f"[+] {RED}{name.replace('_', ' ')}{NC}: {GREEN}{match}{NC} in {file_path}")
        else: 
            print(f"[+] {name.replace('_', ' ')}: {match} in {file_path}")

def search(pathern, directory):
    with open(pathern) as f:
        regex_data = json.load(f)
        for name, filter in regex_data.items():
            if isinstance(filter, list):
                for f in filter:
                    matche_filter(name, f, directory)
            else:
                matche_filter(name, filter, directory)

def main():
    global SILENT

    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument("directory", help="Directory to search secrets")
    parser.add_argument("-r", "--regex", help="Json file with custom regex pattern")
    parser.add_argument("-silent", action="store_true", help="Not show banner")
    args = parser.parse_args()

    SILENT = args.silent
    
    if SILENT == False:
        print(BANNER)

    directory = args.directory
    pathern = os.path.join(str(Path(MAIN_DIR).parent), "config", "regexes.json") if args.regex is None else args.regex

    search(pathern, directory)

if __name__ == "__main__":
    main()