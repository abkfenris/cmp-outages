import requests
import pandas as pd

url = "https://avangrid-maine-ags.esriemcs.com/arcgis/rest/services/CMPOutageMap_v2/MapServer/0/query?f=json&where=Company%20%3D%20%27CMP%27%20AND%20NumOut%20%3E%200&returnGeometry=true&spatialRel=esriSpatialRelIntersects&geometry=%7B%22xmin%22%3A-8153287.339413942%2C%22ymin%22%3A5143134.112231868%2C%22xmax%22%3A-7211583.1509408215%2C%22ymax%22%3A6193684.6289830515%2C%22spatialReference%22%3A%7B%22wkid%22%3A102100%2C%22latestWkid%22%3A3857%7D%7D&geometryType=esriGeometryEnvelope&inSR=102100&outFields=*&outSR=102100&cacheBuster=0.5155317756777305"

r = requests.get(url)
j = r.json()

rows = []
for feature in j["features"]:
    rows.append({**feature["attributes"], **feature["geometry"]})

df = pd.DataFrame(rows)
try:
    df = df.drop(["OBJECTID", "NumServed", "PercentOut", "Company"], axis=1)
    df["BgName"] = df["BgName"].str.rstrip(";,")
    df.sort_values(["x", "y"])
except KeyError:
    print("All CMP customers may just have power right now!")
df.to_csv("cmp_outages.csv", index=False)
