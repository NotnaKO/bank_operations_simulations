import os
import sys

from uml.make_uml import make_uml

ver = sys.version_info
try:
    assert ver.major >= 3 and ver.minor >= 11
except AssertionError:
    print("Нужно установить python версии не ниже 3.11")
    raise
print("Starting installing requirements")
os.system("python.exe -m pip install --upgrade pip")
os.system("pip install -r requirements.txt")

make_uml()
# os.system("cls" if os.name == "nt" else "clear")
print("Setup completed!")
