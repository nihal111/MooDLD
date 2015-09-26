import mechanize

moodle = 'http://moodle.iitb.ac.in/login/index.php'

info = open("user info.txt").read().splitlines()
N=int(info[2])


br = mechanize.Browser()



br.open(moodle)

br.select_form( nr=0 ) 
br['username']=info[0]
br['password']=info[1]

res = br.submit()
print "Successful Login!\n"


for x in range (3,N+3):

    links=[]
    url = br.open(info[x])
    for link in br.links(url_regex="."):
        
        if(not link.url.startswith('http://moodle.iitb.ac.in/login/logout.php')):
            links.append(link)

    for link in links:
        br.open(link.url)
        if ((br.geturl()).endswith('.pdf') or (br.geturl()).endswith('forcedownload=1')):
            br.retrieve(link.url,info[x+N]+link.text[(link.text).index("]")+1:]+'.pdf')
        br.back()
  
print "All Downloads complete!\n"    
  



