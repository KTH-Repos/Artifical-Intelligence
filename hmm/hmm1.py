
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
# this matrix will be used to store alpha-values for efficiency purposes.
alpha = [[0 for _ in range(amountOfStates)] for _ in range(amountOfEmissions)]

# base case: when we are in first time step (subscript 1)
for i in range(amountOfStates):
    alpha[0][i] = initMatrix[0][i] * obsMatrix[i][emissionSequence[0]]

# T = amountOfEmissions = amount of Rows in alpha, N = amountOfStates
for t in range(1, amountOfEmissions):
    for i in range(amountOfStates):
        for j in range(amountOfStates):
            alpha[t][i] += alpha[t-1][j] * transMatrix[j][i] * obsMatrix[i][emissionSequence[t]]

finalProbability = sum(alpha[amountOfEmissions-1])
print(finalProbability)