
# TODO: take a look at the input technique again.

# transition matrix
# transRows = int(input())
# transCol = int(input())
# transMatrix = [[0 for _ in range(transCol)] for _ in range(transRows)]

# for i in range(transRows):
#     for j in range(transCol):
#         value = float(input())
#         transMatrix[i][j] = value
transRows, transCol, *matrix_values = map(float, input().split())
transRows, transCol = int(transRows), int(transCol)
transMatrix = [matrix_values[i:i+transCol] for i in range(0, len(matrix_values), transCol)]

# observation matrix
# obsRows = int(input())
# obsCol = int(input())
# obsMatrix = [[0 for _ in range(obsCol)] for _ in range(obsRows)]

# for i in range(obsRows):
#     for j in range(obsCol):
#         value = float(input())
#         obsMatrix[i][j] = value

obsRows, obsCol, *matrix_values = map(float, input().split())
obsRows, obsCol = int(obsRows), int(obsCol)
obsMatrix = [matrix_values[i:i+obsCol] for i in range(0, len(matrix_values), obsCol)]

# initP matrix
# initRows = int(input())
# initCol = int(input())
# initMatrix = [[0 for _ in range(initCol)] for _ in range(initRows)]

# for i in range(initRows):
#     for j in range(initCol):
#         value = float(input())
#         initMatrix[i][j] = value

initRows, initCol, *matrix_values = map(float, input().split())
initRows, initCol = int(initRows), int(initCol)
initMatrix = [matrix_values[i:i+initCol] for i in range(0, len(matrix_values), initCol)]

# result = initP x transP
result = [[0 for _ in range(transCol)] for _ in range(initRows)]
for i in range(initRows):
    for j in range(transCol):
        for k in range(transRows):
            result[i][j] += initMatrix[i][k] * transMatrix[k][j]

#print(result)

# finalResult = result x obsMatrix
finalResult = [[0 for _ in range(obsCol)] for _ in range(len(result))]
for i in range(len(result)):
    for j in range(obsCol):
        for k in range(obsRows):
            finalResult[i][j] += result[i][k] * obsMatrix[k][j]

print(len(result), obsCol, end=" ")
for i in range(len(result)):
    for j in range(obsCol):
        print(finalResult[i][j], end=" ")
