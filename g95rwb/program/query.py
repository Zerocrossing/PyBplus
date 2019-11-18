"""
query.py
Include into file query.py under program folder the specifications for the following queries
using the three relational algebra functions you create. Then run this file on the provided
database, and use function displayTable(*) to send the resulting relations to file
queryResult.txt.
a. Find the name for the supplier ‘s23’ when a B+_tree exists on Suppliers.sid.
b. Remove the B+_tree from Suppliers.sid, and repeat Question a.
c. Find the address of the suppliers who supplied ‘p15’.
d. What is the cost of ‘p20’ supplied by ‘Kiddie’?
e. For each supplier who supplied products with a cost of 47 or higher, list his/her name,
product name and the cost.
"""
import buildTree
import display
import remove
import relAlg
import indexPagePool

if __name__ == '__main__':
    # reset pools
    indexPagePool.resetPool()
    # Run build(*) on the provided data set, and create two B+_trees with an order of 2, one on
    # Suppliers.sid, and the other on Supply.pid
    suppliersTree = buildTree.build("Suppliers", "sid", 2)
    supplyTree = buildTree.build("Supply", "pid", 2)
    # Run displayTree(*) to display the structures of the two B+_trees you create under item 6
    # above. They should be displayed in files Suppliers_sid.txt and Supply_pid.txt, respectively,
    # under folder treePic

    # display.displayTree(suppliersTree)
    # display.displayTree(supplyTree)

    # question a
    relAlg.select("Supply", "sid", "<", "s23")

    # question b
    # remove.removeTree("Suppliers", "sid")
    # relAlg.select("Suppliers", "sid", "=", "s23")
    # question c
