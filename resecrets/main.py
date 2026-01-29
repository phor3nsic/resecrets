import argparse
import json
import os
import re
from typing import Dict, Iterable, List

from pathlib import Path

MAIN_DIR = os.path.dirname(os.path.realpath(__file__))
RED = "\033[0;31m"
WHITE = "\033[0;37m"
GREEN = "\033[0;32m"
NC = "\033[0m"

BANNER = f"""{WHITE}

┬─┐┌─┐┌─┐┌─┐┌─┐┬─┐┌─┐┌┬┐┌┼┐
├┬┘├┤ └─┐├┤ │  ├┬┘├┤  │ └┼┐
┴└─└─┘└─┘└─┘└─┘┴└─└─┘ ┴ └┼┘

{NC}"""

def search_in_files(directory: str, regex_pattern: str) -> List[Dict[str, str]]:
    regex = re.compile(regex_pattern)
    matches = []

    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    for match in regex.finditer(content):
                        full_match = match.group()
                        matches.append({"file": file_path, "match": full_match})
            except UnicodeDecodeError:
                pass
            except Exception as e:
                raise RuntimeError(f"Unexpected error while reading {file_path}: {e}") from e

    return matches

def match_filter(name: str, regex_pattern: str, directory: str) -> List[Dict[str, str]]:
    matches = search_in_files(directory, regex_pattern)
    return [
        {"name": name, "match": entry["match"], "file": entry["file"]}
        for entry in matches
    ]

def search(pattern_path: str, directory: str) -> List[Dict[str, str]]:
    with open(pattern_path) as f:
        regex_data = json.load(f)
    results: List[Dict[str, str]] = []
    for name, regex_pattern in regex_data.items():
        if isinstance(regex_pattern, list):
            for pattern in regex_pattern:
                results.extend(match_filter(name, pattern, directory))
        else:
            results.extend(match_filter(name, regex_pattern, directory))
    return results

def format_matches(matches: Iterable[Dict[str, str]], use_color: bool = True) -> List[str]:
    lines = []
    for entry in matches:
        name = entry["name"].replace("_", " ")
        match = entry["match"]
        file_path = entry["file"]
        if use_color:
            lines.append(f"[+] {RED}{name}{NC}: {GREEN}{match}{NC} in {file_path}")
        else:
            lines.append(f"[+] {name}: {match} in {file_path}")
    return lines

def main() -> List[Dict[str, str]]:

    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument("directory", help="Directory to search secrets")
    parser.add_argument("-r", "--regex", help="Json file with custom regex pattern")
    parser.add_argument("-silent", action="store_true", help="Not show banner")
    parser.add_argument("--json", action="store_true", help="Output results as JSON")
    parser.add_argument("--no-color", action="store_true", help="Disable ANSI colors")
    args = parser.parse_args()

    if not args.silent:
        print(BANNER)

    directory = args.directory
    pattern_path = (
        os.path.join(str(Path(MAIN_DIR).parent), "config", "regexes.json")
        if args.regex is None
        else args.regex
    )

    results = search(pattern_path, directory)

    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        for line in format_matches(results, use_color=not args.no_color):
            print(line)

    return results

if __name__ == "__main__":
    main()
