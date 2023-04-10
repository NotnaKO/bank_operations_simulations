import pathlib

from pylint import run_pylint


def test_code_style():
    path = pathlib.Path(__file__).parent.resolve()
    path_with_code = path.parent / "src/"
    # run_pylint(argv=[f"{path_with_code}"])
    run_pylint(
        argv=[f"{path_with_code}",
              "--disable=missing-module-docstring, missing-class-docstring, "
              "missing-function-docstring, too-few-public-methods"])
