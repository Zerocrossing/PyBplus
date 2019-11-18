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
    for n in range(0,99):
        fp = "../data/pg{:0>2d}.txt".format(n)
        if os.path.isfile(fp):
            os.remove(fp)
    pool = ["pg{:0>3d}.txt".format(n) for n in range(99,-1,-1)]
    poolstr = json.dumps(pool)
    with open("../data/pagePool.txt", 'w') as f:
        f.write(poolstr)

if __name__ == '__main__':
    """
    running this file as a main file will remove all index pages from the directory
    and return the pool to its default state
    """
    resetPool()


