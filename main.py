import pandas as pd
import psycopg2
import getpass
import pprint
import random as r
import string
import itertools
import FOLL as F

#FEMALE AND MALE TABLES

cols_world = ['Country','Sex', 'Age group', 'year_2010','year_2014']

cols_world = ['Country','Sex', 'Age group', 'year_2014','year_2010']

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

cols = ['Country','BothSexes2014','Female (%) 2014', 'Male (%) 2014','Both Sexes (%) 2010', 'Female (%) 2010', 'Male (%) 2010']
world_table_percentage = pd.read_csv('Londin.csv', sep =',"', header = None, names = cols, engine = 'python', skiprows = 4)

world_table_percentage = world_table_percentage[world_table_percentage.BothSexes2014!= '"No data""']
world_table_percentage=world_table_percentage.rename(columns = {'BothSexes2014':'Both Sexes (%) 2014'})
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


cols_names = ['Country','Continent']
world_countries = pd.read_csv('country_continent.csv', sep =',', header = None, names = cols_names, engine = 'python', skiprows =1)
world_Countries = world_countries.sort_values(by='Continent',ascending=True)

only_continent = []
only_continent = world_Countries['Continent']
only_countries = []
only_countries = world_Countries['Country']

country_continent = {}
for i in range(len(only_continent)):
	country_continent[i] = {'country':only_countries[i],'continent':only_continent[i]}
	print(country_continent[i])
	


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

test = """ 
select country_id
from country"""
cursor.execute(test)
is_empty = len(cursor.fetchall())

#LESUM INN Í TOFLURNAR EF ÞAÐ HEFUR EKKI NÚ ÞEGAR VERIÐ GERT
if is_empty is 0:

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

	for f in country_continent:
		cursor.execute("insert into country_continent (country, continent) values ('{}','{}')\n".format(country_continent[f]['country'].strip(),country_continent[f]['continent'].strip()))

name = input("Hi, what is your name? ")
weight = float(input("What is your body weight in kilograms ? "))
if weight <= 0 or weight > 500:
	print("Weight cannot be less than 0 kg or more than 500 kg, try again..")
	weight = float(input("What is your body weight in kilograms ? "))

height = float(input("What is your height in cm ? "))
if height <= 0:
	print("Height cannot be less than 0 cm..")
	height = float(input("What is your height in cm ? "))

sex = input("What is your gender (Male/Female)? ")
if sex != 'Female' and sex != 'Male':
	print("You need to enter either Male or Female, try again..")
	sex = input("What is your gender (Male/Female)? ")

country = input("What country do you live in? ")
#c = """
#select country_name 
#from country
#where country_name = %s """ % country
#cursor.execute(c)
#c = cursor.fetchall()
#if len(c) is 0:
#	print("The country you entered is not valid, try again..")
#	country = input("What country do you live in? ")

m = float(height/100)
BMI = float(weight / (m*m))
BMI = float(format(BMI,'.2f'))
print("\n")
print("Hi {}, your BMI (Body Mass Index) is {}". format(name,BMI))

if BMI < 18.5:
	print("You have to gain a lot of weight to be obese!")
elif 18.5 <= BMI <= 24:
	print("You are in the normal weight range, that is good!")
elif 24 < BMI <= 25:
	print("You are in the normal weight range, but you have to be careful...")
elif 25 < BMI < 30:
	print("You are overweight.")
else:
	print("You are obese, get help!")

print("\n")

if sex == 'Female':
	ave_bmi_country = F.ave_bmi_kvk_country(country, cursor)[0][0]
	ave_bmi_country = float(format(ave_bmi_country, '.2f'))
	ave_bmi_world = F.ave_bmi_kvk_world(cursor)[0][0]
	ave_bmi_world = float(format(ave_bmi_world, '.2f'))
elif sex == 'Male':
	ave_bmi_country = F.ave_bmi_kk_country(country, cursor)[0][0]
	ave_bmi_country = float(format(ave_bmi_country, '.2f'))
	ave_bmi_world = F.ave_bmi_kk_world(cursor)[0][0]
	ave_bmi_world = float(format(ave_bmi_world, '.2f'))

print("The average BMI for {} in {} is {}".format(sex, country, ave_bmi_country))
print("The average BMI for {} in the world is {}".format(sex, ave_bmi_world))

if ave_bmi_world > BMI:
	prosenta = (BMI / ave_bmi_world)*100
	prosenta = format(prosenta, '.2f')
	print("You have a lower BMI than {}% of {} in the world".format(prosenta, sex))
elif ave_bmi_world < BMI:
	prosenta = (ave_bmi_world / BMI)*100
	prosenta = format(prosenta, '.2f')
	print("You have a higher BMI than {}% of {} in the world".format(prosenta, sex))

if ave_bmi_country > BMI:
	prosenta = (BMI / ave_bmi_country)*100
	prosenta = format(prosenta, '.2f')
	print("You have a lower BMI than {}% of {} in {}".format(prosenta, sex, country))
elif ave_bmi_country < BMI:
	prosenta = (ave_bmi_country / BMI)*100
	prosenta = format(prosenta, '.2f')
	print("You have a higher BMI than {}% of {} in {}".format(prosenta, sex, country))




conn.commit()


cursor.close()
conn.close()





