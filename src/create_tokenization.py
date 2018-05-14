# section and sentence tokenization for MIMIC-III discharge summaries
import os


def match_section_name(name, section_dict, nlp_parser):
    output = nlp_parser.annotate(name.lower(), properties={
                                              'annotators': 'lemma',
                                              'outputFormat': 'json',
                                              'threads': '4',
                                              'tokenize.options': 'normalizeParentheses=false, normalizeOtherBrackets=false'
                                              })
    try:
        name_lemma = set([[str(token['lemma']) for token in sent['tokens']] for sent in output['sentences']][0])
    except:
        return 'None'
    else:
        for section_name, section_name_lemma in section_dict.items():
            if all([item in name_lemma for item in section_name_lemma]):
                return section_name
    return 'None'


def mimic_tokenize(data_dir, filenames, nlp, neg_term): 
	section_names = ['Allergies', 'Chief Complaint', 'Major Surgical or Invasive Procedure', 'History of Present Illness',
	                'Past Medical History', 'Social History', 'Family History', 'Brief Hospital Course', 
	                'Medications on Admission', 'Discharge Medications', 'Discharge Diagnosis', 'Discharge Condition', 
	                 'Discharge Instructions']
	section_dict = {
	 'Allergies': ['allergy'],
	 'Brief Hospital Course': ['hospital', 'course'],
	 'Chief Complaint': ['chief', 'complaint'],
	 'Discharge Condition': ['discharge', 'condition'],
	 'Discharge Diagnosis': ['discharge', 'diagnosis'],
	 'Discharge Instructions': ['discharge', 'instruction'],
	 'Discharge Medications': ['discharge', 'medication'],
	 'Family History': ['family', 'history'],
	 'History of Present Illness': ['history', 'present', 'illness'],
	 'Major Surgical or Invasive Procedure': ['major',
	  'surgical',
	  'invasive',
	  'procedure'],
	 'Medications on Admission': ['medication', 'admission'],
	 'Past Medical History': ['medical', 'history'],
	 'Social History': ['social', 'history']}

	other_section_names = ['Followup Instructions', 'Physical Exam', 'Pertinent Results', 'Facility', 'Discharge Disposition']
	other_section_dict = {
	 'Discharge Disposition': ['discharge', 'disposition'],
	 'Facility': ['facility'],
	 'Followup Instructions': ['followup', 'instruction'],
	 'Pertinent Results': ['pertinent', 'result'],
	 'Physical Exam': ['physical', 'exam']}

	all_section_dict = {}
	all_section_dict.update(section_dict)
	all_section_dict.update(other_section_dict)

	section_names_list = list(section_dict.keys())

	section_to_parse = ['History of Present Illness', 'Brief Hospital Course', 'Discharge Instructions']
	section_not_to_parse = [item for item in section_names_list if item not in section_to_parse] + ['None']

	hard_section_list = ['History of Present Illness', 'Past Medical History', 'Brief Hospital Course', 'Discharge Diagnosis', 'Discharge Instructions']
	easy_section_list = [item for item in section_names_list if item not in hard_section_list]


	for idx in range(len(filenames)):
	    sections = {}
	    sections['None'] = []
	    with open(os.path.join(data_dir, filenames[idx]), 'r') as f:
	        for _ in range(3): next(f)
	        lines_buffer = []
	        previous_section_name = 'None'
	        for line in f:
	            line = line.strip()
	            if line:
	                if line.lower() == 'attending:':
	                    continue
	                lines_buffer.append(line)
	            else:
	                if lines_buffer:
	                    lines_buffer_head = lines_buffer[0]
	                    if ':' in lines_buffer_head:
	                        section_name = lines_buffer_head.split(':')[0]
	                        matched_section_name = match_section_name(section_name, all_section_dict, nlp)
	                        if matched_section_name != 'None':
	                            previous_section_name = matched_section_name
	                            if len(lines_buffer_head.split(':')[1:]) > 1:
	                                sections[matched_section_name] = [' '.join(lines_buffer_head.split(':')[1:])] + lines_buffer[1:]
	                            else:
	                                sections[matched_section_name] = lines_buffer[1:]
	                            lines_buffer = []
	                            continue

	                    sections[previous_section_name] = sections.get(previous_section_name, None) + lines_buffer
	                lines_buffer = []


	for section_name in section_to_parse:
	    if section_name in sections:
	        text = ' '.join(sections[section_name])
	        output = nlp.annotate(text, properties={
	                                          'annotators': 'ssplit',
	                                          'outputFormat': 'json',
	                                          'threads': '4',
	                                          'tokenize.options': 'normalizeParentheses=false, normalizeOtherBrackets=false'
	                                          })
	        try:
	            sents = [[str(token['word']) for token in sent['tokens']] for sent in output['sentences']]
	        except Exception as e:
	            pass
	        else:
	            sections[section_name] = [' '.join(sent) for sent in sents if sent != ['.']]


	for section_name in section_not_to_parse:
	    if section_name in sections:
	        new_section_content = []
	        for text in sections[section_name]:
	            output = nlp.annotate(text, properties={
	                                              'annotators': 'ssplit',
	                                              'outputFormat': 'json',
	                                              'threads': '4',
	                                              'tokenize.options': 'normalizeParentheses=false, normalizeOtherBrackets=false'
	                                              })
	            try:
	                sents = [[str(token['word']) for token in sent['tokens']] for sent in output['sentences']]
	            except Exception as e:
	                pass
	            else:
	                new_section_content.append(' '.join([' '.join(sent) for sent in sents if sent != ['.']]))
	        sections[section_name] = new_section_content


	with open(data_dir + 'tmp', 'w') as f:
	    for section_name in hard_section_list:
	        # add section head tag
	        f.write('\n\n\n\n[SECTION-{}-START]'.format(section_name))
	        if section_name in sections:
	            for item in sections[section_name]:
	                # tag negated or affirmed based on string matching --- negation term list
	                # add one space to prevent loss of 'no ', 'not ', ... etc.
	                if any(substring in ' ' + item for substring in neg_term):
	                    f.write('\n\n\n\n' + item + '\t [NEGATED]')
	                else:
	                    f.write('\n\n\n\n' + item + '\t [AFFIRMED]')
	        # add section end tag
	        f.write('\n\n\n\n[SECTION-{}-END]'.format(section_name)) # this file for concept extraction and sentence parsing

	return hard_section_list
