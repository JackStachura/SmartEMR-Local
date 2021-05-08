#!/usr/bin/python

import mysql.connector
import math
import random
#https://www.geeksforgeeks.org/random-numbers-in-python/
import datetime
import calendar #https://stackoverflow.com/questions/4130922/how-to-increment-datetime-by-custom-months-in-python-without-using-library
#from datetime import date, datetime, timedelta
from mysql.connector import errorcode

#Cause sql 8 takes in tine int not 'TRUE'

Add_to_db = False
num_of_patient = 1

#for inserting data in the database
FALSE = 0
TRUE = 1
#Also note, for safety measure cnx.commit() is commented out at the very bottom
#if false this will print the results
                #position, name, erupt start, erupt end, shed start, shed end(months)   Note average
"""

Upper_primary_teeth = [("Central", "incisor", 8, 12, 6*12, 7*12)
                        ("Lateral", "incisor", 9, 13, 7*12, 8*12)
                        ("Canine", "canine", 16, 22, 10*12, 12*12)
                        ("First", "molar", 13, 19, 9*12, 11*12)
                         ("Second", "molar", 25, 33, 10*12, 12*12)]
Lower_primary_teeth = [ ("Central", "incisor", 6,10,6*12,7*12)
                        ("Lateral", "incisor", 10, 16, 7*12,8*12)
                        ("Canine", "canine", 17, 23, 9*12, 12*12)
                        ("First", "molar", 14, 18, 9*12, 11*12)
                        ("Second", "molar", 23, 31, 10*12, 12*12)]
"""
def add_months(sourcedate, months):
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month // 12
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year,month)[1])
    return datetime.date(year, month, day)

#https://dev.mysql.com/doc/connector-python/en/connector-python-example-cursor-transaction.html
#connect to db
#cnx = mysql.connector.connect(user='root', password='', host='localhost', database='emr')

if(Add_to_db):
    cnx = mysql.connector.connect(user='root', password='', host='localhost', database='medicalRecords')

    cursor = cnx.cursor()

add_Persons = ("INSERT INTO Persons"
              "(PersonID, Date_of_birth, Sex, Orthodontic_treatment)"
              "VALUES (%(PersonID)s,%(Date_of_birth)s,%(Sex)s,%(Orthodontic_treatment)s)")
add_Dental = ("INSERT INTO dental_record"
              "(P_ID, LoggedDate, Num_Teeth, Dentition_stage, Erupt_rate,Occlusion, Tooth_color, Oral_hygiene, TMJ)"
              "Values(%(P_ID)s, %(LoggedDate)s, %(Num_Teeth)s, %(Dentition_stage)s, %(Erupt_rate)s,%(Occlusion)s, %(Tooth_color)s, %(Oral_hygiene)s, %(TMJ)s)")
add_Gums = ("INSERT INTO Gums"
            "(P_ID, LoggedDate, Pocket_depths, Mobility)"
            "Values(%(P_ID)s, %(LoggedDate)s, %(Pocket_depths)s, %(Mobility)s)")
add_Tooth = ("INSERT INTO Tooth"
             "(P_ID, LoggedDate, Tooth, Side, Position, Upper, Secondary, Missing, Size, Color, Eruption)"
             "Values(%(P_ID)s, %(LoggedDate)s, %(Tooth)s, %(Side)s, %(Position)s, %(Upper)s, %(Secondary)s, %(Missing)s, %(Size)s, %(Color)s,%(Eruption)s)")
add_Growth = ("INSERT INTO Growth"
              "(P_ID, LoggedDate, Height, Weight)"
              "Values(%(P_ID)s, %(LoggedDate)s,%(Height)s,%(Weight)s)")
add_Eyes =  ("INSERT INTO EYES"                                     
             "(P_ID, LoggedDate, Iris_R, Iris_L, Sclera)"                     
             "Values(%(P_ID)s, %(LoggedDate)s,%(Iris_R)s,%(Iris_L)s,%(Sclera)s)")
add_Has_Mutation = ("INSERT INTO Has_Mutation"                                                   
                    "(P_ID, Gene)"                         
                    "Values(%(P_ID)s, %(Gene)s)")
add_Diagnose = ("INSERT INTO Diagnose"                                                   
                "(P_ID, C_ID, LoggedDate, Degree_of_Severity)"                         
                "Values(%(P_ID)s, %(C_ID)s,%(LoggedDate)s,%(Degree_of_Severity)s)")

#range of how many patients being created
for x in range(0,num_of_patient):
    #info for table patient
    PersonID = 'P'+str(x)
    #choose a random birthday https://www.kite.com/python/answers/how-to-generate-a-random-date-between-two-dates-in-python
    today = datetime.datetime.now()
    start_date = today - datetime.timedelta(days=60*365) #oldest is a 60 year old
    time_between_dates = today - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)

    Date_of_birth = start_date + datetime.timedelta(days=random_number_of_days)
    #https://docs.python.org/3/library/datetime.html#strftime-strptime-behavior
    #https://stackoverflow.com/questions/7588511/format-a-datetime-into-a-string-with-milliseconds
    #dob = Date_of_birth.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    Sex = 'XY'
    if(random.randint(0,1) == 1):
        Sex = 'XX'
    y_chromsome = False
    if(Sex[len(Sex)-1]=='y'or Sex[len(Sex)-1]=='Y'):
        y_chromsome = True

    #if 20, Orthodontic_treatment is true
    Orthodontic_treatment = 0
    #https://www.geeksforgeeks.org/python-program-to-calculate-age-in-year/
    age = int((today - Date_of_birth).days/365.2425)
    age_in_months = (today.year - Date_of_birth.year) * 12 + (today.month - Date_of_birth.month)
    if(age > 20):
        Orthodontic_treatment = 1
    #insert into table
    data_Persons = {
        'PersonID': PersonID,
        'Date_of_birth': Date_of_birth,
        'Sex': Sex,
        'Orthodontic_treatment':Orthodontic_treatment,
    }
    if(Add_to_db):
            cursor.execute(add_Persons,data_Persons)
    else:
        print(data_Persons)
    #DELETE FROM PERSONS WHERE PersonID = 'P1';

    #gene mutation
    if not(Add_to_db):
        print("\nMutations:")
    gene_mutation = []
    perc = random.randint(0,100)
    if(perc<10):
        gene_mutation.append("COL1A1")
    perc = random.randint(0, 100)
    if (perc < 10):
        gene_mutation.append("COL1A2")
    perc = random.randint(0, 100)
    if (perc < 15):
        if(y_chromsome):
            gene_mutation.append("NHS")
    perc = random.randint(0, 100)
    if (perc < 7):
        gene_mutation.append("ADAMTS20")
    perc = random.randint(0, 100)
    if (perc < 14):
        gene_mutation.append("APC")
    perc = random.randint(0, 100)
    if (perc < 12):
        gene_mutation.append("RUNX2")
    perc = random.randint(0, 100)
    if (perc < 8):
        gene_mutation.append("TNF")
    perc = random.randint(0, 100)
    if (perc < 13):
        gene_mutation.append("hemoglobin-Beta")


    for Gene in  gene_mutation:
        data_Has_Mutation = {
            'P_ID': PersonID,
            'Gene': Gene,
        }
        if(Add_to_db):
            cursor.execute(add_Has_Mutation,data_Has_Mutation)
        else:
            print(data_Has_Mutation)

    #dental record
        #primary teeth
    if not(Add_to_db):
        print("\nPrimary Teeth:")
    delay = 0
    #position, tooth name, eruption, shed date
    """
    R_Upper_primary_teeth = [ ("Central", "incisor", random.randint(8,12), random.randint(6*12, 7*12))
                        ("Lateral", "incisor", random.randint(9, 13), random.randint(7*12, 8*12))
                        ("Canine", "canine" random.randint(16, 22), random.randint(10*12, 12*12))
                        ("First", "molar", random.randint(13, 19), random.randint(9*12, 11*12))
                        ("Second", "molar", random.randint(25, 33), random.randint(10*12, 12*12))]

    L_Upper_primary_teeth = [ ("Central", "incisor", random.randint(8,12), random.randint(6*12, 7*12))
                        ("Lateral", "incisor", random.randint(9, 13), random.randint(7*12, 8*12))
                        ("Canine", "canine", random.randint(16, 22), random.randint(10*12, 12*12))
                        ("First", "molar", random.randint(13, 19), random.randint(9*12, 11*12))
                        ("Second", "molar", random.randint(25, 33), random.randint(10*12, 12*12))]
    R_Lower_primary_teeth = [ ("Central", "incisor", random.randint(6,10),random.randint(6*12,7*12))
                        ("Lateral", "incisor", random.randint(10, 16), random.randint(7*12,8*12))
                        ("Canine", "canine", random.randint(17, 23), random.randint(9*12, 12*12))
                        ("First", "molar", random.randint(14, 18), random.randint(9*12, 11*12))
                        ("Second", "molar", random.randint(23, 31), random.randint(10*12, 12*12))]
    L_Lower_primary_teeth = [ ("Central", "incisor", random.randint(6,10),random.randint(6*12,7*12))
                        ("Lateral", "incisor", random.randint(10, 16), random.randint(7*12,8*12))
                        ("Canine", "canine", random.randint(17, 23), random.randint(9*12, 12*12))
                        ("First", "molar", random.randint(14, 18), random.randint(9*12, 11*12))
                        ("Second", "molar", random.randint(23, 31), random.randint(10*12, 12*12))]
    """
    R_Upper_primary_teeth =[["Central", "incisor"], ["Lateral", "incisor"], ["Canine", "canine"], ["First", "molar"], ["Second", "molar"]]
    L_Upper_primary_teeth =[["Central", "incisor"], ["Lateral", "incisor"], ["Canine", "canine"], ["First", "molar"], ["Second", "molar"]]
    R_Lower_primary_teeth =[["Central", "incisor"], ["Lateral", "incisor"], ["Canine", "canine"], ["First", "molar"], ["Second", "molar"]]
    L_Lower_primary_teeth =[["Central", "incisor"], ["Lateral", "incisor"], ["Canine", "canine"], ["First", "molar"], ["Second", "molar"]]
    #fills eruption and shed date for both sides of Upper teeth
    #the below is dependent on the order of the above so TRY NOT TO CHANGE ^(also effects secondary teeth)
    for x in range(0,2):
        if (x == 0):
            list = R_Upper_primary_teeth
        else:
            list = L_Upper_primary_teeth
        tmp_erupt = random.randint(8, 12)
        tmp_shed = random.randint(6 * 12, 7 * 12)
        list[0].append(tmp_erupt)
        list[0].append(tmp_shed)
        list[0].append(tmp_shed + random.randint(1, 12)) #assuming it takes 1 to 12 months for tooth to appear after it falls out
        tmp_erupt = random.randint(9, 13)
        tmp_shed = random.randint(7 * 12, 8 * 12)
        list[1].append(tmp_erupt)
        list[1].append(tmp_shed)
        list[1].append(tmp_shed + random.randint(1, 12))
        tmp_erupt = random.randint(16, 22)
        tmp_shed = random.randint(10 * 12, 12 * 12)
        list[2].append(tmp_erupt)
        list[2].append(tmp_shed)
        list[2].append(tmp_shed + random.randint(1, 12))
        tmp_erupt = random.randint(13, 19)
        tmp_shed = random.randint(9 * 12, 11 * 12)
        list[3].append(tmp_erupt)
        list[3].append(tmp_shed)
        list[3].append(tmp_shed + random.randint(1, 12))
        tmp_erupt = random.randint(25, 33)
        tmp_shed = random.randint(10 * 12, 12 * 12)
        list[4].append(tmp_erupt)
        list[4].append(tmp_shed)
        list[4].append(tmp_shed + random.randint(1,12))
    for x in range(0,2):
        if (x == 0):
            list = R_Lower_primary_teeth
        else:
            list = L_Lower_primary_teeth
        tmp_erupt = random.randint(6, 10)
        tmp_shed = random.randint(6 * 12, 7 * 12)
        list[0].append(tmp_erupt)
        list[0].append(tmp_shed)
        list[0].append(tmp_shed + random.randint(1, 12))
        tmp_erupt =  random.randint(10, 16)
        tmp_shed = random.randint(7 * 12, 8 * 12)
        list[1].append(tmp_erupt)
        list[1].append(tmp_shed)
        list[1].append(tmp_shed + random.randint(1, 12))
        tmp_erupt = random.randint(17, 23)
        tmp_shed = random.randint(9 * 12, 12 * 12)
        list[2].append(tmp_erupt)
        list[2].append(tmp_shed)
        list[2].append(tmp_shed + random.randint(1, 12))
        tmp_erupt = random.randint(14, 18)
        tmp_shed = random.randint(9 * 12, 11 * 12)
        list[3].append(tmp_erupt)
        list[3].append(tmp_shed)
        list[3].append(tmp_shed + random.randint(1, 12))
        tmp_erupt = random.randint(23, 31)
        tmp_shed = random.randint(10 * 12, 12 * 12)
        list[4].append(tmp_erupt)
        list[4].append(tmp_shed)
        list[4].append(tmp_shed + random.randint(1, 12))
    max_erupt = 33#in month
    Num_Teeth = 0
    teeths = []#a list of data_dental of the past 6 month
    #assuming a visit is every 6 months
    #primary teeth come in between 6-33 months
    # start at 12 months since record past 6 month development
    for monthly_visits in range(2,min(math.floor(age_in_months/6), math.ceil(max_erupt/6))+1):
        LoggedDate = add_months(Date_of_birth,monthly_visits*6)

        #Gums
        Pocket_depth = random.randint(1,3)# mm
        Mobility = random.uniform(0.0, 2.5)# mm
        data_Gums = {
            'P_ID': PersonID,
            'LoggedDate': LoggedDate,
            'Pocket_depths': Pocket_depth,
            'Mobility': Mobility,
        }

        #primary teeth array
        NHS_mesiodens = False
        for Gene in gene_mutation:
            if (Gene == "NHS"):
                NHS_mesiodens = True

        length_primary = len(R_Upper_primary_teeth)
        #Primary teeth are the same length, we have 4 tables for 4 possibilites up, side
        #Should be improved
        for x in range(0, length_primary*4):
            if(x < length_primary):
                tooth = R_Upper_primary_teeth[x % length_primary]
                Side = 'Right'
                Upper = TRUE
            elif(x <(2*length_primary)):
                tooth = L_Upper_primary_teeth[x % length_primary]
                Side = 'Left'
                Upper = TRUE
            elif(x <(3*length_primary)):
                tooth = R_Lower_primary_teeth[x % length_primary]
                Side = 'Right'
                Upper = FALSE
            else:
                tooth = L_Lower_primary_teeth[x % length_primary]
                Side = 'Left'
                Upper = FALSE

            Eruption = tooth[2]
            if (((monthly_visits*6) - 6) <= Eruption < (monthly_visits*6)):
                Num_Teeth=Num_Teeth+1

                Size = 'Normal'
                Color = 'Reddish brown'
                data_Tooth = {
                    'P_ID': PersonID,
                    'LoggedDate': LoggedDate,
                    'Tooth': tooth[1],
                    'Side': Side,
                    'Position': tooth[0],
                    'Upper': Upper,
                    'Secondary': FALSE,
                    'Missing': FALSE,
                    'Size': Size,
                    'Color': Color,
                    'Eruption': Eruption,
                }
                teeths.append(data_Tooth)
                # NHS
                perc = random.randint(0,100)
                NHS_irregular = False
                if (NHS_mesiodens and perc < 10):
                    NHS_irregular = True
                    NHS_mesiodens = False  # We only add one tooth for NHS
                    Num_Teeth = Num_Teeth + 1
                    data_Tooth = {
                        'P_ID': PersonID,
                        'LoggedDate': LoggedDate,
                        'Tooth': "Mesiodens",
                        'Side': "Middle",
                        'Position': "Supernumerary",
                        'Upper': TRUE,
                        'Secondary': FALSE,
                        'Missing': FALSE,
                        'Size': Size,
                        'Color': Color,
                        'Eruption': Eruption,
                    }
                    #should fix the above eruption
                    teeths.append(data_Tooth)
                    data_Diagnose = {
                        'P_ID': PersonID,
                        'C_ID': "C4",
                        'LoggedDate': Date_of_birth,
                        'Degree_of_Severity': "Visable",
                    }
                    if (Add_to_db):
                        cursor.execute(add_Diagnose, data_Diagnose)
                    else:
                        print(data_Diagnose)
                        print("\n")
        #Enter primary into Dental_Record gums, and teeth information for primary teeth
        Erupt_rate = 'normal'
        if(NHS_irregular):
            Erupt_rate = 'irregular'
        data_Dental = {
            'P_ID': PersonID,
            'LoggedDate': LoggedDate,
            'Num_Teeth': Num_Teeth,
            'Dentition_stage': 'Deciduous',
            'Erupt_rate': Erupt_rate,
            'Occlusion': 'normal',
            'Tooth_color': 'normal',
            'Oral_hygiene': 'good',
            'TMJ': FALSE,
        }
        if (Add_to_db):
            cursor.execute(add_Dental, data_Dental)
            for data_Teeth in teeths:
                cursor.execute(add_Tooth, data_Teeth)
            cursor.execute(add_Gums, data_Gums)
        else:
           print(teeths)
           #print(data_Gums)
           print(data_Dental)
           print("\n") 
        teeths.clear()

    # dental record
        #time range before secondary teeth
    #  we add one because of previous range
    if not(Add_to_db):
        print("\nTime before secondary Teeth Done:")
    
    previous_range = math.ceil(max_erupt / 6) + 1
    max_erupt = (12*5)
    #max  before erupt for secondary teeth start coming in(i.e for 33month to 5 years)
    for monthly_visits in range(previous_range,min(math.floor(age_in_months/6), math.ceil(max_erupt/6))+1):
        LoggedDate = add_months(Date_of_birth, monthly_visits * 6)

        # Gums
        Pocket_depth = random.randint(1, 3)  # mm
        Mobility = random.uniform(0.0, 2.5)  # mm
        data_Gums = {
            'P_ID': PersonID,
            'LoggedDate': LoggedDate,
            'Pocket_depths': Pocket_depth,
            'Mobility': Mobility,
        }
        Erupt_rate = 'normal'
        data_Dental = {
            'P_ID': PersonID,
            'LoggedDate': LoggedDate,
            'Num_Teeth': Num_Teeth,
            'Dentition_stage': 'Deciduous',
            'Erupt_rate': Erupt_rate,
            'Occlusion': 'normal',
            'Tooth_color': 'normal',
            'Oral_hygiene': 'good',
            'TMJ': FALSE,
        }

        if (Add_to_db):
            cursor.execute(add_Dental, data_Dental)
            cursor.execute(add_Gums, data_Gums)
        else:
            #print(data_Gums)
            print(data_Dental)
            print("\n")

    # dental record
        # secondary teeth
    if not(Add_to_db):
        print("\nSecondary Teeth:")
    L_Upper_secondary_teeth = [["Molar", "First"],["Molar", "Second"],["Molar", "Third"]]
    R_Upper_secondary_teeth = [["Molar", "First"],["Molar", "Second"],["Molar", "Third"]]
    L_Lower_secondary_teeth = [["Molar", "First"],["Molar", "Second"],["Molar", "Third"]]
    R_Lower_secondary_teeth = [["Molar", "First"],["Molar", "Second"],["Molar", "Third"]]
    #shed date from primary determine secondary teeth coming in
    #  we add one because of previous range
    for x in range(0, 2):
        if (x == 0):
            list = R_Upper_secondary_teeth
        else:
            list = L_Upper_secondary_teeth
        tmp_erupt = random.randint(6*12, 7*12)   #these values are in years, so conver to months
        list[0].append(tmp_erupt)
        tmp_erupt = random.randint(12*12, 14*12)
        list[1].append(tmp_erupt)
        tmp_erupt = random.randint(17*12, 25*12)
        list[2].append(tmp_erupt)


    for x in range(0,2):
        if (x == 0):
            list = R_Lower_secondary_teeth
        else:
            list = L_Lower_secondary_teeth
        tmp_erupt = random.randint(6*12, 7*12)
        list[0].append(tmp_erupt)
        tmp_erupt = random.randint(12*12, 14*12)
        list[1].append(tmp_erupt)
        tmp_erupt = random.randint(17*12, 25*12)
        list[2].append(tmp_erupt)

    previous_range = math.ceil(max_erupt / 6) + 1     
    max_erupt = 25 * 12
    # max erupt for secondary teeth start coming in(i.e for 6years to 25 years)
    First = True #used for inserting COLA1A1 and COLA1A2 into diagonose
    for monthly_visits in range(previous_range, min(math.floor(age_in_months / 6), math.ceil(max_erupt / 6))+1):
        LoggedDate = add_months(Date_of_birth, monthly_visits * 6)

        # Gums
        Pocket_depth = random.randint(1, 3)  # mm
        Mobility = random.uniform(0.0, 2.5)  # mm
        data_Gums = {
            'P_ID': PersonID,
            'LoggedDate': LoggedDate,
            'Pocket_depths': Pocket_depth,
            'Mobility': Mobility,
        }
        length_secondary = len(R_Upper_secondary_teeth)
        x = 0
        for x in range(0, length_primary * 4 + length_secondary * 4):
            if (x < length_primary):
                tooth = R_Upper_primary_teeth[x % length_primary]
                Side = 'Right'
                Upper = TRUE
            elif (x < (2 * length_primary)):
                tooth = L_Upper_primary_teeth[x % length_primary]
                Side = 'Left'
                Upper = TRUE
            elif (x < (3 * length_primary)):
                tooth = R_Lower_primary_teeth[x % length_primary]
                Side = 'Right'
                Upper = FALSE
            elif (x < (4 * length_primary)):
                tooth = L_Lower_primary_teeth[x % length_primary]
                Side = 'Left'
                Upper = FALSE
            elif (x < ((4 * length_primary)+length_secondary)):
                tooth = R_Upper_secondary_teeth[x % length_secondary]
                Side = 'Right'
                Upper = TRUE
            elif (x < ((4 * length_primary) + 2*length_secondary)):
                tooth = L_Upper_secondary_teeth[x % length_secondary]
                Side = 'Left'
                Upper = TRUE
            elif (x < ((4 * length_primary)+ 3*length_secondary)):
                tooth = R_Lower_secondary_teeth[x % length_secondary]
                Side = 'Right'
                Upper = FALSE
            else:
                tooth = L_Lower_secondary_teeth[x % length_secondary]
                Side = 'Left'
                Upper = FALSE

            Color = 'Reddish Brown'

            for Gene in gene_mutation:
                if (Gene == "COL1A1" or Gene == "COL1A2"):
                    # https://www.rdhmag.com/patient-care/article/16408161/implication-of-brittle-bone-diseases
                    # for Col1a1 color of teeth can vary and appeard during secondary stage
                    perc = random.randint(0, 100)
                    if (perc < 25):
                        Color = 'Brown'
                    elif (perc < 25 * 2):
                        Color = 'Yellow'
                    elif (perc < 25 * 3):
                        Color = 'Gray'
                    if (not Color == 'Reddish brown') and First:
                        First = False
                        Color = 'Irregular'
                        perc = random.randint(0, 1)
                        if (perc == 1):
                            Serverity = "Noticeable"
                        else:
                            Serverity = "Slightly Noticeable"
                        data_Diagnose = {
                            'P_ID': PersonID,
                            'C_ID': "C7",
                            'LoggedDate': Date_of_birth,
                            'Degree_of_Severity': Serverity,
                        }
                        if (Add_to_db):
                            cursor.execute(add_Diagnose, data_Diagnose)
                        else:
                            print(data_Diagnose)
                            print("\n")
            #this is statment is to determine if we are working with primary list or secondary list
            if (len(tooth) > length_secondary):
                Shed = tooth[3]
                if (((monthly_visits * 6) - 6) <= Shed < (monthly_visits * 6)):
                    Num_Teeth = Num_Teeth - 1
                    Size = 'Normal'
                    Color == 'Reddish brown'
                    data_Tooth = {
                        'P_ID': PersonID,
                        'LoggedDate': LoggedDate,
                        'Tooth': tooth[1],
                        'Side': Side,
                        'Position': tooth[0],
                        'Upper': Upper,
                        'Secondary': FALSE,
                        'Missing': TRUE,
                        'Size': Size,
                        'Color': Color,
                        'Eruption': Eruption,
                    }
                    teeths.append(data_Tooth)
                Eruption = tooth[4]
                if (((monthly_visits * 6) - 6) <= Eruption < (monthly_visits * 6)):
                    Num_Teeth = Num_Teeth + 1

                    Size = 'Normal'
                    data_Tooth = {
                        'P_ID': PersonID,
                        'LoggedDate': LoggedDate,
                        'Tooth': tooth[1],
                        'Side': Side,
                        'Position': tooth[0],
                        'Upper': Upper,
                        'Secondary': TRUE,
                        'Missing': FALSE,
                        'Size': Size,
                        'Color': Color,
                        'Eruption': Eruption,
                    }
                    teeths.append(data_Tooth)

            else:
                Eruption = tooth[2]
                if (((monthly_visits * 6) - 6) <= Eruption < (monthly_visits * 6)):
                    Num_Teeth = Num_Teeth + 1

                    Size = 'Normal'
                    Color = 'Reddish brown'
                    data_Tooth = {
                        'P_ID': PersonID,
                        'LoggedDate': LoggedDate,
                        'Tooth': tooth[1],
                        'Side': Side,
                        'Position': tooth[0],
                        'Upper': Upper,
                        'Secondary': TRUE,
                        'Missing': FALSE,
                        'Size': Size,
                        'Color': Color,
                        'Eruption': Eruption,
                    }
                    teeths.append(data_Tooth)

        Erupt_rate = 'normal'
        data_Dental = {
            'P_ID': PersonID,
            'LoggedDate': LoggedDate,
            'Num_Teeth': Num_Teeth,
            'Dentition_stage': 'Mixed',
            'Erupt_rate': Erupt_rate,
            'Occlusion': 'normal',
            'Tooth_color': 'normal',
            'Oral_hygiene': 'good',
            'TMJ': FALSE,
        }
        if (Add_to_db):
            cursor.execute(add_Dental, data_Dental)
            for data_Teeth in teeths:
                cursor.execute(add_Tooth, data_Teeth)
            cursor.execute(add_Gums, data_Gums)
        else:
            print(teeths)
            #print(data_Gums)
            print(data_Dental)
            print("\n")
        teeths.clear()



        
    # dental record
        #any other dental record that is not correlated with teeth coming in
        #NOTE: assuming that we dont hold records of dead people
        #add wisdom teeth removal/extra wisdom teeth
    #

    for Gene in gene_mutation:
        if (Gene == "APC"):
            if not(Add_to_db):
                print("\nTime after secondary teeth for supernumerary(APC):")
            previous_range = math.ceil(max_erupt / 6) + 1
            max_erupt = max_erupt + 24
            First = True
            for monthly_visits in range(previous_range, min(math.floor(age_in_months / 6), math.ceil(max_erupt / 6)) + 1):
                LoggedDate = add_months(Date_of_birth, monthly_visits * 6)

                # Gums
                Pocket_depth = random.randint(1, 3)  # mm
                Mobility = random.uniform(0.0, 2.5)  # mm
                data_Gums = {
                    'P_ID': PersonID,
                    'LoggedDate': LoggedDate,
                    'Pocket_depths': Pocket_depth,
                    'Mobility': Mobility,
                }
                perc = random.randint(0,100)
                if(perc < 10):
                    if(First):
                        First = False
                        data_Diagnose = {
                            'P_ID': PersonID,
                            'C_ID': "C4",
                            'LoggedDate': LoggedDate,
                            'Degree_of_Severity': "Visable",
                        }
                        if (Add_to_db):
                            cursor.execute(add_Diagnose, data_Diagnose)
                        else:
                            print(data_Diagnose)
                            print("\n")

                        if (perc == 0):
                            Serverity = 'Small'
                        elif (perc == 1):
                            Serverity = 'Medium'
                        else:
                            Serverity = 'Large'
                        data_Diagnose = {
                            'P_ID': PersonID,
                            'C_ID': "C3",
                            'LoggedDate': LoggedDate,
                            'Degree_of_Severity': Serverity,
                        }
                        if (Add_to_db):
                            cursor.execute(add_Diagnose, data_Diagnose)
                        else:
                            print(data_Diagnose)
                            print("\n")
                    perc = random.randint(0, 1)
                    Secondary = FALSE
                    if(perc == 1):
                        Secondary = TRUE
                    Upper = FALSE
                    if (perc == 1):
                        Upper = TRUE

                    Erupt_rate = 'irregular'
                    Num_Teeth=Num_Teeth+1
                    data_Tooth = {
                        'P_ID': PersonID,
                        'LoggedDate': LoggedDate,
                        'Tooth': "Hyperdontia ",
                        'Side': Side,
                        'Position': "Supernumerary",
                        'Upper': Upper,
                        'Secondary': Secondary,
                        'Missing': FALSE,
                        'Size': Size,
                        'Color': Color,
                        'Eruption': monthly_visits,
                    }
                    #Note should change the above
                    teeths.append(data_Tooth)
                data_Dental = {
                    'P_ID': PersonID,
                    'LoggedDate': LoggedDate,
                    'Num_Teeth': Num_Teeth,
                    'Dentition_stage': 'Mixed',
                    'Erupt_rate': Erupt_rate,
                    'Occlusion': 'normal',
                    'Tooth_color': 'normal',
                    'Oral_hygiene': 'good',
                    'TMJ': FALSE,
                }
                if (Add_to_db):
                    cursor.execute(add_Dental, data_Dental)
                    for data_Teeth in teeths:
                        cursor.execute(add_Tooth, data_Teeth)
                    cursor.execute(add_Gums, data_Gums)
                else:
                    print(teeths)
                    # print(data_Gums)
                    print(data_Dental)
                    print("\n")
                teeths.clear()

    if not(Add_to_db):
        print("\nTime after secondary teeth:")
    previous_range = math.ceil(max_erupt / 6) + 1

    #no need for min since we are going up to current age
    for monthly_visits in range(previous_range,math.floor(age_in_months/6)+1):
        LoggedDate = add_months(Date_of_birth, monthly_visits * 6)

        # Gums
        Pocket_depth = random.randint(1, 3)  # mm
        Mobility = random.uniform(0.0, 2.5)  # mm
        data_Gums = {
            'P_ID': PersonID,
            'LoggedDate': LoggedDate,
            'Pocket_depths': Pocket_depth,
            'Mobility': Mobility,
        }
        Erupt_rate = 'normal'
        data_Dental = {
            'P_ID': PersonID,
            'LoggedDate': LoggedDate,
            'Num_Teeth': Num_Teeth,
            'Dentition_stage': 'Deciduous',
            'Erupt_rate': Erupt_rate,
            'Occlusion': 'normal',
            'Tooth_color': 'normal',
            'Oral_hygiene': 'good',
            'TMJ': FALSE,
        }
        if (Add_to_db):
             cursor.execute(add_Dental, data_Dental)
             cursor.execute(add_Gums, data_Gums)
        else:
            print(data_Dental)
            print("\n")


    #print("\nAny other dental record:")
    #Not implemented")
    # growth
        #


    if not(Add_to_db):
        print("\nGrowth:")
        print("\nBorn information")

    #baby
    #https://www.healthline.com/health/parenting/average-baby-length#length-chart
    #+ and - x is just to give some height difference between male and female
    sex_height_dif = (49.9-49.1)#Note: might not need occurind to KidsHealth

    #https://www.healthline.com/health/parenting/average-baby-length#length-chart
    if(y_chromsome):
       #if male
       height = random.uniform(45.7+sex_height_dif,60) #cm
       weight = random.uniform(2.26796, 3.62874)#kg
       #https://kidshealth.org/en/parents/grownewborn.html
    else:
       #https://www.healthline.com/health/parenting/average-baby-length#length-chart
       height = random.uniform(45.7,60-sex_height_dif) #cm
       weight = random.uniform(2.26796, 3.62874)

    LoggedDate = Date_of_birth
    data_Growth = {
         'P_ID': PersonID,
         'LoggedDate': LoggedDate,
         'Height': height,
         'Weight': weight,
    }
    if (Add_to_db):
      cursor.execute(add_Growth, data_Growth)
    else:
      print(data_Growth)
      print("\n")

    if not(Add_to_db):
        print("\nGrowth of the first 2 years")
    #Note maybe include premature baby
    #Note maybe include 5 days after birth check up
    #https://www.healthline.com/health/parenting/average-baby-length#length-chart
    #https://www.thebump.com/a/new-baby-doctor-visit-checklist
    #for babies and one year olds
    monthly_check_ups = [1, 2, 4, 6, 9, 12, 15, 18, 24]   #https://www.thebump.com/toddler-month-by-month/18-month-old-month-old
    year_1_height_growth = random.uniform(9.5, 12.5)#girls height average boys at this age
    prev_height_growth_cm_1 = 0#used for math of calcuating height for 1 year olds
    for months in  monthly_check_ups:
        if(months<age_in_months):
            LoggedDate = add_months(Date_of_birth, months)  
            if(0<=months<6):
                #https://kidshealth.org/en/parents/grow13m.html   
                weight = weight +  random.uniform(0.680389,1.13398);
                if(y_chromsome):
                    height= height + random.uniform(2.5+sex_height_dif, 3.8)
                else:
                    height= height + random.uniform(2.5, 3.8-sex_height_dif)
            elif(6<=months<12):
                #https://www.mayoclinic.org/healthy-lifestyle/infant-and-toddler-health/expert-answers/infant-growth/faq-20058037
                weight = weight  + random.uniform(0.085, 0.14)
                if(y_chromsome):
                    height = height + random.uniform(0.5+(sex_height_dif/2), 1.5)#average 1cm per month
                else:
                    height= height + random.uniform(0.5, 1.5-(sex_height_dif/2))
            elif(12<=months<=24):
                #https://kidshealth.org/en/parents/grow12yr.html
                weight = weight  + random.uniform(2.04117, 2.4947623699823) #5 pounds
                height_growth = ((months-12)/12)*(year_1_height_growth-prev_height_growth_cm_1)
                prev_height_growth_cm_1 = prev_height_growth_cm_1 + height_growth
                if(y_chromsome):
                    height = height +  height_growth   #not really needed in if girls are same average height as boys at 2
                else:
                    height = height +  height_growth
            data_Growth = {
                 'P_ID': PersonID,
                 'LoggedDate': LoggedDate,
                 'Height': height,
                 'Weight': weight,
            }
            if (Add_to_db):
              cursor.execute(add_Growth, data_Growth)
            else:
              print(data_Growth)
              print("\n")

    if not(Add_to_db):
        print("\nGrowth from 3 to 12 years")

    #1 appointmet per year
    #https://www.disabled-world.com/calculators-charts/height-weight-teens.php
    for years  in range(3,min(12,math.floor(age_in_months/12)+1)):
        LoggedDate = add_months(Date_of_birth, years*12)
        if(years==3):
          #https://www.stanfordchildrens.org/en/topic/default?id=the-growing-child-3-year-olds-90-P02296
          height = height + random.uniform(5.08, 7.62)  #grow 2-3 inches in 3rd year
          weight = weight + random.uniform(1.81437, 2.72155)   #4-6 pounds
        if(years==4 and years==5):
          #https://kidshealth.org/en/parents/growth-4-to-5.html
          height = height +  random.uniform(5.08, 7.62)  #grow 2-3 inches in 3rd year
          weight = weight + random.uniform(1.81437, 2.26796)   #4-5 pounds
        if(6<= years and years <=12):
          #https://www.beaumont.org/services/childrens/health-safety/your-growing-child-school-age
          height = height +  random.uniform(5.08, 7.62)  #grow 2.5 inches in 3rd year
          weight = weight + random.uniform(2.26796, 3.17515) #5-7 pounds
        data_Growth = {
          'P_ID': PersonID,
          'LoggedDate': LoggedDate,
          'Height': height,
          'Weight': weight,
        }
        if (Add_to_db):
            cursor.execute(add_Growth, data_Growth)
        else:
            print(data_Growth)
            print("\n")
         

    if not(Add_to_db):
        print("\nGrowth of puberty")

    #https://kidshealth.org/en/parents/growth-13-to-18.html
    if(y_chromsome):
        #https://www.healthline.com/health/when-do-boys-stop-growing#growth-and-puberty
        puberity_star_year = random.randint(10,13)
        puberity_end_year =  puberity_star_year + 3
    else:
        puberity_star_year = random.randint(8,12)
        puberity_end_year = puberity_star_year + 3

    for years in range(13,min(puberity_end_year, math.floor(age_in_months/12)+1)):
       LoggedDate = add_months(Date_of_birth, years*12)
       if(y_chromsome):
           #https://www.healthline.com/health/when-do-boys-stop-growing
           height = height + random.uniform(3.81, 8.89) #1.5 to 3.5 inches
           #https://thenourishedchild.com/teenage-weight-gain-what-to-do/
           #Note: these sites slightly contradict each other
           weight = weight + random.uniform(11.339811849084, 15.8757)#30 pounds
       else:
           height = height + random.uniform(2.54, 5.08) #1 to 2 inches
           weight = weight+ random.uniform(4.53592,9.07185)  # 15 pounds
       data_Growth = {                         
         'P_ID': PersonID,
         'LoggedDate': LoggedDate,
         'Height': height,
         'Weight': weight,
       }
       if (Add_to_db):
           cursor.execute(add_Growth, data_Growth)
       else:
           print(data_Growth)
           print("\n")                                 
    #last years of growth
    #kind of to just fix why the average is so low

    star_year = puberity_end_year + 1
    if(y_chromsome):
        puberity_end_year= 20
    else:
        puberity_end_year= 18
    for years in range(star_year, min(puberity_end_year, math.floor(age_in_months/12)+1)):
        LoggedDate = add_months(Date_of_birth, years*12)
        weight = weight + random.uniform(1.13398,2.26796)#1.5 to 5 pounds
        height = height + random.uniform(1.27, 2.54) #0.5 to 1 inches
        data_Growth = {
          'P_ID': PersonID,
          'LoggedDate': LoggedDate,
          'Height': height,
          'Weight': weight,
        }
        if (Add_to_db):
            cursor.execute(add_Growth, data_Growth)
        else:
            print(data_Growth)
            print("\n")
       

    if not(Add_to_db):
        print("\nGrowth after puberty")
    for years in range(puberity_end_year,math.floor(age_in_months/12)+1):
        LoggedDate = add_months(Date_of_birth, years*12)
        weight = weight + (-1*random.randint(0,1))* random.uniform(0,1.13398)#wait change of 2.5 pounds per year
        data_Growth = {
           'P_ID': PersonID,
           'LoggedDate': LoggedDate,
           'Height': height,
           'Weight': weight,
        }
        if (Add_to_db):
            cursor.execute(add_Growth, data_Growth)
        else:
            print(data_Growth)
            print("\n")



    #eyes
    if not(Add_to_db):
        print("\nEyes:")

    perc = random.randint(0,100)
    #https://www.worldatlas.com/articles/which-eye-color-is-the-most-common-in-the-world.html
    if(perc<2):
        Iris = 'Green'
    elif(perc<5):
        Iris = 'Grey'
    elif(perc<10):
        Iris = 'Amber'
    elif(perc<15):
        Iris = 'Hazel'
    elif(perc<15):
        Iris = 'Blue'
    else:
        Iris = 'Brown'
    Sclera = 'White'


    for Gene in  gene_mutation:
        if(Gene == 'COL1A1' or Gene == 'COL1A2'):
            #https://www.rdhmag.com/patient-care/article/16408161/implication-of-brittle-bone-diseases
            #for Col1a1 color of teeth can vary
            perc = random.randint(0,100)
            if(perc<25):
                Sclera = 'Purple'
            elif(perc<25*2):
                Sclera = 'Grey'
            elif(perc<25*3):
                Sclera = 'Blue'
            if not Sclera == 'White':
                perc = random.randint(0, 1)
                if(perc == 1):
                    Serverity = "Noticeable"
                else:
                    Serverity = "Slightly Noticeable"
                data_Diagnose = {
                    'P_ID': PersonID,
                    'C_ID': "C8",
                    'LoggedDate': Date_of_birth,
                    'Degree_of_Severity': Serverity,
                }
                if (Add_to_db):
                    cursor.execute(add_Diagnose, data_Diagnose)
                else:
                    print(data_Diagnose)
                    print("\n")
  
    #exam every 2 years starting at the age of two
    for years in range(2, math.floor(age_in_months/(12*2))):
       LoggedDate = add_months(Date_of_birth, years*12*2)
       data_Eyes = {
           'P_ID': PersonID,
           'LoggedDate': LoggedDate,
           'Iris_R': Iris,
           'Iris_L': Iris,
           'Sclera': Sclera,
       }
       if (Add_to_db):
           cursor.execute(add_Eyes, data_Eyes)
       else:
           print(data_Eyes)
           print("\n")


    #Diagonises
    if not(Add_to_db):
        print("\nAdd Diagonises:")

    perc = random.randint(0,100)
    if(perc < 7):
        perc = random.randint(0, 2)
        if (perc == 0):
            Serverity = 'Small'
        elif (perc == 1):
            Serverity = 'Medium'
        else:
            Serverity = 'Large'
        data_Diagnose = {
            'P_ID': PersonID,
            'C_ID': "C1",
            'LoggedDate': Date_of_birth,
            'Degree_of_Severity': Serverity,
        }
        if (Add_to_db):
            cursor.execute(add_Diagnose, data_Diagnose)
        else:
            print(data_Diagnose)
            print("\n")
    perc = random.randint(0, 100)
    if (perc < 5):
        perc = random.randint(0, 2)
        if (perc == 0):
            Serverity = 'Small'
        elif (perc == 1):
            Serverity = 'Medium'
        else:
            Serverity = 'Large'
        data_Diagnose = {
            'P_ID': PersonID,
            'C_ID': "C2",
            'LoggedDate': Date_of_birth,
            'Degree_of_Severity': Serverity,
        }
        if (Add_to_db):
            cursor.execute(add_Diagnose, data_Diagnose)
        else:
            print(data_Diagnose)
            print("\n")
    perc = random.randint(0, 100)
    #if 40 or older
    if ( age_in_months > 40*12 and perc < 3):
        perc = random.randint(0, 2)
        if (perc == 0):
            Serverity = 'Small'
        elif (perc == 1):
            Serverity = 'Medium'
        else:
            Serverity = 'Large'
        start_date = Date_of_birth + datetime.timedelta(days=(40*365))
        time_between_dates = today - start_date
        days_between_dates = time_between_dates.days
        random_number_of_days = random.randrange(days_between_dates)
        LoggedDate = start_date + datetime.timedelta(days=random_number_of_days)
        data_Diagnose = {
            'P_ID': PersonID,
            'C_ID': "C3",
            'LoggedDate': LoggedDate,
            'Degree_of_Severity': Serverity,
        }
        if (Add_to_db):
            cursor.execute(add_Diagnose, data_Diagnose)
        else:
            print(data_Diagnose)
            print("\n")

    perc = random.randint(0, 100)
    greater_chance = 0
    for Gene in gene_mutation:
        if (Gene == "hemoglobin-Beta"):
            greater_chance = 10
    if (perc < (10+greater_chance)):
        if (perc == 0):
            Serverity = 'Small'
        elif (perc == 1):
            Serverity = 'Medium'
        else:
            Serverity = 'Large'
        start_date = Date_of_birth
        time_between_dates = today - start_date
        days_between_dates = time_between_dates.days
        random_number_of_days = random.randrange(days_between_dates)
        LoggedDate = start_date + datetime.timedelta(days=random_number_of_days)
        data_Diagnose = {
            'P_ID': PersonID,
            'C_ID': "C5",
            'LoggedDate': LoggedDate,
            'Degree_of_Severity': Serverity,
        }
        if (Add_to_db):
            cursor.execute(add_Diagnose, data_Diagnose)
        else:
            print(data_Diagnose)
            print("\n")
    perc = random.randint(0, 100)
    if(perc < 12):
        perc = random.randint(0, 6)
        if (perc == 0):
            Serverity = 'Transverse fracture'
        elif (perc == 1):
            Serverity = 'Oblique fracture'
        elif(perc == 2):
            Serverity = 'Comminuted fracture'
        elif (perc == 3):
            Serverity = 'Greenstick fracture'
        elif (perc == 4):
            Serverity = 'Pathologic fracture'
        else:
            Serverity = 'Stress fracture'
        start_date = Date_of_birth
        time_between_dates = today - start_date
        days_between_dates = time_between_dates.days
        random_number_of_days = random.randrange(days_between_dates)
        LoggedDate = start_date + datetime.timedelta(days=random_number_of_days)
        data_Diagnose = {
            'P_ID': PersonID,
            'C_ID': "C6",
            'LoggedDate': LoggedDate,
            'Degree_of_Severity': Serverity,
        }
        if (Add_to_db):
            cursor.execute(add_Diagnose, data_Diagnose)
        else:
            print(data_Diagnose)
            print("\n")
    perc = random.randint(0, 100)
    if (perc < 6):
        perc = random.randint(0, 2)
        if (perc == 0):
            Serverity = 'Abrasions'
        if (perc == 1):
            Serverity = 'Punctures'
        else:
            Serverity = 'Lacerations'
        start_date = Date_of_birth
        time_between_dates = today - start_date
        days_between_dates = time_between_dates.days
        random_number_of_days = random.randrange(days_between_dates)
        LoggedDate = start_date + datetime.timedelta(days=random_number_of_days)
        data_Diagnose = {
            'P_ID': PersonID,
            'C_ID': "C9",
            'LoggedDate': LoggedDate,
            'Degree_of_Severity': Serverity,
        }
        if (Add_to_db):
            cursor.execute(add_Diagnose, data_Diagnose)
        else:
            print(data_Diagnose)
            print("\n")
    perc = random.randint(0, 100)
    if (perc < 6):
        perc = random.randint(0, 2)
        if (perc == 0):
            Serverity = 'Abrasions'
        if (perc == 1):
            Serverity = 'Punctures'
        else:
            Serverity = 'Lacerations'
        start_date = Date_of_birth
        time_between_dates = today - start_date
        days_between_dates = time_between_dates.days
        random_number_of_days = random.randrange(days_between_dates)
        LoggedDate = start_date + datetime.timedelta(days=random_number_of_days)
        data_Diagnose = {
            'P_ID': PersonID,
            'C_ID': "C10",
            'LoggedDate': LoggedDate,
            'Degree_of_Severity': Serverity,
        }
        if (Add_to_db):
            cursor.execute(add_Diagnose, data_Diagnose)
        else:
            print(data_Diagnose)
            print("\n")

    for Gene in gene_mutation:
        if (Gene == "RUNX2"):
            perc = random.randint(0, 100)
            if(perc < 75):
                perc =random.randint(0, 1)
                if(perc == 1):
                    Serverity = 'Collarbone Deformed'
                else:
                    Serverity = 'Cranium Deformed'
                data_Diagnose = {
                    'P_ID': PersonID,
                    'C_ID': "C11",
                    'LoggedDate': Date_of_birth,
                    'Degree_of_Severity':Serverity,
                }
                if (Add_to_db):
                    cursor.execute(add_Diagnose, data_Diagnose)
                else:
                    print(data_Diagnose)
                    print("\n")
    perc = random.randint(0, 100)
    #if 40 or older
    if ( age_in_months > 40*12 and perc < 3):
        perc = random.randint(0, 100)
        if(perc < 10):
            Serverity = "Stage 4"
        elif(perc < 30):
            Serverity = "Stage 3"
        elif (perc < 60):
            Serverity = "Stage 2"
        else:
            Serverity = "Stage 1"
        start_date = Date_of_birth + datetime.timedelta(days=(40 * 365))
        time_between_dates = today - start_date
        days_between_dates = time_between_dates.days
        random_number_of_days = random.randrange(days_between_dates)
        LoggedDate = start_date + datetime.timedelta(days=random_number_of_days)
        data_Diagnose = {
            'P_ID': PersonID,
            'C_ID': "C12",
            'LoggedDate': LoggedDate,
            'Degree_of_Severity': Serverity,
        }
        if (Add_to_db):
            cursor.execute(add_Diagnose, data_Diagnose)
        else:
            print(data_Diagnose)
            print("\n")
    greater_chance = 0
    for Gene in gene_mutation:
        if (Gene == "APC"):
            greater_chance = 20
    perc = random.randint(0, 100)
    if (perc < 6+greater_chance):
        perc = random.randint(0, 2)
        if(perc == 1):
            Serverity = "Problamtic"
        elif(perc == 1):
            Serverity = "Lockjaw"
        else:
            Serverity = "Not Problamtic"
        start_date = Date_of_birth
        time_between_dates = today - start_date
        days_between_dates = time_between_dates.days
        random_number_of_days = random.randrange(days_between_dates)
        LoggedDate = start_date + datetime.timedelta(days=random_number_of_days)
        data_Diagnose = {
            'P_ID': PersonID,
            'C_ID': "C14",
            'LoggedDate': LoggedDate,
            'Degree_of_Severity': Serverity,
        }
        if (Add_to_db):
            cursor.execute(add_Diagnose, data_Diagnose)
        else:
            print(data_Diagnose)
            print("\n")

if (Add_to_db):
    cnx.commit()
    cursor.close()
    cnx.close()