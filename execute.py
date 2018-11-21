import os
import glob
import fileinput
import spacy
import en_core_web_sm
nlp = en_core_web_sm.load()

info_util = ['PERSON','GPE','LOC']

try:
    os.remove("./helpOwl.txt")
except:
    pass

files = glob.glob("./corpus/*")
for file in files:
    f = open(file, "r")
    # on split par phrase
    text = f.read().replace("\n",". ").split(". ")
    f.close()
    # utilisation de spacy
    for t in text:
        pres = 0
        doc = nlp(t)
        res = [(X, X.ent_iob_, X.ent_type_) for X in doc]
        for r in res:
            if r[2] in info_util and str(r[0]).isalpha():
                pres += 1
            
        if pres > 1:
            f = open("./helpOwl.txt", 'a+')
            f.write(t + "\n")
            f.close()
