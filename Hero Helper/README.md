# Hero Helper
#### Video Demo:  <URL HERE>
#### Description:
This project is what I would describe as very niche and mostly something that I personally wanted to create
for myself ever since I started to learn how to code. I would describe it as specifically tailored for Dota 2 players
that are above the level of casual but also not very high level, that assists you in picking heroes during the hero select phase of the game.

Just as a preface for those reading that are unsure of what Dota is or how any of this project works in regards to
the game and why it is helpful:

    Dota 2 is a video game that is the current continuation of a mod that was made for warcraft 3. It is a team game
    involving two teams of five that are pitted against each other, the first team to destroy the others "Ancient"
    is the winner.

        The game currently has 124 heroes as of writing on the 16/07/2023 (Clearly this project ended up being on the backburner for a while as I am now finishing it 13/12/24). Each of these heroes are completely unique,
    all with their own abilities and stats and nuance. In a  game of Dota, there is a banning phase where each team
    bans a number of heroes that are unavailable to be selected for that game. Each hero may also only be selected
    by a single player for that match.

        This leads to every game being very different and varied, but every hero that your team and the oppoosing team chooses being
    incredibly important, needing answers for certain heroes, gameplans, and team compositions. Finally this has led into why my
    project is useful, as the hero you pick in the hero select phase being incredibly important while you also
    have a time limit to pick.

The goal of the project was to create software that can assist in returning a number of hero suggestions based on constraints
that you can select from forms on a website. I originally considered what the best option would be for a platform for the project
and decided that a website would by far suit it the most. While I did entertain the idea of an android app for a little bit, I ended up
deciding that because of time constraints in hero select, and the fact that Dota 2 is a PC game, a website would be the most convenient
and quickest way to enter and select contraints.

The current state that I have finished the project in for this assignment is definitely not the end for the "Hero Helper", I would like
to expand the databases, add items to the database and pair them with heroes that are commonly associated with (as with the current implementation of heroes being associated with traits), and to potentially add other relevant databases. I would also love to add
a Dota 2 client API to detect banned heroes and then selectively not return them as results. But at the end of the day adding the API is a lot of work for a small quality of life improvement, so I decided to exclude it from the project currently, but later on in my coding journey
I would like to add it and get more familiar with using APIs. A number of other improvements I would like to implement in the future are listed in the project page future.html page breaking down future goals.

### WRITING THE CODE AND THE DATABASE - STRUGGLES AND DECISIONS

From the beginning of this project I decided i wanted to implement it with the same stack as the previous finance project due to familiarity, with the addition of using a bootstrap template similar to what I used for my homepage project. This resulted in using Python, Flask, and Jinja with a sprinkling of HTML and CSS to create the project.

#### Creating the database

The first and very time-consuming step was creating a relational database of Dota 2 heroes, common traits, and off-roles. The trait and offrole tables both exist because a hero can have multiple of these variables so the tables were necessary to allow for multi-variable association. Creating this database and going through each hero individually to assign relevant traits and manually entering the data into a spreadsheet was very time consuming and painful but in the end it was worth it.

#### The app.py foundation

App.py is begun by importing flask and CS50's SQL. The database is then connected to app.py so it can be utilised. The first step using the database is to create key lists of all the necessary variable as contained in the database. This allows the ability to pass the variables as options to the individual web pages later. There are then 4 different routes to different html pages, although three of them are very uninteresting being only GET requests to static content. The meat of the project is in in the route for index.html, which has all of the user interactivity and primary purpose of the web app. The other pages exist as supplementary information for the user.

#### The .html visuals

The web pages share the same header/footer/background to keep a consistent visual style throughout with a dark colour scheme. The header at the top contain the title of the web app of the left and links to all of the pages in a navbar, with bootstrap js being used here for hover options and visual style for the text. Bootstrap's cover template was used as the foundation for all of the pages, with a variety of alterations made to better suit my needs. The footer is completely done in css without any bootstrap assistance. On the left and right side of the web pages I included images of Dota 2 heroes taken from official artwork to add some pop and colour. These images only apply to devices with a minimum of 1200px resolution otherwise they would take up too make screenspace, even though this in not really intended for mobile or tablet usage this makes QOL for smaller devices better. There are a few css changes to adjust the formatting and location of text and keeping a consistent distance below the header, and a few small colour changes to the background and form submission button but overall nothing major, the majority is handled by bootstrap.

#### The .html visuals

Layout.html is very boring and just implements the basic structure for all pages with the necessary classes to apply css.

#### SQL query functionality in combination with index.html/quoted.html

The majority of the interesting code for the project is in the route for index.html and in the index.html page itself. The primary idea behind the page is the user selecting a number of restrictions from the available variables and then submitting those variables to receive all of the matching options from the database. It took my quite a while to wrap my head around how to implement this as an SQL query dynamically using Python and eventually turned to youtube to find a video explaining a method very similar to what I wanted to achieve. This receives all of the items through request.form.items and then runs through different conditionals to build the query dynamically and still keep it safe from SQL injection. Upon any valid selection of variable from the various drop down selections on index.html the query is built with two main separate lists, key_query and values. Key_query is appended to based on the id of the form with a '=?' and values is appended to based on the variable selected. If no variable is selected then the key query is appended to as '1=1' so no paired value is expected. There are separate conditionals involving sub_roles and traits as both of these have multi-variable relations across different tables.
There is the beginning of functionality for multiple traits to be selected but it has not yet been implemented and is one of the features I would like to add in the future. However, at this point in time I am not sure what the best way to elegantly include it in the html is to make it not take up space but make it easy for the user to see many options and select/deselect them quickly. Once the query has been built by receving input from the forms through key value pairs the query is finalised and executed to the database (as long as there has been at least one variable selected, otherwise index is reloaded).
One of the options on the form is to show off-role heroes. If this is selected then any heroes that fulfil the requirements and sometimes fulfil that role are returned in an extra list below the main results. If the bos is checked without a main_role being selected it does nothing, as there is no role to compare it to. If both main_role and sub_role are selected by the user then the conditions are fulfilled and the code then follows a similar structure to before, although this time it builds a query just for the offrole options and joins the sub_roles table. I have a feeling there is a more efficient way to implement this but at this point in time I have not worked out how yet, I am happy at least that it doesn't create the suggestions list twice, which I had at the start of the project, so it's not that twice, but I'm sure I can incorporate more of the similar code into the key-value pair loop somehow.
That is the main code covered for app.py, in index.html it is for the most part pretty straightforward. A big chunk of the code is just the form  of 4 select menus, a checkbox, and a submit button. These select menus are populated by the key variables that were taken from the database near the beginning of app.py and passed into render_template(). In addition for the quoted.html page, where results are returned to, the process is very similar for printing the list of hero suggestions based on the list passed through render_template(). The little thing I added here for some user feedback was conditionals if either offsuggestions (if selected) or suggestions is empty then it is printed to the page that there are no valid results based on the restrictions.

#### The other .html pages

The three other html pages are static and just inform the user about basic site functionality, the definitions of the various traits, and the future of the web app.

#### Conclusion

Overall I had a lot of fun creating this project and it was something I had wanted to do since I started learning to code. It ended up taking me much longer than I care to admit, and I struggled a lot trying to wrestle with the process of creating dynamic SQL  queries in Python, but I am happy with where I have ended up with it's current state. I would keep working on it to add planned future features to make it even better in the future, and maybe people other than me will even get use out of it once I polish it up a little more. It may not be the most complex project but it is something that I wanted to create for me and I'm glad that I have.
