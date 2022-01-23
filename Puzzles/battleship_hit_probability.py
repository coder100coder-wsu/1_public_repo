from typing import List
# Write any import statements here

def getHitProbability(R: int, C: int, G: List[List[int]]) -> float:
    # Write your code here
    sum_ships = 0  # initialize
    for i in range(0,R):
        for j in range(0,C):
            sum_ships = sum_ships+G[i][j]
     #print(sum_ships)
    probability = round( float(sum_ships / (R*C)), 7)
    return probability


print( getHitProbability(2,3,[[0,0,1],[1,0,1]]))
print( getHitProbability(2,2,[[1,1],[1,1]]))
print( getHitProbability(2,6,[[1,1,0,0,1,1], [1,0,1,0,1,1] ]))
