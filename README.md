# Character-Archive-Website

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
      
#DATA TABLES
      
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
