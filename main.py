import os
import glob
import spacy
import en_core_web_sm
nlp = en_core_web_sm.load()

info_util = ['PERSON','GPE','LOC']
# on supprime le fichier output pour repartir sur de bonnes bases
try:
    os.remove("./output.txt")
except:
    pass

files = glob.glob("./corpus/*")
for file in files:
    f = open(file, "r")
    text = f.read()
    f.close()
    # utilisation de spacy
    
    doc = nlp(text[:100000])
    res = [(X, X.ent_iob_, X.ent_type_) for X in doc]

    # on ajoute dans le fichier output
    f = open("./output.txt", "a+")
    for r in res:
        # on filtre aux informations importantes
        if r[2] in info_util and len(r[0]) != 0 and str(r[0]).isalpha() :
            f.write(str(r)+"\n")
    f.close()