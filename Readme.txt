MooDLD - the Ultimate Moodle Downloader 
					-Version 1.0
					-For Windows
This application serves the purpose of automating the process of downloading files from Moodle. 
It downloads all the ".pdf" files from the listed courses to preset directories on the user's computer.
Designed for IIT Bombay Moodle. Made using Python. (Libraries: Tkinter, Mechanize)

Instructions for use-

1. Windows- Extract the MooDLD.rar file before use.
   Linux- Download "MooDLD.py" and "moodle.ico" from Github Repo.
Install python 2.7 and libraries: Tkinter and Mechanize.
(Open terminal and type: "sudo apt-get install python2.7" to install Pthon 2.7, "sudo apt-get install python-mechanize" to install mechanize and "sudo apt-get install python-tk" to install Tkinter on Ubuntu and debian like Linuxes. 
The python website describes a whole bunch of other ways to get Python.

2. The user has to login using LDAP ID/Password. ("Keep me logged in" can be checked to avoid entering credentials repeatedly.)

3. On the first run, after logging in, the user must go to the "Preferences" page to browse directories and check the courses to be downloaded. (Default directory is C:/).

4. Press "Save Settings" to save the settings for further use. These can be changed by visiting the Preferences page any time. 

5. The user has to click on the "DLD Files" button to download files of selected courses from Moodle.


The application creates two ".txt" files in the directory in which it is kept - "Cred.txt" and "Preferences.txt" 
These files are essential for the working of the application and must not be deleted! Deletion of above files will lead to loss in saved settings. 
Also if a course has folders within it, MooDLD creates a new folder in the pre-set directory and downloads all the folder contents into this newly created folder, effectively, replicating the entire structure present on the website on your local system.
Assignment handling has also been added so that the assignments which are uploaded are also downloaded as Moodle treats assignments differently.


For any suggestions or feedback:
nihal.111@gmail.com

Made By:
Nihal Singh
Akash Trehan
Arpan Banerjee
