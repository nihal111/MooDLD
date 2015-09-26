MooDLD - the Moodle Downloader

This application serves the purpose of automating the process of downloading files from Moodle. 
It downloads all the '.pdf' files from the listed courses to preset directories on the user's computer.
Designed for IIT Bombay Moodle. But may work for all Moodle's in general.


 Requirements/Dependencies:
- Python 2.7
- Mechanize Library

 Installation Instructions For windows:
-Configure the "user info.txt" file to set your preferences and credentials i.e login username, password, links to courses subscribed (links where all pdf's are uploaded) and download directories
 The "user info.txt" file should be edited as such:

"
<username>
<password>
<no of subjects/courses>
<subject 1 url to course website>
<subject 2 url to course website>
<subject 3 url to course website>
<subject 4 url to course website>
<subject 5 url to course website>
<Download Directory for subject 1>
<Download Directory for subject 2>
<Download Directory for subject 3>
<Download Directory for subject 4>
<Download Directory for subject 5>
"

Here is an example
"
150040015
mypassword
5
http://moodle.iitb.ac.in/mod/folder/view.php?id=9202
http://moodle.iitb.ac.in/course/view.php?id=1879
http://moodle.iitb.ac.in/course/view.php?id=1740
http://moodle.iitb.ac.in/mod/folder/view.php?id=9066
http://moodle.iitb.ac.in/course/view.php?id=1842
D:\Moodle\BB101\
D:\Moodle\PH107\
D:\Moodle\PH107\
D:\Moodle\CH105\
D:\Moodle\MA105\
"
- Download directories must be created before running the code.
- The subject url's should correspond to the website having list of all uploaded pdf's 
