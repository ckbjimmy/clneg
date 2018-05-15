# Clinical Text Summarization Tool with Syntax-based Negation and Semantic Concept Identification

## Introduction
we utilized the power of computational linguistics with human experts-curated knowledge base for identifying clinical concepts with their corresponding negation information in the clinical narrative texts.

We used the medical knowledge base UMLS along with Semantic Network, and take the advantage from the language hierarchical structure, the constituency tree, in order to identify the clinically relevant concepts and the negation information, which is extremely important for summarization.

In this project, we used Stanford CoreNLP, Apache clinical Text Analysis and Knowledge Extraction System (cTAKES), Unified Medical Language System (UMLS) and Semantic Network, to identify clinical concepts in the narrative texts.
We also performed the negation detection in the clinical sentences through sentence pruning, syntactic analysis and parsing using Apache OpenNLP and Stanford Tregex/Tsurgeon.
Then, we constructed itemized lists of clinically important concepts using the information generated from concept identification and negation.


## Dependencies
We provide `setup.sh` to download, install and configure most of the dependencies. 
The process is about 5 minutes.

- [Stanford CoreNLP 3.9.1](http://nlp.stanford.edu/software/stanford-corenlp-full-2018-02-27.zip)
- [Stanford Tregex/Tsurgeon 3.9.1](https://nlp.stanford.edu/software/stanford-tregex-2018-02-27.zip)
- [Apache OpenNLP](https://www.apache.org/dyn/closer.cgi/opennlp/opennlp-1.8.4/apache-opennlp-1.8.4-bin.tar.gz)
- [Apache cTAKES](http://ctakes.apache.org/)

However, you still need to request the access to UMLS by yourself to ensure that you can run semantic concept identification.

- [Access to NLM UMLS Metathesaurus/Ontology](https://www.nlm.nih.gov/databases/umls.html)


## Instruction
1. Request the UMLS access (this step will require few days for NIH/NLM to inspect your access application)
2. Run `sh setup.sh` in the first time
3. Add your UMLS account/password to `./src/ctakes/bin/pipeline.sh` after `-Dctakes.umlsuser=` and `-Dctakes.umlspw=`
4. Run `sh run_corenlp.sh` and `sh run_opennlp.sh` to initialize Stanford CoreNLP server and Apache OpenNLP server (make sure they are running in the background at port 9000 and 8080, respectively)
5. Open the other terminal and run `python main.py [file_path]`

- `../data/dev.txt` for development set
- `../data/test_ready.txt` for evaluation set
- `../data/1.txt` for testing note (as well as `2.txt`, `3.txt`) (The notes are no longer be available here. Please request the DUA of MIMIC-III database for using the notes)

6. We modularized some mutable components into files

- To design and add more rules for Tregex/Tsurgeon, please edit `tree_rules.py`
- To add more negation terms, please edit `./data/neg_list_complete.txt`, which is the modified version of the original `multilingual_lexicon-en-de-fr-sv.csv` open sources with our annotations
- To change the clinical semantic types for filtering, please edit `concept_extraction.py`

7. Baseline can be obatined by running `negex.py`
8. Please check the terminal screen for sentence parsing, and check the `./data/final_output`
9. For the process of development, please check the jupyter notebook `nlp_dev.ipynb` under `src` folder
