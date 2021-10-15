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

indepedent2 = dataFramePrime['YearsExperience'].values.tolist()                           # Gets ip for the people
dependent2 = dataFramePrime['Salary'].values.tolist()  # Get langs for the people

# refer to chart
def KSplit(splitValue=None):
    splitValue = round(len(indepedent2) / (splitValue - 1)) # gets number of items that will be in each section of k

    mseAverage = 0
    rsmeAverage = 0
    mseSciAverage = 0
    rsmeSciAverage = 0
    # visualization of the k-split
    # - a b c d f
    # 1 - - - - t
    # 2 - - - t -
    # 3 - - t - -
    # 4 - t - - -
    # 5 t - - - -

    # splits depedent and independent into lists based on splitvalue
    listIndependent = [indepedent2[i:i + splitValue] for i in range(0, len(indepedent2), splitValue)]
    listDepedent = [dependent2[i:i + splitValue] for i in range(0, len(dependent2), splitValue)]

    # counter
    counter = len(listIndependent) - 1
    inverseCounter = 1 # used for printing out things
    for x in listIndependent:
        print("=============K", inverseCounter)

        testIndependent = listIndependent.copy().pop(counter)   # creates the training set
        testDependent = listDepedent.copy().pop(counter)        # creates the test set

        inverseCounter = inverseCounter + 1
        counter = counter - 1

        # Runs msi, rsme cacluations and returms them to these temp values
        mseAverageTemp, rsmeAverageTemp, mseSciAverageTemp, rsmeSciAverageTemp = RegexCalc(list(itertools.chain.from_iterable(listIndependent)), list(itertools.chain.from_iterable(listDepedent)), testIndependent, testDependent)
        # appends the temp values to there solid lists
        mseAverage, rsmeAverage, mseSciAverage, rsmeSciAverage = mseAverage + mseAverageTemp, rsmeAverage + rsmeAverageTemp, mseSciAverage + mseSciAverageTemp, rsmeSciAverage + rsmeSciAverageTemp

    # just gets the average of them
    mseAverage, rsmeAverage, mseSciAverage, rsmeSciAverage = mseAverage/len(listIndependent), rsmeAverage/len(listIndependent), mseSciAverage/len(listIndependent), rsmeSciAverage/len(listIndependent)
    print("=============K", inverseCounter)
    print("################################################################")
    print("K-", len(listIndependent) + 1, "Average MSE Score:              ", round(mseAverage, 2))
    print("K-", len(listIndependent) + 1, "Average RSME Score:             ", round(rsmeAverage, 2))
    print("################################################################")

    print("K-", len(listIndependent) + 1, "Average MSE Score Scikit-learn: ", round(mseSciAverage, 2))
    print("K-", len(listIndependent) + 1, "Average RSME Score Scikit-learn: ", round(rsmeSciAverage, 2))
    print("################################################################")
    print("\n\n")

def RegexCalc(indepedent, dependent, indepedentTest, dependentTest):
        # Indepedent, Dependent are the training data
        # While The Tests are the test data          Both are already split into there respective groups

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
        partA = 0  # (Xi -x ) * (Yi - x) Index of independent(x) in mean of independent(x) * Index of dependent(x) in mean of dependent(x)
        partB = 0  # (Xi -  x)^2 Index of independent(x) in mean of independent(x) sqaured
        counter = 0
        for x in indepedent:
            partA = partA + (indepedent[counter] - indiMean) * (dependent[counter] - dependiMean)  # denomator
            partB = partB + (indepedent[counter] - indiMean) ** 2  # numartor
            counter = counter + 1

        slope = partA / partB  # Generates slope

        intercept = dependiMean - slope * indiMean  # Generets intercept

        # calculates Pearsons R Score
        counter = 0
        RTop = 0
        RBottom = 0
        for x in indepedent:
            RTop = RTop + ((indepedent[counter] - indiMean) * (dependent[counter] - dependiMean))
            RBottom = RBottom + math.sqrt(
                ((indepedent[counter] - indiMean) ** 2 * (dependent[counter] - dependiMean) ** 2))
        R = RTop / RBottom

        # "Predicts"
        def Predict():
            counter = 0
            total = 0
            totalPrecent = 0
            outputArray = []  # Grabs each prediction
            for x in dependentTest:
                output = slope * indepedentTest[counter] + intercept  # prediction is output
                outputArray.append(output)

                total = total + (output - dependentTest[counter]) ** 2  # Generates MSE Score onse finished looping

                totalPrecent = totalPrecent + output / abs(dependentTest[counter])  # Generates Average Precentage off prediction
                counter = counter + 1

            avgPrediction = totalPrecent / len(dependentTest) * 100  # Turns Average Prediction into prectentage

            # Detirmins if guess over or under and shows accordingly
            if (avgPrediction >= 100):
                avgPrediction = avgPrediction - 100
                print("On Average Predicts:                   ", round(avgPrediction, 2), "% Over")
            elif (avgPrediction <= 100):
                avgPrediction = 100 - avgPrediction
                print("On Average Predicts:                   ", round(avgPrediction, 2), "% Under")

            print("________________________________________________________________")
            print("MSE Score:              ", round((total / (len(dependentTest))), 2))
            print("RSME Score:             ", round((math.sqrt(total / (len(dependentTest)))), 2))
            print("________________________________________________________________")

            print("MSE Score Scikit-learn: ", round(MSE(dependentTest, outputArray), 2))
            print("RSME Score Scikit-learn: ", round(math.sqrt(MSE(dependentTest, outputArray)), 2))
            print("________________________________________________________________")
            print("\n\n")
            return round(total / len(dependentTest), 2), round(math.sqrt(total / len(dependentTest)), 2), round(MSE(dependentTest, outputArray), 2), round(math.sqrt(MSE(dependentTest, outputArray)), 2)
        one, two, three, four = Predict()
        return one, two, three, four

def main():
    print()
    print("KN Split ")
    print("################################################################")
    value = int(input("Please Enter a Value: \n"))
    if(value <= 0):
        value = 4
    KSplit(value)
main()
