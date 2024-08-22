import dbconnect as dbc
import loadsql as load
import pandas as pd

log = open('log.txt','w') #opens crashlog and database
db = dbc.Database()

template = load.get_template() #loads template responses into a dictionary of pandas dataframes (keys are question numbers)
template_proc = {}
for question in template:
    try:
        response = db.query(template[question])
        template_proc[question] = pd.DataFrame(response)
    except BaseException as err:
        print(f'Error loading templates\nError: {err}\n---------------',file=log)

responses = load.get_responses() #loads responses into a dictionary of dictionaries of pandas dataframes (keys are candidates then quesiton numbers)
response_proc = {}
for candidate in responses:
    response_proc[candidate] = {}
    for question in responses[candidate]:
        try:
            response = db.query(responses[candidate][question])
            response_proc[candidate][question] = pd.DataFrame(response)
        except BaseException as err:
            print(f'Candidate: {candidate}\nQuestion: {question}\nError: {err}\n---------------',file=log)

for i in template_proc: #prints the processed templates and responses
    print(f'{template_proc[i]}\n\n')

print('\n--------------------\n\n')

for i in response_proc:
    print(f'{i}\n------------------\n')
    for table in response_proc[i]:
        print(f'{response_proc[i][table]}\n\n')

db.close()