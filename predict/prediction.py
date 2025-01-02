import joblib
import pandas as pd
from tqdm import trange, tqdm
import os


def predict(input, output, model):
    data = pd.read_csv(input)
    X = data
    # y_prd = model.predict(X)
    step = 1000
    records = []
    for i in trange(0, len(X), step):
        s = i
        e = i+step
        Xp = X.iloc[i:i+step, :]
        yp = model.predict(Xp)
        records = records+list(yp)
    data['methane'] = records
    data.to_csv(output, index=False)


def main():
    modelPath = r'model\rfV4.pkl'
    inputDir = r'data'
    outDir = r'output'

    model = joblib.load(modelPath)
    flist = [x for x in os.listdir(inputDir) if x.endswith('.csv')]
    for f in flist:
        predict(input=os.path.join(inputDir, f), output=os.path.join(outDir, f), model=model)


if __name__ == '__main__':
    main()

