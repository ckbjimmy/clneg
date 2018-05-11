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
4. Run `sh init.sh` to initialize Stanford CoreNLP server and Apache OpenNLP server
5. Run `main.py`
6. *Baseline can be obatined by running `negex.py`
