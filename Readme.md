# MooDLD - the Ultimate Moodle Downloader

##### Release 2.0

<p align="center"><b>Designed for IIT Bombay Moodle</b></p>

This application serves the purpose of automating the process of downloading files from Moodle.
It downloads all the files from the listed courses to the user's computer.

### Dependencies

1. Tkinter
2. Mechanize
3. pyCrypto

### Instructions for use

1. **Linux and Mac** - Download `MooDLD.py` and `moodle.ico` from Github Repository.<br/>
**Windows** - Extract the MooDLD.rar file before use.

2. Install Dependencies
  - **mechanize**  <br/>On Ubuntu use `sudo apt-get install python-mechanize`<br/>
  On Mac use `sudo pip install mechanize`

  - **Tkinter** <br/>
  On Ubuntu use `sudo apt-get install python-tk`<br>
  On Mac `Tkinter` is installed by default when you install python

  - **pyCrypto**<br/>
  Install using pip<br/>
  `pip install pycrypto`

3. Run using `python MooDLD.py`

4. The user has to login using LDAP ID/Password. <br/>(**Keep me logged in** can be checked to avoid entering credentials repeatedly)

5. On the first run, after logging in, the user must go to the **Preferences** page to select the courses to be downloaded.

6. Click "Save Settings" to save the settings for further use. These can be changed by visiting the **Preferences** page any time.

7. The user has to click on the **DLD Files** button to download files of selected courses from Moodle. Auto-Download feature is also available.


The application creates two `.txt` files in the directory in which it is kept - `Cred.txt` and `Preferences.txt`.
<br/><br/>These files are essential for the working of the application and must **NOT** be deleted! Deletion of above files will lead to loss in saved settings.<br/>

If a course has folders within it, MooDLD creates a new folder in the pre-set directory and downloads all the folder contents into this newly created folder, effectively, replicating the entire structure present on the website on your local system.
Assignment handling has also been added so that the assignments which are uploaded are also downloaded.

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

