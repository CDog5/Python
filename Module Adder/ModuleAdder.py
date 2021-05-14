import shutil,os
from pathlib import Path
def copy(filename,original,newfolder):
    target = searchdir +"/"+newfolder+"/"+ filename
    original = searchdir + filename
    print("Copying file",original,"to",target,".")
    shutil.copyfile(original,target)

searchdir=str(input("Enter directory to search: "))

try:
    for filename in os.listdir(searchdir):
            
        for extension in photoexts:
            if filename.endswith(extension):
                move(filename,target,"Photos")
                
except:
    print("ERROR.")

        
        
