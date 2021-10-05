import pandas as pd
from sklearn.utils import shuffle
from math import sqrt
import numpy as np

#________________________________________________________________________________________
# Name: George Shea     ßeta
# Date Created: 9/9/21
# Date Modified 17/9/21
# project part 2 this project is parsing through an excel spreadsheet to produce usable data
# Version 1.4
#________________________________________________________________________________________


path = pd.ExcelFile('C:/Users/gshea/Desktop/School/Summer2021/Artifical/DataSets/fruits_classification.xlsx')
dataFramePrime = pd.read_excel(path)                        #Allows for sheet reading


def Primer(k=None, dataStart=None, dataEnd=None):
    # Randomises the Data And Splits it into a 60/40 split
    df = shuffle(dataFramePrime)
    train = df.sample(frac=0.6)
    test = df.drop(train.index)

    average = FindFriends(train, test, k, dataStart, dataEnd)
    return average

def FindFriends(train, test, k=None, dataStart=None, dataEnd=None):
    friends = []
    friendsIndex = []
    topFriends = []

    testCounter = 0

    matchCount = 0
    for index, rowTest in test.iterrows():
        topFriends = []
        friends = []
        friendsIndex = []
        trainCounter = 0
        for index, rowTrain in train.iterrows():
            #value = ((train.iloc[trainCounter::, 3].values[0] - test.iloc[testCounter::, 3].values[0])**2) + ((train.iloc[trainCounter::, 4].values[0] - test.iloc[testCounter::, 4].values[0])**2) + ((train.iloc[trainCounter::, 5].values[0] - test.iloc[testCounter::, 5].values[0])**2) + ((train.iloc[trainCounter::, 6].values[0] - test.iloc[testCounter::, 6].values[0])**2)

            value = 0
            s = dataStart
            while s <= dataEnd:
                value = value + ((train.iloc[trainCounter::, s].values[0] - test.iloc[testCounter::, s].values[0])**2)
                s = s + 1

            friends.append(sqrt(value))
            friendsIndex.append((trainCounter))

            trainCounter = trainCounter + 1

        # f is the nearest neighbor, fI is its index in the train data set
        fI, f = np.array(friendsIndex), np.array(friends)
        inds = f.argsort()
        fI, f = fI[inds], f[inds]

        #print("F Indxes:  ", fI[:k])
        #print("F:  ", f[:k])

        # gets k nearest nieghbors
        i = 0
        while i <= k:
            topFriends.append(train.iloc[fI[i], 1])
            i = i + 1
        guess = MostFrequent(topFriends)

        #print("Nearest Fruits: ", topFriends)
        #print("Actual test fruit: ", test.iloc[testCounter, 1])
        #print("Guess is: ", guess)
        #print()
        #print(test.iloc[f[testCounter]::,1])
        # Actual value                  #Guess
        if(test.iloc[testCounter, 1] == guess):
            matchCount = matchCount + 1

        testCounter = testCounter + 1
    return round(matchCount / len(test) * 100, 2)

def MostFrequent(listCount):
    # first encountered item in list will be returend in case of Apple, apple, Orange Orange. Apple would be returned
    mostCommon = max(listCount, key=listCount.count)
    return mostCommon


# Lets make toast
def ScreamingProcesser(iterations, kNear):
    iterationsReset = iterations
    while kNear > 0:
        runningTotal = 0
        iterations = iterationsReset
        while iterations > 0:
            temp = Primer(kNear, 3, 6)
            runningTotal = runningTotal + temp
            iterations = iterations - 1

        print("|| Neighbors || ", kNear , " || Average Accuracy || " ,round(runningTotal / iterationsReset, 2), "%")
        kNear = kNear - 1


def main():
    print("More iterations take longer")
    value =  int(input("Please enter iteration: \n"))
    print("Loading... . ")
    ScreamingProcesser(value, 10)
    
    print("Done")
main()
