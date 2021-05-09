# Natural Language Processing (NLP) Webservice

The NLP service is responsible for handling RESTful requests for tokenization of clinical notes using medaCy, and translation of english queries to SQL using ln2sql.

## Install virtualenv
```
pip install virtualenv
```

## Activate the virtual environment
### MacOS/Linux
```
virtualenv ./env
source ./env/Scripts/activate
```
### Windows
```
virtualenv ./env
./env/Scripts/activate
```

## Install the dependency list using pip
```
cd NLPWebservice/
pip install -r requirements.txt
```

## Install the medaCy clinical model
```
cd NLPWebservice/
pip install git+https://github.com/NLPatVCU/medaCy_model_clinical_notes.git
```
## Install the ln2sql embedded module
```
cd NLPWebservice/
pip install ./ln2sql/
```

## Start the backend server on default port 8080
```
cd NLPWebservice/
python wsgi.py
```
If a numpy error is encountered upon running the server, reinstall numpy:
```
pip uninstall numpy
pip reinstall numpy
```
## Sample curl command once server is running
```
curl -i -d '{"PID": "P302", 
             "Comments":"I prescribed 3 doses of Morphine and Advil to John because of severe pain. He should take 1 capsule every 3 days"}' 
             -H "Content-Type:application/json" 
             -X POST http://sdp2.cse.uconn.edu:8080/process}
```
## Helpful links

medaCy : https://github.com/NLPatVCU/medaCy
ln2sql : https://github.com/FerreroJeremy/ln2sql

ln2sql is published in the following paper:
<i><a rel="license" href="https://www.researchgate.net/publication/278965118_fr2sql_Interrogation_de_bases_de_donnees_en_francais">Benoît Couderc and Jérémy Ferrero. fr2sql : Database Query in French. (fr2sql : Interrogation de bases de données en français [in French]). In Proceedings of the 17th RECITAL (affiliated with the 22th TALN Conference). June 2015. Caen, France. ATALA. pp.1-12 </a></i>


