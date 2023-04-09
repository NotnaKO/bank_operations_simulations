import pathlib

from pylint import run_pyreverse


class SpacesInPathWithPyreverse(Exception):
    pass


def make_uml():
    print("Starting creating UML file")
    path = pathlib.Path(__file__).parent.resolve()
    path_with_code = path.parent / "src"
    run_pyreverse(
        (f"{path_with_code}",
         "-o=puml", "--all-ancestors", "--all-associated", "--colorized"))


if __name__ == '__main__':
    make_uml()
