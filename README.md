# Answer Digital Auto Marking for Data Test

## Setup
- Install PostgreSQL: https://www.postgresql.org/ - remember the database name, username and password you enter
- Install Python interpreter https://www.python.org/downloads/ - ensure you tick "Add python to PATH"
- Install package dependences (listed in dependencies section) 
- Create .env file in the same directory as the .py files with variables:
    - db_name = [Postgres database name]
    - db_user = [Postgres username]
    - db_password = [Postgres password]
    - template = [Directory of template SQL queries (not html templates)]
    - responses = [Directory of test submissions]  
- Ensure the tags in settings.json are correct
    - "rollback": An array of commands to be passed to the database after it is reset. By default, they are commands resetting the SERIAL datatype sequences to start at the right number.
    - "requires_order": An array of integers which correspond to questions where the order of the output matters

### Notes
By default, psql_setup.sql is populated with a sample game server dataset. If using a different dataset, you will need to provide your own setup file with different CREATE and INSERT commands.

### Dependencies  
- Pandas (pip install pandas)
- Psycopg2 (pip install psycopg2)
- Python-dotenv (pip install python-dotenv)  
- Flask (pip install flask)

## How to Use
Create a directory containing model solutions to your questions. These model solutions will be passed to the database to produce an answer set that can be compared against each candidate's results. Each question should have an individual .sql file, with its file name being the question number.  
  
Add a file called info.txt to the template directory. The first line should be an identifier to label the output directory with, then proceeding lines will be written to an info file in the output directory.   
  
Edit the "requires_order" tag in settings.json to contain an array with the question numbers that require a specific order. By default, questions are marked without respect to the order of the table in the output, but this tag is passed to marking.py to let it know that those questions should be marked with order taken into consideration.  
  
Create a directory that will store the candidate files. Each candidate should have their own folder that contains their .sql files. Each question in the responses should also have its own file, with filename [question number].sql, like in the template directory.  
  
To run, run auto-mark.cmd. This will create the database schema and tables, open up localhost on port 5000 to display the web page, then run the python code.
 
Clicking the button on the web page runs the marking program and redirects to the output page, which will eventually display the results of the most recent operation.

The score of each candidate is also written to results/scorecard.txt as a pandas dataframe. Any mistakes are written to results/mistakes.txt for review of the query. Any erroneous queries are output to results/log.txt for review.

### Notes
The templates folder (containing html files) is where the web pages that flask uses are. This is **not** the folder for template responses.  

Only include the essential columns to the template queries. The program checks that each row of the response contains the elements of the template, but ignores any extras. Unnescessary columns in the templates will mean responses may be erroneously marked incorrectly.

## Troubleshooting

If auto-mark.cmd does not work, check the installation directory of Postgres. You might have to change the PATH commands. Alternatively, you could manually add it to PATH in the system environment variables if you have admin access. Another possible issue is that your database and username are also not 'postgres'. This can be changed after the -U (user) and -d (database) flags.  
   
If pip doesn't work, make sure python is in PATH in the system environment variables. You can do this through the python installer. 
   
If there are issues regarding INSERT or other non-select commands, the database reverts to its initial state when there is an error and at the start of each candidate's set of queries. This may cause issues if a query fails and other queries are dependent on it executing.  
   
The way the database reverts is via the SAVEPOINT and ROLLBACK queries. ROLLBACK is unable to revert once COMMIT has been used, which could cause issues when the next candidate is processed. To undo any commits, the app must be rerun.  

## Thanks
Thank you to Yamin and Harry for reviewing this project.  
Thank you to everyone at Answer for being so welcoming.  
