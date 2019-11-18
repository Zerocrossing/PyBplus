"""
display.py
"""
import bPlusTree
def displayTree(fname):
    """
    displayTree(fname): display the structure of the B+_tree with root file fname. The
    parameter fname is a plain file name under index folder. Return the plain file name for
    the file under treePic folder where the tree is displayed. Note that you are not required
    to plot a B+_tree like the ones plotted in the lecture notes. The looking can be similar to
    a nested directory hierarchy. Refer to the sample in Section 4.
    """
    bPlusTree.printTree(fname)

def displayTable(rel, fname):
    """
    display the relation instance for rel in a file with name fname.
    """
    pass
