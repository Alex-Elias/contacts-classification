import sys
from pathlib import Path
import pandas as pd
import numpy as np

INTERACTION = ['HBOND', 'VDW', 'PIPISTACK', 'IONIC', 'PICATION', 'SSBOND', 'PIHBOND']

RESIDUES = ['pdb_id', 's_ch', 's_resi', 's_resn', 't_ch', 't_resi', 't_resn']


if __name__ == '__main__':
    file = sys.argv[1]
    pdb_id = Path(file).stem
    df = pd.read_csv(file, sep="\t")

    df = df[RESIDUES + INTERACTION]

    

    data = []
    n = np.array(INTERACTION)

    for i in range(len(df)):
        mask = df.iloc[i][INTERACTION] > 0.65
        mask = mask.tolist()
        interactions = n[mask]
        if len(interactions) == 0:
            interactions = [df.iloc[i][INTERACTION].idxmax()]
        for interaction in interactions:
            row = df.iloc[i].tolist()
            row.append(interaction)
            data.append(row)

    df = pd.DataFrame(data, columns= RESIDUES + INTERACTION + ['Interaction'])
    df = df[RESIDUES + ['Interaction']]

    df.to_csv("./{}_i.tsv".format(pdb_id), sep="\t", index=False)

