def ave_bmi_kk(country, cursor):
	sql = """
	select avg(k.female_2014)
	from kvk k, country c
	where k.countryid = c.country_id
	and c.country_name = '%s'
	""" % (country)
	cursor.execute(sql)
	ave = cursor.fetchall()
	return ave


def ave_bmi_kvk(country, cursor):
	sql = """
	select avg(k.male_2014)
	from kk k, country c
	where k.countryid = c.country_id
	and c.country_name = '%s'
	""" % (country)
	cursor.execute(sql)
	ave = cursor.fetchall()
	return ave
