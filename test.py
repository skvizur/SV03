import pandas as pd
import psycopg2
import getpass
import pprint
import random as r
import string
import itertools

#FEMALE AND MALE TABLES

cols = ['Country','BothSexes2010','Female (%) 2010', 'Male (%) 2010','Both Sexes (%) 2014', 'Female (%) 2014', 'Male (%) 2014']
world_table_percentage = pd.read_csv('Londin.csv', sep =',"', header = None, names = cols, engine = 'python', skiprows = 4)

world_table_percentage = world_table_percentage[world_table_percentage.BothSexes2010!= '"No data""']
world_table_percentage=world_table_percentage.rename(columns = {'BothSexes2010':'Both Sexes (%) 2010'})
world_table_percentage.drop(world_table_percentage.columns[[1,4]], axis=1, inplace=True)

pd.set_option('display.max_rows', 1000)
print(world_table_percentage)

