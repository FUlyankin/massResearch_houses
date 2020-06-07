#!usr/bin/env python
# -*- coding: utf-8 -*-
import string
import re
import sys

from pymorphy2 import MorphAnalyzer
m = MorphAnalyzer()

from pymystem3 import Mystem
m2 = Mystem(entire_input=False)

from nltk.corpus import stopwords
stopwords_ru = stopwords.words('russian') 

from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize

# Библиотека для распараллеливания кода
from tqdm import tqdm
from joblib import Parallel, delayed
NJOBS = -1 # параллелим на все ядра 

# Таблица преобразования частеречных тэгов Mystem в тэги UPoS:
MYSTEM2UPOS = {'A': 'ADJ', 'ADV': 'ADV', 'ADVPRO': 'ADV', 'ANUM': 'ADJ',
             'APRO': 'DET', 'COM': 'ADJ', 'CONJ': 'SCONJ', 'INTJ': 'INTJ',
             'NONLEX': 'X', 'NUM': 'NUM', 'PART': 'PART', 'PR': 'ADP', 
             'S': 'NOUN', 'SPRO': 'PRON', 'UNKN': 'X', 'V': 'VERB'}


def prepare_text(text):
    tokens = word_tokenize(text.lower())
    clean_tokens = [m.normal_forms(word)[0]  for word in tokens if (word not in stopwords_ru) and 
                         (len(re.sub('[' + string.punctuation + ']', '', word)) > 1) and 
                         (len(re.sub('\d', '', word)) > 1)]
    return clean_tokens


def tag_mystem(text='Текст нужно передать функции в виде строки!', mapping=MYSTEM2UPOS, postags=True):
    # если частеречные тэги не нужны (например, их нет в модели), выставьте postags=False
    # в этом случае на выход будут поданы только леммы
  
    processed = m2.analyze(text)
    tagged = []
    
    for w in processed:
        try:
            lemma = w["analysis"][0]["lex"].lower().strip()
            pos = w["analysis"][0]["gr"].split(',')[0]
            pos = pos.split('=')[0].strip()
            if mapping:
                if pos in mapping:
                    pos = mapping[pos]  # здесь мы конвертируем тэги
                else:
                    pos = 'X'  # на случай, если попадется тэг, которого нет в маппинге
            tagged.append(lemma.lower() + '_' + pos)
        except:
            continue  # игнорируем все ошибки 
    if not postags:
        tagged = [t.split('_')[0] for t in tagged]
    return tagged


def make_batch(vect, batch_size=1000):
    cnt = (vect.size + batch_size - 1) // batch_size  #округление вверх
    out = [vect[i*batch_size: (i + 1)*batch_size] for i in range(cnt)]
    return out


def parallel_prepare_text(T, function):
    vect_lemm = [ ]
    T_batches = make_batch(T)

    for batch in tqdm(T_batches):
        cur_lemm = Parallel(n_jobs=NJOBS)(delayed(function)(text) for text in batch)
        vect_lemm.extend(cur_lemm)
    return vect_lemm



