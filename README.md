# Answer Digital Auto Marking for Data Test

## --Setup--
- Install PostgreSQL: https://www.postgresql.org/ - remember the database name, username and password you enter
- Install Python interpreter https://www.python.org/downloads/ - ensure you tick "Add python to PATH"
- Install package dependences (listed in dependencies section)
- Open "init.cmd" and change the placeholder to the file location of psql_setup.sql
- Run init.cmd 
- Create .env file in the same directory as the .py files with variables:
    - db_name = [Postgres database name]
    - db_user = [Postgres username]
    - db_password = [Postgres password]
    - template = [Directory of template SQL queries]
    - responses = [Directory of test submissions]

### Dependencies  
- Pandas (pip install pandas)
- Psycopg2 (pip install psycopg2)
- Python-dotenv (pip install python-dotenv)  

## --How to use--
Create a directory containing model solutions to your questions. These model solutions will be passed to the database to produce an answer set that can be compared against each candidate's results. Each question should have an individual .sql file, with its file name being the question number.  
Edit the "requires_order" tag in settings.json to contain an array with the question numbers that require a specific order. By default, questions are marked without respect to the order of the table in the output, but this tag is passed to marking.py to let it know that those questions should be marked with order taken into consideration.  
Create a directory that will store the candidate files. Each candidate should have their own folder that contains their .sql files. Each question in the responses should also have its own file, with filename [question number].sql, like in the template directory.  
To run, run marking.py as \_\_main\_\_ (ie. run with the python interpreter by double clicking on it or running it in command prompt)
The score of each candidate is written to results/scorecard.txt as a pandas dataframe. Any mistakes are written to results/mistakes.txt for review of the query. Any erroneous queries are output to log.txt for review.

## --Troubleshooting--

If init.cmd does not work, check the installation directory of Postgres. You might have to change the PATH commands. Alternatively, you could manually add it to PATH in the system environment variables if you have admin access, but I don't :(  
If pip doesn't work, make sure it is in PATH in the system environment variables. You can do this through the installer. 
If there are issues regarding INSERT or other non-select commands, the database reverts to its initial state when there is an error and at the start of each candidate's set of queries. This may cause issues if a query fails and other queries are dependent on it executing.  
The way the database reverts is via the SAVEPOINT and ROLLBACK queries. ROLLBACK is unable to revert once COMMIT has been used, which could cause issues when the next candidate is processed. To undo any commits, init.cmd must be rerun.  

## --Thanks--
Thank you to Yamin and Harry for reviewing this project.  
Thank you to everyone at Answer for being so welcoming.  
