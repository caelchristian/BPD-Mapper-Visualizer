Cael Christian
Professor Jackie Horton
Dec, 11, 2022
Final Project

For my final project I have decided to create a Burlington Police statistical calculator and web mapper using Flask. The site is styled with bootstrap and utilizes Flask's SQL toolkit and ORM (object-relational mapper), SQLAlchemy to store, modify and fetch database records. Invalid queries and user input have exception handling.

You can insert Records in all tables by:
- creating an account
- submitting an arrest
- submitting an incident
You can also modify existing arrest/incident records as well as delete them. As of now you cannot delete an account using the web app.

You can also query with a statistical operation as well as create a conditional query with a specific column. A conditional query will return record results by default or column results. All of these queries involve a join between incidents and arrests with incident_id.

My initial goal of this project was to allow the user to create plots with incident coordinates, but I had created ambitious goals for myself. I plan on adding to this project in the future. Static plots are displayed on the home page of the app.


All call types:
- 911 Hangup
- Airport - AOA Perimeter Check
- Airport - Alarm
- Airport - Parking
- Airport - TSA Checkpoint Post
- Airport AOA Violation
- Airport Duress Alarm
- Airport LEO Escort
- Airport Taxi Inspection
- Alarm
- Alcohol Offense
- Animal Problem
- Animals
- Arrest on Warrant
- Arson
- Assault - Aggravated
- Assault - Simple
- Assist - Agency
- Assist - Car Seat Inspection
- Assist - K9
- Assist - Motorist
- Assist - Other
- Assist - Public
- Background Investigation
- Bad Check
- Bar / Liquor License Violation
- Bomb Threat
- Burglary
- CHINS
- COVID-19 Compliance Check
- Community Outreach
- Compliance Check
- Computer Crime
- Contributing to Deliquency of Minor
- Counterfeiting
- Crash - Fatality
- Crash - Injury to person(s)
- Crash - LSA
- Crash - Non-Investigated
- Crash - Property damage only
- Cruelty to Animals
- Cruelty to a Child
- Custodial Interference
- DLS
- DUI
- Disorderly Conduct
- Disorderly Conduct by Electronic Communication
- Disturbance
- Domestic Assault - Felony
- Domestic Assault - Misd
- Domestic Disturbance
- Drugs
- Drugs - Possession
- Drugs - Sale
- Eluding Police
- Embezzlement
- Enabling Consumption by Minors
- Encampment Outreach
- Encampment Policy
- Escape
- Extortion
- False Info to Police
- False Pretenses
- False Public Alarms
- False Swearing
- Fireworks
- Foot Patrol
- Forgery
- Found/Lost Property
- Fraud
- Fugitive From Justice
- Graffiti Removal
- Hindering Arrest
- Homicide
- Identity Theft
- Illegal Dumping
- Impeding a Public Officer
- Impersonation of a Police Officer
- Inciting a Felony
- Intoxication
- Investigation - Cold Case
- Juvenile Problem
- Kidnapping
- Larceny - Other
- Larceny - from Building
- Larceny - from Motor Vehicle
- Larceny from a Person
- Lewd and Lascivious Conduct
- Lockdown Drill
- Mental Health Issue
- Minor in Possession of Alcohol
- Missing Person
- Motor Vehicle Complaint
- Neighbor Dispute
- Noise
- Obstruction of Justice
- Operations
- Ordinance Violation - Other
- Overdose
- Parking
- Possession of Stolen Property
- Prescription Fraud
- Prohibited Acts
- Property Damage
- Reckless Endangerment
- Recovered Property
- Resisting Arrest
- Retail Theft
- Roadway Hazard
- Robbery
- Runaway
- Runaway Apprehension
- SRO Activity
- Search
- Search Warrant
- Service Coordination
- Sex Offender Registry Violation
- Sexual Assault
- Sheltering/Aiding Runaway
- Stalking
- Stolen Vehicle
- Subpoena Service
- Suicide - Attempted
- Suspicious Event
- TRO/FRO Service
- TRO/FRO Violation
- Theft of Rental Property
- Theft of Service
- Threats/Harassment
- Traffic
- Trespass
- UVM Agency Assist
- Unlawful Restraint
- Untimely Death
- Use of Electronic Comm to Lure a Child
- Uttering a Forged Instrument
- VIN verification
- Vandalism
- Vandalism - graffiti
- Violation of Conditions of Release
- Voyeurism
- Weapons Offense
- Welfare Check

Deleting rows that don't share an incident_number
```sql
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