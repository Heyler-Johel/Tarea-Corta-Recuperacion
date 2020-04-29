import threading
import os.path
import nltk
import re
from nltk.tokenize import word_tokenize
from unicodedata import normalize
from nltk.corpus import stopwords
from bs4 import BeautifulSoup
from time import time

lsta = [] #Lista total de palabras
links = [] #Lista total de links

def create_txt (path, load):
    if path == 'Geografia':
        name = "Geografia"
    elif os.path.exists(path) and os.path.isfile(path):
        name = path.split('\\')[-3]+'_'+path.split('\\')[-1]
        name = name.split('.')[0]+"_lm.txt"
        name = path.split('\\')[-1]+"_lm.txt"
    elif os.path.exists(path) and os.path.isdir(path):
        name = path.split('\\')[-2]+'_'+path.split('\\')[-1]+".txt"
    file = open("ArchivoTxts\\"+name, "w")
    for w in load:
        try:
            file.write(w[0]+"  :  "+str(w[1])+" : "+str(w[2])+"\n")
        except:
            pass
    file.close()
    
def create_txt_ref (path):
    if path == 'Geografia':
        name = "Geografia_ref.txt"
    elif os.path.exists(path) and os.path.isfile(path):
        name = path.split('\\')[-3]+'_'+path.split('\\')[-1]
        name = name.split('.')[0]+"_ref.txt"
    elif os.path.exists(path) and os.path.isdir(path):
        name = path.split('\\')[-2]+'_'+path.split('\\')[-1]+"_ref.txt"
    file = open("ArchivoRefs\\"+name, "w")
    for w in links:
        try:
            file.write(w+"\n")
        except:
            pass
    file.close()

def tild(text):
    replacements = (
        ("á", "a"),
        ("é", "e"),
        ("í", "i"),
        ("ó", "o"),
        ("ú", "u"),
    )
    for a, b in replacements:
        text = text.replace(a, b).replace(a.upper(), b.upper())
    return text

def txt(text):
    text = tild(text)
    tokens = nltk.word_tokenize(text, 'spanish')
    stop_words = set(stopwords.words('spanish'))
    tokens = [w for w in tokens if w.isalpha() and w not in stop_words]
    return tokens

def freq():
    global lsta
    frec = []
    prob = []
    N = len(lsta)
    for w in lsta:
        prob.append(float(lsta.count(w)/N))
        frec.append(lsta.count(w))
    rslt = list(set(zip(lsta, frec, prob)))
    return rslt
    
def genere_LM(path):
    global lsta
    lsta = []
    genere_LM_aux(path)
    listresult = list(freq())
    listresult.sort()
    create_txt(path, listresult)
    return

def genere_LM_aux(path):
    #print(path)
    global lsta
    if os.path.exists(path) and os.path.isfile(path):
        ph = open(path, "r", encoding="utf-8")
        soup = BeautifulSoup(ph, 'html.parser')
        text = soup.get_text().lower()
        lsta += txt(text)
        ph.close()
        return 
    elif os.path.exists(path) and os.path.isdir(path):
        #print('************')
        dirs = os.listdir( path )
        for file in dirs:
            file = path+'\\'+file
            genere_LM_aux(file)
        return
    else:
        return

#def opr (LM_general, LM_specific)

def extraer_refs (path):
    global links
    links = []
    if os.path.exists(path):
        if os.path.isfile(path):
            extraer_refs_specific (path)
        elif os.path.isdir(path):
            extraer_refs_general (path)
    else:
        print ("No existe")
    links = list(set(links))
    links.sort()
    print(len(links))
    #print (links[0])
    #for l in links:
        #print(l)
    create_txt_ref (path)
    return
    

def extraer_refs_specific (path):
    global links
    if os.path.exists(path) and os.path.isfile(path):
        ph = open(path, "r", encoding="utf-8")
        soup = BeautifulSoup(ph, 'html.parser')

        for link in soup.find_all('a'):
            if not (link.get('href') == None or link.get('href') == '/' or link.get('href')[0] == '#'):
                links.append(link.get('href'))

        ph.close()
    else:
        print ("No existe")
    return

def extraer_refs_general (path):
    if os.path.exists(path) and os.path.isdir(path):
        dirs = os.listdir( path )
        for file in dirs:
            direction = path+'\\'+file
            if os.path.isdir(direction):
                #print(direction)
                extraer_refs_general (direction)
            elif os.path.isfile(direction):
                extraer_refs_specific (direction)
            else:
                pass
    else:
        print ("No existe")
    return
        
