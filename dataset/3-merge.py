import os
import pandas as pd
import numpy as np


def main():
    rawDir = r'output_all'
    raws = os.listdir(rawDir)

    gosatDir = r'GOSAT_CSV2'
    # gosats = os.listdir(gosatDir)

    output = 'attr_all'

    for raw in raws:
        if os.path.exists(os.path.join(gosatDir, raw)):
            gosatDf = pd.read_csv(os.path.join(gosatDir, raw))
            rawDf = pd.read_csv(os.path.join(rawDir, raw))
            columns = np.concatenate((gosatDf.columns.values, rawDf.columns.values))
            df = pd.concat([gosatDf, rawDf], axis=1, ignore_index=True)
            df.columns = columns
            df.to_csv(os.path.join(output, raw), index=False)
        pass
    pass


if __name__ == '__main__':
    main()




