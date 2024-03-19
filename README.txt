This repo is for all of the mysql code I'm assuming?I'm mostly just adding this to get credit for a github edit for milestone3

In order to export your database
    mysqldump -u [username] -p [database_name] > [filename.sql]
In order to import the the database after you pull the repo 
    mysql -u [username] -p [database_name] < [filename.sql]
Note that the dump needs to be moved into the repository in order to share it 