"""
This file simulates a page pool system
"""
import json
import os


def getPage():
    """
    gets the next available page, removing it from the page pool
    :return:
    """
    with open("../data/pagePool.txt", 'r') as f:
        line = f.readline()
        pool = json.loads(line)
        pgStr = pool.pop()
    with open("../data/pagePool.txt", 'w') as f:
        f.write(json.dumps(pool))
    return pgStr


def releasePage(pageStr):
    """
    returns the passed page to the pool
    deletes the corresponding page file
    raises and exception if the page already exists
    """
    with open("../data/pagePool.txt", 'r') as f:
        line = f.readline()
        pool = json.loads(line)
    if pageStr in pool:
        raise Exception("Attempting to release a free page")
    pool.append(pageStr)
    with open("../data/pagePool.txt", 'w') as f:
        f.write(json.dumps(pool))
    os.remove("../data/{}".format(pageStr))
    return True


def removePage(pageStr):
    """
    removes a page from the pool
    throws an exception if the page isn't in the pool
    """
    with open("../data/pagePool.txt", 'r') as f:
        line = f.readline()
        pool = json.loads(line)
    if pageStr not in pool:
        raise Exception("Attempting to remove a nonexistent page")
    pool.remove(pageStr)
    with open("../data/pagePool.txt", 'w') as f:
        f.write(json.dumps(pool))
    return True


def removePages(pageList):
    """
    like removePage but removes a list of pages
    """
    with open("../data/pagePool.txt", 'r') as f:
        line = f.readline()
        pool = json.loads(line)
    print(pool)
    for page in pageList:
        print("Removing page: ", page)
        pool.remove(page)
    with open("../data/pagePool.txt", 'w') as f:
        f.write(json.dumps(pool))
    return True


def resetPool():
    """
    returns the pool to it's default state
    """
    for n in range(0, 99):
        fp = "../data/pg{:0>2d}.txt".format(n)
        if os.path.isfile(fp):
            os.remove(fp)
    pool = ["pg{:0>3d}.txt".format(n) for n in range(99, -1, -1)]
    poolstr = json.dumps(pool)
    with open("../data/pagePool.txt", 'w') as f:
        f.write(poolstr)


def resetData():
    """
    returns schemas to the assignment default
    deletes all folders in /data that aren't the originals
    """
    schemaDefault = [["Suppliers", "sid", "str", 0], ["Suppliers", "sname", "str", 1],
                     ["Suppliers", "address", "str", 2], ["Products", "pid", "str", 0], ["Products", "pname", "str", 1],
                     ["Products", "color", "str", 2], ["Supply", "sid", "str", 0], ["Supply", "pid", "str", 1],
                     ["Supply", "cost", "int", 2]]
    with open("../data/schemas.txt", 'w') as f:
        json.dump(schemaDefault, f)
    for dirName in os.listdir("../data"):
        if os.path.isdir("../data/{}".format(dirName)):
            if dirName not in ["Products","Suppliers", "Supply"]:
                for fileName in os.listdir("../data/{}".format(dirName)):
                    filePath = "../data/{}/{}".format(dirName, fileName)
                    os.remove(filePath)
                os.rmdir("../data/{}".format(dirName))


if __name__ == '__main__':
    """
    running this file as a main file will remove all index pages from the directory, reset the schema
    and return the pool to its default state
    """
    resetPool()
    resetData()