### connect directly to database 
    - from django.db import connection
    - connection.cursor Returns cursor object 
    - cursor.execute() execute raw sql to db
    - cursor.calproc() call procedure to db 