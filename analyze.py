from matplotlib import container
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


#Answers for every question
quesDict = {
    1: "Czy jest dla Ciebie ważna ochrona środowiska?",
    2: "Czy wiedziałeś, że coraz częściej sięga się po drony w ochronie środowiska?",
    3: "Czy wiedziałeś, że drony znajdują coraz powszechniejsze użycie w codziennym życiu, np. przesyłki kurierskie, policyjne?",
    4: "Czy kiedykolwiek miałeś styczność z wykorzystaniem dronów jak w poprzednich pytaniach?",
    5: "Czy uważasz, że rozpowszechnienie dronów może stworzyć zagrożenia, które obecnie nie występują?",
    6: "Czy uważasz, że drony powinny być używane do sztucznego kształtowania systemów biologicznych?",
    7: "Czy uważasz, że wykorzystanie dronów w eksplorowaniu ciężko dostępnych miejsc, może mieć negatywny wpływ na tamtejsze środowisko?",
    8: "Czy uważasz, że drony mogą stanowić zagrożenie dla dzikich zwierząt?",
    9: "Czy uważasz, że wykorzystanie dronów w monitorowaniu pól rolniczych, lasów oraz nabrzeży może budzić dyskomfort u osób przebywających na wymienionych terenach?",
    10: "Czy uważasz, że drony są tańszym rozwiązaniem niż obecnie używane środki w ochronie środowiska?",
    11: "Czy uważasz, że drony w ochronie środowiska powinny być eksploatowane przez prywatne instytucje?",
    12: "Czy uważasz, że wykorzystanie dronów w ochronie środowiska powinno zostać dofinansowane przez państwo?",
    13: "Czy uważasz, że powinno się zwiększyć wykorzystanie dronów w ochronie środowiska oraz monitorowaniu zagrożeń z tym związanych?",
    14: "Czy uważasz, że wykorzystanie dronów przynosi więcej korzyści niż zagrożeń?",
    15: "Czy uważasz, że używanie dronów w ochronie środowiska jest przyszłościowe?",
}

for row in range (0,14):
    quesAns = pd.DataFrame(result.apply(pd.Series.value_counts, axis=1).fillna(0))
    rowAns = quesAns.iloc[row].to_frame().T
    rowAns.columns=['Zdecydowanie tak', 'Raczej tak', 'Nie wiem', 'Raczej nie', 'Zdecydowanie nie']
    rowAns = rowAns.astype('int')
    f, ax = plt.subplots(figsize=(15,6))
    rows = sns.barplot(data=rowAns).set(title=quesDict[row+1])
    plt.yticks([5,10,15,20,25,30])
    plt.show()