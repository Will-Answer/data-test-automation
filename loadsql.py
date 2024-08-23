#loadsql.py - if run as main reads the template and response files 
#Template is a dictionary where the keys are the question numbers and values are the queries that produce correct answers
#Responses is a dictionary of dictionaries where each key is a candidate's answer folder, then the values mimic the template dictionary

import os
from dotenv import load_dotenv

log=open('log.txt','a')

load_dotenv()
def extract(dir):
    """Reads a directory for .sql files and returns their contents  
    
    ### Parameters:
      dir - the directory that files should be extracted from 

    ### Returns:
    Dict  
      -Keys are the file names  
      -Values are lists  
        -First item in list is a list of comments in the file  
        -Second item in list is a list of queries in the file
    """
    try:
        os.chdir(dir)
        contents = {}

        for file in os.listdir():
            commlines =[]
            querlines = []
            if file.endswith('.sql'): #only recognises .sql files
                filename = file.replace('.sql','')

                for line in open(file): #reads files, adds comments to the comment list and queries to the query list
                    if not line.startswith('--'):
                        querlines.append(line.strip())
                    elif line.isspace():
                        pass
                    else:
                        commlines.append(line.strip())
                queries = (" ".join(querlines)).split(";")

                for iter in range(len(queries)): #parses the queries
                    if not queries[iter] == '':
                        queries[iter] = queries[iter].strip() + ';'
                    else:
                        queries.remove('')
                contents[filename] = queries
        return contents #returns dictionary with its value as a list containing a list of comment lines and list of queries
    except BaseException as err:
        print(f'SQL Load Crash\nError: {err}\n--------------',file=log)
        raise Exception

def get_template():
    """Gets the template solutions as a dictionary

    ### Returns:  
    Dict {'question number' : [queries]}
    """
    return extract(os.getenv('template'))

def get_responses():
    """Gets all candidate responses as a dictionary containing dictionaries

    ### Returns:  
    Dict {'candidate name': {  
        'question number' : [queries]}  
    }
    """
    rsp_dirs = os.listdir(os.getenv('responses'))
    responses = {}
    for dir in rsp_dirs:
        responses[dir] = extract(f'{os.getenv('responses')}\\{dir}')
    return responses

if __name__ == '__main__':
    print(get_responses()['will_pinder']['2'])