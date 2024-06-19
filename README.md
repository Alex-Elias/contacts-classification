# contacts-classification
This repository was created for the Classification in contact proteins structures project for the Structural Bioinformatics final project in spring 2024 at the University of Padua.

Residue Interaction Networks are derived from protein structures based on geometrical and physico-chemical properties of the amino acids. The aim of this project was to create a software that takes a PDB file, predicts the contacts of the residue-residue pairs with their types in the protein structure, and returns a file with the data. The interactions types considered included: Hydrogen Bonds (HBOND), Van der Waals (VDW), π-π Stacking (PIPISTACK), Ionic Bonds (IONIC), π-Cation Interactions (PICATION), and Disulfide Bonds (SSBOND). 
## Structure of the repository

## Installing the dependencies
The dependencies for this repository are found in the requirements.txt file. They can be installed using the command 

```pip3 install -r requirements.txt```

The DSSP software must also be installed and the path to it be changed in the configuration.json file in the configuration folder.
## Running the software
This software was created using Python 3.10 and has not been tested on older versions of Python.

To run the predictor.py software, it first requires a pickle of the classifier model to be found in the same folder as it as well as calc_features.py. The pretrained model can be downloaded [here](https://drive.google.com/file/d/16TD9RbjN7m8Beiu-6PJDNuNNHj40B18N/view?usp=sharing) (900MB zip, 4GB uncompressed) or a new one can be trained from scratch using the train_model.py script.

The predictor.py file takes up to three command line inputs, PDB file (required), configuration file (defaults to the one found in configuration), and the path to the directory to save the .tsv file (defaults to ./) 

An example to run predictor.py

``` python3 predictor.py your_pdb_file.pdb```

The train_model.py script does not require any command line parameters, but requires the training data to be found in a folder named *features_ring* in the same directory as the train_model.py script. The features_ring folder with training data can be downloaded [here](https://drive.google.com/file/d/1fuFonB7P-xPZ4hYL8ZGn12EC20thRG2s/view)
