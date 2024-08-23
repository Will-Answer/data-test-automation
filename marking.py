import dbconnect as dbc
import loadsql as load
import pandas as pd
import sys
import json

log = open('log.txt','a') #opens crashlog and database
db = dbc.Database()
with open('settings.json') as settingsjson:
    settings = json.load(settingsjson)

def queryall(queries,type='t',candidate='tester'):
    """Processes a dictionary of queries with keys as quesion numbers into a dictionary of dataframes

    ### Parameters:
    - queries - a dictionary of queries
    - type - 't' or 'r' for template or response, used for error handling
    - candidate - used for error handling when a candidate's query does not execute

    ### Returns:
    Dict of pandas dataframes

    Ceases operation if a template causes an error  
    Outputs the candidate, question and error to log if a response causes an error
    """
    processed = {}
    for query in queries:
        try:
            response = db.query(queries[query])
            processed[query] = pd.DataFrame(response)
        except BaseException as err:
            if type == "t":
                print(f'Error loading templates\nError: {err}\n---------------',file=log)
                sys.exit()
            elif type == "r":
                print(f'Candidate: {candidate}\nQuestion: {query}\nError: {err}\n---------------',file=log)
                processed[query] = 'Err'
                db.close() #reloads connection so subsequent blocks can execute
                db.connect()
    return processed

def mark(template,responses,ordered=[]):
    """Compares template answers to responses, using a list to determine questions that require order.
    Incorrect responses fetch the SQL query from its file and errors in execution are reported in log.txt.

    ### Parameters:
    - template (dict) - the template responses as a dictionary of pandas dataframes
    - responses (dict) - the response dictionary of all of the canditates
    - ordered (list) - a list of the questions that should be ordered
    """
    scores = {'name':['Total'],'score':[len(template)]}
    candnum = 0
    for candidate in responses:
        candnum += 1
        scores['name'].append(candidate)
        scores['score'].append(0)
        for qnum in responses[candidate]:
            restable = responses[candidate][qnum]
            temptable = template[qnum]
            if type(restable) == str:
                if restable == 'Err':
                    pass
            elif restable.size == 1:
                if restable.values == temptable.values:
                    scores['score'][candnum] += 1
                else:
                    pass
    return pd.DataFrame(scores)
                    

template = load.get_template() #loads template responses into a dictionary of pandas dataframes (keys are question numbers)
responses = load.get_responses() #loads responses into a dictionary of dictionaries of pandas dataframes (keys are candidates then quesiton numbers)

template_proc = queryall(template,'t') #processes template
response_proc = {}
for candidate in responses: #processes responses
    response_proc[candidate] = queryall(responses[candidate],'r',candidate)

print(mark(template_proc,response_proc,settings['requires_order']))
'''for i in template_proc: #prints the processed templates and responses
    print(f'{i})\n{template_proc[i]}\n\n')

print('\n--------------------\n\n')

for i in response_proc:
    print(f'{i}\n------------------\n')
    for table in response_proc[i]:
        print(f'{table})\n{response_proc[i][table]}\n\n')

db.close() #commented out, remove quotes for testing'''