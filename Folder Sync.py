from dirsync import sync
import os,sys
source_path = 'C:/Users/adams/Documents/New folder (2)/'
target_path='E:/AutoBackup'
syncing = True
def blockPrint():
    sys.stdout = open(os.devnull, 'w')
while syncing:
    sync(source_path, target_path, 'sync')
