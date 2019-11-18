"""
A class representing a B+ tree
"""
import json
import indexPagePool


# region node functions
def makeNode(isLeaf=None, parentPage=None, lSibling=None, rSibling=None, keys=[]):
    """
    creates a node, and requests a new page from the index page pool to store it in
    :return: tuple (node, page)
    """
    page = indexPagePool.getPage()
    n = {
        "isLeaf": isLeaf,
        "parentPage": parentPage,
        "lSibling": lSibling,
        "rSibling": rSibling,
        "keys": keys
    }
    f = open("../index/{}".format(page), 'w+')
    json.dump(n, f)
    f.close()
    return n, page


def writeNode(node, page):
    """
    writes the contents of node to the page
    used after changing a node's information
    note: node is a node object, not a reference to the node page
    """
    f = open("../index/{}".format(page), 'w+')
    json.dump(node, f)
    f.close()
    return True


def getNode(pageStr):
    """
    returns the python representation of a node from it's page path
    """
    with open("../index/{}".format(pageStr), 'r') as f:
        node = json.load(f)
    return node


def nodeOverfull(pageStr, order):
    """
    returns whether or not a given node is full
    """
    node = getNode(pageStr)
    # for leaf nodes the number of entries is the size of "keys"/3 because each key has 3 parts: (val,page,num)
    if node.get("isLeaf"):
        n = len(node.get("keys")) // 3
    # for internal nodes the size is the number of keys, which is (n-1)/2
    else:
        n = (len(node.get("keys")) - 1) // 2
    return n > order * 2


def addValToNode(valList, nodePage):
    """
    adds values to a node, may cause node to go over capacity
    leaf list contains [val, dataPage, entryNum]
    internal list contains [val, indexPage]
    writes node to disk regardless of new size
    """
    node = getNode(nodePage)
    nodeKeys = node["keys"]
    # print("adding {} to {} now has {} entries".format(valList, nodePage, len(nodeKeys)))
    newVal = valList[0]
    inserted = False
    # insert new value in appropriate place
    if node.get("isLeaf"):
        # print(nodePage, " is a leaf node")
        # print(nodeKeys)
        for n in range(0, len(nodeKeys), 3):
            nodeVal = nodeKeys[n]
            if newVal == nodeVal:
                # print("Duplicate entry", valList)
                # print("Existing entry", nodeKeys[n+1])
                # add existing value to list
                nodeKeys[n + 1].append(valList[1][0])
                nodeKeys[n + 2].append(valList[2][0])
                inserted = True
                break
            if newVal < nodeVal:
                # print("adding new value of {} in position {}".format(newVal, n))
                for j in range(2, -1, -1):
                    nodeKeys.insert(n, valList[j])
                inserted = True
                break
        if not inserted:  # new value is largest, append to end
            # print("adding new value of {} to the end".format(newVal))
            node["keys"].extend(valList)
    else:
        # print(nodePage, " is an internal node containing ", nodeKeys)
        # print("To which we are adding ", valList)
        newPage = valList[1]
        for i in range(0, len(nodeKeys) - 1, 2):
            nodeVal = nodeKeys[i + 1]
            if newVal == nodeVal:
                # print("attempting to add internal value of {} on {} to node {}".format(newVal, newPage, nodeKeys))
                break
            if newVal <= nodeVal:
                # print("#"*25)
                # print("New val of {} is less than {}, inserting {} into pos {}".format(newVal, nodeVal, newPage, i))
                # print("Keys before insertion: ", nodeKeys)
                nodeKeys.insert(i+1, newPage)  # page
                nodeKeys.insert(i+1, newVal)  # val
                break
        else:
            node["keys"].append(newVal)
            node["keys"].append(newPage)
    writeNode(node, nodePage)


def partitionFullNodeValues(nodePage, order):
    """
    takes a node and returns the left, right, and center keys
    used when splitting nodes
    :return:
    """
    node = getNode(nodePage)
    # leaf nodes use groupings of 3
    keys = node["keys"]
    if node.get("isLeaf"):
        midStart = ((order * 2 + 1) // 2) * 3
        lVals = keys[0:midStart + 3]
        midVals = keys[midStart:midStart + 3]
        rVals = keys[midStart + 3:]
        # print("OG: ", keys)
        # print(lVals)
        # print(midVals)
        # print(rVals)
        return (lVals, midVals, rVals)

    # if the node is internal, the midval is just the singlular middle value and is not included in the remaining nodes
    else:
        # print("This node is not a leaf node:", nodePage, node)
        midPoint = (len(keys) // 2) + 1
        lVals = keys[0:midPoint - 1]
        rVals = keys[midPoint:]
        midVals = keys[midPoint - 1]
        # print("OG: ", keys)
        # print(lVals)
        # print(midVals)
        # print(rVals)
        return (lVals, midVals, rVals)


def updateParentsofChildren(nodePage):
    """
    When a node splits its children need to be updated
    by definition this node cannot be a leaf
    """
    node = getNode(nodePage)
    if node.get("isLeaf"):
        raise Exception("Attempting to update children of a leaf node")
    for n, val in enumerate(node.get("keys")):
        if n % 2 == 0:
            child = getNode(val)
            child["parentPage"] = nodePage
            writeNode(child, val)


# endregion

# region tree functions
class bPlusTree:
    def __init__(self, rel, atr, order):
        self.root = None
        self.order = order
        self.rel = rel
        self.atr = atr

    def insertOne(self, val, dataPage, entryNum):
        """
        inserts a new value into the tree
        :param val: key value
        :param dataPage: page string (from data, not index)
        :param entryNum: which entry in the page the value is associated with
        :return: reference to the leaf page where the value was stored
        """
        # create root if this is first entry
        dataPage = [dataPage]
        entryNum = [entryNum]
        if self.root is None:
            keys = [val, dataPage, entryNum]
            node, indexPage = makeNode(isLeaf=True, keys=keys)
            self.root = indexPage
            return indexPage
        # find the appropriate location for insertion and add value
        leafPage = self.findLeafForVal(val, self.root)
        vals = [val, dataPage, entryNum]
        addValToNode(vals, leafPage)
        # insertion may cause node to go over capacity
        if nodeOverfull(leafPage, self.order):
            self.splitNode(leafPage)
        # print("Added {}, {}".format(val, dataPage))
        # printTree(self.root)
        # print("*" * 10)

    def findLeafForVal(self, val, nodePage):
        """
        Finds the appropriate leaf node for a value
        is NOT a search, as the value may not exist
        this lets us use this function for search and insertion
        """
        node = getNode(nodePage)
        if node.get("isLeaf"):
            return nodePage
        keys = node.get("keys")
        for i in range(0, len(keys) - 1, 2):
            nodePage = keys[i]
            nodeVal = keys[i + 1]
            if val <= nodeVal:
                return self.findLeafForVal(val, nodePage)
        # val is larger than the last val, go to right page
        return self.findLeafForVal(val, keys[-1])

    def splitNode(self, nodePage):
        # print("Splitting", nodePage)
        if nodePage == self.root:
            self.splitRoot()
            return
        node = getNode(nodePage)
        if node.get("isLeaf"):
            # print(nodePage, "is a leaf...")
            self.splitLeaf(nodePage)
            return
        else:
            self.splitInternal(nodePage)

    def splitLeaf(self, nodePage):
        # print("Splitting leaf")
        node = getNode(nodePage)
        # print("OG: ", node.get("keys"))
        # split node in half
        # print("\nSplitting node ")
        lVals, midVals, rVals = partitionFullNodeValues(nodePage, self.order)
        newNodeKeys = rVals
        # create new node, pair siblings
        parentPage = node.get("parentPage")
        rSibling = node.get("rSibling")
        newNode, newNodePage = makeNode(isLeaf=True, parentPage=parentPage, lSibling=nodePage, rSibling=rSibling,
                                        keys=newNodeKeys)
        node["rSibling"] = newNodePage
        node["keys"] = lVals
        # assign lsibling of former rsibling to be new node
        if rSibling is not None:
            rsibNode = getNode(rSibling)
            rsibNode["lSibling"] = newNodePage
            writeNode(rsibNode, rSibling)
        # insert key into parent
        # print("Adding {}, {} to parent".format(midVals[0], newNodePage))
        parentVals = [midVals[0], newNodePage]
        writeNode(node, nodePage)
        writeNode(newNode, newNodePage)
        # print("after Split {} contains \n{}".format(nodePage, node["keys"]))
        # print("new node {} contains \n{}".format(newNodePage, newNodeKeys))
        addValToNode(parentVals, parentPage)
        if nodeOverfull(parentPage, self.order):
            # print("Split has caused parent to be overfull")
            self.splitNode(parentPage)

    def splitInternal(self, nodePage):
        node = getNode(nodePage)
        # print("Splitting internal node")
        # partition data
        lVals, midVals, rVals = partitionFullNodeValues(nodePage, self.order)
        # print("L ", lVals)
        # print("M ", midVals)
        # print("R ", rVals)
        # make new node, assign data split
        newNode, newPage = makeNode(isLeaf=False, parentPage=node.get("parentPage"), keys=rVals)
        node["keys"] = lVals
        writeNode(node, nodePage)
        # bubble up middle value to parent
        addValToNode([midVals, newPage], node.get("parentPage"))

    def splitRoot(self):
        """
        Splits a root note, has special cases apart from other nodes
        """
        root = getNode(self.root)
        if root.get("isLeaf"):
            self.splitLeafRoot()
            return
        # print("Splitting a non-leaf root")
        lVals, midVals, rVals = partitionFullNodeValues(self.root, self.order)
        # print(lVals, midVals, rVals)
        # make 2 new pages
        leftNode, leftPage = makeNode(isLeaf=False, parentPage=self.root, keys=lVals)
        rightNode, rightPage = makeNode(isLeaf=False, parentPage=self.root, keys=rVals)
        # change root values
        root["keys"] = [leftPage, midVals, rightPage]
        writeNode(root, self.root)
        updateParentsofChildren(leftPage)
        updateParentsofChildren(rightPage)

    def splitLeafRoot(self):
        """
        helper for splitroot for when the root is also a leaf node
        """
        root = getNode(self.root)
        # print("Splitting leafroot")
        lVals, midVals, rVals = partitionFullNodeValues(self.root, self.order)
        # we can "recycle" the root page by reassigning the keys
        # print("L:\n", lVals)
        # print("M:\n", midVals)
        # print("R:\n", rVals)
        root["isLeaf"] = False
        # we need to add the middle leaf value to the left side
        # left because we are using leq for search
        lNode, lNodePage = makeNode(isLeaf=True, parentPage=self.root, keys=lVals)
        rNode, rNodePage = makeNode(isLeaf=True, parentPage=self.root, keys=rVals)
        # we need to declare the leafs as siblings using their page references
        # additionally, the root needs to be updated to have the proper 2-value keys
        lNode["rSibling"] = rNodePage
        rNode["lSibling"] = lNodePage
        writeNode(lNode, lNodePage)
        writeNode(rNode, rNodePage)
        root["keys"] = [lNodePage, midVals[0], rNodePage]
        # print("Split root", root)
        writeNode(root, self.root)


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


def printTree(rootPage, indent=0):
    node = getNode(rootPage)
    keys = node.get("keys")
    if node.get("isLeaf"):
        print("\t" * indent + rootPage + ", parent:", node.get("parentPage")," lsib:{}, rsib:{} ".format(node.get("lSibling"), node.get("rSibling")), keys)
    else:
        print("\t" * indent + rootPage + ", par:", node.get("parentPage"), keys)
        children = [val for n, val in enumerate(keys) if n % 2 == 0]
        for child in children:
            printTree(child, indent + 1)


def deleteTree(nodePage):
    node = getNode(nodePage)
    keys = node.get("keys")
    if node.get("isLeaf"):
        indexPagePool.releasePage(nodePage)
    else:
        children = [val for n, val in enumerate(keys) if n % 2 == 0]
        indexPagePool.releasePage(nodePage)
        for child in children:
            deleteTree(child)

# endregion

if __name__ == '__main__':
    indexPagePool.releasePage("pg02.txt")
    # node, page = makeNode()
    # node["isLeaf"] = True
    # writeNode(node, page)
    # print(json.dumps(node))
