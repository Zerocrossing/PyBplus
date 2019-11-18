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
    # start at root, find left or rightmost child depending
    node = getNode(rootPage)
    cost = 1
    while(not node.get("isLeaf")):
        if op[0] == "<":
            nextPage = node.get("keys")[0]
            node = getNode(nextPage)
        else:
            nextPage = node.get("keys")[-1]
            node = getNode(nextPage)
        cost+=1
    if op[0] == "<":
        nextSib = "rSibling"
    else:
        nextSib = "lSibling"
    # perform a scan left or right (depending) until OP is no longer true
    dataPages = []
    while node is not None:
        keys = node.get("keys")
        for k in range(0, len(keys), 3):
            nodeVal = keys[k]
            result = doOp(nodeVal, val, op)
            if not result:
                return dataPages, cost
            pageTuple = list(zip(keys[k + 1], keys[k + 2]))
            dataPages.extend(pageTuple)
        nextPage = node.get(nextSib)
        if nextPage is None:
            break
        node = getNode(nextPage)
        cost +=1
    return dataPages, cost



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

