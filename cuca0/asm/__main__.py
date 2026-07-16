from __future__ import annotations
from abc import ABC, abstractmethod
from typing import NamedTuple
from sys import argv
import re

ROM_SIZE = 256


def main() -> None:
    assert len(argv) == 2
    input_file = argv[1]
    with open(input_file, "r", encoding="utf-8") as fd:
        print(parse(fd.read()))


def parse(input: str) -> bytearray:
    labels = {}
    addr = 0
    to_gen = []

    result = bytearray(ROM_SIZE)

    for line_ in input.split("\n"):
        line = line_.strip()
        if line == "":
            pass
        elif line[0] == ";":
            pass  # skip comment
        elif (lb := parse_label(line)) is not None:
            if lb in labels:
                raise ValueError(f"label {repr(lb)} defined more than once")
            else:
                labels[lb] = addr
        elif (vd := parse_var_decl(line)) is not None:
            lb, val = vd
            if lb in labels:
                raise ValueError(f"label {repr(lb)} defined more than once")
            else:
                labels[lb] = addr
                result[addr] = val
                addr += 1
        elif (instr := parse_instr(line, addr)) is not None:
            to_gen.append(instr)
            addr += instr.size()
        else:
            raise ValueError(f"could not parse line: {repr(line)}")

    for instr in to_gen:
        instr.gen(labels, result)
    return result


class Instr:
    def __init__(
        self, template: bytes, args_fill: list[tuple[int, str]], addr: int
    ) -> None:
        self.template = template
        self.args_fill = args_fill
        self.addr = addr

    def size(self) -> int:
        return len(self.template)

    def gen(self, labels: dict[str, int], result: bytearray) -> None:
        for i in range(self.size()):
            result[self.addr + i] = self.template[i]
        for i, l in self.args_fill:
            result[self.addr + i] = labels[l]


LABEL_RE = re.compile(r"^\s*([A-Za-z_][A-Za-z0-9_]*)\s*:\s*$")
VAR_DECL_START_RE = re.compile(r"^\s*\.var\s")
WORD_RE = re.compile(r"^([A-Za-z_][A-Za-z0-9_]*)")
INT_RE = re.compile(r"^([+-]?\d+)")
WHITESPACE_RE = re.compile(r"^\s+")


def parse_label(s: str) -> str | None:
    m = re.match(LABEL_RE, s)
    if m is None:
        return None
    return m.group(1)


def parse_var_decl(s: str) -> tuple[str, int] | None:
    m = re.match(VAR_DECL_START_RE, s)
    if m is None:
        return None
    s = s[m.end() :]

    s = skip_whitespace(s)
    s, w = parse_word(s)
    if w is None:
        return None

    s = skip_whitespace(s)
    s, x = parse_int(s)
    if x is None:
        return None

    s = skip_whitespace(s)
    if len(s) != 0:
        return None

    return (w, x)


def parse_instr(s: str, addr: int) -> Instr | None:
    return (
        parse_imm_instr(s, 0, "ldi", addr)
        or parse_imm_instr(s, 1, "add", addr)
        or parse_imm_instr(s, 2, "sub", addr)
        or parse_imm_instr(s, 3, "read", addr)
        or parse_imm_instr(s, 4, "write", addr)
        or parse_0arg_instr(s, 0x0C, "halt", addr)
        or None
    )


def parse_0arg_instr(s: str, opcode: int, name: str, addr: int) -> Instr | None:
    s = skip_whitespace(s)
    s, w = parse_word(s)
    if w != name:
        return None
    return Instr(template=opcode.to_bytes(length=1), args_fill=[], addr=addr)


def parse_imm_instr(s: str, opcode: int, name: str, addr: int) -> Instr | None:
    s = skip_whitespace(s)
    s, w = parse_word(s)
    if w != name:
        return None

    template = bytearray(2)
    template[0] = opcode
    fill = []

    s = skip_whitespace(s)
    s, w = parse_word(s)
    if w is not None:
        fill.append((1, w))
    else:
        s, x = parse_int(s)
        if x is not None:
            template[1] = x
        else:
            return None

    s = skip_whitespace(s)
    if len(s) != 0:
        return None

    return Instr(template=bytes(template), args_fill=fill, addr=addr)


def skip_whitespace(s: str) -> str:
    m = re.match(WHITESPACE_RE, s)
    if m is None:
        return s
    s = s[m.end() :]
    return s


def parse_int(s: str) -> tuple[str, int | None]:
    m = re.match(INT_RE, s)
    if m is None:
        return (s, None)
    return (s[m.end() :], int(m.group(1)))


def parse_word(s: str) -> tuple[str, str | None]:
    m = re.match(WORD_RE, s)
    if m is None:
        return (s, None)
    return (s[m.end() :], m.group(1))


if __name__ == "__main__":
    main()
