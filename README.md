# Answer Digital Auto Marking for Data Test

## --Setup--
Install PostgreSQL: https://www.postgresql.org/ - remember the database name, username and password you enter
Open "init.cmd" and change the placeholder to the file location of psql_setup.sql
Run init.cmd 
Create file in the same directory as the .py files
Create .env file with variables:
  db_name = [Postgres database name]
  db_user = [Postgres username]
  db_password = [Postgres password]
  template = [Directory of template SQL queries]
  responses = [Directory of test submissions]

## --Troubleshooting--

If init.cmd does not work, check the installation directory of Postgres. You might have to change the path commands.