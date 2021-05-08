from flask import Response
import medacy_model_clinical_notes
import json
import mysql.connector
import subprocess
from ln2sql import Ln2sql
#Class for NLPUnit
class NLPUnit:
    def processRequest(self, js):
        #method to tokenize a string inputted from a json object
        #present in an http request.
        model = medacy_model_clinical_notes.load()
        json_data = js
        free_text = json_data['Comments']
        pid = json_data['PID']
        free_quoted = "\"" + free_text + "\""
        attributes = {'P_ID':pid, 'Drug':'', 'Strength':'', 'Duration':'', 'Route':'', 'Form':'', 'ADE':'', 'Dosage':'', 'Reason':'', 'Frequency':'', 'Note': free_quoted}
        for i in model.predict(free_text):
            if (attributes[i.tag] != ''):
                attributes[i.tag] += "," + i.text
            else:
                attributes[i.tag] = i.text
        
        #for i in attributes.keys():
        #    attributes[i] = "\"" + attributes[i] + "\""
        cnx = mysql.connector.connect(user='root',
                              host='localhost',
                              database='medicalRecords')
        cur = cnx.cursor()
        add_data = ("INSERT INTO clinical_notes "
                    "(PID, Drug, Strength, Duration, Route, Form, ADE, Dosage, Reason, Frequency, Note) "
                    "VALUES (%(P_ID)s, %(Drug)s, %(Strength)s, %(Duration)s, %(Route)s, %(Form)s, %(ADE)s, %(Dosage)s, %(Reason)s, %(Frequency)s, %(Note)s)")
        
        cur.execute(add_data, attributes)
        cnx.commit()
        
        return json.dumps(attributes)

    def processQuery(self, js):
        #method to process an NL query and convert to SQL, respond with JSON containing SQL statement and results from clinical_notes
        PATH_TO_ENGLISH = './ln2sql/ln2sql/lang_store/english.csv'
        PATH_TO_DUMP = './emr.sql'
        CMD_STR = 'python3 -m ln2sql.main -d ' + PATH_TO_DUMP + ' -l ' + PATH_TO_ENGLISH + ' -j out.json -i ' + '\"' + str(js['NLQuery']) + '\"'   
        sql_text = subprocess.run(CMD_STR, cwd='./ln2sql', shell=True, capture_output=True)
        query_str = str(sql_text.stdout.decode('utf-8'))
        query_str = query_str.replace("\n", " ").strip()
        
        to_return = {"Query": query_str}
        cnx = mysql.connector.connect(user='root',
                              host='localhost',
                              database='medicalRecords')
        cur = cnx.cursor()
        cur.execute(query_str)
        rows = [list(i) for i in cur.fetchall()]
        attr = (query_str.split("SELECT"))[1].split("FROM")[0]
        return {"List": rows, "Query String": query_str, "Attributes": attr}
        
    def processNLQuery(self, js):
        PATH = '.'
        PATH_TO_DUMP = PATH + '/emr.sql'
        PATH_TO_ENGLISH = PATH + '/ln2sql/ln2sql/lang_store/english.csv'
        PATH_TO_STOPWORDS = PATH + '/ln2sql/ln2sql/stopwords/english.txt'
        PATH_TO_THESAURUS = PATH + '/ln2sql/ln2sql/thesaurus_store/th_english.dat'
        queryPredictor = Ln2sql(PATH_TO_DUMP, PATH_TO_ENGLISH, thesaurus_path = PATH_TO_THESAURUS)
        text_to_predict = js['NLQuery']
        result = queryPredictor.get_query(text_to_predict)
        result = str(result).replace("\n", " ").strip()
        cnx = mysql.connector.connect(user='root',
                              host='localhost',
                              database='medicalRecords')
        cur = cnx.cursor()
        cur.execute(result)
        rows = [list(i) for i in cur.fetchall()]
        for row in rows:
            for i in range(len(row)):
                row[i] = str(row[i]) + "|"
        
        headers = [i[0] + "|" for i in cur.description]
        rows = [headers] + rows
        return {"Data": rows, "SQL" : result}

    def insertPatient(self, js):
        cnx = mysql.connector.connect(user='root',
                              host='localhost',
                              database='medicalRecords')
        cur = cnx.cursor()
        fname = js['Fname']
        lname = js['Lname']
        pid = js['PID']
        DOB = js['DOB']
        phone = js['Phone']
        ssn = js['ssn4']
        attributes = {'Fname':fname, 'Lname' : lname, 'PID':pid, 'DOB':DOB, 'Phone': phone, 'SSN4':ssn}
        add_data = ("INSERT INTO Patient "
                    "(Fname, Lname, PID, DOB, Phone1, SSN4) "
                    "VALUES (%(Fname)s, %(Lname)s, %(PID)s, %(DOB)s, %(Phone)s, %(SSN4)s)")

        cur.execute(add_data, attributes)
        cnx.commit()
        
        return json.dumps(attributes)
        

    
    def processText(self, free_text, pid):
        model = medacy_model_clinical_notes.load()
        attributes = {'P_ID':pid, 'Drug':'NULL', 'Strength':'NULL', 'Duration':'NULL', 'Route':'NULL', 'Form':'NULL', 'ADE':'NULL', 'Dosage':'NULL', 'Reason':'NULL', 'Frequency':'NULL', 'Note': free_text}
        for i in model.predict(free_text):
            attributes[i.tag] = i.text
        cnx = mysql.connector.connect(user='root',
                              host='localhost',
                              database='medicalRecords')
        cur = cnx.cursor()
        add_data = ("INSERT INTO clinical_notes "
                    "(P_ID, LoggedDate, Drug, Strength, Duration, Route, Form, ADE, Dosage, Reason, Frequency, Note) "
                    "VALUES (%(P_ID)s, CURDATE(), %(Drug)s, %(Strength)s, %(Duration)s, %(Route)s, %(Form)s, %(ADE)s, %(Dosage)s, %(Reason)s, %(Frequency)s, %(Note)s)")
        cur.execute(add_data, attributes)
        return open("response.html").read().format(pid=attributes["P_ID"], 
                                                Drug=attributes["Drug"], 
                                                Strength=attributes["Strength"],
                                                Duration=attributes["Duration"],
                                                Route=attributes["Route"],
                                                Form=attributes["Form"],
                                                ADE=attributes["ADE"],
                                                Dosage=attributes["Dosage"],
                                                Reason=attributes["Reason"],
                                                Frequency=attributes["Frequency"])
        
        

#nlp = NLPUnit()
#nlp.processRequest(json.loads('{"Comments":"I prescribed Advil to Joun for his severe pain"}')
