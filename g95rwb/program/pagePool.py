"""
This file simulates a page pool system
"""
import json

def getPage():
    """
    gets the next available page, removing it from the page pool
    :return:
    """
    with open("../index/pagePool.txt", 'r') as f:
        line = f.readline()
        pool = json.loads(line)
        pgStr = pool.pop()
    with open("../index/pagePool.txt", 'w') as f:
        f.write(json.dumps(pool))
    return pgStr


def releasePage(pageStr):
    with open("../index/pagePool.txt", 'r') as f:
        line = f.readline()
        pool = json.loads(line)
    if pageStr in pool:
        raise Exception("Attempting to release a free page")
    pool.append(pageStr)
    with open("../index/pagePool.txt", 'w') as f:
        f.write(json.dumps(pool))
    return True

def resetPool():
    """
    returns the pool to it's default state
    """
    pool = ["pg{:0>2d}.txt".format(n) for n in range(99,-1,-1)]
    poolstr = json.dumps(pool)
    with open("../index/pagePool.txt", 'w') as f:
        f.write(poolstr)

if __name__ == '__main__':
    resetPool()


