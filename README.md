#### Teddy Dumélé M2 Architecture logicielle - WEB 3.0

# Utilisation du script
Il y a deux scripts présents:
- main.py
- exec.py

Le main.py correspond à la première étape qui ressort toutes les entités nommées. Le execute.py lui correspond à la deuxième étape qui permet d'avoir les phrases avec les relations pour nous aider à la construction de notre ontologie.

Pour démarrer le script, il suffit de lancer la commande suivante:
```py
python3.7 main.py
# ou
python3.7 execute.py
```
> J'utilise cette version mais le script devrait normalement fonctionner avec Python3 en général.

Attention, execute.py est très long, n'hésitez pas à le couper en cours de route, le fichier généré permettra de montrer déjà une grosse partie de l'information récupérée.

- Le fichier __output.txt__ correspond à l'extraction d'informations (étape 1)
- Le fichier __helpOwl.txt__ correspond à l'aide de création de l'ontologie (étape 2)
- Le dossier __corpus__ contient les textes à analyser

#### Dépendences
- os
- glob
- spacy
- en_core_web_sm

> Récupérer les dernières versions serait préférable

# Etape 1 : voir si mon texte à du sens avec Spacy
On commence par créer le corpus, pour cela j'ai créé mon dossier corpus dans lequel j'ai placé pour commencer trois textes en anglais (Germinal, Ulysse, et l'Odyssey d'Homère), étant donné que ces trois textes correspondent aux attentes de mon ontologie (relation entre Personnes et Bâtiments(lieu)). 

## Navigation entre fichiers
J'ai choisis de ne pas concaténer tous les fichiers pour ne pas devoir allouer trop de mémoire (recommandations  de spacy). Je boucle donc sur tous les fichiers du corpus pour les traiter un à un, et une fois qu'un fichier est fini d'être traité, je concatène la sortie sur __output.txt__.

Pour naviguer sur les fichiers j'utilise glob
```py
files = glob.glob("./corpus/*")
for file in files:
    f = open(file, "r")
    text = f.read()
    f.close()
```

> J'ai donc mon texte, utilisé par spacy pour extraire l'information

## Utilisation de Spacy
J'ai choisi d'utiliser le modèle de langue __en_core_web_sm__, sachant que mes textes sont en anglais et que ce modèle de langue est supérieur à la version française.

Pour l'utilisation de Spacy je rajoute en haut de mon fichier main.py:
```py
import spacy
import en_core_web_sm
nlp = en_core_web_sm.load()
```

Puis j'utilise un doc de spacy sur lequel je vais extraire les entités nommées (je ne prends que les 100000 caractères de chaque fichier étant donné que cela suffit pour mon test. Sinon j'aurai pu découper les fichiers par 100000 caractères, mais ici ce serait une perte de temps)

```py
doc = nlp(text[:100000])
res = [(X, X.ent_iob_, X.ent_type_) for X in doc]
```

Je concatène ensuite le résultat vers mon fichier output.txt, en supprimant les informations qui ne me 
sont pas utiles, comme par exemple les tuples avec le troisième élément vide, les types MONEY, etc..
Pour faire simple, tous ce qui n'est pas de type PERSON, GPE ou LOC. On récupère donc tous les tuples 
avec le premier élément non nul et le troisième correspondant soit à PERSON, GPE ou LOC.

```py
# info_util est defini avant toutes boucles car il reste constant
info_util = ['PERSON','GPE','LOC']
# on ajoute dans le fichier output
    f = open("./output.txt", "a+")
    for r in res:
        # on filtre aux informations importantes
        if r[2] in info_util and len(r[0]) != 0 and str(r[0]).isalpha() :
            f.write(str(r)+"\n")
    f.close()
```

Ici, j'arrive donc à récuperer un début d'informations utiles pour la création de mon ontologie:
```txt
[...]
(Stephen, 'B', 'PERSON')
(Buck, 'B', 'PERSON')
(Mulligan, 'I', 'PERSON')
(Dublin, 'B', 'GPE')
(Algy, 'B', 'PERSON')
(Epi, 'B', 'PERSON')
(Greeks, 'B', 'PERSON')
[...]
(Hath, 'I', 'PERSON')
(Had, 'I', 'PERSON')
(Troy, 'I', 'PERSON')
(Greeks, 'B', 'GPE')
[...]
```

> On voit ici qu'il y a quand même des erreurs , comme "Greeks", qui est interprété comme une personne et après comme un lieu.

# Etape 2 : Aide pour la création de mon ontologie
Je vais maintenant boucler sur toutes les phrases et vérifier si la phrase contient un lieu (_GPE_) et un personnage (_PERSON_), je vais ensuite pouvoir utiliser ce "pattern" pour évaluer si une phrase ressemble à ce pattern et donc qu'il y a de grandes chances qu'une relation assez semblable soit présente.

Pour cela : 
```py
files = glob.glob("./corpus/*")
for file in files:
    f = open(file, "r")
    # on split par phrase
    text = f.read().replace("\n",".").split(". ")
    f.close()
    # utilisation de spacy
    for t in text:
```
J'ai donc un tableau qui correspond à toutes mes phrases. Sur ces phrases je regarde si elle possède une entité et à chaque entité j'incrémente la valeur __pres__ permettant de compter le nombre d'entités dans la phrase.
```py
pres = 0
doc = nlp(t)
res = [(X, X.ent_iob_, X.ent_type_) for X in doc]
for r in res:
    if r[2] in info_util and str(r[0]).isalpha():
        pres += 1
```
Et je pars du principe que s'il n'y a qu'une seule entité cela n'est pas important et je préfère avoir des phrases avec au moins deux entités car il est fort probable que j'ai une relation dans cette phrase
```py
if pres > 1:
    f = open("./helpOwl.txt", 'a+')
    f.write(t + "\n")
    f.close()
```

On aurait pu créer des patterns en pondérant les différentes entités dans la phrase, pour par exemple n'afficher que les phrases ayant __pres > 5__ Ce qui permet d'être plus sûr d'avoir une phrase intéressante. Si par exemple on ajoute 2 pour une personne et 1 pour un lieu, si on a __pres=5__, on a alors de fortes chances que la phrase contienne 2 PERSON et 1 GPE et donc, on est presque sûr d'avoir une relation dans la phrase. On pourrait alors ne s'intéresser qu'à ces phrases au détriment de perdre des informations.

# Améliorations possibles
Pour améliorer ce script, on pourrait créer une liste de mots comprenant toutes les relations de notre ontologie avec toutes les variantes de la langue (est marié, femme de, femme, etc.). Et on vérifiera donc lors de l'étape 2 si un des mots de la phrase est dans la liste et seulement dans ce cas on affiche la phrase comme potentiellement intéressante. Mais pour faire cela il faudrait passer un temps relativement conséquent à la création de cette liste.

# Problèmes rencontrés
On peut voir dans un premier temps comme dit au dessus, le fait qu'il y ai quelques incohérences. De plus bien découper par phrase est compliquer si l'auteur ne respecte pas certaines règles basiques.
Un deuxième problème est le fait qu'une personne John Doe, ce fera découper en 2 entités PERSON (John et Doe). Et donc le choix des phrases est biaisé dans le cas où la personne est définie par son nom et son prénom en même temps. On aura donc ici une phrase avec potentiellement aucune relation.
