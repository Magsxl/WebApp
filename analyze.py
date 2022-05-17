from encodings import utf_8
import pandas as pd
import numpy as np

ankietowany = pd.read_csv(r'static/ankietowany.csv', encoding='cp1252', sep=";", index=False)
pytania1_4 = pd.read_csv(r'static/pytania1_4.csv', encoding='cp1252', sep=";", index=False)
pytania5_12 = pd.read_csv(r'static/pytania5_12.csv', encoding='cp1252', sep=";", index=False)
pytania13_15 = pd.read_csv(r'static/pytania13_15.csv', encoding='cp1252', sep=";", index=False)

#Prints how many rows have null values
#print(len(ankietowany[pd.isnull(ankietowany.Zawod)]))

if ankietowany['Zawod'].isnull:
    ankietowany['Zawod'] = ankietowany['Zawod'].fillna("Brak")

ankietowany.to_csv(r'static/ankietowany_out.csv', encoding='cp1252', sep=";", index=False)