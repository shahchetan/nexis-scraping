# nexis-scraping

This is the data scraping repository for scraping https://www.nexis.com

*Softwares:*
- selenium 
- pandas
- Internet Browser: Google Chrome
- Note for windows, download chromedriver.exe and keep it the src directory for running selenuim.


*Steps for collecting HTML files:*

- Keep all lexis-ids in a text file.
- Generate a config file with name 'config.json' the format as: {username:\<name\>, password: \<password\>}
- This will be used in signing in website.
- Use command python auto.py <file_name>
- All the html files will be generates in html/ folder.

-Ensure all text and json files should be in the same directory as auto.py file.

*Steps for parsing HTML files:*

- Run python process_data.py file
- All the data is processed in 3 files:
  - main.csv: Contains a table with columns as
    - 'Full Name', 'Address', 'County', 'Phone', 'SSN', 'DOB', 'Gender', 'LexID(sm)', 'Email'
  - address.csv: Contains a table with columns as
    - 'LexID(sm)', 'Address', 'Dates', 'Phone No'
  - relative.csv: Contains a table with columns as 
    - 'LexID(sm)', 'Name', 'AlterName', 'SSN', 'DOB'
