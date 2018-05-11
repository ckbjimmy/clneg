import os
import sys
import re
import numpy as np
#from create_neglist import *
import pandas as pd
pd.set_option('display.max_rows', None)
from create_tokenization import *
from pycorenlp import StanfordCoreNLP
from concept_extraction import *
from syntactic_parsing import *
from tree_rules import *
from nltk.corpus import stopwords
from difflib import SequenceMatcher


def print_out_result(df):
    for s in set(df['section'].values):
        if s != '':
            subset = df[df['section'] == s][['preferred', 'negation']]
            subset['preferred'] = np.where(subset['negation'] == 1, subset['preferred'] + '(-)', subset['preferred'] + '(+)')
            print('--- ' + s + ' ---\n' + ', '.join(subset['preferred']))
    

if __name__ == '__main__':
	# can be extended to batch processing if needed (feed a list of filenames)
	#filenames = ['12825_165653_2137-02-22.txt']
	filenames = ['negex_ready.txt']
	#filenames = ['test120_ready.txt']

	data_dir = '../data/'
	ctakes_folder = './ctakes/'
	tregex_dir = './stanford-tregex-2018-02-27/'

	# negated term list (use the human annotated version)
	neg_list = pd.read_csv(data_dir + 'neg_list_complete.txt', sep='\t', header=0)
	neg = neg_list['ITEM'].values
	neg_term = [' ' + item + ' ' for item in neg]
	neg_term.extend(item + ' ' for item in neg)

	nlp = StanfordCoreNLP('http://localhost:9000')
	mimic_tokenize(data_dir, filenames, nlp, neg_term)

	df = ctakes_concept_extraction(data_dir, ctakes_folder)

	openNLP = OpenNLP()
	sl, tree_list = synparse(data_dir, neg_list, openNLP)

	stopwords = stopwords.words('english')
	POS = ['NN', 'NNS', 'RB', 'NP']


	for i, t in enumerate(tree_list):
	    print('sent: ' + str(i))
	    print('original: ' + sl[i])
	    # get negated part of the sentence
	    with open(data_dir + 'ntree_tmp', 'w') as fw:     
	        fw.write(t)
	    s = re.sub('\([A-Z]*\$? |\(-[A-Z]+- |\)|\)|\(, |\(. ', '', t)
	    print('neg part: ' + s)
	    
	    # find what neg term is matched and use its neg type
	    try:
	        m = ''
	        for neg in [x for x in sorted(neg_list['ITEM'].tolist(), key=len)]:
	            match = SequenceMatcher(None, s, neg).find_longest_match(0, len(s), 0, len(neg))
	            matched_string = s[match.a: match.a + match.size]
	            try: # if next char might be different, means partial match
	                if s[match.a + match.size + 1] == neg[match.b + match.size + 1] and \
	                   s[match.a + match.size + 2] == neg[match.b + match.size + 2]:
	                    if (len(matched_string) > len(m)) and \
	                        ((matched_string[0] == s[0] and matched_string[1] == s[1]) or \
	                         (matched_string[len(matched_string)-1] == s[len(s)-1] and matched_string[len(matched_string)-2] == s[len(s)-2])): # either match from the beginning or laast
	                        m = matched_string 
	                        matched_neg_item = neg[match.b: match.b + match.size]
	                        if matched_neg_item[len(matched_neg_item)-1] == ' ':
	                            matched_neg_item = matched_neg_item[0:len(matched_neg_item)-1]
	                else:
	                    continue
	            except: # if no next char, means full match
	                try:
	                    if (len(matched_string) > len(m)) and \
	                        ((matched_string[0] == s[0] and matched_string[1] == s[1]) or \
	                         (matched_string[len(matched_string)-1] == s[len(s)-1] and matched_string[len(matched_string)-2] == s[len(s)-2])): # either match from the beginning or laast
	                        m = matched_string 
	                        matched_neg_item = neg[match.b: match.b + match.size]
	                        if matched_neg_item[len(matched_neg_item)-1] == ' ':
	                            matched_neg_item = matched_neg_item[0:len(matched_neg_item)-1]
	                except: # match only one char!? rare case
	                    if (len(matched_string) > len(m)) and \
	                        (matched_string[0] == s[0]): # either match from the beginning or laast
	                        m = matched_string 
	                        matched_neg_item = neg[match.b: match.b + match.size]
	                        if matched_neg_item[len(matched_neg_item)-1] == ' ':
	                            matched_neg_item = matched_neg_item[0:len(matched_neg_item)-1]                    
	        print('negated term: ' + matched_neg_item)
	        
	        neg_type = neg_list[neg_list.ITEM == matched_neg_item]['TYPE'].values[0]
	        print('--- tregex/tsurgeon with negated type: ' + neg_type)

	        # run tregex/tsurgeon based on the selected neg type
	        ts_out = tregex_tsurgeon(data_dir + 'ntree_tmp', neg_type)

	        # deal with corner cases
	        if neg_type == 'NP' and ('that' in ts_out):
	            print('--- NP with that')
	            ts_out = tregex_tsurgeon(data_dir + 'ntree_tmp', 'NP-denies')
	        
	        if neg_type == 'NP' and s == ts_out:
	            print('--- NP without S node')
	            ts_out = tregex_tsurgeon(data_dir + 'ntree_tmp', 'NP-nS')
	        
	        if neg_type == 'PP' and sum([item in neg_list['ITEM'].tolist() for item in ts_out.split()]) > 0:
	            print('--- NP without S node')
	            ts_out = tregex_tsurgeon(data_dir + 'ntree_tmp', 'NP-nS')
	            
	        if neg_type == 'VP-A' and s == ts_out:
	            print('--- VP-A remove denies')
	            ts_out = tregex_tsurgeon(data_dir + 'ntree_tmp', 'NP-denies')
	            
	        if neg_type == 'ADVP-A' and s == ts_out:
	            print('--- ADVP-A remove SBAR')
	            ts_out = tregex_tsurgeon(data_dir + 'ntree_tmp', 'ADVP-sbar')
	        
	        if neg_type == 'ADVP-A' and s == ts_out:
	            print('--- ADVP-A remove RB')
	            ts_out = tregex_tsurgeon(data_dir + 'ntree_tmp', 'ADVP-RB')
	                    
	        if sum([item in POS for item in ts_out.split()]) > 0:
	            print('--- remove POS')
	            ts_out = ' '.join(ts_out.split()[1:])
	            
	        if ts_out.split()[0] in neg_list['ITEM'].tolist() + stopwords:
	            print('--- remove first token f if f in negated list or stopword list')
	            ts_out = ' '.join(ts_out.split()[1:])
	            
	        print('>> ' + ts_out + '\n')

	        try:
	            neg_range = (sl[i].index(ts_out) + 1, sl[i].index(ts_out) + len(ts_out)) # negated place
	        except:
	            neg_range = (0, len(sl))
	        
	        print(neg_range)

	        for idx in df.index:
	            if df['sent_id'][idx] == i+1 and df['sent_loc'][idx] in range(neg_range[0], neg_range[1]):
	                df['negation'][idx] = 1
	                
	    except: # need to debug why very few cases don't work
	        continue

	os.system('rm ../data/ntree_tmp')

	# preserve the longest strings/concepts
	df_s = df
	df_s['start'] = df_s['start'].astype(int)
	df_s['len'] = df_s['original'].str.len()
	df_s = df_s.sort_values('len', ascending=False)
	df_s = df_s.drop_duplicates(['sent_id', 'start'], keep='first')
	df_s = df_s.drop_duplicates(['sent_id', 'end'], keep='first')
	df_s = df_s.sort_values('start', ascending=True)
	df_s.to_csv('output', sep='\t', index=False)
	df_s[(df_s.sent_id != 0) & (df_s.section != '')]

	print_out_result(df)
