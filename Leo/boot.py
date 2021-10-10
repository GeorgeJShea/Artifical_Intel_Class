import math
import pandas as pd #import pandas module for data manipulation
from matplotlib import pyplot as plt
import xlsxwriter

path = 'C:/Users/leeleoy/Documents/Special Topics/Project 1 - part 2/'

filename = 'project_1_part_2.xlsx'
MainDataFrame = pd.read_excel(path + filename)
OutputWorkbook = xlsxwriter.Workbook(path + 'output_data.xlsx')
Writer = pd.ExcelWriter(path + 'output_data.xlsx')

def AddToDictionary(TargetDictionary, Key, Value): #Function for adding values to the designated dictionary, and create a new pair if it doesn't exist yet.
    Key = str(Key) #Ensure key is a string
    OriginalValue = TargetDictionary.get(Key) #Try to get the value from the dictionary
    if type(OriginalValue) is type(None): #If the type of the value is none, set the new key-value pair.
        TargetDictionary[Key] = Value
    else:                                 #Else add the value to the existing pair.
        #print(type(OriginalValue))
        TargetDictionary[Key] += Value
    return TargetDictionary[Key] #Return the present value.

def AppendToDictionary(TargetDictionary, TargetKey): #Function for ensuring a key is in the dictionary, and create a new pair if it doesn't exist yet.
    TargetKey = str(TargetKey)                       #Ensure key is a string
    OriginalDictionary = TargetDictionary.get(TargetKey) #Try to get the dictionary from the target dictionary
    if type(OriginalDictionary) is type(None): #If the type of the value is none, set up a new dictionary.
        TargetDictionary[TargetKey] = {}
    return TargetDictionary[TargetKey] #Return the present dictionary.

def IntFromDictionary(TargetDictionary, TargetKey): #Function for grabbing numbers from a dictionary, and return 0 if it is invalid/none.
    TargetKey = str(TargetKey)                      #Ensure key is a string
    Output = TargetDictionary.get(TargetKey)        #Try to get the value from the dictionary
    if type(Output) is type(None):                  #If the type of value is none, return 0
        Output = 0
    return Output                                   #Return the value

def NumCheck(Num):      #Ensure nan equals 0 and nothing else
    if math.isnan(Num):
        Num = 0
    return Num

def NewSheetFromDictionary(Dictionary, WorksheetName, ColumnName): #Create a new Sheet on the designated Excel sheet.
    DataFrame = pd.DataFrame.from_dict(Dictionary, orient='index',columns=[ColumnName]) #Assemble DataFrame from Dictionary
    OutputWorkbook.add_worksheet(WorksheetName) #adding a sheet in designated Excel file.
    DataFrame.to_excel(Writer, WorksheetName, index = True) #writing the sheet into the Excel file as WorksheetName

#Total Number of Votes for each crop. 1
#['CropName'] = NumberVotes
TotalVotes = {}
CropTypes = ['Basil','Beets','Bell Pepper','Broccoli','Brussels Sprouts','Carrots','Cauliflower','Cayenne Pepper','Cherry Tomatoes','Cilantro','Collards','Garlic','Green Beans','Green Cabbage','Habanero Pepper','Head Lettuce','Jalapeño Pepper','Kale','Loose Leaf Lettuce','Muskmelon','Okra','Onions','Potatoes','Pumpkins','Radishes','Red Cabbage','Roma Tomatoes','Slicer Tomatoes','Swiss Chard','Tomatillos','Turnips','Watermelon','Winter Squash']
print(MainDataFrame.groupby(CropTypes))
for CropType in CropTypes:
    Votes = MainDataFrame.groupby(CropType)
    #print(type(Votes.size()[0]))
    AddToDictionary(TotalVotes, CropType, Votes.size()[0])
#print(TotalVotes)
NewSheetFromDictionary(TotalVotes, "Sheet 1", "Total Votes")


#CropVotes = MainDataFrame.groupby(['

#Number of responses for each language at each site location. 2
#['IPAddress'] = {['Language'] = NumberResponses}
TotalResponses = {}

#3&4
#['IPAddress'] = {['Email'] = Name, ['Responses'] = NumberResponses}

#4
#['IPAddress'] = {}

LanguageResponses = MainDataFrame.groupby('What Language Do You Speak?')

Writer.save()