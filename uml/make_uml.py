import os
import pathlib

from pylint import run_pyreverse


def make_uml():
    print("Starting creating UML file")
    path = pathlib.Path(__file__).parent.resolve()
    path_with_code = path.parent / "src"
    os.chdir(path)
    run_pyreverse(
        (f"{path_with_code}",
         "-o=puml", "--all-ancestors", "--all-associated", "--filter-mode=ALL", "--colorized"))


if __name__ == '__main__':
    make_uml()
