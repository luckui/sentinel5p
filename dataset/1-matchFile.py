import os 
from s5py import query
import pandas as pd


def matchIt():
    tropomiDir = r'TROPOMI'
    gosatDir = r'GOSAT_CSV'

    tpmList = os.listdir(tropomiDir)
    gosatList = os.listdir(gosatDir)

    pairs = []
    for gosat in gosatList:
        date = gosat.split('_')[1].split('.')[0]
        tpm = [x for x in tpmList if date in x]
        gosatPath = os.path.join(gosatDir, gosat)
        tpmPath = os.path.join(tropomiDir, tpm[0], tpm[0]+'.nc')
        pairs.append([gosatPath, tpmPath])
    df = pd.DataFrame(pairs, columns=['gosat', 'tropomi'])
    df.to_csv('records2.csv', index=False)


if __name__ == "__main__":
    matchIt()
    pass


