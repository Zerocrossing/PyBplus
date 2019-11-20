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
import dataPagePool
import queryHelpers

if __name__ == '__main__':
    # reset everything
    indexPagePool.resetPool()
    dataPagePool.resetPool()
    dataPagePool.resetData()
    queryHelpers.resetQueries()
    # Run build(*) on the provided data set, and create two B+_trees with an order of 2, one on
    # Suppliers.sid, and the other on Supply.pid
    suppliersTree = buildTree.build("Suppliers", "sid", 2)
    supplyTree = buildTree.build("Supply", "pid", 2)
    # Run displayTree(*) to display the structures of the two B+_trees you create under item 6
    # above. They should be displayed in files Suppliers_sid.txt and Supply_pid.txt, respectively,
    # under folder treePic
    display.displayTree(suppliersTree, "Suppliers_sid.txt")
    display.displayTree(supplyTree, "Supply_pid.txt")

    # question a
    aStr = "Query a) Find the name for the supplier 's23' when a B+_tree exists on Suppliers.sid:\n"
    queryHelpers.writeToQueryFile(aStr)
    aSel = relAlg.select("Suppliers", "sid", "=", "s23")
    aProj = relAlg.project(aSel, ["sname"])
    display.displayTable(aProj, "queryResult.txt")
    queryHelpers.writeToQueryFile("\n")

    # question b
    remove.removeTree("Suppliers", "sid")
    bStr = "Query b) Find the name for the supplier 's23' without a B+ tree:\n"
    queryHelpers.writeToQueryFile(bStr)
    aSel2 = relAlg.select("Suppliers", "sid", "=", "s23")
    aProj2 = relAlg.project(aSel, ["sname"])
    display.displayTable(aProj2, "queryResult.txt")
    queryHelpers.writeToQueryFile("\n")

    # there are a few common queries we will perform here
    suppliersJoinSupply = relAlg.join("Suppliers", "sid", "Supply", "sid")
    joinAll = relAlg.join(suppliersJoinSupply, "pid", "Products", "pid")

    # question c: Find the address of the suppliers who supplied ‘p15’
    cStr = "Query c) Find the address of the suppliers who supplied 'p15':\n"
    queryHelpers.writeToQueryFile(cStr)
    cProj = relAlg.project(suppliersJoinSupply, ["address"])
    display.displayTable(cProj, "queryResult.txt")
    queryHelpers.writeToQueryFile("\n")

    # question d What is the cost of ‘p20’ supplied by ‘Kiddie’?
    dStr = "Query d) What is the cost of 'p20' supplied by 'Kiddie'?:\n"
    queryHelpers.writeToQueryFile(dStr)
    dSelPart = relAlg.select(suppliersJoinSupply, "pid", "=", "p20")
    dSelName = relAlg.select(dSelPart, "sname", "=", "Kiddie")
    dCost = relAlg.project(dSelName, ["cost"])
    display.displayTable(dCost, "queryResult.txt")
    queryHelpers.writeToQueryFile("\n")

    # question e For each supplier who supplied products with a cost of 47 or higher, list his/her name,
    # product name and the cost.
    eStr = "Query e) For each supplier who supplied products with a cost of 47 or higher, list his/her name, product name and the cost:\n"
    queryHelpers.writeToQueryFile(eStr)
    eAttrs = ["sname", "pname", "cost"]
    eSel = relAlg.select(joinAll, "cost", ">=", 47)
    eProj = relAlg.project(eSel, eAttrs)
    display.displayTable(eProj, "queryResult.txt")
