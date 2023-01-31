from subprocess import Popen, PIPE
import subprocess
import datetime
import paramiko
import getpass
import time
import sys
import re
import os

def progressIndicator(count, total, status=''):
    bar_len = 25
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('[%s] %s%s %s\r' % (bar, percents, '%', status))
    sys.stdout.flush()
    
def pause_exec(msg):
    print(msg)
    proceed = str(input("Hit enter to continue, or enter any key to stop"))
    print("================================================")
    if proceed != '':
        exit()
    return 

def getOutput(channel,showMenu):
    if showMenu:
        while not channel.recv_ready():
            time.sleep(3)
        out = channel.recv(sys.maxsize)
        # print all output after getting
        sys.stdout.write(out.decode("utf-8"))
    else:
        # kill shell script
        channel.send(chr(3))
        sys.stdout.write("Terminating shell")


def waitOutput(channel,display=True):
    while not channel.recv_ready():
        time.sleep(3)
    out = channel.recv(sys.maxsize)
    # print all output after getting
    if display:
        sys.stdout.write(out.decode("utf-8"))
    
def getMenu(channel):
    out = b''
    while b'Enter Choice' not in out:
        out = channel.recv(sys.maxsize)
    # adding extra clause to quit, handled by this code though
    sys.stdout.write(out.decode("ascii"))
    
def categorise_files(inpath,outpath):
    folder = {
        "unknown" : [],
        "api": [],
        "registrar" : [],
        "regtemplates" : [],
        "reseller" : [],
        "restemplates" : [],
        "hpl" : [],
        "srs" : [],
        "mRestful" : [],
        "mWeb" : []
    }

    lines = open(inpath, "r")
    # generate changedFiles.txt
    for line in lines:
        if line.startswith("etisalat/api/"):
            ## API (etisalat/api)
            folder["api"].append(line)
        elif line.startswith("etisalat/registrar/"):
            ## registrar (etisalat/registrar)
            folder["registrar"].append(line)
        elif line.startswith("etisalat/regtemplates/"):
            ## regtemplates (etisalat/regtemplates)
            folder["regtemplates"].append(line)
        elif line.startswith("etisalat/reseller/"):
            ## reseller (etisalat/reseller)
            folder["reseller"].append(line)
        elif line.startswith("etisalat/restemplates/"):
            ## restemplates (etisalat/restemplates)
            folder["restemplates"].append(line)
        elif line.startswith("etisalat-hpl/"):
            ## hpl (etisalat-hpl)
            folder["hpl"].append(line)
        elif line.startswith("etisalat-srs/"):
            ## Srs (etisalat-srs)
            folder["srs"].append(line)
        elif line.startswith("mEtisalatRestful/"):
            ## mRestful (mEtisalatRestful)
            folder["mRestful"].append(line)
        elif line.startswith("mEtisalatWeb/"):
            ## mWeb (mEtisalatWeb)
            folder["mWeb"].append(line)
        else:
            ## unknown (doesnt really affect anything)
            folder["unknown"].append(line)

    ## once all lines are categorised, start writing changedFiles.txt
    f = open(outpath,'w')
    for category,lines in folder.items():
        f.write("\n## "+category+"\n")
        #loop and write categories, then lines
        for line in lines:
            f.write(line)
    f.close()

# we expect this file to be in cron, replacing the deployment.py
# the batch file must be ran first, to get the diff files in changedFiles.txt
# the batch file will take the below inputs:
# <path_to_src_repo> <path_to_output_txt> <SHA_0> <SHA_1>
# SHA 0 and 1 is interchangable, they do not matter

output_path = os.getcwd() # we want it to output here
# note that here means /etisalat/cron/deploy, so this dir will contain all files
# used in the old deployment automation
# everyone's repo is in a different path so we will take it as inputs
try:
    local_path = sys.argv[1]
    old_deploy_hash = sys.argv[2]
    new_deploy_hash = sys.argv[3]

    # not really needed but doing it anyway for readability
    arg1 = local_path
    arg2 = output_path
    arg3 = old_deploy_hash
    arg4 = new_deploy_hash

    # running process to git diff in txt
    subprocess.run(["git","diff","--name-only",
                    arg3,arg4,">",arg2+"/diff.txt"],
                   check=False, shell=True, cwd=arg1)
    
except IndexError as e:
    print("Invalid number of parameters.\nCorrect usage: python diffy.py <local_repo_path> <hash#1> <hash#2> ")

# post diff, we want to categorise the files for easy inspection
categorise_files("diff.txt","changedFiles.txt")

## once this stage is complete, we start the tar generation using changedFile.txt
## checkpoint to allow manual checking of changedFIle.txt
pause_exec("Please verify changedFiles.txt MANUALLY before proceeding")

# now we execute the tar generation py script, we know that it takes in
# <path to_changedFiles.txt> <path_to_src_repo>
# which we already have because changedFIles is cwd and paht is arg[1]
# tar generation sequence
# we will delete old files first
subprocess.call(["rmdir","/s","/q","www"],shell=True)

subprocess.call(["del","diff.txt","www_api.tar", "www_app.tar", "www_dns.tar", "www_mEtisalatRestful.tar","www_web.tar"],shell=True)

# changedFile WILL be in cwd, so
changedFile_path = output_path+"/changedFiles.txt"
# for readabiity
repo_path = local_path

# running process to package tars (using deployment_package.py
subprocess.run(["python","deployment_package.py",changedFile_path,repo_path]
                ,check=False)

# [!] -- FROM HERE ONWARDS, OPERATIONS ARE DONE ON THE SERVER, PLEASE BE CAREFUL
# once that is done, we will push it to server. ask for login creds first
host = "10.237.229.51"
username = "qinetics"
# hide password from cmd history
password = getpass.getpass("\n [!] Password for "+username+" : ")

# directories, can be hardcoded because UAT always deploy here
target_dir = "/home/qinetics/stag_deployment/" #THIS IS JUST THE FINAL TEST DIR
tar_files = ["www_app.tar","www_api.tar","www_dns.tar","www_web.tar","www_mEtisalatRestful.tar"]

# setup client
client = paramiko.client.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(host, username=username, password=password)

# upload files via ftp
sftp = client.open_sftp()
print("> Logged into",host,"as",username)
# first upload filechg as filechg_temp, we will rename later
sftp.put("filechg_temp", os.path.join(target_dir, "filechg_temp"))
i = 0
for tar in tar_files:
    progressIndicator(i,len(tar_files),status=" | Uploading "+tar_files[i])
    try:
        sftp.put(tar, os.path.join(target_dir, tar))
    except FileNotFoundError as e:
        print("File",tar,"cannot be located")
    i+=1
progressIndicator(i,len(tar_files),status="Upload completed")
print("\n")
# command to run bash to run menu script
x = datetime.datetime.now()
# this path should be the path where we uploaded the stuff
path = target_dir
escalate = "sudo -k su\n"
invokeMenu = "sh "+path+"menu_uat.sh\n"
renameFilechgOld = "mv "+path+"filechg "+path+"filechg"+x.strftime("%Y%m%d")+"\n"
renameFilechgNew = "mv "+path+"filechg_temp "+path+"filechg\n"
keepRunning = True

# run shell script on server
showMenu = True
cmd = client.invoke_shell()
# backup the filechg
cmd.send(escalate)
waitOutput(cmd,display=False)
cmd.send( "%s\n" % password )
waitOutput(cmd,display=False)
cmd.send(renameFilechgOld)
cmd.send(renameFilechgNew)
time.sleep(3)
print("\n")
print("=============== Client SHELL ===============")
print("* * * Enter any invalid option to quit * * *")
print("============================================")
### loop here to keep getting the menu
## TODO: this part doesnt really work because of cannot
## stat file error, which is a bug in the menu_uat.sh
while showMenu:
    time.sleep(1)
    cmd.send(invokeMenu)
    getMenu(cmd)
    option = str(input("> "))
    arg = option.split(" ")
    if arg[0] not in ["2","3","4","5","6","7"]:
        showMenu = False
    else:
        cmd.send(option+"\n")
    getOutput(cmd,showMenu)
client.close()
