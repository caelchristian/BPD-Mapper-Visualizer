Cael Christian
Professor Jackie Horton
Dec, 11, 2022
Final Project


## Getting Started:
- Recommended to create a new venv, activate it and install the requirements into it with
- `python3 -m venv venv`
- linux/mac -> `source venv/bin/activate`, windows -> `venv\Scripts\activate`
- `pip install -r requirements.txt`
- You should now be ready to run the app :)
- `python3 main.py`

For my final project I have decided to create a Burlington Police statistical calculator and web mapper using Flask. The site is styled with bootstrap and utilizes Flask's SQL toolkit and ORM (object-relational mapper), SQLAlchemy to store, modify and fetch database records. Invalid queries and user input have exception handling.

You can insert Records in all tables by:
- creating an account
- submitting an arrest
- submitting an incident
You can also modify existing arrest/incident records as well as delete them. As of now you cannot delete an account using the web app.

You can also query with a statistical operation as well as create a conditional query with a specific column. A conditional query will return record results by default or column results. All of these queries involve a join between incidents and arrests with incident_id.

My initial goal of this project was to allow the user to create plots with incident coordinates, but I had created ambitious goals for myself. I plan on adding to this project in the future. Static plots are displayed if you uncomment show_plots(). 

The SQL queries used to clean the data
```sql
-- Deleting rows that don't share an incident_number
-- Also deletes duplicate entries
DELETE FROM Incidents WHERE incident_number IN
(SELECT Incidents.incident_number 
	FROM Incidents
	LEFT JOIN Arrests 
	ON Incidents.incident_number=Arrests.incident_number 
	WHERE Arrests.incident_number IS NULL);
DELETE FROM Arrests WHERE incident_number IN
(SELECT Arrests.incident_number 
	FROM Arrests
	LEFT JOIN Incidents 
	ON Arrests.incident_number=Incidents.incident_number 
	WHERE Incidents.incident_number IS NULL);
```