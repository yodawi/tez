# tez

A blazingly fast auth framework.

# Speed 🚀🚀🚀

All api endpoints take less than **30ms** !!

# /admin/upsert

inputs:
• email, String
• password, String
• origin_verification, String

# config

Tez requires a MySQL database. It assumes the database server is running localy (massive performance improvement), has a database called `db`, and that the user running the api already has mysql privilleges without a password, however this configuration can be easelly modified.
You will need to create a table inside od your database called `Users` with the command inside of the file at `src/db.sql`.

# OS

We recommend using Ubuntu 20.4 as your server's operating system.
