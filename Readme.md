# MooDLD - the Ultimate Moodle Downloader

##### Release 1.0

<p align="center"><b>Designed for IIT Bombay Moodle</b></p>

This application serves the purpose of automating the process of downloading files from Moodle.
It downloads all the files from the listed courses to the user's computer.

### Dependencies

1. Tkinter
2. Mechanize
3. pyCrypto

### Instructions for use

1. **Linux and Mac** - Download `MooDLD.py` and `moodle.ico` from Github Repository.<br/>
**Windows** - Extract the Setup.rar file from [here](https://github.com/nihal111/MooDLD/raw/master/Setup.rar) and run it. Installation is straightforward.
Note: It is recommended to set the installation directory to a location which does not require administrator access to modify files. If you set it to "C:/Program Files(x86)/MooDLD", MooDLD might give an error like "MooDLD returned -1". To fix this, either change the installation directory or right click on the icon and "Run MooDLD as administrator".

2. Install Dependencies
  - **mechanize**  <br/>On Ubuntu use `sudo apt-get install python-mechanize`<br/>
  On Mac use `sudo pip install mechanize`

  - **Tkinter** <br/>
  On Ubuntu use `sudo apt-get install python-tk`<br>
  On Mac `Tkinter` is installed by default when you install python

  - **pyCrypto**<br/>
  Install using pip<br/>
  `pip install pycrypto`

3. Run using one of the following:<br/>
    a. `python2 MooDLD.py`(Won't work with python3)<br/>
    b. `./MooDLD.py`<br/>

    In case you get a `Permission Denied` error for method `b`. Run `chmod +x MooDLD.py` and then try again.

4. The user has to login using LDAP ID/Password. <br/>(**Keep me logged in** can be checked to avoid entering credentials repeatedly)

5. On the first run, after logging in, the user must go to the **Preferences** page to select the courses to be downloaded. The directory for each course also needs to be specified. The user can also change the root directory to effectively set the directory of all courses to <Root Directory>/Course_Name/. On Windows, the auto-download option configures the app to open on every Windows boot and automatically start download of selected courses.

6. Click "Save Settings" to save the settings for further use. These can be changed by visiting the **Preferences** page any time.

7. The user has to click on the **DLD Files** button to download files of selected courses from Moodle.


The application creates two `.txt` files in the directory in which it is kept - `Cred.txt` and `Preferences.txt`.
<br/><br/>These files are essential for the working of the application and must **NOT** be deleted! Deletion of above files will lead to loss in saved settings.<br/>

If a course has folders within it, MooDLD creates a new folder in the pre-set directory and downloads all the folder contents into this newly created folder, effectively, replicating the entire structure present on the website on your local system.
Assignment handling has also been added so that the assignments which are uploaded are also downloaded.
News Forum download has also been integrated, MooDLD downloads all downloadable files from News Forum threads as well.

### Made By
Nihal Singh - [nihal111](https://github.com/nihal111)<br/>
Arpan Banerjee - [arpan98](https://github.com/arpan98)<br/>
Akash Trehan - [CodeMaxx](https://github.com/CodeMaxx)

### Suggestions and Feedback

Please feel free to contact us:

<mailto:nihal.111@gmail.com><br/>
<mailto:arpanbnrj9@gmail.com><br/>
<mailto:akash.trehan123@gmail.com><br/>

**Any bugs found should be reported to the issue tracker.**<br/><br/>
**You can send in Pull Requests to contribute to the project.**

