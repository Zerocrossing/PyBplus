"""
buildTree.py
"""
import json
import indexPagePool
import bPlusTree

def build(rel, att, od):
    """
    build(rel, att, od): build a B+ tree with an order of od on search key att of relation rel.
    Returns a reference to the root page of the constructed B+_tree
    """
    # find the index number of the attribute by checking schema
    attIndex = None
    with open("../data/schemas.txt") as f:
        schemas = json.load(f)
    for tuple in schemas:
        relName = tuple[0]
        attrName = tuple[1]
        type = tuple[2]
        colPos = tuple[3]
        if relName == rel and attrName == att:
            attIndex = colPos
            break
    # scan the pagelink to get the relevant pages
    with open("../data/{}/pageLink.txt".format(rel), 'r') as f:
        leafPages = json.load(f)
    # iterate through the data pages, inserting the appropriate values into a new tree
    tree = bPlusTree.bPlusTree(rel,att,od)
    for pageName in leafPages:
        # read page
        with open ("../data/{}/{}".format(rel, pageName)) as f:
            pageData = json.load(f)
            # pages can have multiple entries
            for entryNum, entry in enumerate(pageData):
                val = entry[attIndex]
                # insert into tree
                tree.insertOne(val, pageName, entryNum)
    # write new tree information to directory
    dirData = [rel, att, tree.root]
    dirPath = "../index/directory.txt"
    with open(dirPath, 'r') as f:
        directory = json.load(f)
    directory.append(dirData)
    with open(dirPath, 'w') as f:
        json.dump(directory, f)
    # done, return root to new tree
    return tree.root


if __name__ == '__main__':
    indexPagePool.resetPool()
    print("Building Suppliers")
    suppliersTree = build("Suppliers", "sid", 2)
    # bPlusTree.printTree(suppliersTree)
    # print("Building Supply")
    # build("Supply", "pid", 2)