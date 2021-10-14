#--------------------------#
#                          #
# Title: Sheet 3           #
#                          #
# Name: Jake Cermak        #
#                          #
#--------------------------#

import pandas as pd
import matplotlib as mpl
from matplotlib import pyplot as plt
import random as random
import xlsxwriter as xlsx

path = 'C:/Users/JakeC/OneDrive - Dunwoody College of Technology/SENG Year 3/SENG4340//Projects/Project 1/Part 2/Jake/'

filename = 'project_1_part_2.xlsx'
dataframe = pd.read_excel(path + filename)

wb = path + 'outputData.xlsx'
file = xlsx.Workbook(wb)
writer = pd.ExcelWriter(wb)

yes_people = dataframe[["Would you like to learn more?", "Name", "Email Address", "User IP"]] #using relevant columns
yes_people = yes_people.replace(['はい!','Oui!','Si'],'Yes!') #replacing foreign yeses with english yeses
yes_people = yes_people.replace('لا','Nope') #replacing arabic noes with nopes
yes_people = (yes_people.loc[yes_people['Would you like to learn more?'] == 'Yes!']) #filtering the dataframe by people that have said yes
yes_people = yes_people.drop(yes_people.columns[[0]], axis = 1) #dropping the yes column because it is no longer relevant at this point
print(yes_people)

yes_people.to_excel(writer, "Sheet 3", index = False)
writer.save()




