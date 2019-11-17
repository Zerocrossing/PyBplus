"""
relalg.py
Includes relational algebra functions
"""
import bPlusTree
def select(rel, att, op, val):
    """
    select(rel, att, op, val): Select tuples from relation rel which meet a select condition. The
    select condition is formed by att, op, and val, where att is an attribute in rel, op is one of
    the six strings, ‘<’, ‘<=’, ‘=’, ‘>’, ‘>=’, corresponding respectively to the comparison
    operators, <, ≤, =, >, , and val is a value. Returns the name of the resulting relation. The
    schema for the resulting relation is identical to that for rel.
    """
    tree = bPlusTree.getTree(rel,att)
    cost = 0
    if tree:
        print("With tree the cost of selecting {} {} {} on {} is {}".format(att, op, val, rel, cost))
    else:
        print("Without tree the cost of selecting {} {} {} on {} is {}".format(att, op, val, rel, cost))
    pass

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

