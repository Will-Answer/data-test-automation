import dbconnect as dbc
import loadsql as load
import pandas as pd
import decimal
from dotenv import load_dotenv
import sys
import json
import os
from datetime import datetime

#open logs and database
db = dbc.Database()
with open('settings.json') as settingsjson:
    settings = json.load(settingsjson)
load_dotenv()
info = load.get_info()
name = info.readline().strip()

def queryall(questions,type='t',candidate='tester'):
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
    db.rollback() #ensure the database is in its default state
    for qnum in questions:
        try:
            response = db.query(questions[qnum])
            for item in response:
                processed[qnum] = pd.DataFrame(item)
        except BaseException as err:
            if type == "t":
                print(f'Error loading templates\nError: {err}\n---------------',file=log,flush=True)
                sys.exit()
            elif type == "r":
                print(f'Candidate: {candidate}\nQuestion: {qnum}\nError: {err}\n---------------',file=log,flush=True)
                processed[qnum] = 'Err'
                db.rollback() #rolls back so subsequent blocks can execute
    return processed

def mark(template,responses,ordered=[]):
    """Compares template answers to responses, using a list to determine questions that require order.
    Incorrect responses fetch the SQL query from its file and errors in execution are reported in log.txt.

    ### Parameters:
    - template (dict) - the template responses as a dictionary of pandas dataframes
    - responses (dict) - the response dictionary of all of the canditates
    - ordered (list) - a list of the questions that should be ordered
    """
    scores = {'name':['Total'],'score':[len(template)]} #used to track candidate scores
    candnum = 0 #used to track position in the lists
    for candidate in responses:
        candnum += 1
        scores['name'].append(candidate)
        scores['score'].append(0)

        for qnum in responses[candidate]:
            res_table = responses[candidate][qnum]
            temp_table = template[qnum]

            if type(res_table) == str: #error output
                if res_table == 'Err':
                    print(f'Candidate: {candidate}\nQuestion: {qnum}\nError, see log\n------------',file=mistakes,flush=True)

            elif res_table.size == 1: #handles single value outputs
                if res_table.values == temp_table.values:
                    scores['score'][candnum] += 1
                else:
                    incorrect(candidate,qnum,res_table,temp_table)
            
            elif len(res_table) == 1: #handles single row outputs
                if comparerow(temp_table[:],res_table[:]):
                    scores['score'][candnum] += 1
                else:
                    incorrect(candidate,qnum,res_table,temp_table)
            
            elif int(qnum) in ordered: #handles multi-row ordered outputs
                if res_table.shape[0] == temp_table.shape[0]:
                    if comparerows(temp_table,res_table):
                        scores['score'][candnum] += 1
                    else:
                        incorrect(candidate,qnum,res_table,temp_table)
                else:
                    incorrect(candidate,qnum,res_table,temp_table)
            
            else: #handles multi-row unordered outputs. compares each response row to the rows in template
                if res_table.shape[0] == temp_table.shape[0]:
                    equivalent = True
                    temp_dupe = temp_table[::1]
                    res_dupe = temp_dupe[::1]
                    for a in range(len(res_table.index)):
                        found = False
                        for b in range(len(temp_table.index)):
                            try:
                                if comparerow(temp_dupe[b:b+1],res_dupe[a:a+1]): #if a match is found, delete that row and go to the next row in response
                                    found = True
                                    break
                            except IndexError: #if no matching row is found, loop breaks and q is marked as incorrect 
                                break
                        if not found:
                            equivalent = False
                            break
                    if equivalent:
                        scores['score'][candnum] += 1
                    else:
                        incorrect(candidate,qnum,res_table,temp_table)
                else:
                    incorrect(candidate,qnum,res_table,temp_table)
    scoresframe = pd.DataFrame(scores)
    scoresframe=scoresframe.sort_values(by=['score'],ascending=False)
    return scoresframe

def comparerow(temp_row,res_row):
    '''Compares a template row of a dataframe to a response'''
    temp = scrub(temp_row.values.flatten().tolist())
    res = scrub(res_row.values.flatten().tolist())
    try:
        for item in temp:
            res.remove(item)
        return True
    except ValueError:
        return False
    
def scrub(lst):
    for i in range(len(lst)):
        cls = type(lst[i])
        if cls == str:
            lst[i] = lst[i].strip()
            if lst[i].isnumeric():
                lst[i] = int(lst[i])
        elif cls == decimal.Decimal:
            lst[i] = float(lst[i])
            lst[i] = f'{lst[i]}'.split('.')
            lst[i][1] = lst[i][1][:4]
            lst[i] = '.'.join(lst[i])
            lst[i] = float(lst[i])
            try:
                lst[i] = int(lst[i])
            except TypeError:
                pass
    return lst

def comparerows(temp_table,res_table):
    '''Iterated comparerow() functions, taking a whole table instead of a single row'''
    comps = []
    for i in range(len(list(res_table.index))):
        try:
            comps.append(comparerow(temp_table[i:i+1],res_table[i:i+1]))
        except IndexError:
            return False
    if False in comps:
        return False
    else:
        return True

def incorrect(candidate,qnum,table,correct):
    '''Outputs candidate name, question number and SQL query to mistakes file'''
    queryfile = open(f'{os.getenv('responses')}\\{candidate}\\{qnum}.sql')
    querylines = ''
    for line in queryfile:
        querylines += line
    print(f'Candidate: {candidate}\nQuestion: {qnum}\nQuery:\n{querylines}\nOutput:\n{table}\n\nCorrect answer:\n{correct}\n--------------\n',file=mistakes,flush=True)
    queryfile.close()
                    
def main(now):
    global log
    global mistakes
    global scorecard
    if 'results' not in os.listdir():
        os.mkdir('results')
    dir = f'results/{name}_{now}'
    if f'{name}_{now}' not in os.listdir('results'):
        os.mkdir(dir)
    log = open(f'{dir}/log.txt','w')
    scorecard = open(f'{dir}/scorecard.txt','w')
    mistakes = open(f'{dir}/mistakes.txt','w')
    infonew = open(f'{dir}/info.txt','w')
    for line in info:
        infonew.write(line)
    template = load.get_template() #loads template responses into a dictionary of pandas dataframes (keys are question numbers)
    responses = load.get_responses() #loads responses into a dictionary of dictionaries of pandas dataframes (keys are candidates then quesiton numbers)

    template_proc = queryall(template,'t') #processes template
    response_proc = {}
    for candidate in responses: #processes responses
        response_proc[candidate] = queryall(responses[candidate],'r',candidate)
    print(mark(template_proc,response_proc,settings['requires_order']),file=scorecard,flush=True) #compares templates to responses
    log.close()
    mistakes.close()
    scorecard.close()
    infonew.close()
    return 'Done it :)'
if __name__=='__main__':
    print(main(datetime.now()))
'''for i in template_proc: #prints the processed templates and responses
    print(f'{i})\n{template_proc[i]}\n\n')

print('\n--------------------\n\n')

for i in response_proc:
    print(f'{i}\n------------------\n')
    for table in response_proc[i]:
        print(f'{table})\n{response_proc[i][table]}\n\n')

db.close() #commented out, remove quotes for testing'''