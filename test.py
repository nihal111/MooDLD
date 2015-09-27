class savedata():
    def __init__(self,url,directory):
        self.url = url
        self.directory = directory

save = []
save.append(savedata("afa","dir"))

print save[0].directory
