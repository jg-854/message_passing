## Showing some of the features of the class


from fg import *
fred = factor_graph (7,4,[(0,0),(0,1),(0,2),(1,0),(1,2),(1,3),(2,0),(2,1),(2,3),(3,0),(4,1),(5,2),(6,3)])

fred.view_attributes()



print("\n Now showing the systematic Generator matrix. Note that other Generator matrices can be used which have the same"
      "vector space. But Systematic Generator matrices are preffered.\n")
print(fred.generator_matrix())


print("\nNow showing the Parity check matrix. \n")
print(fred.parity_check_matrix())


print("\n Let us decode the following sequence : [1 ? ? 0 ? 1 ?]")

print("Upon, using message passing algorithm, we receive",fred.decode_bec([1,-1,-1,0,-1,1,-1]))