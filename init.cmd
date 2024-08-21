::Adds psql to path
set PATH=%PATH%;C:\Program Files\PostgreSQL\16\bin
set PATH=%PATH%;C:\Program Files\PostgreSQL\16\lib

::Initialises database
psql -h localhost -U postgres -d postgres -f "[psql_setup.sql location goes here]"