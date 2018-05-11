wget https://github.com/curzona/opennlp-python/archive/master.zip; \
unzip master.zip; \
rm master.zip; \
mv opennlp-python-master opennlp-python; \
pip install -r .opennlp-python/requirements.txt; \
wget http://mirrors.ibiblio.org/apache/opennlp/opennlp-1.8.4/apache-opennlp-1.8.4-bin.tar.gz; \
tar -zxvf apache-opennlp-1.8.4-bin.tar.gz -C ./opennlp-python; \
rm apache-opennlp-1.8.4-bin.tar.gz; \
mkdir ./opennlp-python/apache-opennlp-1.8.4/models; \
wget http://opennlp.sourceforge.net/models-1.5/en-parser-chunking.bin; \
mv en-parser-chunking.bin ./opennlp-python/apache-opennlp-1.8.4/models/; \
wget http://nlp.stanford.edu/software/stanford-corenlp-full-2018-02-27.zip; \
unzip stanford-corenlp-full-2018-02-27.zip; \
rm stanford-corenlp-full-2018-02-27.zip; \
wget https://nlp.stanford.edu/software/stanford-tregex-2018-02-27.zip; \
unzip stanford-tregex-2018-02-27.zip; \
rm stanford-tregex-2018-02-27.zip; \
wget http://mirror.stjschools.org/public/apache//ctakes/ctakes-4.0.0/apache-ctakes-4.0.0-bin.tar.gz; \
tar -zxvf apache-ctakes-4.0.0-bin.tar.gz; \
mv apache-ctakes-4.0.0 ctakes; \
rm apache-ctakes-4.0.0-bin.tar.gz; \
mkdir ./ctakes/note_input/; \
mkdir ./ctakes/note_output/; \
wget wget http://sourceforge.net/projects/ctakesresources/files/sno_rx_16ab.zip/download --no-check-certificate; \
unzip download -d ./ctakes/resources/org/apache/ctakes/dictionary/lookup/fast; \
rm download; \
cp ./ctakes_config/pipeline.sh ./ctakes/bin; \
cp ./ctakes_config/test_plaintext_auto.xml ./ctakes/desc/ctakes-clinical-pipeline/desc/collection_processing_engine