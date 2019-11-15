"""
fileOps.py
Utility file for reading and writing files
"""
import json

def getAttrs(rel):
    """
    when run on an
    """
    with open("../data/schemas.txt") as f:
        schemas = json.load(f);
    for relName, atrName, type, pos in schemas:
        print(relName, atrName, type, pos)


if __name__ == '__main__':
    getAttrs("suppliers")