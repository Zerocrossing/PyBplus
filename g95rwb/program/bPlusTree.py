"""
A class representing a B+ tree
"""
import json


def getTree(relName, keyAttr):
    """
    getTree returns the root page of a B+ tree for the passed relation and attribute if one exists
    Else returns false
    """
    with open("../index/directory.txt") as f:
        schemas = json.load(f)
    for rel, attr, rootDir in schemas:
        if rel == relName and attr == keyAttr:
            return rootDir
    return False
