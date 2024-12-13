from flask import Flask, redirect, render_template, request
from cs50 import SQL
import re

# Configure application
app = Flask(__name__)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///heroes.db")

# Pulling Keys from database
TRAITS = db.execute("SELECT DISTINCT(trait) FROM traits ORDER BY trait")
ATTRIBUTES = db.execute("SELECT DISTINCT(attribute) FROM heroes ORDER BY attribute")
TYPES = db.execute("SELECT DISTINCT(type) FROM heroes ORDER BY type")
ROLES = db.execute("SELECT DISTINCT(main_role) FROM heroes ORDER BY main_role")


@app.route("/", methods=["GET", "POST"])
def index():
    # Render the main page on GET request
    if request.method == "GET":
        return render_template("index.html", traits=TRAITS, attributes=ATTRIBUTES, types=TYPES, roles=ROLES)
    # Render the page with the suggestions once requirements are posted
    else:

        # Check the heroes table and traits table for any hero that matches the requirements
        # Dynamically create SQL query from items returned (referenced code and idea from this video https://www.youtube.com/watch?v=BwmDzqgbl-I)
        values = []
        traits = []
        key_query = []
        trait_key_query = f'=?'
        counter = 0

        ########################
        ########################
        ## MAIN FUNCTIONALITY ##
        ########################
        ########################

        # Iterate through all key value pairs returned from form items
        for key, val in request.form.items():
            if val:
                # If the key is traits save it separately and increment counter
                if key == "traits":
                    counter = counter + 1
                    traits.append(val)
                    # If the counter is greater than 1 add an additional '?' to the query
                    if int(counter) > 1:
                        trait_key_query = trait_key_query + f',?'
                elif key == "sub_role":
                    # Do nothing
                    pass
                # If key is not traits append to key_query and add value to values
                else:
                    values.append(val)
                    key_query.append(key + "=? ")
            # If no key returned append '1=1' to key_query to ignore variable
            if not key:
                key_query.append("1=1")

        # Converting the traits to a single string
        # If number of traits is > 1, add all traits to the start of the values list
        trait_query = f' '
        if len(traits) > 0:
            values = traits + values
            trait_query = f' id IN (SELECT hero_id FROM traits WHERE trait' + \
                (trait_key_query) + ' )'
            if len(key_query) > 0:
                trait_query = trait_query + f' AND '

        # Modular query with standard beginning  and endfor all queries
        beginning = f'SELECT DISTINCT name FROM heroes JOIN traits ON heroes.id = traits.hero_id WHERE'
        end_query = f'{" AND ".join(key_query)} ORDER BY name'
        # If there is a trait in query add it
        if trait_query:
            sql_query = f'{beginning}{trait_query}{end_query}'
        # Else submit query with no Join to trait table
        else:
            sql_query = f'{beginning}{end_query}'
        # Populate list with all valid options from requested restrictions
        if len(values) > 0:
            suggestions = db.execute(sql_query, *values)

        ################################################################################
        ################################################################################
        ## OFFROLE BUTTON FUNCTIONALITY (only works if a main role is also selected) ###
        ################################################################################
        ################################################################################

        sub_role = request.form.get("sub_role")
        main_role = request.form.get("main_role")

        if all([sub_role, main_role]) == True:
            # Begin building additional query for off_role heroes
            # Dynamically create SQL query from items returned (referenced code and idea from this video https://www.youtube.com/watch?v=BwmDzqgbl-I)
            values = []
            traits = []
            off_role = []
            key_query = []
            trait_key_query = f'=?'
            counter = 0

            # Iterate through all key value pairs returned from form items
            for key, val in request.form.items():
                if val:
                    # If the key is traits save it separately and increment counter
                    if key == "traits":
                        counter = counter + 1
                        traits.append(val)
                        # If the counter is greater than 1 add an additional '?' to the query
                        if int(counter) > 1:
                            trait_key_query = trait_key_query + f',?'
                    # If key is not traits append to key_query and add value to values
                    elif key == "main_role":
                        off_role.append(val)
                    elif key == "sub_role":
                        # do nothing
                        pass
                    else:
                        values.append(val)
                        key_query.append(key + "=? ")
                # If no key returned append '1=1' to key_query to ignore variable
                if not key:
                    key_query.append("1=1")

            # Converting the traits to a single string
            # If number of traits is > 1, add all traits to the start of the values list
            trait_query = f' '
            if len(traits) > 0:
                values = traits + values
                trait_query = f' id IN (SELECT hero_id FROM traits WHERE trait' + \
                    (trait_key_query) + ' )'
                if len(key_query) > 0:
                    trait_query = trait_query + f' AND '

            # Add off-role to beginning of values
            values = off_role + values

            # Modular query with standard beginning for all queries
            off_beginning = f'SELECT DISTINCT name FROM heroes LEFT JOIN traits ON heroes.id = traits.hero_id LEFT JOIN sub_roles ON heroes.id = sub_roles.hero_id WHERE id IN (SELECT hero_id FROM sub_roles WHERE roles=?) '
            # Logic to add AND to end of beginning if any variables other than main role are selected
            if len(values) > 1:
                off_beginning = off_beginning + f'AND '
            end_query = f'{" AND ".join(key_query)} ORDER BY name'
            # If there is a trait in query add it
            if trait_query:
                off_sql_query = f'{off_beginning}{trait_query}{end_query}'
            # Else submit query with no Join to trait table
            else:
                off_sql_query = f'{off_beginning}{end_query}'
            # Populate list with all valid options from requested restrictions
            offsuggestions = db.execute(off_sql_query, *values)
            # render the quoted.html page with all variables passed
            return render_template("quoted.html", suggestions=suggestions, offsuggestions=offsuggestions, traits=TRAITS, attributes=ATTRIBUTES, types=TYPES, roles=ROLES, key_query=key_query)

        # If nothing is submitted through the forms reload index.html, otherwise submit non-off-role query
        else:
            if len(values) == 0:
                return render_template("index.html", traits=TRAITS, attributes=ATTRIBUTES, types=TYPES, roles=ROLES)
            else:
                return render_template("quoted.html", suggestions=suggestions, traits=TRAITS, attributes=ATTRIBUTES, types=TYPES, roles=ROLES, key_query=key_query)


@app.route("/how", methods=["GET"])
def help():
    return render_template("how_to.html")


@app.route("/trait", methods=["GET"])
def trait():
    return render_template("traits.html")


@app.route("/future", methods=["GET"])
def future():
    return render_template("future.html")
