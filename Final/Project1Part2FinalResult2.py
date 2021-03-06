#Merged by Leo
'''
Merge Changes: (10:42 10/14/2021)
Made global Path and FileName(s) definitions
Inserted relevant code from Jake Cermak for Sheet 3
Renamed globals to be universal between each person.
Modified UniversalSort and main to merge Leo's code.
'''
import pandas as pd
import matplotlib as mpl
from matplotlib import pyplot as plt
import random as random
import xlsxwriter as xlsx
from itertools import count

#________________________________________________________________________________________
# Name: George Shea
#________________________________________________________________________________________
path = 'C:/Users/leeleoy/Documents/Special Topics/Project 1 - part 2/' #variable dependant on user
excelFileName = 'project_1_part_2.xlsx'
outputFileName = 'outputData.xlsx'
# Path In
excelFile = pd.ExcelFile(path + excelFileName)
dataFramePrime = pd.read_excel(excelFile)                        #Allows for sheet reading

outputFilePath = path + outputFileName
#Path out
outputFile = xlsx.Workbook(outputFilePath)
writer = pd.ExcelWriter(outputFilePath)

#--------------------------#
#                          #
# Title: Sheet 3           #
#                          #
# Name: Jake Cermak        #
#                          #

yes_people = dataFramePrime[["Would you like to learn more?", "Name", "Email Address", "User IP"]] #using relevant columns
yes_people = yes_people.replace(['はい!','Oui!','Si'],'Yes!') #replacing foreign yeses with english yeses
yes_people = yes_people.replace('لا','Nope') #replacing arabic noes with nopes
yes_people = (yes_people.loc[yes_people['Would you like to learn more?'] == 'Yes!']) #filtering the dataframe by people that have said yes
yes_people = yes_people.drop(yes_people.columns[[0]], axis = 1) #dropping the yes column because it is no longer relevant at this point

yes_people.to_excel(writer, "Sheet 3", index = False)
#--------------------------#




#________________________________________________________________________________________
# Name: George Shea
#Replaces any answer in the negative with nan
counter = 0
for x in dataFramePrime:
    dataFramePrime.iloc[:, counter] = dataFramePrime.iloc[:, counter].replace({"Nope" : None }, regex=True).replace({"No" : None}, regex=True).replace({"Nan" : None}, regex=True).replace({"لا" : None}, regex=True)
    counter = counter + 1

#Used Lists
ipList = dataFramePrime['User IP'].values.tolist()                           # Gets ip for the people
launageList = dataFramePrime['What Language Do You Speak?'].values.tolist()  # Get langs for the people
spamMe = dataFramePrime['Would you like to learn more?'].values.tolist()     # The please spam me button


potato = []
#________________________________________________________________________________________
# Name: Leo Lee
#Returns the count of vegies in a dataframe, assuming it's in the same format as the prime dataframe
def ReturnVegieCount(DataFrame):
    dualOutput = DataFrame.iloc[:, 1:33].notnull().sum(axis=0)
    dualOutput = dualOutput.sort_values(ascending=True)
    return dualOutput
#________________________________________________________________________________________

# Graphs out for problem A and B
def DualSearch(probA = None, probB = None):
    print()

    #Prints Out Vegis Count
    if(probA == True):
        dualOutput = dataFramePrime.iloc[:, 1:33].notnull().sum(axis=0)
        dualOutput = dualOutput.sort_values(ascending=True)
        dualOutput = dualOutput.to_frame()

        test = dualOutput.plot.bar(legend=None)
        plt.title("Problem A")
        plt.xlabel("Crops")

    #Prints Out Launages Count
    elif(probB == True):
        plt.title("Problem B")
        plt.xlabel("Languages")
        dualOutput = dataFramePrime['What Language Do You Speak?'].replace("日本語", "Japanese").replace("中文", "Chinese") .value_counts()
        test = dualOutput.plot.bar(legend=None)
    print("________________________________________________")

    # Makes Bar Graph pretty
    plt.ylabel("Number Of People")
    bars = [rect for rect in test.get_children() if isinstance(rect, mpl.patches.Rectangle)]
    counter = 0
    #Assigns random colors to graph
    for x in bars:
        color = (random.random(), random.random(), random.random())
        bars[counter].set_color(color)
        counter = counter + 1
    bars[(len(bars) - 1)].set_color('white')

    plt.xticks( rotation='vertical')
    plt.show()

    return dualOutput


# Sorts Data ands prints it out
def UniversalSort(searchList, printerTru = None):
    uniqueSearch = []
    counter = 0
    sheetOne = []
    sheetTwo = []
    sheetThree = []
    sheetFour = []
    sheetFive = []

    # Creates List of unique items
    for x in searchList:
        tag = searchList[counter]
        # Check for if there is a new item
        if (not (str(tag) in uniqueSearch)):
            uniqueSearch.append(str(tag))
        counter = counter + 1
    #print(uniqueSearch)
    dfStorage = []
    # Each list within organized holder is a unique value based on organzaiton cretiria
    counter = 0
    counterTwo = 0
    for x in uniqueSearch: #for each unique IP
        dfTemp = pd.DataFrame(columns = dataFramePrime.columns.values.tolist()) #create a new dataframe for this unique IP
        counter = 0
        for y in searchList: #for each ip
            # Goes Through and assigns each item to its corsponding list
            if(searchList[counter] == uniqueSearch[counterTwo]): #if the IPs match
                #Magic Syntax https://www.geeksforgeeks.org/how-to-add-one-row-in-an-existing-pandas-dataframe/
                dfTemp.loc[len(dfTemp.index)] = dataFramePrime.iloc[counter] #add a new row to dfTemp that is the data of the matched IP row
            # Goes Through entire dataset
            counter = counter + 1

        # Goes Through each list
        counterTwo = counterTwo + 1

        dfStorage.append(dfTemp) #add the new dataframe for use later
        sheetOne.append(dfTemp) 
    # Sends organzied things to excel
    def Printer():
        counter = 0
        print("________________________________________________________________________________________________________________________________________________________________________________________________")
        for x in dfStorage:
            # Prints out total survays for the area and how many launages are spoken by search
            print(uniqueSearch[counter], " Unique Votes: ", len(dfStorage[counter]))

            # used to get precents
            totalLen = len(dfStorage[counter])

            # Gets vegi votes and vegi vote precentage
            output = dfStorage[counter].iloc[:, 1:33].notnull().sum(axis=0)
            percent = ((dfStorage[counter].iloc[:, 1:33].notnull().sum(axis=0)) / totalLen) * 100
            potato.append(percent)
            sheetFour.append(output)
            sheetFive.append(percent)
            # Sorts them in decsending order
            percent = percent.sort_values(ascending=False)
            output = output.sort_values(ascending=False)
            #percent = round(percent)    # Rounds to get rid of end bit
            tempDataFrame = pd.concat([output, round(percent)], axis=1)

            # Renames coloumns to be logical
            tempDataFrame.columns = ("Votes", "Precents")
            # Writes to excel file

            #Please Spam me data
            banna = dfStorage[counter].iloc[:, [0, 34, 35, 36, 43]].loc[dfStorage[counter]['Would you like to learn more?'].notnull()]
            sheetThree.append(banna)

            counter = counter + 1

    if (printerTru == True):
        Printer()
    return sheetOne, sheetThree, sheetFour, sheetFive, uniqueSearch

#________________________________________________________________________________________
# Name: Leo Lee
def MakeSheet1():
    VeggieSeries = ReturnVegieCount(dataFramePrime)
    VeggieDataFrame = pd.DataFrame(VeggieSeries,columns=['Crop Counts'])
    VeggieDataFrame = VeggieDataFrame.sort_values('Crop Counts',ascending=False)
    VeggieDataFrame.to_excel(writer,"Sheet 1")
    return

def MakeSheets2(IPAddresses, Languages, IPGroupedData):
    Sheet2 = []
    for i in range(len(IPAddresses)):
        ThisIPData = IPGroupedData[i]
        Sheet2Data = []
        for Language in Languages:
            LanguageCount = 0
            for DataLanguage in ThisIPData['What Language Do You Speak?'].values:
                if Language == DataLanguage:
                    LanguageCount+=1
            Sheet2Data.append(LanguageCount)
        Sheet2.append(Sheet2Data)
    Sheet2Frame = pd.DataFrame(Sheet2,IPAddresses,Languages)
    Sheet2Name = "Sheet 2"
    Sheet2Frame.to_excel(writer,Sheet2Name)
    return

def MakeSheet4(IPAddresses, IPGroupedData, UseCounterName = False, Counter = None):
    Sheet4 = []
    for i in range(len(IPAddresses)):
        ThisIPData = IPGroupedData[i]
        Sheet4Data = ReturnVegieCount(ThisIPData)
        Sheet4.append(Sheet4Data)
    Sheet4Frame = pd.DataFrame(Sheet4,IPAddresses)
    Sheet4Frame = Sheet4Frame.swapaxes("columns","index")
    Sheet4Name = "Sheet 4"
    if UseCounterName:
        Sheet4Name = "Sheet " + str(next(Counter))
    Sheet4Frame.to_excel(writer,Sheet4Name)
    #print(Sheet4Frame)
    return True
#________________________________________________________________________________________
def main():
    fo = DualSearch(probA=True)
    bar = DualSearch(probB=True)
    
    sheetOneOutput, sheetThreeOutput, sheetFourOutput, sheetFiveOutput, IpAddresses = UniversalSort(ipList, printerTru=True)
#________________________________________________________________________________________
# Name: Leo Lee
    MakeSheet1()
    _, _, _, _, Languages = UniversalSort(launageList)
    MakeSheets2(IpAddresses, Languages, sheetOneOutput)
    Sheet4Done = MakeSheet4(IpAddresses, sheetOneOutput)
    searchListOutput = IpAddresses
    SheetCounter = count(5)
#________________________________________________________________________________________
    def Sheet5And6():
        sheetFive = pd.DataFrame()
        counter = 0

        # sheet 5
        for x in sheetFiveOutput:
            sheetFiveOutput[counter] = sheetFiveOutput[counter].round(2)
            tempsheet = pd.DataFrame()
            tempsheet2 = pd.DataFrame()
            tempsheet["CROPS"] = sheetFiveOutput[counter].index
            tempsheet2[searchListOutput[counter]] = sheetFiveOutput[counter].array
            sheetFive = pd.concat([sheetFive, tempsheet], axis=1)
            sheetFive = pd.concat([sheetFive, tempsheet2], axis=1)
            counter = counter + 1

        sheetName = random.randrange(1,100)
        sheetFive.to_excel(writer, "Sheet " + str(next(SheetCounter)))

        sheetSix = pd.DataFrame()
        counter = 0

        # sheet 6
        for x in sheetFiveOutput:
            sheetFiveOutput[counter] = sheetFiveOutput[counter].sort_values(ascending=False)
            sheetFiveOutput[counter] = sheetFiveOutput[counter].round(2)
            tempsheet = pd.DataFrame()
            tempsheet2 = pd.DataFrame()
            tempsheet["CROPS"] = sheetFiveOutput[counter].index
            tempsheet2[searchListOutput[counter]] = sheetFiveOutput[counter].array
            sheetSix = pd.concat([sheetSix, tempsheet], axis=1)
            sheetSix = pd.concat([sheetSix, tempsheet2], axis=1)
            counter = counter + 1

        sheetName = random.randrange(1,100)
        sheetSix.to_excel(writer, "Sheet " + str(next(SheetCounter)))
    Sheet5And6()
    sheetOneOutput, sheetThreeOutput, sheetFourOutput, sheetFiveOutput, searchListOutput = UniversalSort(launageList, printerTru=True)
#________________________________________________________________________________________
# Name: Leo Lee
    MakeSheet4(searchListOutput, sheetOneOutput, Sheet4Done,SheetCounter)
#________________________________________________________________________________________
    Sheet5And6()

    print("\n\n\n\n")
    writer.save()
main()

#________________________________________________________________________________________

