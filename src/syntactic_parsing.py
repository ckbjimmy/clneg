# syntactic parsing
from jsonrpclib.jsonrpc import ServerProxy
import requests

class OpenNLP:
    def __init__(self, host='localhost', port=8080):
        uri = "http://%s:%d" % (host, port)
        self.server = ServerProxy(uri)

    def parse(self, text):
        return self.server.parse(text)


def synparse(data_dir, neg_list, openNLP):
	# preparing sentence for parsing
	l = []
	sl = []
	with open(data_dir + 'tmp') as fr:
	    for s in fr:
	        if s.endswith('[NEGATED]\n') or s == '\n':
	            l.append(s)
	        if s.endswith('[NEGATED]\n'):
	            sl.append(s)

	# remove before/after words!
	neg_front = [i + ' ' for i in neg_list[neg_list['EN (SV) ACTION'] == 'forward']['ITEM'].tolist()]
	neg_back = [' ' + i for i in neg_list[neg_list['EN (SV) ACTION'] == 'backward']['ITEM'].tolist()]

	ll = []
	for sent in l:
	    s1 = ''
	    s2 = ''
	    for nw in neg_front:
	        try:
	            s1 = sent[sent.index(nw):]
	            break
	        except:
	            continue
	    for nw in neg_back:
	        try:
	            s2 = sent[:sent.index(nw)]
	            break
	        except:
	            continue
	    if s1 != '' and s2 == '':
	        s = s1 + ' , ' + s2
	        s = re.sub(' , $', '', s)
	        ll.append(s)
	    else:
	        ll.append(sent)
	    
	tree_list = []
	while len(sl) != len(tree_list): # run until opennlp can parse with correct number of sentences. bug???
	    # opennlp parsing the neg tree
	    print('\n--- parse negated part of the sentence ---\n')
	    tree_list = []
	    with open(data_dir + 'tmp_neg_tree', 'w') as fw:
	        for i, s in enumerate(ll):
	            t = (openNLP.parse(s.replace('[NEGATED]', '')))
	            if t != '':
	                fw.write(t + '\n')
	                tree_list.append(t)
	    print len(sl)
	    print len(tree_list)

	return sl, tree_list


# # using stanford corenlp parsing too slow
# def extract_subtree(text, tregex):
#     r = requests.post(url="http://localhost:9000/tregex", 
#                       data=text, 
#                       params={"pattern": tregex})
#     js = r.json()
#     if js['sentences'][0] and '0' in js['sentences'][0] and 'namedNodes' in js['sentences'][0]['0']:
#         return js['sentences'][0]['0']['namedNodes']
#     return ''


def extract_subtree_treefile(f, tregex):
    t = subprocess.Popen(tregex_dir + 'tregex.sh ' + tregex + ' ' + f , stdout=subprocess.PIPE, shell=True)
    p = subprocess.Popen(tregex_dir + 'tregex.sh ' + tregex + ' ' + f + ' -t', stdout=subprocess.PIPE, shell=True)
    (tree, err) = t.communicate()
    (output, err) = p.communicate()
    print(tree)
    print(output)
    return output


def tregex_tsurgeon(f, pos):
    cmd = trts[pos][0] + '\n\n' + trts[pos][1].replace(',', '\n')
    with open('./stanford-tregex-2018-02-27/ts', 'w') as fw:     
        fw.write(cmd)
    t = subprocess.Popen('cd ' + tregex_dir + '; ./tsurgeon.sh -treeFile ../' + f + ' ts; cd ..', stdout=subprocess.PIPE, shell=True)
    p = subprocess.Popen('cd ' + tregex_dir + '; ./tsurgeon.sh -treeFile ../' + f + ' ts -s; cd ..', stdout=subprocess.PIPE, shell=True)
    (tree, err) = t.communicate()
    (output, err) = p.communicate()
    print('constituency tree: ' + output.replace('\n', ''))
    ts_out = re.sub('\([A-Z]*\$? |\(-[A-Z]+- |\)|\)|\(, |\(. |\n', '', output)
    ts_out = re.sub('-LRB-', '(', ts_out)
    ts_out = re.sub('-RRB-', ')', ts_out)
    return ts_out

