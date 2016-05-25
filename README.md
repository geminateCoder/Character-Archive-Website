# Character-Archive-Website

![alt text](http://i.imgur.com/GYyqbsO.png "RolePlayGrounds") #subject to change

##Basic Information
A website designed to save multiple characters at once, give them a profile, and display them for others to find and admire. 

##Features include:
* Users can have a personal profile for each of their character and themselves.
* Users can create as many characters as they wish. #subject to change
* The characters recently created will be displayed in the front page
* Users can favorite a character to save on their dashboard.
* Users can follow/friend other users.
* Users can private message other users.
* There is stats with # of Characters # of favorited characters # of followers.
* . . .
	
##Pages: 
* The *Index* page should have a header with a login and sign up button on floating to the left of the screen. There needs to be a section where it will display recent characters with links that will display once a user hovers over the character image. Login and Signup buttons pops out on the page.

* The *Login* and *Signup* page will be made just as a procaution. Login Form should only have username and password. Sighn up Form should have username, email, password, and confim password.

* The *Dashboard* page is only accessable if a user has logged into the session. There will be their image on the right of the screen. There should be a notification/character/recent characters/favorted/stats/friend-followed/news section on the dashboard. The header should change if user is in session to a small avatar image with a dropdown that will have the settings page and the logout link.



##Files
    Character-Archive-Website\
      .idea\+includes\+Scripts\
        <virtual environment files>
      Lib\
        <virtual environment files>
      site-packages #Should be made Sources Root.
      Project\
        <virtual environment files>
        app\
          static\
          templates\ 
          __init__.py 
          views.py #app routes
          forms.py #wtforms
          models.py #Database Tables
          OLDapp.py #Resource 
      run.py #Application      
      config.py 
      db.migrate.py #Updates DB
      
##CURRENT DATA TABLES
      
    DB Models:
      TABLES:
        favorite:
          user_id + character_id
        follow:
          follower_id + following_id
          
    User(Model):
      id - primary key
      username - unique
      email - unique
      password
      settings - relationship 'User' [one to many] > UserSettings
      posts - relationship 'Post' [one to many] > Posts
      following - relationship [many to many] > follow
      last_login_at ----| 
      current_login_at -| Will use append date stamps for current login/ip during login
      last_login_ip ----| Will use append date stamps for last login/ip durring logout  
      current_login_ip -|
      
    UserSettings(Model):
      id - primary key
      username - ForeignKey > user.username
      . . .
      img - Using links for now.
      
    Character(Model:
      id - primary key
      username - user.username
      . . .
      favorited - relationship 'User' [many to many] > favorite
      img - Using links for now.
      created - datestamp
      
    Post(Model):
      id - primary key
      . . .
      user_id - ForeignKey > user.id
