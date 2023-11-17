import argparse
import pathlib
import re
import sys

import afp


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pattern", action="append")
    parser.add_argument("file", type=pathlib.Path, nargs="*")
    args = parser.parse_args()

    patterns = [re.compile(p) for p in args.pattern]

    unparsed = []

    for file in args.file:
        try:
            parsed = afp.asciidoc_fake_parse(file, silence_asciidoctor=True)
        except:
            unparsed.append(file)
            continue
        for elem in parsed:
            matched = []
            for pattern in patterns:
                if pattern.search(elem["text"]):
                    matched.append(pattern)
            if matched:
                print(elem["path"], elem["start"], matched, repr(elem["text"]))

    if unparsed:
        print("Not parsed", unparsed, file=sys.stderr, flush=True)
