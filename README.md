# Uhcapp

## Local Development

        - Clone Repo in virtualenv
    
        - Install requirements

        - Migrate Database

        - Create Super User

        - Start local Server

## Production
        - Edit .env files
        - `docker compose up `

## Available commands
    Add files in directory from base dir using

    `python manage.py load_company -folder_path=[name of folder]`
    

## Available Routes

    Route details can be found on **/api/v1**

### Summary
    **/api/v1/company/search**
    Allowed methods
    *GET*
    
    Params
    company_name : string

    Return 
    list of companies matching company_name


    **/api/v1/company/auto-search**
    Allowed methods
    *GET*
    params 
    q : string

    Return
    List of company names matching q

    **/api/v1/entity/search**
    Allowed methods
    *GET*

    params
    name : string

    Return
    List of companies where the entity type  equals name



    **/api/v1/entity/auto-search**
    Allowed methods
    *GET*
    params 
    q : string

    Return
    List of entity names matching q


    **/api/v1/company/file**
    Allowed Methods
    *POST*
    
    params
    file: file

    Return
    Name of file and accepted status of file
    


## Optional Assets Build
    