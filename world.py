import vincent
world_countries = r'world-countries.json'
world = vincent.Map(width=1200, height=1000)
world.geo_data(projection='winkel3', scale=200, world=world_countries)
world.to_json(path)