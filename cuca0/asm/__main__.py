from __future__ import annotations
from sys import argv

def main() -> None:
    assert len(argv) == 2
    input_file = argv[1]
    with open(input_file, "r", encoding="utf-8") as fd:
        parse(fd.read())

def parse(input: str) -> None:
    for line in input.split("\n"):
        print(line)

if __name__ == "__main__":
    main()
