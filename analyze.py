import pandas as pd
import numpy as np
from sqlalchemy import create_engine
'''
sqlEngine = create_engine('mysql+pymysql://mgasxl:Najlepszy@magsxl.mysql.pythonanywhere-services.com/magsxl$ankieta', pool_recycle=3600)

dbConn = sqlEngine.connect()

ankietowany = pd.read_sql("select*from ankietowany", dbConn)
pytania1_4 = pd.read_sql("select*from pytania1_4", dbConn)
pytania5_12 = pd.read_sql("select*from pytania5_12", dbConn)
pytania13_15 = pd.read_sql("select*from pytania13_15", dbConn)'''

#Read files for testing purposes 
ankietowany = pd.read_csv(r'static/ankietowany.csv', encoding='cp1252', sep=";")
pytania1_4 = pd.read_csv(r'static/pytania1_4.csv', encoding='cp1252', sep=";")
pytania5_12 = pd.read_csv(r'static/pytania5_12.csv', encoding='cp1252', sep=";")
pytania13_15 = pd.read_csv(r'static/pytania13_15.csv', encoding='cp1252', sep=";")

#Prints how many rows have null values
#print(len(ankietowany[pd.isnull(ankietowany.Zawod)]))

ankietowany.loc[ankietowany['Pochodzenie'].str.contains('250'), 'Pochodzenie'] = '250'
ankietowany.loc[ankietowany['Pochodzenie'].str.contains('100'), 'Pochodzenie'] = '100'
ankietowany.loc[ankietowany['Pochodzenie'].str.contains('Miasteczko'), 'Pochodzenie'] = '30'
ankietowany.loc[ankietowany['Pochodzenie'].str.contains('Wie'), 'Pochodzenie'] = '0'

print(ankietowany)

'''
#Check if there's empty row and fill it
if ankietowany['Zawod'].isnull:
    ankietowany['Zawod'] = ankietowany['Zawod'].fillna("Brak")



#Write corrected version to csv
ankietowany.to_csv(r'static/ankietowany_out.csv', encoding='cp1252', sep=";", index=False)'''