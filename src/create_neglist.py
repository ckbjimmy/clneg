import pandas as pd
from nltk import pos_tag, word_tokenize

neg_list = pd.read_csv(data_dir + 'multilingual_lexicon-en-de-fr-sv.csv', sep=',', header=0)[['ITEM', 'CATEGORY', 'EN (SV) ACTION']]
neg_list = neg_list[neg_list['CATEGORY'].isin(['definiteNegatedExistence', 'probableNegatedExistence', 'pseudoNegation'])]
neg_list['NEG'] = ''
neg_list['FIRST_TOKEN'] = ''
neg_list['FIRST_POS'] = ''
neg_list['LAST_TOKEN'] = ''
neg_list['LAST_POS'] = ''
for idx in neg_list.index:
    if neg_list['CATEGORY'][idx] == 'definiteNegatedExistence' and neg_list['EN (SV) ACTION'][idx] == 'forward': 
        neg_list['NEG'][idx] = 'PREN'
    if neg_list['CATEGORY'][idx] == 'definiteNegatedExistence' and neg_list['EN (SV) ACTION'][idx] == 'backward': 
        neg_list['NEG'][idx] = 'POST'
    if neg_list['CATEGORY'][idx] == 'definiteNegatedExistence' and neg_list['EN (SV) ACTION'][idx] == 'bidirectional': 
        neg_list['NEG'][idx] = 'POST'
    if neg_list['CATEGORY'][idx] == 'probableNegatedExistence' and neg_list['EN (SV) ACTION'][idx] == 'forward':
        neg_list['NEG'][idx] = 'PREP'
    if neg_list['CATEGORY'][idx] == 'probableNegatedExistence' and neg_list['EN (SV) ACTION'][idx] == 'backward': 
        neg_list['NEG'][idx] = 'POSP'
    if neg_list['CATEGORY'][idx] == 'probableNegatedExistence' and neg_list['EN (SV) ACTION'][idx] == 'bidirectional': 
        neg_list['NEG'][idx] = 'POSP'
    if neg_list['CATEGORY'][idx] == 'pseudoNegation': 
        neg_list['NEG'][idx] = 'PSEU'
    neg_list['FIRST_TOKEN'][idx] = neg_list['ITEM'][idx].split()[0]
    neg_list['FIRST_POS'][idx] = pos_tag(word_tokenize(neg_list['FIRST_TOKEN'][idx]))[0][1]
    neg_list['LAST_TOKEN'][idx] = neg_list['ITEM'][idx].split()[len(neg_list['ITEM'][idx].split())-1]
    neg_list['LAST_POS'][idx] = pos_tag(word_tokenize(neg_list['LAST_TOKEN'][idx]))[0][1]

neg = neg_list['ITEM'].values
neg_list.head()
neg_list.to_csv(data_dir + 'neg_list.txt', sep='\t', index=False, quoting=False)