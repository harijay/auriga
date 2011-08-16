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
C1_model="C1_model.pdb"
P_model="P_model.pdb"
# Has two copies 
#C_model="C_model.pdb"
C_model=C1_model
B_model=B1_model

modeldict = dict(B1=(os.path.join(mr_models_dir,B1_model),1), \
              B2=(os.path.join(mr_models_dir,B2_model),1), \
              D=(os.path.join(mr_models_dir,D_model),1), \
              S=(os.path.join(mr_models_dir,S_model),2),\
              G=(os.path.join(mr_models_dir,G_model),2),\
              I=(os.path.join(mr_models_dir,I_model),1),\
              B=(os.path.join(mr_models_dir,B1_model),1),\
              A=(os.path.join(mr_models_dir,A_model),1),\
	      C1=(os.path.join(mr_models_dir,C1_model),4),\
	      C=(os.path.join(mr_models_dir,C_model),2),
                 P=(os.path.join(mr_models_dir,P_model),2))


centredict =dict(C="ND2 ASN A1168")
