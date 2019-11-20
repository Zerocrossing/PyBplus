"""
display.py
"""
import bPlusTree
import json


def displayTree(rootFile, outputFileName):
    """
    displayTree(fname): display the structure of the B+_tree with root file fname. The
    parameter fname is a plain file name under index folder. Return the plain file name for
    the file under treePic folder where the tree is displayed. Note that you are not required
    to plot a B+_tree like the ones plotted in the lecture notes. The looking can be similar to
    a nested directory hierarchy. Refer to the sample in Section 4.
    """
    str = bPlusTree.printTree(rootFile)
    with open("../treePic/{}".format(outputFileName), 'w+') as f:
        f.write(str)
    return


def displayTable(rel, fname):
    """
    display the relation instance for rel in a file with name fname.
    """
    # writeStr = "\nShowing relation {}\n".format(rel)
    writeStr = ""
    with open("../data/{}/pageLink.txt".format(rel)) as f:
        pages = json.load(f)
    for pageName in pages:
        with open("../data/{}/{}".format(rel,pageName)) as f:
            data = json.load(f)
            for tuple in data:
                for entry in tuple:
                    writeStr += "|{}\t".format(entry)
                writeStr+='\n'
    with open("../queryOutput/{}".format(fname), 'a+') as f:
        f.write(writeStr)

