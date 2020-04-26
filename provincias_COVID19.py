import pandas as pd
import folium
import os
import webbrowser

# https://www.salud.gob.ec/coronavirus-covid-19/
# https://almacenamiento.msp.gob.ec/index.php/s/JgWHk8QARpWbF3Z
# https://www.latlong.net/
# https://github.com/jpmarindiaz/geo-collection/blob/master/ecu/ecuador.geojson


pd.set_option('display.max_columns', None)


df_COV_EC = pd.read_csv('Base_covid19_msp_23abr2020.csv', sep=';', header='infer', encoding='ISO-8859-1')

print(df_COV_EC.head(5))

print(df_COV_EC.columns)

print(df_COV_EC.dtypes)

print(df_COV_EC.describe())


# Pre-processing data
se_provs = df_COV_EC[df_COV_EC['clasificacion_caso']=='Confirmado'].groupby(['prov_residencia']).count().loc[:, 'total_muestras']

df_provs = pd.DataFrame()
df_provs['prov_residencia'] = se_provs.index
df_provs['total_muestras'] = se_provs.values
df_provs.replace({'CAÑAR': 'CANAR'}, inplace=True)
print(df_provs)
print(df_provs.dtypes)



# Locate map in Ecuador
ec_map = folium.Map(location=[-1.831239, -78.183403], zoom_start=7, tiles='cartodbpositron') 

ec_geo = r'provs-ec.json' # geojson file
threshold_scale = [1, 50, 150, 350, 1500, 7503]

# generate choropleth map using COVID-19
folium.Choropleth(
    geo_data=ec_geo,
    data=df_provs,
    columns=['prov_residencia', 'total_muestras'],
    key_on='feature.properties.dpa_despro',
    fill_color='YlOrRd', 
    fill_opacity=0.7, 
    line_opacity=0.2,
    legend_name='COVID-19 en Ecuador',
    threshold_scale=threshold_scale,
    reset=True,
).add_to(ec_map)


# Load markers data
df_loc_provs = pd.read_csv('loc_provs.csv', sep=',', header='infer', encoding='ISO-8859-1')
df_loc_provs.replace({'Cañar': 'Canar'}, inplace=True)
print(df_loc_provs)

for lat, lng, label in zip(df_loc_provs.lat, df_loc_provs.lng, df_loc_provs.admin):
	for prov, casos in zip(df_provs.prov_residencia, df_provs.total_muestras):
		if prov == label.upper():
			cad = label + ' ' +  str(casos) + ' casos'
			folium.Marker([lat,lng], popup=cad).add_to(ec_map)



# Display world map
filepath = 'C:/Users/Hugoa/Desktop/Espol/Coursera/IBM Data Science/Data_Visualization/COVID-19/Map_Ecuador.html'
ec_map.save(filepath)
webbrowser.open('file://' + filepath)