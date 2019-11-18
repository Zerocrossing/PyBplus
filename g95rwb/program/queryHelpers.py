"""
queryHelpers.py
as the name implies, these are subfunctions so that relAlg and query operations look nicer
"""
import json
from bPlusTree import getNode


def getSchema(rel):
    """
    gets the schema for a relation in a format where each entry is (in order) [attr, type]
    so if column 2 is address, then schema[2] = ["address", "string"]
    :return: schema list
    """
    schema = []
    with open("../data/schemas.txt", 'r') as f:
        s = json.load(f)
        res = []
        for tuple in s:
            if tuple[0] == rel:
                res.append(tuple)
    schema = [None] * len(res)
    for tuple in res:
        colNum = tuple[3]
        schema[colNum] = [tuple[1], tuple[2]]
    return schema


def findEqualValueInTree(nodePage, val, cost=0):
    """
    searches a b+ tree for the value passed
    :return: a list of tuples of (dataPage, pageIndex) and the cost of the search
    eg) [("page11",0), ("page03", 1)] tells us that this value can be found on page 11, entry 0 and page 3 value 1
    will return False if no value is found
    """
    node = getNode(nodePage)
    # base case: value is either here or not in tree
    if node.get("isLeaf"):
        keys = node.get("keys")
        for n in range(0, len(keys), 3):
            nodeVal = keys[n]
            if nodeVal == val:
                ret = list(zip(keys[n + 1], keys[n + 2]))
                return ret, cost
        else:
            return [], cost
    else:
        keys = node.get("keys")
        for i in range(0, len(keys) - 1, 2):
            newPage = keys[i]
            nodeVal = keys[i + 1]
            if val <= nodeVal:
                return findEqualValueInTree(newPage, val, cost + 1)
        return findEqualValueInTree(keys[-1], val, cost + 1)


def scanTree(rootPage, val, op):
    """
    for greater or less than scans
    :return: a list of tuples of (dataPage, pageIndex) and the cost of the search
    eg) [("page11",0), ("page03", 1)] tells us that this value can be found on page 11, entry 0 and page 3 value 1
    will return False if no value is found
    """
    pass


def writeRelation(relList, relName):
    with open("../queryOutput/{}.txt".format(relName), 'w+') as f:
        json.dump(relList, f)


funcs = {
    "<": (lambda a, b: a < b),
    "<=": (lambda a, b: a <= b),
    "=": (lambda a, b: a == b),
    ">": (lambda a, b: a > b),
    ">=": (lambda a, b: a >= b),
}


def doOp(lVal, rVal, op):
    """
    helper method for string boolean operations
    ‘<’, ‘<=’, ‘=’, ‘>’, ‘>=’
    """
    return funcs[op](lVal, rVal)

