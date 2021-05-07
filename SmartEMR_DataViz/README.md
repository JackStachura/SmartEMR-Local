# NLP for Data Visualization

The analytics webservice uses the nl4dv library to generate dynamic data visualizations from natural language. The requests are handled by a Flask backend that is integrated with other webservices.

## Install virtualenv
```
pip install virtualenv
```

## Activate the virtual environment
### MacOS/Linux
```
virtualenv ~/.analytics
source ~/.analytics/bin/activate
```
### Windows
```
virtualenv C:\.analytics
C:\.analytics\Scripts\activate.bat
```

## Install the dependencies
```
cd analytics/app
pip install -r requirements.txt
python -m nltk.downloader popular
python -m spacy download en_core_web_sm
```

## Start the backend server
```
flask run -h localhost -p 5000
```
