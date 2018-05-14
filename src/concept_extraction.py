# concept extraction
import os
from lxml import etree
#import subprocess


def get_cui_spans(xml_filename):
    tree = etree.parse(xml_filename)
    textsems = tree.xpath('*[@_ref_ontologyConceptArr]')
    span = lambda e: (int(e.get('begin')), int(e.get('end')))
    ref_to_span = {e.get('_ref_ontologyConceptArr'): span(e) for e in textsems}
    fsarrays = tree.xpath('uima.cas.FSArray')
    id_to_ref = {e.text: fs.get('_id') for fs in fsarrays for e in fs}
    umlsconcepts = tree.xpath('org.apache.ctakes.typesystem.type.refsem.UmlsConcept')
    cui_ids = [(c.get('cui'), c.get('tui'), c.get('preferredText'), c.get('_id')) for c in umlsconcepts]
    id_to_span = lambda _id: ref_to_span[id_to_ref[_id]]
    cui_spans = [(cui, tui, pt, id_to_span(_id)) for cui, tui, pt, _id in cui_ids]    
    seen = set()
    seen_add = seen.add
    return [cs for cs in cui_spans if not (cs in seen or seen_add(cs))]


def extract_cuis(xml_filename):
    cui_spans = get_cui_spans(xml_filename)
    cui_spans.sort(key=lambda cs: cs[3])
    row_id = os.path.basename(xml_filename).split('.')[0]
    txt = etree.parse(xml_filename).xpath('uima.cas.Sofa')[0].get('sofaString')
    return [(row_id, str(cs[3][0]), str(cs[3][1]), cs[0], cs[1], txt[(cs[3][0]):(cs[3][1])], cs[2]) for cs in cui_spans]


def ctakes_concept_extraction(data_dir, ctakes_folder):
	# run ctakes
	os.system('find . -name ".DS_Store" -type f -delete -print; ')
	os.system('cp ' + data_dir + 'tmp ' + ctakes_folder + 'note_input/')
	os.system('sh ' + ctakes_folder + 'bin/pipeline.sh')
	#(output, err) = p.communicate()
	os.system('rm ' + ctakes_folder + 'note_input/tmp')
	os.system('mv ' + ctakes_folder + 'note_output/tmp.xml '+ data_dir)

	# keep: 047, 046, 033, 184, 061, 048, 131
	# discard: 029, 034, 197, 121, 023, 059, 060, 195, 109, 022, 122, 

	d = {
	  "ddx": ["T047", "T191"], # disease/disorder/syndrome 
	  "ssx": ["T033", "T040", "T046", "T048", "T049", "T184"], # symptoms/signs
	  "med": ["T116", "T123", "T126", "T131"], # medications
	  "dxp": [], # diagnostic proc
	  "txp": ["T061"], # therapeutic proc
	  "lab": [], # labs
	  "ana": ["T017", "T024", "T025"], # anatomy
	}

	tui_list = []
	for k, v in d.items():
	    tui_list.extend(v)


	d = [e for e in extract_cuis(data_dir + 'tmp.xml')]
	df = pd.DataFrame(d, columns=['fname', 'start', 'end', 'cui', 'tui', 'original', 'preferred'])
	df = df[df['tui'].isin(tui_list)]

	with open(data_dir + 'tmp', 'r') as f:
	    doc = f.read()

	sec_dict = {}
	for sec_head in hard_section_list:
	    sec_dict[sec_head] = (doc.index('[SECTION-' + sec_head + '-START]') + len('[SECTION-' + sec_head + '-START]'), \
	                          doc.index('[SECTION-' + sec_head + '-END]'))
	sec_dict

	df['section'] = ''
	for idx in df.index:
	    for k, v in sec_dict.iteritems():
	        if int(df['start'][idx]) > v[0] and int(df['end'][idx]) < v[1]:
	            df['section'][idx] = str(k)

	s_neg_start = [s.start() for s in re.finditer('\\n\\n\\n\\n.*\\t \[NEGATED\]', doc)]
	s_neg_end = [s.start() for s in re.finditer('\[NEGATED\]', doc)]
	s_neg = zip(s_neg_start, s_neg_end) # range of negation in sentence level
	neg_range_list = [range(r[0], r[1]) for r in s_neg]
	#neg_range_list = [y for x in neg_range_list for y in x]

	df['negation'] = 0
	df['sent_id'] = 0
	df['sent_loc'] = 0
	for idx in df.index:
	    for i, nl in enumerate(neg_range_list):
	        if int(df['start'][idx]) in nl:
	            df['negation'][idx] = 0
	            df['sent_id'][idx] = i + 1 # sent_id from 1
	            df['sent_loc'][idx] = int(df['start'][idx]) - nl[0] + 1 # sent_loc also start from 1

	return df