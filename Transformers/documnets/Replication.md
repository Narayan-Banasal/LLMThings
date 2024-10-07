Setup Replications 
which initdb -> to check the path of the server instance 

initdb -D /tmp/primary_db -> primary instance has been created
Steps to configure primary node : 
1. change postgresql.conf to enable networking -> nano /tmp/primary_db/postgresql.conf and change the localhost to * and also the port 
2. Create a replication user(best practice) ->  pg_ctl -D /tmp/primary_db start to start the server.  To go inside of the db: psql --port=5433 postgres Create the user with the flag replication: create user repuser replication
3. Allow remote accesss in pg_hba.conf Make changes use: nano /tmp/primary_db/pg_hba.conf under the IPv4 section add one same line for the repuser 
4. Restart the primary server to restart: pg_ctl -D /tmp/primary_db restart

Setup replica: 
1. pg_basebackup -h localhost -U repuser --checkpoint=fast -D /tmp/replica_db/ -R --slot=some_name -C --port=5433: command to be run
2. nano /tmp/replica_db/postgresql.conf and change the port 

To start the primary go like this pg_ctl -D /tmp/primary_db start
And to start the replica go like this pg_ctl -D /tmp/replica_db start
https://www.youtube.com/watch?v=Yy0GJjRQcRQ