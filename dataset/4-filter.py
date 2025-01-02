from geopy.distance import geodesic
import os
import pandas as pd
from tqdm import tqdm
import matplotlib.pyplot as plt
import numpy as np


def addGeodesic():
    dire = r'attr_all'
    flist = [x for x in os.listdir(dire)]
    for f in flist:
        df = pd.read_csv(os.path.join(dire, f))
        # df['geodesic'] = [x for x in ]
        geod = []
        for idx, row in tqdm(df.iterrows()):
            # print(row)
            lon = row['lon']
            lat = row['lat']
            longitude = row['longitude']
            latitude = row['latitude']
            geod.append(geodesic((lat, lon), (latitude, longitude)).meters)
        df['geodesic'] = geod
        df.to_csv(os.path.join(dire, f), index=False)


def scatter():
    path = r'attr2\GOSAT_20210101.csv'
    df = pd.read_csv(path)
    geod = df['geodesic'].values.ravel()
    geod = np.sort(geod)
    x = np.arange(0, len(geod)) 
    fig, axs = plt.subplots(1,2)
    axs[0].scatter(x, geod, alpha=0.05, c='red')
    axs[1].hist(geod, bins=50, alpha=0.5)
    plt.show()


def filterGeodesic():
    dire = r'attr_all'
    outDir = r'filtered\geodesic_all'
    flist = [x for x in os.listdir(dire)]
    for f in flist:
        path = os.path.join(dire, f)
        df = pd.read_csv(path)
        df = df[df['geodesic']<10000]
        df.to_csv(os.path.join(outDir, f), index=False)


if __name__ == '__main__':
    # addGeodesic()
    scatter()
    # filterGeodesic()
    pass

