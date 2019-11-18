"""
relalg.py
Includes relational algebra functions
"""
import bPlusTree
import dataPagePool
from queryHelpers import *
import json


def select(rel, att, op, val):
    """
    select(rel, att, op, val): Select tuples from relation rel which meet a select condition. The
    select condition is formed by att, op, and val, where att is an attribute in rel, op is one of
    the six strings, ‘<’, ‘<=’, ‘=’, ‘>’, ‘>=’, corresponding respectively to the comparison
    operators, <, ≤, =, >, , and val is a value. Returns the name of the resulting relation. The
    schema for the resulting relation is identical to that for rel.
    """
    treeRootPage = bPlusTree.getTree(rel, att)
    cost = 0
    relation = []
    # tree exists
    if treeRootPage:
        # equality search
        if op == "=":
            dataPages, searchCost = findEqualValueInTree(treeRootPage, val)
            cost += searchCost
        # leq and geq
        else:
            dataPages, searchCost = scanTree(treeRootPage, val, op)
            print("Less than or greater than search...")
        # we have a list of data pages and entry numbers, fetch the pages and write the data to the new relation
        for tuple in dataPages:
            cost = cost + 1
            dataPage = tuple[0]
            entryNo = tuple[1]
            with open("../data/{}/{}".format(rel, dataPage)) as f:
                data = json.load(f)[entryNo]
                relation.append(data)
        print("With tree the cost of selecting {} {} {} on {} is {}".format(att, op, val, rel, cost))
    # No Tree
    else:
        # find which column value the att is in
        schema = getSchema(rel)
        for n, schemaVal in enumerate(schema):
            newAtt = schemaVal[0]
            if att == newAtt:
                attNum = n
                break
        else:
            raise Exception("Attribute {} not found in relation {}".format(att, rel))
        # get pageLink for iterating
        with open("../data/{}/pageLink.txt".format(rel), 'r') as f:
            pages = json.load(f)
        # read pages, increase cost, do operation
        for page in pages:
            cost += 1
            with open("../data/{}/{}".format(rel, page), 'r') as f:
                data = json.load(f)
                for tuple in data:
                    newVal = tuple[attNum]
                    isValid = doOp(val, newVal, op)
                    if isValid:
                        relation.append(tuple)
        print("Without tree the cost of selecting {} {} {} on {} is {}".format(att, op, val, rel, cost))
    # we should have our relation now, write it
    relname = "{}_{}_{}".format(rel, att, val)
    if treeRootPage:
        relname += "_with_tree"
    else:
        relname += "_no_tree"
    writeRelation(relation, relname)


def project(rel, attList):
    """
    project(rel, attList): project relation rel on attributes in attList, which is a list of strings,
    corresponding to a list of attributes in relation rel. Return the name of the resulting
    relation. The schema for the resulting relation is the set of attributes in attList.
    """
    pass


def join(rel1, att1, rel2, att2):
    """
    join(rel1, att1, rel2, att2): join two relations rel1 and rel2 based on join condition rel.att1
    = rel2.att2. Returns the name of the resulting relation, with schema being the union of
    the schemas for rel1 and rel2, minus either att1 or att2.
    """
    pass
