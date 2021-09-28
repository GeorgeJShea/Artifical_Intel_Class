import pandas as pd
from sklearn.metrics import mean_squared_error as MSE
import math

#________________________________________________________________________________________
# Name: George Shea     ßeta
# Date Created: 28/9/21
# Date Modified 28/9/21
# Project 1 part  will be using a linear regestion algretyhm to predict
# Version 1.5
#________________________________________________________________________________________

pathTwo = "C:/Users/gshea/Desktop/School/Summer2021/Artifical/DataSets/experience_salary_data.csv"
dataFramePrime = pd.read_csv(pathTwo)

indepedent = dataFramePrime['YearsExperience'].values.tolist()                           # Gets ip for the people
dependent = dataFramePrime['Salary'].values.tolist()  # Get langs for the people

# Splits lists into given test and train data based on given precentage
def Split(split = None):
    divsionPoint = round(len(indepedent) * split)

    indiTrainA = indepedent[:divsionPoint]
    indiTestA = indepedent[divsionPoint:]

    indiTrainB = dependent[:divsionPoint]
    indiTestB = dependent[divsionPoint:]

    # Returns split data to regexcalc
    return indiTrainA, indiTrainB, indiTestA, indiTestB

# Does the regex calculations and compares it to the scikit-learn
def RegexCalc(precent):
    #Indepedent, Dependent are the training data
    #While The Tests are the test data          Both are already split into there respective groups
    indepedent, dependent, indepedentTest, dependentTest = Split(precent)

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

main()
