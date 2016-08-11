MooDLD - the Ultimate Moodle Downloader

Release 1.0

Designed for IIT Bombay Moodle

This application serves the purpose of automating the process of downloading files from Moodle. 
It downloads all the files from the listed courses to the user’s computer.

Dependencies

Tkinter
Mechanize
pyCrypto

Instructions for use

Linux and Mac - Download MooDLD.py and moodle.ico from Github Repository.

Windows - Extract the Setup.rar file and run it. Installation is straightforward. 
Note: It is recommended to set the installation directory to a location which does not require administrator access to modify files. If you set it to “C:/Program Files(x86)/MooDLD”, MooDLD might give an error like “MooDLD returned -1”. To fix this, either change the installation directory or right click on the icon and “Run MooDLD as administrator”.

Install Dependencies

mechanize 
On Ubuntu use sudo apt-get install python-mechanize

On Mac use sudo pip install mechanize

Tkinter 

On Ubuntu use sudo apt-get install python-tk
On Mac Tkinter is installed by default when you install python

pyCrypto

Install using pip

pip install pycrypto

Run using python MooDLD.py

-------------------
The user has to login using LDAP ID/Password. 
(Keep me logged in can be checked to avoid entering credentials repeatedly)

On the first run, after logging in, the user must go to the Preferences page to select the courses to be downloaded. The directory for each course also needs to be specified. The user can also change the root directory to effectively set the directory of all courses to /Course_Name/. On Windows, the auto-download option configures the app to open on every Windows boot and automatically start download of selected courses.

Click “Save Settings” to save the settings for further use. These can be changed by visiting the Preferences page any time.

The user has to click on the DLD Files button to download files of selected courses from Moodle.

The application creates two .txt files in the directory in which it is kept - Cred.txt and Preferences.txt. 

These files are essential for the working of the application and must NOT be deleted! Deletion of above files will lead to loss in saved settings.

If a course has folders within it, MooDLD creates a new folder in the pre-set directory and downloads all the folder contents into this newly created folder, effectively, replicating the entire structure present on the website on your local system. 
Assignment handling has also been added so that the assignments which are uploaded are also downloaded. 
News Forum download has also been integrated, MooDLD downloads all downloadable files from News Forum threads as well.

Made By

Nihal Singh - nihal111
Arpan Banerjee - arpan98
Akash Trehan - CodeMaxx

Suggestions and Feedback
Please feel free to contact us:
nihal.111@gmail.com
arpanbnrj9@gmail.com
akash.trehan123@gmail.com

Any bugs found should be reported to the issue tracker.
You can send in Pull Requests to contribute to the project.