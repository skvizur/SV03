import pandas as pd
import psycopg2
import getpass
import pprint
import random as r
import string
import itertools
import pandas as pd
from sqlalchemy import create_engine

#FEMALE AND MALE TABLES
cols_world = ['Country','Sex', 'Age group', 'year_2014','year_2010']
world_table = pd.read_csv('BMI_heimur.csv', sep =',', header = None, names = cols_world, engine = 'python', skiprows =2)

world_Table = world_table.sort_values(by='Sex',ascending=True)
#world_Table['year_2010'] = world_Table['year_2010'].map(lambda x:x.rstrip('No data'))
#world_Table['year_2014'] = world_Table['year_2014'].map(lambda x:x.rstrip('No data'))
world_Table = world_Table[world_Table.Country != 'South Sudan']
world_Table.drop(world_Table.columns[[2]], axis=1, inplace=True)



world_Table['year_2010'] = world_Table['year_2010'].map(lambda x: x.split('[')[0])
world_Table['year_2014'] = world_Table['year_2014'].map(lambda x: x.split('[')[0])


UniqueNames = world_Table.Sex.unique()

DataFrameDict = {elem : pd.DataFrame for elem in UniqueNames}

for key in DataFrameDict.keys():
    DataFrameDict[key] = world_Table[:][world_Table.Sex == key]


only_males = DataFrameDict[' Male']
only_males=only_males.rename(columns = {'Country': 'Country','Sex':'Sex','year_2010':'Male 2010','year_2014':'Male 2014'})
only_males.drop(only_males.columns[[1]], axis = 1, inplace = True)
only_males = only_males[['Country','Male 2010','Male 2014']]
only_males = only_males.sort_values(by='Country',ascending=True)
only_males['Country nr.'] = range(1, len(only_males) + 1)
only_males = only_males[['Country nr.','Country','Male 2010','Male 2014']]



year1_KK = list(only_males.iloc[:,2])
year2_KK = list(only_males.iloc[:,3])



only_females = DataFrameDict[' Female']
only_females=only_females.rename(columns = {'Country': 'Country','Sex':'Sex','year_2010':'Female 2010','year_2014':'Female 2014'})
only_females.drop(only_females.columns[[1]], axis = 1, inplace = True)
only_females = only_females[['Country','Female 2010','Female 2014']]
only_females = only_females.sort_values(by='Country',ascending=True)
only_females['Country nr.'] = range(1, len(only_females) + 1)
only_females = only_females[['Country nr.','Country','Female 2010','Female 2014']]




country_nr = list(only_females.iloc[:,0])
country_name = list(only_females.iloc[:,1])
year1_KVK = list(only_females.iloc[:,2])
year2_KVK = list(only_females.iloc[:,3])

country = {}

for i in range(len(country_nr)):
	country[i] = {'country_id':country_nr[i],'country_name':country_name[i]}


index = 0
kvk = {}

for i in range(len(country_nr)):
	kvk[i] = {'countryid':country_nr[i],'female_2010':year1_KVK[i],'female_2014':year2_KVK[i]}


index = 0
kk = {}

for i in range(len(country_nr)):
	kk[i] = {'countryid':country_nr[i],'male_2010':year1_KK[i],'male_2014':year2_KK[i]}






#______________________________________________________________

past_years_table = pd.read_csv('datayears.csv',delimiter = ',', sep = '"', header = 0, engine = 'python', skiprows = 1)
df2 = past_years_table[past_years_table.columns[0]].apply(lambda x: pd.Series(x.split(',')))

df3 = pd.DataFrame(data = df2)
df3.columns = [past_years_table.columns[0].split(',')]
df3.drop(df3.columns[[2]], axis = 1, inplace = True)
df4 = df3.sort_values(by = '"Sex"', ascending = True)


for i in range(2009,1979,-1):
	df4['"%d"'%i] = df4['"%d"'%i].map(lambda x: x.split('[')[0].lstrip('"').rstrip('"'))
	#df4['"%d"'%i] = df4['"%d"'%i].map(lambda x: x.replace(' ‰Û_','-1'))
	df4=df4.rename(columns = {'"%d"'%i:'%d'%i})


df4 = df4.rename(columns = {'"Sex"':'Sex'})
df4['Sex'] = df4['Sex'].map(lambda x: x.lstrip('"').rstrip('"'))

print(df4)

UniqueNames = df4.Sex.unique()

DataFrameDict = {elem : pd.DataFrame for elem in UniqueNames}

for key in DataFrameDict.keys():
    DataFrameDict[key] = df4[:][df4.Sex == key]


females_years = DataFrameDict['Female']
females_years.drop(females_years.columns[[1]], axis = 1, inplace = True)
females_years = females_years.sort_values(by = 'Country', ascending = True)
females_years['Country nr.'] = range(1, len(females_years) + 1)
#print(females_years)

countries = pd.DataFrame({'country_id': females_years['Country nr.'], 'country_name': females_years['Country']})
print(countries)

females_years = females_years[['Country nr.','1980','1981','1982','1983','1984','1985','1986','1987',
'1988','1989','1990','1991','1992','1993','1994','1995','1996','1997','1998','1999','2000','2001','2002',
'2003','2004','2005','2006','2007','2008','2009']]
females_years['2010'] = year1_KVK
females_years['2014'] = year2_KVK

updated_females = pd.melt(females_years, id_vars = 'Country nr.',value_vars = list(females_years.columns[1:]), var_name = 'Year',value_name = 'Female BMI')
updated_females = updated_females.sort_values(by = 'Country nr.', ascending = True)
#print(updated_females)

kvk_all_years = list(updated_females.iloc[:,2])


males_years = DataFrameDict['Male']
males_years.drop(males_years.columns[[1]], axis = 1, inplace = True)
males_years = males_years.sort_values(by = 'Country', ascending = True)
males_years['Country nr.'] = range(1, len(males_years) + 1)
males_years = males_years[['Country nr.','1980','1981','1982','1983','1984','1985','1986','1987',
'1988','1989','1990','1991','1992','1993','1994','1995','1996','1997','1998','1999','2000','2001','2002',
'2003','2004','2005','2006','2007','2008','2009']]
males_years['2010'] = year1_KK
males_years['2014'] = year2_KK

males_years = males_years.rename(columns = {'Country nr.':'countryid'})	

#print(males_years)	

updated_males = pd.melt(males_years, id_vars = 'countryid',value_vars = list(males_years.columns[1:]), var_name = 'year',value_name = 'bmi_male')
updated_males = updated_males.sort_values(by = 'countryid', ascending = True)
updated_males['bmi_female'] = kvk_all_years
updated_males = updated_males.sort_values(by = ['countryid'], ascending = True)
print(updated_males)




#TENGJAST GAGNAGRUNN

host = 'localhost'
dbname = 'obesity'

username = 'hildurrungudjonsdottir' #input('User name for {}.{}: '.format(host,dbname)) 
pw = '1313' #getpass.getpass()

conn_string = "host='{}' dbname='{}' user='{}' password='{}'".format(host, dbname, username, pw)

print("Connecting to database {}.{} as {}".format(host, dbname, username))

conn = psycopg2.connect(conn_string)

cursor = conn.cursor()

print("Connected!\n")

engine = create_engine('postgresql://hildurrungudjonsdottir:hildurrungudjonsdottir@localhost/obesity')

countries.to_sql('country', engine, if_exists = 'append', index = False)
#id_year.to_sql('years', engine, if_exists = 'append', index = False)
updated_males.to_sql('bmi', engine, if_exists = 'append', index = False)

conn.commit()


s = """ update bmi 
		set bmi_male = NULL 
		where bmi_male < 0; """

cursor.execute(s)		

cursor.execute("update bmi set bmi_female = NULL where bmi_female < 0;")


cursor.close()
conn.close()

