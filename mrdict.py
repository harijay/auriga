#!/usr/bin/python
import os

mr_models_dir=os.environ.get("AURIGA_MODELS_DIR")
B1_model="B1_model.pdb"
B2_model="B2_model.pdb"
S_model="S_model.pdb"
G_model="G_model.pdb"
I_model="I_model.pdb"
D_model="D_model.pdb"
A_model="A_model.pdb"

modeldict = dict(B1=(os.path.join(mr_models_dir,B1_model),1), \
              B2=(os.path.join(mr_models_dir,B2_model),1), \
              D=(os.path.join(mr_models_dir,D_model),1), \
              S=(os.path.join(mr_models_dir,S_model),2),\
              G=(os.path.join(mr_models_dir,G_model),2),\
              I=(os.path.join(mr_models_dir,I_model),1),
              A=(os.path.join(mr_models_dir,A_model),1))



