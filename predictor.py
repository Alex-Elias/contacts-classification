
from pathlib import Path
import pickle
import argparse

import calc_features

FEATURES = [ 's_up', 's_down', 's_phi', 's_psi', 's_a1', 's_a2', 's_a3', 's_a4', 's_a5', 
         't_up', 't_down', 't_phi', 't_psi', 't_a1', 't_a2', 't_a3', 't_a4', 't_a5']

def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('pdb_file', help='mmCIF or PDB file')
    parser.add_argument('-conf_file', help='Configuration and parameters file', default=None)
    parser.add_argument('-out_dir', help='Output directory', default='.')
    return parser.parse_args()


if __name__ == '__main__':
    args = arg_parser()

    pdb_file = args.pdb_file
    conf_file = args.conf_file
    pdb_id = Path(pdb_file).stem

    pdb_features = calc_features.generate_features_pdb(pdb_file, conf_file)

    with open('model.pkl', 'rb') as f:
        model = pickle.load(f)
    
    procent = model.predict_proba(pdb_features[FEATURES])



    pdb_features['hbond'] = procent[0][:,1]
    pdb_features['vdw'] = procent[6][:,1]
    pdb_features['ssbond'] = procent[5][:,1]
    pdb_features['ionic'] = procent[1][:,1]
    pdb_features['pipistack'] = procent[4][:,1]
    pdb_features['pication'] = procent[2][:,1]
    pdb_features['pihbond'] = procent[3][:,1]


    pdb_features.to_csv("{}/{}.tsv".format(args.out_dir, pdb_id), sep="\t", index=False)
