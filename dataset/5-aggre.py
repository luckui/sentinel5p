import os
import pandas as pd

# def main():
#     aDir = r'filtered\geodesic'
#     bDir = r'GOSAT_CSV2'
#     alist = os.listdir(aDir)
#     blist = os.listdir(bDir)
#     for a in alist:
#         if os.path.exists(os.path.join(bDir, a)):
#             b = pd.read_csv(os.path.join(bDir, a))
#             a = pd.read_csv(os.path.join(aDir, a))

#         pass
#     pass


def main():
    flist = os.listdir(r'filtered\geodesic_all')
    dfs = [pd.read_csv(os.path.join(r'filtered\geodesic_all', x)) for x in flist]
    df = pd.concat(dfs)
    print(df)
    df.to_csv('data2.csv', index=False)
    pass


if __name__ == '__main__':
    main()


