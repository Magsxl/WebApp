import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
from sqlalchemy import Column, create_engine
'''
sqlEngine = create_engine('mysql+pymysql://mgasxl:Najlepszy@magsxl.mysql.pythonanywhere-services.com/magsxl$ankieta', pool_recycle=3600)

dbConn = sqlEngine.connect()

ankietowany = pd.read_sql("select*from ankietowany", dbConn)
pytania1_4 = pd.read_sql("select*from pytania1_4", dbConn)
pytania5_12 = pd.read_sql("select*from pytania5_12", dbConn)
pytania13_15 = pd.read_sql("select*from pytania13_15", dbConn)'''

#Read files for testing purposes 
ankietowany = pd.read_csv(r'static/ankietowany.csv', encoding='cp1252', sep=";")
pytania1_4 = pd.read_csv(r'static/pytania1_4.csv', encoding='cp1252', sep=";", usecols = ['Nr_Pytania', 'Odpowiedz', 'Person_ID'])
pytania5_12 = pd.read_csv(r'static/pytania5_12.csv', encoding='cp1252', sep=";", usecols = ['Nr_Pytania', 'Odpowiedz', 'Person_ID'])
pytania13_15 = pd.read_csv(r'static/pytania13_15.csv', encoding='cp1252', sep=";", usecols = ['Nr_Pytania', 'Odpowiedz', 'Person_ID'])

#Translate string values to int
ankietowany.loc[ankietowany['Pochodzenie'].str.contains('250'), 'Pochodzenie'] = '250'
ankietowany.loc[ankietowany['Pochodzenie'].str.contains('100'), 'Pochodzenie'] = '100'
ankietowany.loc[ankietowany['Pochodzenie'].str.contains('Miasteczko'), 'Pochodzenie'] = '30'
ankietowany.loc[ankietowany['Pochodzenie'].str.contains('Wie'), 'Pochodzenie'] = '0'

#Cleaning useless white spaces
ankietowany['Zawod'] = ankietowany['Zawod'].str.strip()

#Counting people without job
#print("Liczba osób bez zawodu: " + str(ankietowany.Zawod.str.count("Brak").sum()))

#Pivot questions
pytania1_4 = pytania1_4.pivot(index="Nr_Pytania", columns=["Person_ID"], values="Odpowiedz")
pytania5_12 = pytania5_12.pivot(index="Nr_Pytania", columns=["Person_ID"], values="Odpowiedz")
pytania13_15 = pytania13_15.pivot(index="Nr_Pytania", columns=["Person_ID"], values="Odpowiedz")

#concate questions
pytania = [pytania1_4, pytania5_12, pytania13_15]
result = pd.concat(pytania)

#Clean ankietowany without answers
countCol = len(result.columns)
for x in range(1,countCol):
    if not x in result.iloc[0]:
        ankietowany = ankietowany[ankietowany.ID != x]

#Check if there's empty row and fill it
if ankietowany['Zawod'].isnull:
    ankietowany['Zawod'] = ankietowany['Zawod'].fillna("Brak")

#Write corrected and concated version to csv
result.to_csv(r'static/result.csv', encoding='cp1252', sep=";")
ankietowany.to_csv(r'static/ankietowany_out.csv', encoding='cp1252', sep=";", index=False)

#DATA EXPLORATION
'''
for x in range(1,countCol):
    colName = result.columns[x]
    if x in result.iloc[0]:
        print("Answers for: " + str(colName) + "\n" + str(result[x].values))
    else:
        print("Value: " + str(x) + " doesn't exist")
'''
#All answers distribution
resultValues = {'Odpowiedzi': ['Zdecydowanie tak', 'Raczej tak', 'Nie wiem', 'Raczej nie', 'Zdecydowanie nie'], 'Ilosc': [(result.values==1).sum(), (result.values==2).sum(), (result.values==3).sum(), (result.values==4).sum(), (result.values==5).sum()]}
resultVal = pd.DataFrame(data=resultValues)
f, ax = plt.subplots(figsize=(10,7))
resultValPlot = sns.barplot(x='Odpowiedzi', y='Ilosc', palette="Blues_d", data=resultVal)
resultValPlot.bar_label(resultValPlot.containers[0])
plt.show()

#Answers distribution
ans1 = result.eq(1).sum(axis=1).to_frame().T
ans2 = result.eq(2).sum(axis=1).to_frame().T
ans3 = result.eq(3).sum(axis=1).to_frame().T
ans4 = result.eq(4).sum(axis=1).to_frame().T
ans5 = result.eq(5).sum(axis=1).to_frame().T

#Plot answers distribution
resPartPlot = sns.barplot(data=ans1).set(title='Zdecydowanie tak')
plt.figure()
resPartPlot2 = sns.barplot(data=ans2).set(title='Raczej tak')
plt.figure()
resPartPlot3 = sns.barplot(data=ans3).set(title='Nie wiem')
plt.figure()
resPartPlot4 = sns.barplot(data=ans4).set(title='Raczej nie')
plt.figure()
resPartPlot5 = sns.barplot(data=ans5).set(title='Zdecydowanie nie')
plt.show()

#Answers for first question
#ques1 = result.eq(1).sum(axis=1).to_frame().T
#print(result.loc[result[1]==1])