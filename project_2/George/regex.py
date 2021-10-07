import pandas as pd
from sklearn.metrics import mean_squared_error as MSE
import math
import itertools

#________________________________________________________________________________________
# Name: George Shea     ßeta
# Date Created: 28/9/21
# Date Modified 28/9/21
# Project 1 part  will be using a linear regestion algretyhm to predict
# Version 1.5
#________________________________________________________________________________________
# part do that k score thing

pathTwo = "C:/Users/gshea/Desktop/School/Summer2021/Artifical/DataSets/experience_salary_data.csv"
dataFramePrime = pd.read_csv(pathTwo)

indepedent = dataFramePrime['YearsExperience'].values.tolist()                           # Gets ip for the people
dependent = dataFramePrime['Salary'].values.tolist()  # Get langs for the people

kNAverage = 0

# Splits lists into given test and train data based on given precentage
def Split(split = None, KSplit = None):
    divsionPoint = round(len(indepedent) * split)

    indiTrainA = indepedent[:divsionPoint]
    indiTestA = indepedent[divsionPoint:]

    depndiTrainB = dependent[:divsionPoint]
    denpdiTestB = dependent[divsionPoint:]

    # Returns split data to regexcalc
    return indiTrainA, depndiTrainB, indiTestA, denpdiTestB

def FourKSplit(PartA = None, PartB = None, PartC = None ):
    print()
    #   A B C
    # 1 - - t
    # 2 - t -
    # 3 t - -
    divsionPoint = round(len(indepedent) * .33)
    divsionPoint2 = round(len(indepedent) * .66)

    ''' functional eye sore
    trainPartOneDependent = dependent[:divsionPoint] + dependent[divsionPoint:divsionPoint2]
    trainPartTwoDependent = dependent[:divsionPoint] + dependent[divsionPoint2:]
    trainPartThreeDependent = dependent[divsionPoint:divsionPoint2] + dependent[divsionPoint2:]

    trainPartOneIndepedent = indepedent[:divsionPoint] + indepedent[divsionPoint:divsionPoint2]
    trainPartTwoIndepedent = indepedent[:divsionPoint] + indepedent[divsionPoint2:]
    trainPartThreeIndepedent = indepedent[divsionPoint:divsionPoint2] + indepedent[divsionPoint2:]
    '''

    if(PartA == True):
        return indepedent[:divsionPoint] + indepedent[divsionPoint:divsionPoint2], dependent[:divsionPoint] + dependent[divsionPoint:divsionPoint2], indepedent[:divsionPoint], dependent[:divsionPoint]
    elif(PartB == True):
        return indepedent[:divsionPoint] + indepedent[divsionPoint2:], dependent[:divsionPoint] + dependent[divsionPoint2:], indepedent[divsionPoint:divsionPoint2], dependent[divsionPoint:divsionPoint2]
    elif(PartC == True):
        return indepedent[divsionPoint:divsionPoint2] + indepedent[divsionPoint2:], dependent[:divsionPoint] + dependent[divsionPoint2:], indepedent[divsionPoint2:], dependent[divsionPoint2:]
    return

def KSplit(splitValue = None):
    splitValue = round(len(indepedent)/splitValue)
    counter = splitValue
    # - a b c d f
    # 1 - - - - t
    # 2 - - - t -
    # 3 - - t - -
    # 4 - t - - -
    # 5 t - - - -

    listIndependent = [indepedent[i:i + splitValue] for i in range(0, len(indepedent), splitValue)]
    listDepedent = [dependent[i:i + splitValue] for i in range(0, len(dependent), splitValue)]
    listIndependentReset = listIndependent
    listDepedentReset = listDepedent

    print(listIndependent)
    for x in listIndependent:
        testIndependent = listIndependent.pop(counter)
        testDependent = listDepedent.pop(counter)

        list(itertools.chain.from_iterable(listIndependent.pop(counter)))
        list(itertools.chain.from_iterable(listDepedent.pop(counter)))
        return list(itertools.chain.from_iterable(listIndependent.pop(counter))), list(itertools.chain.from_iterable(listDepedent.pop(counter))), testIndependent, testDependent

    # return these values
    # 1 independent train
    # 2 dependent train
    # 3 independent test
    # 4 dependent test

# Does the regex calculations and compares it to the scikit-learn
def RegexCalc(precent = None, PartA = None, PartB = None, PartC = None ):
    #Indepedent, Dependent are the training data
    #While The Tests are the test data          Both are already split into there respective groups

    if(precent != None):
        indepedent, dependent, indepedentTest, dependentTest = Split(precent)
    if(PartA == True):
        indepedent, dependent, indepedentTest, dependentTest = FourKSplit(PartA=True)
    elif(PartB == True):
        indepedent, dependent, indepedentTest, dependentTest = FourKSplit(PartB=True)
    elif(PartC == True):
        indepedent, dependent, indepedentTest, dependentTest = FourKSplit(PartC=True)

    indiMean = 0
    dependiMean = 0
    counter = 0
    # Calculates Mean for indipedent and dependent
    for x in indepedent:
        indiMean = indepedent[counter] + indiMean
        dependiMean = dependent[counter] + dependiMean
        counter = counter + 1
    indiMean = indiMean / len(indepedent)
    dependiMean = dependiMean / len(dependent)

    # calculates Slope
    partA = 0 # (Xi -x ) * (Yi - x) Index of independent(x) in mean of independent(x) * Index of dependent(x) in mean of dependent(x)
    partB = 0 # (Xi -  x)^2 Index of independent(x) in mean of independent(x) sqaured
    counter = 0
    for x in indepedent:
        partA = partA + (indepedent[counter] - indiMean) * (dependent[counter] - dependiMean) # denomator
        partB = partB + (indepedent[counter] - indiMean)**2                                   # numartor
        counter = counter + 1

    slope = partA / partB   # Generates slope

    intercept = dependiMean - slope * indiMean  # Generets intercept

    # calculates Pearsons R Score
    counter = 0
    RTop = 0
    RBottom = 0
    for x in indepedent:
        RTop = RTop + ((indepedent[counter] - indiMean) * (dependent[counter] - dependiMean))
        RBottom = RBottom + math.sqrt(((indepedent[counter] - indiMean)**2 * (dependent[counter] - dependiMean)**2))
    R = RTop/RBottom

    #"Predicts"
    def Predict():
        counter = 0
        total = 0
        totalPrecent = 0
        outputArray = [] # Grabs each prediction
        for x in dependentTest:
            output = slope * indepedentTest[counter] + intercept    # prediction is output
            outputArray.append(output)

            total = total + (output - dependentTest[counter])**2    # Generates MSE Score onse finished looping

            totalPrecent = totalPrecent + output/abs(dependentTest[counter])    # Generates Average Precentage off prediction
            counter = counter + 1

        avgPrediction = totalPrecent/len(dependentTest) * 100   # Turns Average Prediction into prectentage

        # Detirmins if guess over or under and shows accordingly
        if(avgPrediction >= 100):
            avgPrediction = avgPrediction - 100
            print("On Average Predicts:                   ", round(avgPrediction, 2), "% Over")
        elif(avgPrediction <= 100):
            avgPrediction =  100 - avgPrediction
            print("On Average Predicts:                   ", round(avgPrediction, 2), "% Under")
        print("________________________________________________________________")
        print("MSE Score:              ", round( (total / (len(dependentTest))), 2 ))
        print("RSME Score:             ", round((math.sqrt(total / (len(dependentTest)))),2))
        print("________________________________________________________________")

        print("MSE Score Scikit-learn: ", round(MSE(dependentTest, outputArray), 2))
        print("RSME Score Scikit-learn: ", round(math.sqrt(MSE(dependentTest, outputArray)), 2))
        print("________________________________________________________________")
        print("\n\n")
    Predict()

def main():
    print()
    print("80/20 Split ")
    print("################################################################")
    RegexCalc(.80)
    print()
    print("70/30 Split ")
    print("################################################################")
    RegexCalc(.70)

    print(" - - t ")
    print("################################################################")
    RegexCalc(PartA=True)

    print(" - t - ")
    print("################################################################")
    RegexCalc(PartB=True)

    print(" t - - ")
    print("################################################################")
    RegexCalc(PartC=True)

    KSplit(2)
    KSplit(3)
    KSplit(5)
main()
