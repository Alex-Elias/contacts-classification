# contacts-classification
This repository was created for the Classification in contact proteins structures project for the Structural Bioinformatics final project in spring 2024 at the University of Padua.

Residue Interaction Networks are derived from protein structures based on geometrical and physico-chemical properties of the amino acids. The aim of this project was to create a software that takes a PDB file, predicts the contacts of the residue-residue pairs with their types in the protein structure, and returns a file with the data. The interactions types considered included: Hydrogen Bonds (HBOND), Van der Waals (VDW), π-π Stacking (PIPISTACK), Ionic Bonds (IONIC), π-Cation Interactions (PICATION), and Disulfide Bonds (SSBOND). 

The model chosen for this classification task was sklearn's OneVsRestClassifier with the estimator being sklearn's RandomForestClassifier. OneVsRestClassifier was trained on a balanced subsample of 3299 pdb files. 
## Desciption of the software

The predictor.py software uses the calc_features.py script to transform the pdb file into a Pandas DataFrametakes with the values of the columns in the following table besides the interactions. Then, predictory.py uses the pretrained model to predict the interactions and saves everyting on a .tsv file in the following format:

| Column position | Column name |               Column meaning               |       Type of column      |
|:---------------:|:-----------:|:------------------------------------------:|:-------------------------:|
|        1        |    pdb_id   |                                            |                           |
|        2        |     s_ch    |                    chain                   | source residue identifier |
|        3        |    s_resi   |                    index                   |                           |
|        4        |    s_ins    |               insertion code               |                           |
|        5        |    s_resn   |                    name                    |                           |
|        6        |    s_ss8    |     secondary structure 8 states (DSSP)    |  source residue features  |
|        7        |    s_rsa    |       relative solvent accessibility       |                           |
|        8        |     s_up    |           half sphere exposure up          |                           |
|        9        |    s_down   |          half sphere exposure down         |                           |
|        10       |    s_phi    |                  phi angle                 |                           |
|        11       |    s_psi    |                  psi angle                 |                           |
|        12       |    s_ss3    | secondary structure 3 states (from angles) |                           |
|        13       |     s_a1    |              Atchley feature 1             |                           |
|        14       |     s_a2    |              Atchley feature 2             |                           |
|        15       |     s_a3    |              Atchley feature 3             |                           |
|        16       |     s_a4    |              Atchley feature 4             |                           |
|        17       |     s_a5    |              Atchley feature 5             |                           |
|        18       |     t_ch    |                    chain                   | target residue identifier |
|        19       |    t_resi   |                    index                   |                           |
|        20       |    t_ins    |               insertion code               |                           |
|        21       |    t_resn   |                    name                    |                           |
|        22       |    t_ss8    |     secondary structure 8 states (DSSP)    |  target residue features  |
|        23       |    t_rsa    |       relative solvent accessibility       |                           |
|        24       |     t_up    |           half sphere exposure up          |                           |
|        25       |    t_down   |          half sphere exposure down         |                           |
|        26       |    t_phi    |                  phi angle                 |                           |
|        27       |    t_psi    |                  psi angle                 |                           |
|        28       |    t_ss3    | secondary structure 3 states (from angles) |                           |
|        29       |     t_a1    |              Atchley feature 1             |                           |
|        30       |     t_a2    |              Atchley feature 2             |                           |
|        31       |     t_a3    |              Atchley feature 3             |                           |
|        32       |     t_a4    |              Atchley feature 4             |                           |
|        33       |     t_a5    |              Atchley feature 5             |                           |
|        34       |    HBOND    |              interaction type              |        Interaction        |
|        35       |     VDW     |              interaction type              |                           |
|        36       |    SSBOND   |              interaction type              |                           |
|        37       |     IONIC   |              interaction type              |                           |
|        38       |   PIPISTACK |              interaction type              |                           |
|        39       |   PICATION  |              interaction type              |                           |
|        40       |    PIHBOND  |              interaction type              |                           |

The columns HBOND, VDW, SSBOND, IONIC, PIPISTACK, PICATION, AND PIHBOND store the predicted percentage that the interaction of the contact is of that type. Since each contact can be of multiple interactions, the score for each interaction type can be interpreted individually.

The train_model.py script trains a new classifier model from scratch. It reads the training data from the features_ring folder, preprocesses the data and takes a balanced subsample of it to train the new model. The new model is pickled and saved in the same directory as model.pkl

## Installing the dependencies
The dependencies for this repository are found in the requirements.txt file. They can be installed using the command 

```pip3 install -r requirements.txt```

The DSSP software must also be installed and the path to it be changed in the configuration.json file in the configuration folder.
## Running the software
This software was created using Python 3.10 and has not been tested on older versions of Python.

To run the predictor.py software, it first requires a pickle of the classifier model to be found in the same folder as it as well as calc_features.py. The pretrained model can be downloaded [here](https://drive.google.com/file/d/16TD9RbjN7m8Beiu-6PJDNuNNHj40B18N/view?usp=sharing) (900MB zip, 4GB uncompressed) or a new one can be trained from scratch using the train_model.py script.

The predictor.py file takes up to three command line inputs, PDB file (required), configuration file (defaults to the one found in configuration), and the path to the directory to save the .tsv file (defaults to ./) 

An example to run predictor.py

```
python3 predictor.py your_pdb_file.pdb
```

The train_model.py script does not require any command line parameters, but requires the training data to be found in a folder named *features_ring* in the same directory as the train_model.py script. The features_ring folder with training data can be downloaded [here](https://drive.google.com/file/d/1fuFonB7P-xPZ4hYL8ZGn12EC20thRG2s/view). The model is pickeled and saved as model.pkl in the same directory as train_model.py.

train_model.py can be run with the following command

``` 
python3 train_model.py
```
