import folium as fl
import pandas as pd

df = pd.read_csv('./datafiles/data.txt'
	, sep = '|'
	)


map_ = fl.Map(location = [df.lat.iloc[0]
						 , df.lng.iloc[0]]
	, tiles = 'cartodbpositron'
	, zoom_start = 12)

for item in df.itertuples():
	fl.Circle(location = (item.lat, item.lng)
		, color = item.color
		, weight = 3
		, radius = 100
		, popup = item.location
		, fill = True
		, fill_color = item.color
		, fill_opacity = 0.2
		).add_to(map_)



map_.save("index.html")





