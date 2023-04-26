import os
import sys

from static_analyze.consistence import check_consistence


def check_requirements():
    ver = sys.version_info
    try:
        assert ver.major == 3 and ver.minor >= 11
    except AssertionError:
        print("Нужно установить python версии не ниже 3.11")
        raise
    print("Starting installing requirements")
    # os.system("python -m pip install --upgrade pip")
    os.system("pip install -r requirements.txt")


def make_uml_function():
    from uml.make_uml import make_uml
    make_uml()


if __name__ == '__main__':
    check_requirements()
    make_uml_function()
    check_consistence()
    print("Setup completed!")
