import dbconnect as dbc
import loadsql as load
import pandas as pd
import sys

log = open('log.txt','a') #opens crashlog and database
db = dbc.Database()

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
    return processed


template = load.get_template() #loads template responses into a dictionary of pandas dataframes (keys are question numbers)
responses = load.get_responses() #loads responses into a dictionary of dictionaries of pandas dataframes (keys are candidates then quesiton numbers)

template_proc = queryall(template,'t') #processes template
response_proc = {}
for candidate in responses: #processes responses
    response_proc[candidate] = queryall(responses[candidate],'r',candidate)

for i in template_proc: #prints the processed templates and responses
    print(f'{i})\n{template_proc[i]}\n\n')

print('\n--------------------\n\n')

for i in response_proc:
    print(f'{i}\n------------------\n')
    for table in response_proc[i]:
        print(f'{table})\n{response_proc[i][table]}\n\n')

db.close()