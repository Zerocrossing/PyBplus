"""
query.py
Include into file query.py under program folder the specifications for the following queries
using the three relational algebra functions you create. Then run this file on the provided
database, and use function displayTable(*) to send the resulting relations to file
queryResult.txt.
a. Find the name for the supplier ‘s23’ when a B+_tree exists on Suppliers.sid.b. Remove the B+_tree from Suppliers.sid, and repeat Question a.
c. Find the address of the suppliers who supplied ‘p15’.
d. What is the cost of ‘p20’ supplied by ‘Kiddie’?
e. For each supplier who supplied products with a cost of 47 or higher, list his/her name,
product name and the cost.
"""
import buildTree

# first step is to build the trees with order 2, defined by project
if __name__ == '__main__':
    buildTree.build()