# RRTS
Road Repair Tracking Software

A Python-based system software for registering complaints, allocating wokforce and resources, and reviewing the status of complaints.<br>
Includes Tkinter-based UI for four users.

USE CASES:

Clerk Page:<br>
-Read user inputs from the clerk and update the database.

Supervisor Page:<br>
-Display complaint report and read severity, traffic, resources, etc. while updating the database.<br>
-Display schedule report and update status of repair on the database.

City Admin Page:<br>
-Display and update available resource counts on the database.<br>
-Approve and Authorize new users into the system.

Mayor Page:<br>
-Display resource utilization statistics for a given time period as input by the user.<br>
-Display repairs statistics such as number and type of repairs, and repairs outstanding at any point of time.<br>

Scheduler:<br>
-Retrieve appropriate information from the database and use it to schedule pending repairs according to the available resources.<br>


FEATURES:<br>
-Separate personalized storage space for each city<br>
-Customizable options for book-keeping activities<br>
-Real time updates<br>
-Access management functionality<br>
-Security: Password encryption, Restricted database file access<br>

TECH STACK:<br>
Front-end: Tkinter (Python), Pillow for images<br>
Back-end: Python<br>
Modules used: os, re, pandas, time, datetime<br>
Database: PyDrive module (Python) with Google Drive APIs to access csv files stored on the cloud.<br>
