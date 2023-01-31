# @author Ts. Mohd Solehuddin Abd Wahab
# m.soleh@qinetics.net
# 26 November 2021

import sys, os, shutil, tarfile

current_directory = os.path.dirname(os.path.abspath(__file__))

print('current dir:' + current_directory)

# get the 1st cli argument which is the list of changed files
changed_file_list = sys.argv[1]

# get the 2nd cli argument which should the project root folder where we want to retrieve the class files.
source_folder = sys.argv[2]

f = open(changed_file_list, 'r')
lines = f.readlines()

filechg = open("filechg_temp",'w')

filechg.write("## compulsory to backup srs.jar for each project dir, line 1 to 7 is untouchable\n")
filechg.write("etisalat/api/WEB-INF/lib/srs.jar\n")
filechg.write("etisalat/reseller/WEB-INF/lib/srs.jar\n")
filechg.write("etisalat/registrar/WEB-INF/lib/srs.jar\n")
filechg.write("etisalat/dnsws/WEB-INF/lib/srs.jar\n")
filechg.write("etisalat-hpl/WEB-INF/lib/srs.jar\n")
filechg.write("mEtisalatRestful/WEB-INF/lib/srs.jar\n")

source_lines = [];

is_contain_srs = False
is_contain_mEtisalatRestful = False

for line in lines:

    # remove new line symbols
    line = line.replace("\n","").strip()

    # replace .java with .class
    if line.endswith('java'):
        line = line.replace('.java','.class')

    # replace source folders with class folders as we actually want to copy the classes instead of source files.
    if "etisalat-srs" in line:
        is_contain_srs = True
        line = line.replace("source","classes")
    if "mEtisalatRestful" in line:
        is_contain_mEtisalatRestful = True
        line = line.replace("src/main/java","target/classes")
    if "etisalat-hpl" in line:
        line = line.replace("source","classes")
        
    if (line != "") and (not line.startswith("##")) : #skip empty lines
        source_lines.append(line)

    # no matter what, generate a filechg.txt with the replaced lines
    filechg.write(line+"\n")
    
    
source_set = set(source_lines) #remove duplicates by turning it into a Set object

source_lines = list(source_set) #reconvert to list

src = []

# print out the file names
for index in range(len(source_lines)):
    print(index+1 , source_lines[index])
    # https://www.geeksforgeeks.org/python-os-path-split-method/
    # os.path.split = 
    src.append(os.path.split(source_folder + source_lines[index]))

countWeb = 0 
countNonWeb = 0
for (src_folder, _file) in src:
    # build the deployment package folder structure
    if (_file.endswith('.js') or _file.endswith('.html') or _file.endswith('.css') or _file.endswith('.jsp') ):
        #print("extension web file=" + _file)
        countWeb += 1
    else:
        countNonWeb += 1

    new_package_root = current_directory + '\\www\\'
    deployment_pkg_folder = src_folder.replace(source_folder, new_package_root)

    #copy all files from the source folder to deployment package folder. skipping srs as it will be packaged as jar instead.
    if "etisalat-srs" not in deployment_pkg_folder:
        if "mEtisalatRestful" in deployment_pkg_folder:
            deployment_pkg_folder = deployment_pkg_folder.replace("mEtisalatRestful/target","mEtisalatRestful/WEB-INF")
        if "etisalat-hpl" in deployment_pkg_folder:
            deployment_pkg_folder = deployment_pkg_folder.replace("etisalat-hpl","etisalat/hpl")
        if "mEtisalatWeb" in deployment_pkg_folder:
            deployment_pkg_folder = deployment_pkg_folder.replace("mEtisalatWeb","etisalat/mobileweb")
            
        os.makedirs(deployment_pkg_folder, exist_ok=True)
        print('deployment_pkg_folder ' + deployment_pkg_folder)
        shutil.copyfile(os.path.join(src_folder, _file), os.path.join(deployment_pkg_folder, _file))
        #shutil.copyfile(src_folder +'/'+ _file.strip(), deployment_pkg_folder + '/' + _file.strip())     

print("web file count " + str(countWeb))
print("Non web file count " + str(countNonWeb))
#if change effects srs project, create all deployable packages and copy the srs.jar into them.
if(is_contain_srs):
    os.makedirs(current_directory + '/www/etisalat/api/WEB-INF/lib/', exist_ok=True)
    shutil.copyfile(source_folder + 'etisalat-hpl/WEB-INF/lib/srs.jar', current_directory + '/www/etisalat/api/WEB-INF/lib/srs.jar')
    
    os.makedirs(current_directory + '/www/etisalat/dnsws/WEB-INF/lib/', exist_ok=True)
    shutil.copyfile(source_folder + 'etisalat-hpl/WEB-INF/lib/srs.jar', current_directory + '/www/etisalat/dnsws/WEB-INF/lib/srs.jar')
    
    os.makedirs(current_directory + '/www/etisalat/hpl/WEB-INF/lib/', exist_ok=True)
    shutil.copyfile(source_folder + 'etisalat-hpl/WEB-INF/lib/srs.jar', current_directory + '/www/etisalat/hpl/WEB-INF/lib/srs.jar')
    
    os.makedirs(current_directory + '/www/etisalat/registrar/WEB-INF/lib/', exist_ok=True)
    shutil.copyfile(source_folder + 'etisalat-hpl/WEB-INF/lib/srs.jar', current_directory + '/www/etisalat/registrar/WEB-INF/lib/srs.jar')
    
    os.makedirs(current_directory + '/www/etisalat/reseller/WEB-INF/lib/', exist_ok=True)
    shutil.copyfile(source_folder + 'etisalat-hpl/WEB-INF/lib/srs.jar', current_directory + '/www/etisalat/reseller/WEB-INF/lib/srs.jar')
    
    os.makedirs(current_directory + '/www/mEtisalatRestful/WEB-INF/lib/', exist_ok=True)
    shutil.copyfile(source_folder + 'etisalat-hpl/WEB-INF/lib/srs.jar', current_directory + '/www/mEtisalatRestful/WEB-INF/lib/srs.jar')


#create the tar archives compressed with gzip
api_tar = None
app_tar = None
dns_tar = None
web_tar = None
mEtisalatRestful_tar = None

for root, dirs, files in os.walk('www'):
    for file in files:
        target_add = os.path.join(root, file)
        
        #for www_api.tar
        if('\\etisalat\\api\\' in target_add):
            if(api_tar == None):
                api_tar = tarfile.open('www_api.tar','w:gz')
            api_tar.add(target_add)
            # www_web.tar
            if(web_tar == None ):
                web_tar = tarfile.open('www_web.tar','w:gz')
            if (file.endswith('.js') or file.endswith('.html') or file.endswith('.css') or file.endswith('.jsp')):    
                web_tar.add(target_add)
        
        #for www_dnsws.tar
        elif('\\etisalat\\dnsws\\' in target_add):
            if(dns_tar == None):
                dns_tar = tarfile.open('www_dns.tar','w:gz')
            dns_tar.add(target_add)
            # www_web.tar
            if(web_tar == None ):
                web_tar = tarfile.open('www_web.tar','w:gz')
            if (file.endswith('.js') or file.endswith('.html') or file.endswith('.css') or file.endswith('.jsp')):    
                web_tar.add(target_add)          
   
        #for www_mEtisalatRestful
        elif('\\mEtisalatRestful\\' in target_add):
            if(mEtisalatRestful_tar == None):
                mEtisalatRestful_tar = tarfile.open('www_mEtisalatRestful.tar','w:gz')
            mEtisalatRestful_tar.add(target_add)
            # www_web.tar
            if(web_tar == None ):
                web_tar = tarfile.open('www_web.tar','w:gz')
            if (file.endswith('.js') or file.endswith('.html') or file.endswith('.css') or file.endswith('.jsp')):    
                web_tar.add(target_add)

        #everything else goes into www_app.tar
        #question: do we need to create tar file for urlforwarding?
        else:
            if(app_tar == None):
                app_tar = tarfile.open('www_app.tar','w:gz')
            app_tar.add(target_add)
            # www_web.tar
            if(web_tar == None ):
                web_tar = tarfile.open('www_web.tar','w:gz')
            if (file.endswith('.js') or file.endswith('.html') or file.endswith('.css') or file.endswith('.jsp')):    
                web_tar.add(target_add)
           
#close the file io streams
if(not api_tar == None):
    api_tar.close()
if(not app_tar == None):
    app_tar.close()
if(not dns_tar == None):
    dns_tar.close()
if(not mEtisalatRestful_tar == None):
    mEtisalatRestful_tar.close()
if(not web_tar == None):
    web_tar.close()        
