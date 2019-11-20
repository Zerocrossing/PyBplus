"""
remove.py
"""
import json
import bPlusTree
import os

def removeTree(rel, att):
    """
    removeTree(rel, att): remove the B+-tree on rel.att from the system. Its entry in the
    directory is deleted and all the pages occupied are returned to the page pool. If the
    B+_tree does not exist, do nothing
    """
    with open("../index/directory.txt") as f:
        directory = json.load(f)
        for drel, datt, page in directory:
            if rel == drel and datt==att:
                bPlusTree.deleteTree(page)
                directory.remove([drel, datt, page])
                break
    with open("../index/directory.txt", 'w') as f:
        json.dump(directory, f)



def removeTable(rel):
    """
    removeTable(rel): Remove the relation rel from the system. Its entry in the catalog is
    deleted and all the pages occupied are returned to the page pool. If the relation does not
    exist, do nothing
    """
    if os.path.isdir("../data/{}".format(rel)):
        for fileName in os.listdir("../data/{}".format(rel)):
            filePath = "../data/{}/{}".format(rel, fileName)
            os.remove(filePath)
        os.rmdir("../data/{}".format(rel))
    with open("../data/schemas.txt", 'r') as f:
        schema = json.load(f)
    newSchema = []
    for tuple in schema:
        if tuple[0] == rel:
            continue
        else:
            newSchema.append(tuple)
    with open("../data/schemas.txt", 'w') as f:
        json.dump(newSchema, f)

