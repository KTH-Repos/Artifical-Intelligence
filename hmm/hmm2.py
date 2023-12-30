import math

# transition matrix
transRows, transCol, *matrix_values = map(float, input().split())
transRows, transCol = int(transRows), int(transCol)
transMatrix = [matrix_values[i:i+transCol] for i in range(0, len(matrix_values), transCol)]

# observation matrix
obsRows, obsCol, *matrix_values = map(float, input().split())
obsRows, obsCol = int(obsRows), int(obsCol)
obsMatrix = [matrix_values[i:i+obsCol] for i in range(0, len(matrix_values), obsCol)]

# initP matrix
initRows, initCol, *matrix_values = map(float, input().split())
initRows, initCol = int(initRows), int(initCol)
initMatrix = [matrix_values[i:i+initCol] for i in range(0, len(matrix_values), initCol)]

# note that this line of code is not optimal for this task, but since I do not want to introduce unnecessary complexity
# and since we are not expected to handle errors related to this, I will let it be as it is.
amountOfEmissions, *emissionSequence = map(int, input().split())

amountOfStates = initCol

delta = [[0 for _ in range(amountOfStates)] for _ in range(amountOfEmissions)]
delta_index = [[0 for _ in range(amountOfStates)] for _ in range(amountOfEmissions)]

# base case: when we are in first time step (subscript 1)
for i in range(amountOfStates):
    delta[0][i] = initMatrix[0][i] * obsMatrix[i][emissionSequence[0]]

for t in range(1, amountOfEmissions):
    for j in range(amountOfStates):
        maxDeltaValue = -math.inf
        maxDeltaIndex = 0
        for i in range(amountOfStates):
            
            tempDeltaValue = delta[t-1][i] * transMatrix[i][j] * obsMatrix[j][emissionSequence[t]]
            
            if tempDeltaValue > maxDeltaValue:
                maxDeltaValue = tempDeltaValue
                maxDeltaIndex = i

        delta[t][j] = maxDeltaValue
        delta_index[t][j] = maxDeltaIndex

# 'best' here is equivalent to 'most probable'
bestStateSequence = [0 for _ in range(amountOfEmissions)]

# get most probable hidden state of last observation in the sequence
bestStateSequence[amountOfEmissions - 1] = delta[amountOfEmissions-1].index(max(delta[amountOfEmissions - 1]))

# backtrack to fill in the rest of the sequence
for t in range(amountOfEmissions - 2, -1, -1):
    bestStateSequence[t] = delta_index[t+1][bestStateSequence[t+1]]

for i in range(len(bestStateSequence)):
    print(bestStateSequence[i], end=" ")

# TODO: Just understand everything from line 31 to the end. I think my confusion is more with the mathematical concepts, not with the programming at all.