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

maxIterations = 100
iterations = 0
oldLogProb = -math.inf

for i in range(maxIterations):

    # following part is to calculate alpha:
    alpha = [[0 for _ in range(amountOfStates)] for _ in range(amountOfEmissions)]
    scalermatrix = [0 for _ in range(amountOfEmissions)]

    # base case: when we are in FIRST time step (subscript 1)
    for i in range(amountOfStates):
        alpha[0][i] = initMatrix[0][i] * obsMatrix[i][emissionSequence[0]]
        scalermatrix[0] += alpha[0][i]

    # scale alpha[0][i]
    scalermatrix[0] = 1/scalermatrix[0]
    for i in range(amountOfStates):
        alpha[0][i] = scalermatrix[0] * alpha[0][i]

    # T = amountOfEmissions = amount of Rows in alpha, N = amountOfStates
    for t in range(1, amountOfEmissions):
        scalermatrix[t] = 0
        for i in range(amountOfStates):
            alpha[t][i] = 0
            for j in range(amountOfStates):
                alpha[t][i] += alpha[t-1][j] * transMatrix[j][i]

            alpha[t][i] = alpha[t][i] * obsMatrix[i][emissionSequence[t]]
            scalermatrix[t] += alpha[t][i]

        # scale alpha[t][i]
        scalermatrix[t] = 1/scalermatrix[t]
        for i in range(amountOfStates):
            alpha[t][i] = scalermatrix[t] * alpha[t][i]

    # following part is to calculate beta:
    beta = [[0 for _ in range(amountOfStates)] for _ in range(amountOfEmissions)]

    # base case: when we are in LAST time step (subscript T)
    for i in range(amountOfStates):
        beta[amountOfEmissions-1][i] = 1 * scalermatrix[amountOfEmissions-1]

    for t in range(amountOfEmissions-2, -1, -1):
        for i in range(amountOfStates):
            beta[t][i] = 0
            for j in range(amountOfStates):
                beta[t][i] += transMatrix[i][j] * obsMatrix[j][emissionSequence[t+1]] * beta[t+1][j]

            beta[t][i] = scalermatrix[t] * beta[t][i]

    # following part is to caculate di-gamma and gamma:
    di_gamma = [[[0 for _ in range(amountOfStates)] for _ in range(amountOfStates)] for _ in range(amountOfEmissions)]
    gamma = [[0 for _ in range(amountOfStates)] for _ in range(amountOfEmissions)]

    for t in range(amountOfEmissions-1):
        for i in range(amountOfStates):
            gamma[t][i] = 0
            for j in range(amountOfStates):
                di_gamma[t][i][j] = alpha[t][i] * transMatrix[i][j] * obsMatrix[j][emissionSequence[t+1]] * beta[t+1][j]
                gamma[t][i] += di_gamma[t][i][j]

    # special case for gamma[t-1][i]
    for i in range(amountOfStates):
        gamma[amountOfEmissions-1][i] = alpha[amountOfEmissions-1][i]

    # following part is estimations of HMM parameters (except Pi (initMatrix)):

    # transition matrix
    for i in range(amountOfStates):
        denominator = 0
        for t in range(amountOfEmissions-1):
            denominator += gamma[t][i]
        for j in range(amountOfStates):
            numerator = 0
            for t in range(amountOfEmissions-1):
                numerator += di_gamma[t][i][j]
            transMatrix[i][j] = numerator/denominator

    # observation matrix
    for i in range(amountOfStates):
        denominator = 0
        for t in range(amountOfEmissions):
            denominator += gamma[t][i]
        for j in range(obsCol):
            numerator = 0
            for t in range(amountOfEmissions):
                if emissionSequence[t]==j:
                    numerator += gamma[t][i]
            
            obsMatrix[i][j] = numerator/denominator

                
    logProb = 0
    for i in range(amountOfEmissions):
        logProb += math.log(scalermatrix[i])

    logProb = (-1) * logProb

    iterations += 1
    if iterations < maxIterations and logProb > oldLogProb:
        oldLogProb = logProb
    else:
        break

print(transRows, transCol, end=" ")
for i in range(transRows):
    for j in range(transCol):
        print(transMatrix[i][j], end=" ")
print("")
print(obsRows, obsCol, end=" ")
for i in range(obsRows):
    for j in range(obsCol):
        print(obsMatrix[i][j], end=" ")