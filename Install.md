# Installation Guide for Shorten Urls Service

### Required Software

  - MS SQL 2012+
  - Visual Studio 2017 , you can download it from [Here](https://pages.github.com/).

### Install Steps

  - Download Code from GitHub
  - Create a DB on SQL and run the script src/Shorten.DB/DDL/CREATE SCHEMA AND SPs.sql on it
  - Open the solution src/ShortenUrl.sln 
 - Change the "DefaultConnection" value with your DB details on shortenurl.api/appsettings.json file 
- Run shortenurl.api project


### Endpoints
    Base Url:  https://localhost:[Port]/api/ShortenUrl
    
    