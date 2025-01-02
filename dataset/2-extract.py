from s5py import query, wave2channel, QueryS5
import pandas as pd
from h5py import File
from tqdm import tqdm
import numpy as np
import os


def main():
    records = pd.read_csv('records2.csv')
    arr = records.values
    outdir = 'output2'
    for rec in arr:
        extractSingle(gosatPath=rec[0], trpmPath=rec[1], wavePath='sensitive_channel.csv', output=os.path.join(outdir,os.path.basename(rec[0])))


def extractSingle(gosatPath, trpmPath, wavePath, output):
    gosat = pd.read_csv(gosatPath)
    gosatVs = gosat.values

    waves = pd.read_csv(wavePath).values.ravel()
    # print(waves.shape)
    columns = np.concatenate((waves, ['so_azi', 'so_zen', 'v_azi', 'v_zen', 'longitude', 'latitude']), axis=0)
    # channels = [wave2channel(x) for x in waves]
    with File(trpmPath) as f:
        q5 = QueryS5(f=f)
        data = []
        for v in tqdm(gosatVs):
            # print(v)
            lon, lat = v[0], v[1]
            row = []
            flag = False
            for count, wav in tqdm(enumerate(waves)):
                if count == len(waves)-1:
                    flag = True
                    pixv, so_azi, so_zen, v_azi, v_zen, longitude, latitude = q5.query(lon=lon, lat=lat, wave=wav, flag=flag)
                    row = row+[pixv, so_azi, so_zen, v_azi, v_zen, longitude, latitude]
                else:
                    pixv = q5.query(lon=lon, lat=lat, wave=wav, flag=flag)
                    row.append(pixv)
            data.append(row)
            # for count, wav in tqdm(enumerate(waves)):
            #     if count == len(waves)-1:
            #         flag = True
            #         pixv, so_azi, so_zen, v_azi, v_zen, longitude, latitude = query(f, lon=lon, lat=lat, wave=wav, flag=flag)
            #         row = row+[pixv, so_azi, so_zen, v_azi, v_zen, longitude, latitude]
            #     else:
            #         pixv = query(f, lon=lon, lat=lat, wave=wav, flag=flag)
            #         row.append(pixv)
        df = pd.DataFrame(data, columns=columns)
        df.to_csv(output, index=False)



if __name__ == '__main__':
    main()
    pass

