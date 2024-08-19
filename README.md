This document is an academic report submitted by Rohin Mehra for Assignment 1 at Griffith College Dublin, as part of the Big Data Analysis and Management department. 
The report outlines a comprehensive set of functions developed for a Formula One application, built using Google Cloud Datastore and Flask, a web framework.

The application consists of multiple functions that handle various aspects of user and data management:

User Management:

createUserInfo(claims) and retrieveUserInfo(claims) create and retrieve user data from the datastore.
login(), logout(), and root() manage user sessions and authentication.
Driver and Team Management:

Functions like retrieveDriverList(first_name) and retrieveTeamList(name) fetch lists of drivers and teams.
updateDriver() and updateTeam() update existing driver and team information in the datastore.
add_driver() and add_team() add new drivers and teams.
delete_driver() and delete_team() remove drivers and teams from the datastore.
Search and Comparison:

search_driver() and search_team() allow users to search for drivers and teams based on specified criteria.
compare_drivers() and compare_teams() compare statistics of drivers and teams, highlighting differences.
Flask Routes:

Several routes are defined for handling different functionalities such as displaying lists of drivers and teams, searching for them, adding new entries, 
and updating or deleting existing ones.

Each function is carefully explained, detailing the processes involved in interacting with the datastore, handling user sessions, 
and rendering appropriate templates for the web application. 
The report provides a clear understanding of how these functions contribute to the overall functionality of the Formula One application.
