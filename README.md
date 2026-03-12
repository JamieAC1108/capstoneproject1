# DATA DICTIONARY TICKET

### ABOUT THE PROGRAM

This is a program that creates a dash application to navigate the CMCC school database. You'll also need a .env file that contains the valid credentials. It would be in the following format:

    db_host=__HOST__
    db_user=__USERNAME__
    db_pass=__PASSWORD__
    db_port=__PORT___
    db_db=__DATABASE NAME___

### VIRTUAL ENVIRONMENT

The first step is to make sure you're in the guacamole VM for the school. You cannot connect to the schools network if you don't do this. 

1. Open the code in VSCode, or the editor of your choosing. VSCode is what the code was originally written in, so that's most likely the appropraite option.

2. In the Terminal, create the virtual environment with the following command:

    python3 -m venv venv

3. Then, to activate it, do the following command:

    source venv/bin/activate

4. The next step is to install all the appropriate libraries.

The libraries that you need to install:

    pandas 
    psycopg2-binary
    sqlalchemy
    python-dotenv
    dash

5. You'll install them with the following command:

    pip install pandas psycopg2-binary sqlalchemy python-dotenv dash

6. You should be all set to go at this point!

