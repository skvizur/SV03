import pandas as pd
import psycopg2
import getpass
import pprint
import random as r
import string
import itertools

#FEMALE AND MALE TABLES

cols_world = ['Country','Sex', 'Age group', 'year_2010','year_2014']
world_table = pd.read_csv('BMI_heimur.csv', sep =',', header = None, names = cols_world, engine = 'python', skiprows =2)

world_Table = world_table.sort_values(by='Sex',ascending=True)
world_Table = world_Table[world_Table.year_2010 != 'No data']
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




#PERCENTAGE TABLES

cols = ['Country','BothSexes2010','Female (%) 2010', 'Male (%) 2010','Both Sexes (%) 2014', 'Female (%) 2014', 'Male (%) 2014']
world_table_percentage = pd.read_csv('Londin.csv', sep =',"', header = None, names = cols, engine = 'python', skiprows = 4)

world_table_percentage = world_table_percentage[world_table_percentage.BothSexes2010!= '"No data""']
world_table_percentage=world_table_percentage.rename(columns = {'BothSexes2010':'Both Sexes (%) 2010'})
world_table_percentage.drop(world_table_percentage.columns[[1,4]], axis=1, inplace=True)


world_table_percentage['Female (%) 2010'] = world_table_percentage['Female (%) 2010'].map(lambda x: x.split('[')[0].lstrip('"'))
world_table_percentage['Female (%) 2014'] = world_table_percentage['Female (%) 2014'].map(lambda x: x.split('[')[0].lstrip('"'))
world_table_percentage['Male (%) 2010'] = world_table_percentage['Male (%) 2010'].map(lambda x: x.split('[')[0].lstrip('"'))
world_table_percentage['Male (%) 2014'] = world_table_percentage['Male (%) 2014'].map(lambda x: x.split('[')[0].lstrip('"'))

world_table_percentage['Country'] = world_table_percentage['Country'].map(lambda x: x.lstrip('"'))
world_table_percentage['Country nr.'] = range(1, len(world_table_percentage) + 1)

female_world_percentage = world_table_percentage[['Country nr.', 'Country','Female (%) 2010','Female (%) 2014']]


year1_KVKpr = list(female_world_percentage.iloc[:,2])
year2_KVKpr = list(female_world_percentage.iloc[:,3])

kvk_pr = {}

for i in range(len(country_nr)):
	kvk_pr[i] = {'countryid':country_nr[i],'female_pr_2010':year1_KVKpr[i],'female_pr_2014':year2_KVKpr[i]}
	


male_world_percentage = world_table_percentage[['Country nr.','Country','Male (%) 2010','Male (%) 2014']]


year1_KKpr = list(male_world_percentage.iloc[:,2])
year2_KKpr = list(male_world_percentage.iloc[:,3])

kk_pr = {}

for i in range(len(country_nr)):
	kk_pr[i] = {'countryid':country_nr[i],'male_pr_2010':year1_KKpr[i],'male_pr_2014':year2_KKpr[i]}
	


#TENGJAST GAGNAGRUNN

host = 'localhost'
dbname = 'obesity'

username = input('User name for {}.{}: '.format(host,dbname)) 
pw = getpass.getpass()

conn_string = "host='{}' dbname='{}' user='{}' password='{}'".format(host, dbname, username, pw)

print("Connecting to database {}.{} as {}".format(host, dbname, username))

conn = psycopg2.connect(conn_string)

cursor = conn.cursor()

print("Connected!\n")


for a in country:
	cursor.execute("insert into country (country_id, country_name) values('{}','{}')\n".format(country[a]['country_id'],country[a]['country_name'].replace("'","''").strip()))

for b in kk:
	cursor.execute("insert into kk (countryid, male_2010, male_2014) values('{}','{}','{}')\n".format(kk[b]['countryid'],kk[b]['male_2010'].strip(),kk[b]['male_2014'].strip()))

for c in kvk:
	cursor.execute("insert into kvk (countryid,female_2010,female_2014) values('{}','{}','{}')\n".format(kvk[c]['countryid'],kvk[c]['female_2010'].strip(),kvk[c]['female_2014'].strip()))

for d in kk_pr:
	cursor.execute("insert into kk_pr (countryid, male_pr_2010, male_pr_2014) values('{}','{}','{}')\n".format(kk_pr[d]['countryid'],kk_pr[d]['male_pr_2010'],kk_pr[d]['male_pr_2014'].strip()))

for e in kvk_pr:
	cursor.execute("insert into kvk_pr (countryid, female_pr_2010, female_pr_2014) values('{}','{}','{}')\n".format(kvk_pr[e]['countryid'],kvk_pr[e]['female_pr_2010'],kvk_pr[e]['female_pr_2014'].strip()))



conn.commit()


cursor.close()
conn.close()




