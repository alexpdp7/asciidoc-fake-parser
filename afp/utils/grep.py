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

    for file in args.file:
        try:
            parsed = afp.asciidoc_fake_parse(file, silence_asciidoctor=True)
        except:
            print("Error parsing:", str(file), file=sys.stderr, flush=True)
            continue
        for elem in parsed:
            for pattern in patterns:
                for match in pattern.findall(elem["text"]):
                    print("\t".join(map(str, [elem["path"], str(file), elem["start"], match, repr(elem["text"])])))
