Cael Christian
Professor Jackie Horton
Dec, 11, 2022
Final Project

For my final project I have decided to create a Burlington Police statistical calculator and web mapper using Flask. The site is styled with bootstrap and utilizes Flask's SQL toolkit and ORM (object-relational mapper), SQLAlchemy to store, modify and fetch database records.
It's also protected from SQL injections.
Passwords are salted and hashed with 100,000 iterations of Sha-1.


Modify Records Page should allow user to add, remove, and modify police records from all tables.
Statstics Page should let user choose numerical columns for finding mean, min, max, median, standard deviation mean, on numerical columns. 
c) Allow user to query against any column using WHERE and list sample data. 
d) Allow for 2 queries that require a JOIN. 
e) Allow visualizations for key metrics of your choice with at least two different types of plots.



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