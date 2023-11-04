import pathlib
import sys

def setUtilPackagePath():
    file = pathlib.Path(__file__).resolve().parents[1]
    sys.path.append(str(file))

def t():
    pass