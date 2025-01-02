from shapely.geometry import Point
import geopandas as gpd
import os
import pandas as pd
from tqdm import tqdm


def csv2shp(path, output):
    df = pd.read_csv(path)
    geom = []
    for idx, item in df.iterrows():
        lon, lat = item['longitude'], item['latitude']
        p = Point([lon, lat])
        geom.append(p)
    gdf = gpd.GeoDataFrame(df, geometry=geom, crs='EPSG:4326')
    gdf.to_file(output)
    


def main():
    inDir = r'val_out'
    outDir = r'val_shp'
    
    shpList = os.listdir(inDir)
    for shp in tqdm(shpList):
        path = os.path.join(inDir, shp)
        output = os.path.join(outDir, shp.split('.')[0]+'.shp')
        csv2shp(path=path, output=output)


if __name__ == '__main__':
    main()
    pass 

