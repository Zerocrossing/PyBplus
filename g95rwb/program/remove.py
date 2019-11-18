"""
remove.py
"""
import json
import bPlusTree

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
    pass
