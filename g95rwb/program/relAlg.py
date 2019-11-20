"""
relalg.py
Includes relational algebra functions
"""
import bPlusTree
import dataPagePool
from queryHelpers import *
import json


def select(rel, att, op, val, newRelName):
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
    schema = getSchema(rel)
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
    relname = "select_{}_{}_{}".format(rel, att, val)

    dirName = "select_{}_{}_{}".format(rel, att, val)
    makeRelation(relation, schema, dirName)
    outputString = "Result of select {} {} {} on {} ".format(att, op, val, rel)
    if treeRootPage:
        outputString += " with tree:"
    else:
        outputString += " without tree:"
    printRelation(relation, dirName, outputString)
    return dirName


def project(rel, attList):
    """
    project(rel, attList): project relation rel on attributes in attList, which is a list of strings,
    corresponding to a list of attributes in relation rel. Return the name of the resulting
    relation. The schema for the resulting relation is the set of attributes in attList.
    """
    # get the column numbers of the attributes
    print("Projecting ", attList)
    schema = getSchema(rel)
    projTupleSize = len(attList)
    # attMap maps attribute column numbers from the schema to the projection
    # eg (3,2) means column 3 of the original tuple now maps to column 2 in the projection
    attMap = []
    for n, tuple in enumerate(schema):
        if tuple[0] in attList:
            map = (n, attList.index(tuple[0]))
            attMap.append(map)
    # load the pageLink and iterate over each tuple
    newRelation = []
    with open("../data/{}/pageLink.txt".format(rel)) as f:
        pages = json.load(f)
    for pageName in pages:
        with open("../data/{}/{}".format(rel,pageName)) as f:
            page = json.load(f)
            for data in page:
                proj = [None]*projTupleSize
                for map in attMap:
                    proj[map[1]] = data[map[0]]
                newRelation.append(proj)
    newRelName = "project_{}_{}".format(rel, "_".join(attList))
    outputString = "The result of projecting {} onto relation {}".format(" ".join(attList), rel)
    makeRelation(newRelation, schema, newRelName)
    printRelation(newRelation, newRelName, outputString)





def join(rel1, att1, rel2, att2):
    """
    join(rel1, att1, rel2, att2): join two relations rel1 and rel2 based on join condition rel.att1
    = rel2.att2. Returns the name of the resulting relation, with schema being the union of
    the schemas for rel1 and rel2, minus either att1 or att2.
    """
    # check if a tree exists
    print("Joining {} and {} on attributes {} and {}".format(rel1, rel2, att1, att2))
    lRel, lAtt = rel1, att1
    rRel, rAtt = rel2, att2
    lTree = bPlusTree.getTree(lRel, lAtt)
    rTree = bPlusTree.getTree(rRel, rAtt)
    newRelation = []
    # we assume right side is the tree if either of them is, so switch in case where only left side has tree
    if lTree and not rTree:
        lRel, lAtt = rel2, att2
        rRel, rAtt = rel1, att1
        lTree, rTree = rTree, lTree
    lSchema = getSchema(lRel)
    rSchema = getSchema(rRel)
    # find column numbers for left and right join attributes
    lAttCol = None
    rAttCol = None
    for n, att in enumerate(lSchema):
        if att[0] == lAtt:
            lAttCol = n
            break
    for n, att in enumerate(rSchema):
        if att[0] == rAtt:
            rAttCol = n
            break
    # if tree exists (is guaranteed to be right from above)
    if rTree:
        #iter over left relation using pageLink
        with open("../data/{}/pageLink.txt".format(lRel)) as f:
            leftPageNames = json.load(f)
        for leftPage in leftPageNames:
            with open("../data/{}/{}".format(lRel, leftPage), 'r') as f:
                lData = json.load(f)
            for lTuple in lData:
                searchVal = lTuple[lAttCol]
                # can potentially find several results
                results, cost = findEqualValueInTree(rTree,searchVal)
                if not results:
                    continue
                for rPage, entryNo in results:
                    with open("../data/{}/{}".format(rRel, rPage), 'r') as f:
                        rTuple = json.load(f)[entryNo]
                    # remove rAtt and add to results
                    del rTuple[rAttCol]
                    result = lTuple + rTuple
                    newRelation.append(result)
    # no tree
    else:
        pass
    # delete duplicate attribute from r scheme and combine them
    del rSchema[rAttCol]
    newSchema = lSchema + rSchema
    newRelName = "join_{}_{}_on_{}".format(lRel, rRel, lAtt)
    outputString = "The result of joining relations {} and {} on attributes {} and {}".format(lRel, rRel, lAtt, rAtt)
    print(newRelName)
    makeRelation(newRelation, newSchema, newRelName)
    # printRelation(newRelation, newSchema, outputString)



