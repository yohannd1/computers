from sys import argv, executable, platform
from os import chdir, environ, name as os_name
from pathlib import Path
from subprocess import run

MYPY_OPTS = ["--strict", "--cache-fine-grained", "--explicit-package-bases"]


def main(args: list[str]) -> None:
    here = Path(args[0]).parent
    chdir(here)

    assert len(args) > 1
    cmd = args[1]

    if cmd == "check":
        assert len(args) in {2, 3}
        folder_to_check = "asm" if len(args) == 2 else args[2]
        run(["mypy", *MYPY_OPTS, folder_to_check])
    elif cmd == "format":
        assert len(args) == 2
        run(["black", "."])
    elif cmd == "test":
        assert len(args) == 2
        run([executable, "-m", "asm", "input.asm"])
    else:
        print(f"Ação desconhecida: {repr(cmd)}")


if __name__ == "__main__":
    main(argv)
