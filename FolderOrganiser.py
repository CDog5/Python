import shutil,os
from pathlib import Path
def copy(filename,newfolder):
    esc="\\"
    newdir = searchdir +f"{esc}{newfolder}{esc}"
    if not os.path.exists(newdir):
       os.makedirs(newdir)
    target = searchdir +f"{esc}{newfolder}{esc}"+ filename
    original = searchdir +esc+ filename 
    print("Copying file",original,"to",target,".")
    shutil.move(original,target)
photoexts=[".png",".jpg",".jpeg",".gif"]
videoexts=[".mp4",".avi",".mov",".m4v"]
musicexts=[".mp3",".wav",".flac",".m4a"]
docexts=[".doc",".docx",".xlsx",".pptx",".ppt",".pub",".accdb"]
searchdir=str(input("Enter directory to search: "))

try:
    for filename in os.listdir(searchdir):
            
        for extension in photoexts:
            if filename.lower().endswith(extension):
                copy(filename,"Pictures")
        for extension in videoexts:
            if filename.lower().endswith(extension):
                copy(filename,"Videos")
        for extension in musicexts:
            if filename.lower().endswith(extension):
                copy(filename,"Music")
        for extension in docexts:
            if filename.lower().endswith(extension):
                copy(filename,"Documents")
                
except:
    print("ERROR.")

        
        
