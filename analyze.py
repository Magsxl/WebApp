import os
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.tree import DecisionTreeClassifier
from sqlalchemy import create_engine
from dtreeviz.trees import dtreeviz
from sklearn import tree

#Reading tables from MySQL Database
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

#Cleaning useless white spaces
ankietowany['Zawod'] = ankietowany['Zawod'].str.strip()

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

#Translate string values to int
ankietowany.loc[ankietowany['Pochodzenie'].str.contains('250', na=False), 'Pochodzenie'] = 250
ankietowany.loc[ankietowany['Pochodzenie'].str.contains('100', na=False), 'Pochodzenie'] = 100
ankietowany.loc[ankietowany['Pochodzenie'].str.contains('Miasteczko', na=False), 'Pochodzenie'] = 30
ankietowany.loc[ankietowany['Pochodzenie'].str.contains('Wie', na=False), 'Pochodzenie'] = 0
ankietowany.loc[ankietowany['Plec'].str.contains('M', na=False), 'Plec'] = 0
ankietowany.loc[ankietowany['Plec'].str.contains('F', na=False), 'Plec'] = 1
ankietowany.loc[ankietowany['Status'].str.contains('Student', na=False), 'Status'] = 0
ankietowany.loc[ankietowany['Status'].str.contains('Pracownik', na=False), 'Status'] = 1
ankietowany.loc[ankietowany['Status'].str.contains('Ucz', na=False), 'Status'] = 2
ankietowany.loc[ankietowany['Zawod'].str.contains('Brak', na=False), 'Zawod'] = 0
ankietowany.loc[ankietowany['Zawod'].str.contains('[A-Za-z]', na=False), 'Zawod'] = 1

#Check if there's empty row and fill it
if ankietowany['Zawod'].isnull:
    ankietowany['Zawod'] = ankietowany['Zawod'].fillna("Brak")

#Write corrected and concated version to csv
result.to_csv(r'static/result.csv', encoding='cp1252', sep=";")
ankietowany.to_csv(r'static/ankietowany_out.csv', encoding='cp1252', sep=";", index=False)

#Get only students from ankietowany
ankStudent = ankietowany[ankietowany['Status']==0]
ankStudent = ankStudent[['ID', 'Status']]

#Get only workers from ankietowany
ankPE = ankietowany[ankietowany['Status']==1]
ankPE = ankPE[['ID', 'Status']]

#DATA EXPLORATION
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

#Dictionary with questions
quesDict = {
    0: "Czy jest dla Ciebie ważna ochrona środowiska?",
    1: "Czy wiedziałeś, że coraz częściej sięga się po drony w ochronie środowiska?",
    2: "Czy wiedziałeś, że drony znajdują coraz powszechniejsze użycie w codziennym życiu, np. przesyłki kurierskie, policyjne?",
    3: "Czy kiedykolwiek miałeś styczność z wykorzystaniem dronów jak w poprzednich pytaniach?",
    4: "Czy uważasz, że rozpowszechnienie dronów może stworzyć zagrożenia, które obecnie nie występują?",
    5: "Czy uważasz, że drony powinny być używane do sztucznego kształtowania systemów biologicznych?",
    6: "Czy uważasz, że wykorzystanie dronów w eksplorowaniu ciężko dostępnych miejsc, może mieć negatywny wpływ na tamtejsze środowisko?",
    7: "Czy uważasz, że drony mogą stanowić zagrożenie dla dzikich zwierząt?",
    8: "Czy uważasz, że wykorzystanie dronów w monitorowaniu pól rolniczych, lasów oraz nabrzeży może budzić dyskomfort u osób przebywających na wymienionych terenach?",
    9: "Czy uważasz, że drony są tańszym rozwiązaniem niż obecnie używane środki w ochronie środowiska?",
    10: "Czy uważasz, że drony w ochronie środowiska powinny być eksploatowane przez prywatne instytucje?",
    11: "Czy uważasz, że wykorzystanie dronów w ochronie środowiska powinno zostać dofinansowane przez państwo?",
    12: "Czy uważasz, że powinno się zwiększyć wykorzystanie dronów w ochronie środowiska oraz monitorowaniu zagrożeń z tym związanych?",
    13: "Czy uważasz, że wykorzystanie dronów przynosi więcej korzyści niż zagrożeń?",
    14: "Czy uważasz, że używanie dronów w ochronie środowiska jest przyszłościowe?",
}

#Answers for every question
for row in range (0,15):
    quesAns = pd.DataFrame(result.apply(pd.Series.value_counts, axis=1).fillna(0))
    rowAns = quesAns.iloc[row].to_frame().T
    rowAns.columns=['Zdecydowanie tak', 'Raczej tak', 'Nie wiem', 'Raczej nie', 'Zdecydowanie nie']
    rowAns = rowAns.astype('int')
    f, ax = plt.subplots(figsize=(15,6))
    rows = sns.barplot(data=rowAns).set(title=quesDict[row])
    plt.yticks([5,10,15,20,25,30])
    plt.show()

#Answers distribution for people
ankStatus = ankietowany['Status'].value_counts().to_frame().T
ankStatus.columns = ['Student', 'Pracownik etatowy', 'Uczeń']
ankStat = sns.barplot(data=ankStatus)
plt.show()

#Get answers of only students
answers=pd.DataFrame()
for x in range(1,countCol):
    if x in ankStudent['ID']:
        if x in result.columns:
            fileName = "res"+str(x)
            resX = result[x].apply(pd.Series)
            resX.columns=['Odpowiedzi']
            resX.to_csv(fileName+".csv", encoding='cp1252', sep=";")
            resX = pd.read_csv(fileName+".csv", encoding='cp1252', sep=";")
            answers = answers.append(resX)
            os.remove(fileName+".csv")
answers.to_csv('static/answers.csv', encoding='cp1252', sep=";", index=False)

#Plot students answers
answers = pd.read_csv('static/answers.csv', encoding='cp1252', sep=";")
ansCount1 = answers.Odpowiedzi.eq(1).sum()
ansCount2 = answers.Odpowiedzi.eq(2).sum()
ansCount3 = answers.Odpowiedzi.eq(3).sum()
ansCount4 = answers.Odpowiedzi.eq(4).sum()
ansCount5 = answers.Odpowiedzi.eq(5).sum()

answerCount = {'Zdecydowanie tak': ansCount1, 'Raczej tak': ansCount2, 'Nie wiem': ansCount3, 'Raczej nie': ansCount4, 'Zdecydowanie nie': ansCount5}

dfAnswer = pd.DataFrame.from_dict(answerCount, orient='index', columns = ['Ilosc odpowiedzi']).T
f, ax = plt.subplots(figsize=(10,7))
sns.barplot(data=dfAnswer).set(title="Odpowiedzi studentów")
plt.show()

#Get answers of only workers
answersPE=pd.DataFrame()
for x in range(1,countCol):
    if x in ankPE['ID']:
        if x in result.columns:
            fileName = "resPE"+str(x)
            resX = result[x].apply(pd.Series)
            resX.columns=['Odpowiedzi']
            resX.to_csv(fileName+".csv", encoding='cp1252', sep=";")
            resX = pd.read_csv(fileName+".csv", encoding='cp1252', sep=";")
            answersPE = answersPE.append(resX)
            os.remove(fileName+".csv")
answersPE.to_csv('static/answersPE.csv', encoding='cp1252', sep=";", index=False)

#Plot workers answers
answersPE = pd.read_csv('static/answersPE.csv', encoding='cp1252', sep=";")
ansPECount1 = answersPE.Odpowiedzi.eq(1).sum()
ansPECount2 = answersPE.Odpowiedzi.eq(2).sum()
ansPECount3 = answersPE.Odpowiedzi.eq(3).sum()
ansPECount4 = answersPE.Odpowiedzi.eq(4).sum()
ansPECount5 = answersPE.Odpowiedzi.eq(5).sum()

answerCountPE = {'Zdecydowanie tak': ansPECount1, 'Raczej tak': ansPECount2, 'Nie wiem': ansPECount3, 'Raczej nie': ansPECount4, 'Zdecydowanie nie': ansPECount5}

dfAnswerPE = pd.DataFrame.from_dict(answerCountPE, orient='index', columns = ['Ilosc odpowiedzi']).T
f, ax = plt.subplots(figsize=(10,7))
sns.barplot(data=dfAnswerPE).set(title="Odpowiedzi pracowników etatowych")
plt.show()

#Get all answers for particular questions
nrAns = pd.DataFrame(result.values).T
nrAns.columns = ['NrPytania_1', 'NrPytania_2', 'NrPytania_3', 'NrPytania_4', 'NrPytania_5', 'NrPytania_6', 'NrPytania_7', 'NrPytania_8', 'NrPytania_9', 'NrPytania_10', 'NrPytania_11', 'NrPytania_12', 'NrPytania_13', 'NrPytania_14', 'NrPytania_15']
ankietowanyAns = pd.concat([ankietowany, nrAns], axis=1, join="inner")
ankietowanyAns = ankietowanyAns.drop(['Timestamp'], axis=1)
ankietowanyAns = ankietowanyAns.drop(['ID'], axis=1)
ankietowanyAns.to_csv('static/allAns.csv', encoding='cp1252', sep=";", index=False)

#Create heatmap with correlation between people and anwsers
ankietowanyAns['Status'] = pd.to_numeric(ankietowany['Status'])
ankietowanyAns['Plec'] = pd.to_numeric(ankietowany['Plec'])
ankietowanyAns['Pochodzenie'] = pd.to_numeric(ankietowany['Pochodzenie'])

plt.figure(figsize=(20,20),dpi = 100)
sns.heatmap(ankietowanyAns.corr(),annot = ankietowanyAns.corr())
plt.show()

#Decision tree
features = list(ankietowanyAns.columns[:5])
y = ankietowanyAns['NrPytania_4']
x = ankietowanyAns[features].values
dt = DecisionTreeClassifier(min_samples_split=10, random_state=99)
dt.fit(x,y)
class_list = ['Zdecydowanie tak','Raczej tak','Nie wiem','Raczej nie','Zdecydowanie nie']
plt.figure(figsize=(20,20), dpi=50)
tree.plot_tree(dt, feature_names=features, class_names=list(class_list), rounded=True, filled=True)
plt.show()
viz = dtreeviz(dt, x, y, target_name="NrPytania_4", feature_names=features, class_names=list(class_list))
viz.view()