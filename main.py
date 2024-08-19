import datetime  # this is the library we will use to get the current time.
import os  # this is the library we will use to access environment variables.
from typing import Optional  # this is the library we will use to define optional parameters.
import flask  # this is the library we will use to create the web app.
from flask import redirect, Response, render_template, request, flash, Flask
# this is the library we will use to create the web app.
from google.cloud import datastore, storage  # this is the library we will use to access the datastore.
import google.oauth2.id_token  # this is the library we will use to authenticate users.
from google.auth.transport import requests  # this is the library we will use to authenticate users.
import local_constants  # this is the library we will use to store local constants.

app: Flask = flask.Flask(__name__)  # create the web app.

# get access to the datastore client, so we can add and store data in the datastore
datastore_client = datastore.Client()

# get access to a request adapter for firebase as we will need this to authenticate users
firebase_request_adapter = requests.Request()  # this is the request adapter for firebase


# get access to the storage client, so we can add and store data in the storage.

def createUserInfo(claims):  # this function creates the user info in the datastore.
    entity_key = datastore_client.key('UserInfo', claims['email'])  # this is the key of the child object.
    entity = datastore.Entity(key=entity_key)  # this is the entity object.
    entity.update({  # this is the data we want to store.
        'email': claims['email'],  # this is the email of the user.
        'name': claims['name'],  # this is the name of the user.
    })
    datastore_client.put(entity)  # store the entity object in the datastore.


def retrieveUserInfo(claims):
    entity_key = datastore_client.key('UserInfo', claims['email'])  # create a key for the user info.
    user_info = datastore_client.get(entity_key)  # get the user info from the datastore.
    return user_info  # return the user info.


def retrieveDriverList(first_name):  # this function retrieves the list of drivers.
    datastore_client.key('team')  # get the key of the driver.
    datastore.Entity(key=entity_key)  # get the driver from the datastore.
    query = datastore_client.query(kind='driver')  # create a query for the 'Team' entity kind
    query.add_filter('first_name', '=', first_name)  # filter by 'name' property equal to given name
    driver_list = list(query.fetch())  # retrieve teams matching the query
    return driver_list  # return the list of teams


def retrieveTeamList(name):
    datastore_client.key('team')  # get the key of the driver.
    datastore.Entity(key=entity_key)  # get the driver from the datastore.
    query = datastore_client.query(kind='team')  # create a query for the 'Team' entity kind
    query.add_filter('name', '=', name)  # filter by 'name' property equal to given name
    team_list = list(query.fetch())  # retrieve teams matching the query
    return team_list  # return the list of teams


def updateDriver(first_name, last_name, nationality, number, wins, age):  # this function updates the
    entity_key = datastore_client.key('driver')  # get the key of the driver.
    user_info = datastore.Entity(key=entity_key)  # get the driver from the datastore.
    drivers_list = user_info['drivers_list']  # get the list of drivers from the user's info.
    drivers_list.append(first_name)  # add the driver id to the list of drivers.
    drivers_list.append(last_name)  # add the driver first name to the list of drivers.
    drivers_list.append(nationality)  # add the driver last name to the list of drivers.
    drivers_list.append(birth_date)  # add the driver birth date to the list of drivers.
    drivers_list.append(team_id)  # add the driver team id to the list of drivers.
    drivers_list.append(number)  # add the driver number to the list of drivers.
    drivers_list.append(wins)  # add the driver wins to the list of drivers.
    drivers_list.append(age)  # add the driver age to the list of drivers.
    user_info.update({
        'drivers_list': drivers_list  # update the user's info with the new list of drivers.
    })
    datastore_client.put(entity)  # store the driver in the datastore.


def updateTeam(name, year_founded, race_wins, world_titles, team_principal, team_base, championships):
    # function updates the information of a team.
    entity_key = datastore_client.key('team')  # get the key of the team.
    user_info = datastore_client.get(entity_key)  # get the team from the datastore.
    teams_list = user_info.get('teams_list', [])  # get the list of teams from the user's info or an empty list.
    teams_list.append(name)  # add the team name to the list of teams.
    teams_list.append(year_founded)  # add the team year_founded to the list of teams.
    teams_list.append(race_wins)  # add the team race_wins to the list of teams.
    teams_list.append(world_titles)  # add the team world_titles to the list of teams.
    teams_list.append(team_principal)  # add the team team_principal to the list of teams.
    teams_list.append(team_base)  # add the team team_base to the list of teams.
    teams_list.append(championships)  # add the team championships to the list of teams.
    user_info.update({
        'teams_list': teams_list  # update the user's info with the new list of teams.
    })
    datastore_client.put(user_info)  # store the updated user info in the datastore.


def search_driver(first_name, last_name, age, points):  # this function searches for a driver.
    query = datastore_client.query(kind='driver')  # create a query for the 'driver' entity kind
    if not first_name and not last_name and not age and not points:
        # if the user did not enter any search criteria.
        return redirect('/')  # redirect the user to the home page.
    if first_name:
        query.add_filter('first_name', '=', first_name)  # filter by 'first_name' property equal to given first_name
    if last_name:
        query.add_filter('last_name', '=', last_name)  # filter by 'last_name' property equal to given last_name
    if age:
        query.add_filter('age', '=', age)  # filter by 'age' property equal to given age
    if points:
        query.add_filter('points', '=', points)  # filter by 'points' property equal to given points
    results = query.fetch()  # retrieve drivers matching the query
    return results


def search_team(team_name):
    team_key = datastore_client.key('team', team_name)  # get the key of the team.
    team = datastore_client.get(team_key)  # get the team from the datastore.
    if team is None:  # if the team is not found.
        return redirect('/')  # Redirect to the home page if the team is not found.
    return team  # return the team.


def add_driver(user_info, first_name, last_name, nationality, birth_date, team_id, number, wins, age):
    # get the list of drivers from the user's info
    drivers_list = user_info.get('drivers_list', [])
    # create a new driver entity and add it to the list of drivers
    driver = {
        'first_name': first_name,
        'last_name': last_name,
        'nationality': nationality,
        'birth_date': birth_date,
        'team_id': team_id,
        'number': number,
        'wins': wins,
        'age': age
    }
    drivers_list.append(driver)
    # update the user's info with the new list of drivers
    user_info.update({'drivers_list': drivers_list})
    # store the user's info in the datastore
    datastore_client.put(user_info)


def add_team(user_info, name, year_founded, race_wins, world_titles, team_principal, team_base, championships):
    # get the list of teams from the user's info
    teams_list = user_info.get('teams_list', [])
    # create a new team entity and add it to the list of teams
    team = {
        'name': name,
        'year_founded': year_founded,
        'race_wins': race_wins,
        'world_titles': world_titles,
        'team_principal': team_principal,
        'team_base': team_base,
        'championships': championships
    }
    teams_list.append(team)
    # update the user's info with the new list of teams
    user_info.update({'teams_list': teams_list})
    # store the user's info in the datastore
    datastore_client.put(user_info)


def delete_driver(user_info, first_name):
    # get the list of drivers from the user's info
    drivers_list = user_info.get('drivers_list', [])
    for index, driver in enumerate(drivers_list):
        if driver['first_name'] == first_name:
            # get the key of the driver to delete
            driver_key = datastore_client.key('Drivers', driver.key.id_or_name)
            # delete the driver
            datastore_client.delete(driver_key)
            # remove the driver from the list of drivers
            del drivers_list[index]
            break
    # update the user's info with the new list of drivers
    user_info.update({'drivers_list': drivers_list})
    # store the user's info in the datastore
    datastore_client.put(user_info)


def delete_team(name):  # this function deletes a team from the user's list of teams.
    datastore.Entity(key=entity_key)  # get the driver from the datastore.
    user_info = retrieveUserInfo(name)  # retrieve the user's info.
    teams_list = user_info['teams_list']  # get the list of teams from the user's info.
    name = None

    for index, idx in enumerate(teams_list):  # loop through the list of teams.
        if teams_list[index] == id:  # if the team id matches the id of the team to delete.
            name = index
    team_keys = datastore_client.key('Teams', teams_list[name])  # get the key of the team to delete.
    datastore_client.delete(team_keys)  # delete the team.
    del teams_list[name]  # delete the team id from the list of teams.
    user_info.update({
        'teams_list': teams_list  # update the user's info with the new list of teams.
    })
    datastore_client.put(user_info)  # put the user's info back into the database.


def compare_drivers(driver1, driver2):
    stats = ['wins', 'age']  # the stats to compare.
    comparison = []  # the list of tuples to return.
    for stat in stats:
        val1 = driver1.get(stat, 0)  # get the value of the stat for driver1.
        val2 = driver2.get(stat, 0)  # get the value of the stat for driver2.
        if val1 > val2:
            comparison.append((stat, val1, 'green'))  # if driver1 has a higher value, append a tuple with the stat
            # name, driver1's value, and the color green.
        else:
            comparison.append((stat, val2, 'green'))  # if driver2 has a higher value, append a tuple with the stat
            # name, driver2's value, and the color green.
    return comparison  # return the list of tuples.


def compare_teams(race_wins, world_titles):
    # this function compares two teams and returns a list of tuples.
    datastore_client.key('Teams', teams_list[team_id])  # get the key of the team to compare.
    datastore.Entity(key=entity_key)  # get the driver from the datastore.
    stats = ['race_wins', 'world_titles']  # the stats to compare.
    comparison = []  # the list of tuples to return.
    for stat in stats:
        val1 = year.get(stat, race_wins)  # get the value of the stat for team1.
        val2 = team_principal.get(stat, world_titles)  # get the value of the stat for team2.
        if val1 > val2:
            comparison.append((stat, val1, 'green'))  # if team1 has a higher value, append a tuple with the stat
            # name, team1's value, and the color green.
        else:
            comparison.append((stat, val2, 'green'))  # if team2 has a higher value, append a tuple with the stat
            # name, team2's value, and the color green.

    # compare team principal and team base
    if team1.get('race_wins', '') >= team2.get('race_wins', ''):  # if the team principals are the same.
        comparison.append(('race_wins', team1.get('race_wins', ''), 'green'))  # append a tuple with the stat
    else:
        comparison.append(
            ('world_titles', team2.get('world_titles', ''), 'red'))  # name, team1's value, and the color green.

    if team1.get('world_titles') >= team2.get('world_titles'):  # if the team bases are the same.
        comparison.append(('world_titles', team1.get('world_titles', ''),
                           'green'))  # append a tuple with the stat name, team1's value, and the color green.
    else:
        comparison.append(('race_wins', team2.get('race_wins', ''),
                           'red'))  # append a tuple with the stat name, team2's value, and the color red.

    return comparison_team  # return the list of tuples.


@app.route('/login', methods=['GET', 'POST'])  # this is the route for the login page.
def login():
    error = None
    if request.method == 'POST':  # if the user is trying to log in.
        username = request.form['username']  # get the username from the form.
        password = request.form['password']  # get the password from the form.
        if username != 'admin' or password != 'admin':  # if the username or password is incorrect.
            error = 'Invalid credentials. Please try again.'  # set the error message.
        else:
            session['logged_in'] = True  # set the session variable.
            flash('You were logged in')  # display a flash message.
            return redirect(url_for('index'))  # redirect to the index page.
    return render_template('index.html', error=error)  # render the login page.


@app.route('/logout')  # this is the route for the logout page.
def logout():
    session.pop('logged_in', None)  # remove the session variable.
    flash('You were logged out')  # display a flash message.
    return redirect(url_for('index'))  # redirect to the index page.


@app.route('/')  # this is the route for the home page.
def root():  # this is the function that handles the home page.
    id_token = request.cookies.get("token")  # get the token from the cookies.
    error_message = None  # this is the error message.
    claims = None  # this is the claims object.
    if id_token:  # if the token exists, it means that the user is logged in.
        try:  # try to authenticate the user.
            claims = google.oauth2.id_token.verify_firebase_token(id_token, firebase_request_adapter)  # this is the
            # claims object.
            user_info = retrieveUserInfo(claims)  # retrieve the user info from the datastore.
            if user_info is None:  # if the user info does not exist, it means that the user is logging in for the first
                createUserInfo(claims)  # create the user info in the datastore.
                retrieveUserInfo(claims)  # retrieve the user info from the datastore.
        except ValueError as exc:  # if the token is invalid, show an error message.
            error_message = exc  # set the error message.
    return render_template('index.html', user_data=claims, error_message=error_message)  # render the home page.


@app.route('/list_teams', methods=['GET', 'POST'])
def retrieveTeamList():
    id_token = request.cookies.get("token")  # get the token from the cookies.
    error_message = None  # this is the error message.
    claims = None  # this is the claims object.
    if id_token:  # if the token exists, it means that the user is logged in.
        try:  # try to authenticate the user.
            claims = google.oauth2.id_token.verify_firebase_token(id_token, firebase_request_adapter)  # this is the
            # claims object.
            if 'name' in claims and 'email' in claims:  # Check if the necessary keys are present in claims
                user_info = retrieveUserInfo(claims)  # retrieve the user info from the datastore.
                if user_info is None:  # if the user info does not exist, it means that the user is logging in for
                    # the first time
                    createUserInfo(claims)  # create the user info in the datastore.
                    retrieveUserInfo(claims)  # retrieve the user info from the datastore.
                    retrieveTeamList(claims)
            else:
                error_message = "Missing user information"
        except ValueError as exc:  # if the token is invalid, show an error message.
            error_message = exc  # set the error message.

    return render_template('list_teams.html', error_message=error_message, claims=claims)


@app.route('/list_driver', methods=['GET', 'POST'])
def retrieveDriverList():
    id_token = request.cookies.get("token")  # get the token from the cookies.
    error_message = None  # this is the error message.
    claims = None  # this is the claims object.
    if id_token:  # if the token exists, it means that the user is logged in.
        try:  # try to authenticate the user.
            claims = google.oauth2.id_token.verify_firebase_token(id_token, firebase_request_adapter)  # this is the
            # claims object.
            if 'name' in claims and 'email' in claims:  # Check if the necessary keys are present in claims
                user_info = retrieveUserInfo(claims)  # retrieve the user info from the datastore.
                if user_info is None:  # if the user info does not exist, it means that the user is logging in for
                    # the first time
                    createUserInfo(claims)  # create the user info in the datastore.
                    retrieveUserInfo(claims)  # retrieve the user info from the datastore.
                    retrieveDriverList(claims)  # retrieve the driver's list from the datastore.
            else:
                error_message = "Missing user information"
        except ValueError as exc:  # if the token is invalid, show an error message.
            error_message = exc  # set the error message.

    return render_template('list_drivers.html', error_message=error_message, claims=claims)


# initiation of the CURD operations.
@app.route('/driver_results', methods=['GET', 'POST'])  # this is
# the route for the
# search driver page.
def SearchDriver():  # this is the function that handles the search driver page.
    id_token = request.cookies.get("token")  # get the token from the cookies.
    error_message = None  # this is the error message.
    claims = None  # this is the claims object.
    if id_token:  # if the token exists, it means that the user is logged in.
        try:  # try to authenticate the user.
            claims = google.oauth2.id_token.verify_firebase_token(id_token, firebase_request_adapter)  # this is the
            # claims object.
            if 'name' in claims and 'email' in claims:  # Check if the necessary keys are present in claims
                user_info = retrieveUserInfo(claims)  # retrieve the user info from the datastore.
                if user_info is None:  # if the user info does not exist, it means that the user is logging in for
                    # the first time
                    createUserInfo(claims)  # create the user info in the datastore.
                    retrieveUserInfo(claims)  # retrieve the user info from the datastore.
                    searchDriver(claims)  # search the datastore for the drivers.
                    error_message = None
            else:
                error_message = "Missing user information"
        except ValueError as exc:  # if the token is invalid, show an error message.
            error_message = exc  # set the error message.
    return render_template('driver_results.html', error_message=error_message,
                           claims=claims)  # render the driver results


@app.route('/team_results', methods=['GET', 'POST'])  # this is the
# route for the search team page.
def SearchTeam():
    id_token = request.cookies.get("token")  # get the token from the cookies.
    error_message = None  # this is the error message.
    if id_token:  # if the token exists, it means that the user is logged in.
        try:  # try to authenticate the user.
            claims = google.oauth2.id_token.verify_firebase_token(id_token, firebase_request_adapter)  # this is the
            # claims object.
            if 'name' in claims:  # Check if the necessary keys are present in claims
                retrieveUserInfo(claims)  # retrieve the user info from the datastore.
            else:
                error_message = "Missing user information"
        except ValueError as exc:  # if the token is invalid, show an error message.
            error_message = exc  # set the error message.

        return render_template('team_results.html', error_message=error_message)  # render the team results.


@app.route('/add_driver', methods=['GET', 'POST'])  # this is the route for the add
def add_driver():  # this is the function
    error_message = None  # this is the error message.
    id_token = request.cookies.get("token")  # get the token from the cookies.
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    nationality = request.form['nationality']
    number = request.form['number']
    wins = request.form['wins']
    age = request.form['age']
    if id_token:  # if the token exists, it means that the user is logged in.
        try:  # try to authenticate the user.
            claims = google.oauth2.id_token.verify_firebase_token(id_token, firebase_request_adapter)  # this is the
            # claims object.
            if 'name' in claims and 'email' in claims:  # Check if the necessary keys are present in claims
                user_info = retrieveUserInfo(claims)  # retrieve the user info from the datastore.
                if user_info is None:  # if the user info does not exist, it means that the user is logging in for
                    # the first time
                    createUserInfo(claims)  # create the user info in the datastore.
                    retrieveUserInfo(claims)  # retrieve the user info from the datastore.
                    add_driver(first_name, last_name, nationality, number, wins, age)  # add the driver to the user.
            else:
                error_message = "Missing user information"
        except ValueError as exc:  # if the token is invalid, show an error message.
            error_message = exc  # set the error message.

    return render_template('add_driver.html', error_message=error_message)  # return the add driver page.


@app.route('/add_team', methods=['GET', 'POST'])  # this is the route for the add team page.
def add_team():
    error_message = None  # this is the error message.
    id_token = request.cookies.get("token")  # get the token from the cookies.
    if id_token:  # if the token exists, it means that the user is logged in.
        try:  # try to authenticate the user.
            claims = google.oauth2.id_token.verify_firebase_token(id_token, firebase_request_adapter)  # this is the
            # claims object.
            if 'name' in claims and 'email' in claims:  # Check if the necessary keys are present in claims
                user_info = retrieveUserInfo(claims)  # retrieve the user info from the datastore.
                if user_info is None:  # if the user info does not exist, it means that the user is logging in for
                    # the first time
                    createUserInfo(claims)  # create the user info in the datastore.
                    retrieveUserInfo(claims)  # retrieve the user info from the datastore.
                    add_team(name, year_founded, race_wins, world_titles, team_principal, team_base, championships)
                    # add the driver to the user.
            else:
                error_message = "Missing user information"
        except ValueError as exc:  # if the token is invalid, show an error message.
            error_message = exc  # set the error message.

    return render_template('add_team.html', error_message=error_message)  # return the add team page.


@app.route('/edit_driver', methods=['GET', 'POST'])  # this is the route for the update driver page.
def updatedriver():
    error_message = None  # this is the error message.
    id_token = request.cookies.get("token")  # get the token from the cookies.
    if id_token:  # if the token exists, it means that the user is logged in.
        try:  # try to authenticate the user.
            claims = google.oauth2.id_token.verify_firebase_token(id_token, firebase_request_adapter)  # this is the
            # claims object.
            if 'name' in claims and 'email' in claims:  # Check if the necessary keys are present in claims
                user_info = retrieveUserInfo(claims)  # retrieve the user info from the datastore.
                if user_info is None:  # if the user info does not exist, it means that the user is logging in for
                    # the first time
                    createUserInfo(claims)  # create the user info in the datastore.
                    retrieveUserInfo(claims)  # retrieve the user info from the datastore.
                    updatedriver(first_name, last_name, nationality, number, wins, age)  # add the driver to the user.
                    # add the driver to the user.
            else:
                error_message = "Missing user information"
        except ValueError as exc:  # if the token is invalid, show an error message.
            error_message = exc  # set the error message.

    return render_template('edit_driver.html', error_message=error_message)


@app.route('/edit_team', methods=['GET', 'POST'])  # this is the route for the update team page.
def updateTeam():
    error_message = None  # this is the error message.
    id_token = request.cookies.get("token")  # get the token from the cookies.
    if id_token:  # if the token exists, it means that the user is logged in.
        try:  # try to authenticate the user.
            claims = google.oauth2.id_token.verify_firebase_token(id_token, firebase_request_adapter)  # this is the
            # claims object.
            if 'name' in claims and 'email' in claims:  # Check if the necessary keys are present in claims
                user_info = retrieveUserInfo(claims)  # retrieve the user info from the datastore.
                if user_info is None:  # if the user info does not exist, it means that the user is logging in for
                    # the first time
                    createUserInfo(claims)  # create the user info in the datastore.
                    retrieveUserInfo(claims)  # retrieve the user info from the datastore.
                    updateTeams(name, year_founded, race_wins, world_titles, team_principal, team_base, championships)
                    # add the driver to the user.
            else:
                error_message = "Missing user information"
        except ValueError as exc:  # if the token is invalid, show an error message.
            error_message = exc  # set the error message.

    return render_template('edit_team.html', error_message=error_message)


@app.route('/drivers', methods=['POST'])  # this is the route for
# the delete driver page.
def delete_driver():
    error_message = None  # this is the error message.
    id_token = request.cookies.get("token")  # get the token from the cookies.
    if id_token:  # if the token exists, it means that the user is logged in.
        try:  # try to authenticate the user.
            claims = google.oauth2.id_token.verify_firebase_token(id_token, firebase_request_adapter)  # this is the
            # claims object.
            if 'name' in claims and 'email' in claims:  # Check if the necessary keys are present in claims
                user_info = retrieveUserInfo(claims)  # retrieve the user info from the datastore.
                if user_info is None:  # if the user info does not exist, it means that the user is logging in for
                    # the first time
                    createUserInfo(claims)  # create the user info in the datastore.
                    retrieveUserInfo(claims)  # retrieve the user info from the datastore.
                    delete_driver(claims)  # add the driver to the user.
            else:
                error_message = "Missing user information"
        except ValueError as exc:  # if the token is invalid, show an error message.
            error_message = exc  # set the error message.

    return render_template('index.html', error_message=error_message)


@app.route('/teams', methods=['POST'])  # this is the route for
# the delete team page.
def delete_team():
    error_message = None  # this is the error message.
    id_token = request.cookies.get("token")  # get the token from the cookies.
    if id_token:  # if the token exists, it means that the user is logged in.
        try:  # try to authenticate the user.
            claims = google.oauth2.id_token.verify_firebase_token(id_token, firebase_request_adapter)  # this is the
            # claims object.
            if 'name' in claims and 'email' in claims:  # Check if the necessary keys are present in claims
                user_info = retrieveUserInfo(claims)  # retrieve the user info from the datastore.
                if user_info is None:  # if the user info does not exist, it means that the user is logging in for
                    # the first time
                    createUserInfo(claims)  # create the user info in the datastore.
                    retrieveUserInfo(claims)  # retrieve the user info from the datastore.
                    delete_team(claims)  # add the driver to the user.
            else:
                error_message = "Missing user information"
        except ValueError as exc:  # if the token is invalid, show an error message.
            error_message = exc  # set the error message.

    return render_template('index.html', error_message=error_message)


@app.route('/driver_details', methods=['POST', 'GET'])  # this is the
# route for the compare drivers page.
def compare_drivers():
    error_message = None  # this is the error message.
    id_token = request.cookies.get("token")  # get the token from the cookies.
    if id_token:  # if the token exists, it means that the user is logged in.
        try:  # try to authenticate the user.
            claims = google.oauth2.id_token.verify_firebase_token(id_token, firebase_request_adapter)  # this is the
            # claims object.
            if 'wins' in claims and 'age' in claims:  # Check if the necessary keys are present in claims
                user_info = retrieveUserInfo(claims)  # retrieve the user info from the datastore.
                if user_info is None:  # if the user info does not exist, it means that the user is logging in for
                    # the first time
                    createUserInfo(claims)  # create the user info in the datastore.
                    retrieveUserInfo(claims)  # retrieve the user info from the datastore.
                    compare_drivers(claims)  # add the driver to the user.
            else:
                error_message = "Missing user information"
        except ValueError as exc:  # if the token is invalid, show an error message.
            error_message = exc  # set the error message.

    return render_template('driver_details.html', error_message=error_message)


@app.route('/team_details', methods=['POST', 'GET'])  # this is the route for
# the compare teams page.
def compare_teams():  # this is the compare teams function.
    comparison = None  # this is the comparison object. It will be used to compare the two teams.
    datastore_client.key('team', race_wins)  # get the team 1 key.
    datastore_client.key('team', world_titles)  # get the team 2 key.
    team_1 = datastore_client.get(race_wins)  # get the team 1.
    team1 = datastore_client.get(world_titles)  # get the team 2.
    team_2 = datastore_client.get(race_wins)  # get the team 1.
    team2 = datastore_client.get(world_titles)  # get the team 2.
    id_token = request.cookies.get("token")  # get the token from the cookies.
    error_message = None  # this is the error message.
    if id_token:  # if the token exists, it means that the user is logged in.
        try:  # try to authenticate the user.
            claims = google.oauth2.id_token.verify_firebase_token(id_token, firebase_request_adapter)  # this is the
            # claims object.
            if 'name' in claims and 'email' in claims:  # Check if the necessary keys are present in claims
                user_info = retrieveUserInfo(claims)  # retrieve the user info from the datastore.
                if user_info is None:  # if the user info does not exist, it means that the user is logging in for
                    # the first time
                    createUserInfo(claims)  # create the user info in the datastore.
                    retrieveUserInfo(claims)  # retrieve the user info from the datastore.
                    compare_teams(claims)
                    if not team1 or not team2:  # if either team is empty, raise a 404 error.
                        abort(404)

                    stats = ['race_wins', 'world_titles']  # get the stats.
                    comparison = []  # create an empty list.
                    for stat in stats:
                        val1 = team1.get(stat, race_wins)  # get the value of the stat for team 1.
                        val2 = team2.get(stat, race_wins)  # get the value of the stat for team 2.
                        if val1 < val2:
                            comparison.append(
                                (stat, val1, 'red'))  # if the value of the stat for team 1 is less than
                            # the value of the stat for team 2, append the stat, the value of the stat for team 1,
                            # and the color red to the comparison list.
                        else:
                            comparison.append(
                                (stat, val2, 'green'))  # if the value of the stat for team 1 is greater than
                            # the value of the stat for team 2, append the stat, the value of the stat for team 2,
                            # and the color green to the comparison list.
                    if not team1 or not team2:  # if either team is empty, raise a 404 error.
                        abort(404)
            else:
                if not team1 or not team2:
                    stats = ['race_wins', 'world_titles']  # get the stats.
                    comparison = []  # create an empty list.
                    for stat in stats:
                        val1 = team_1.get(stat, world_titles)  # get the value of the stat for team 1.
                        val2 = team_2.get(stat, world_titles)  # get the value of the stat for team 2.
                        if val1 < val2:
                            comparison.append(
                                (stat, val1, 'red'))  # if the value of the stat for team 1 is less than
                            # the value of the stat for team 2, append the stat, the value of the stat for team 1,
                            # and the color red to the comparison list.
                        else:
                            comparison.append(
                                (stat, val2, 'green'))  # if the value of the stat for team 1 is greater than
                            # the value of the stat for team 2, append the stat, the value of the stat for team 2,
                            # and the color green to the comparison list.
                    if not team1 or not team2:  # if either team is empty, raise a 404 error.
                        abort(404)
                error_message = "Missing user information"
        except ValueError as exc:  # if the token is invalid, show an error message.
            error_message = exc  # set the error message.

    return render_template('team_details.html', team1=team1, team2=team2, comparison=comparison,
                           error_message=error_message)
    # render the template.


if __name__ == '__main__':  # if the file is being run directly.
    app.run(host='127.0.0.1', port=8080, debug=True)  # run the app.
