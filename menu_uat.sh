#!/bin/bash 

HOME="/www/etisalat/"
MIRROR="/home/qinetics/www/etisalat/"
HPL="hpl"
MOBILEWEB="mobileweb"
API="api"
RESELLER="reseller"
REGISTRAR="registrar"
DNSWS="dnsws"
METISALATRESTFUL="mEtisalatRestful"
REGTEMPLATES="regtemplates"
RESTEMPLATES="restemplates"
TOMCAT_PATH="/usr/local/tomcat7/webapps/"

HPL_STR="etisalat-hpl"
HPL_REGEX="^(etisalat-hpl)" 
MOBILEWEB_STR="mEtisalatWeb"
MOBILEWEB_STR_REGEX="^(mEtisalatWeb)"              
API_STR="etisalat/api"
API_REGEX="^(etisalat/api)"   
RESELLER_STR="etisalat/reseller"
RESELLER_REGEX="^(etisalat/reseller)"       
REGISTRAR_STR="etisalat/registrar"
REGISTRAR_REGEX="^(etisalat/registrar)"       
DNSWS_STR="etisalat/dnsws"
DNSWS_REGEX="^(etisalat/dnsws)"       
METISALATRESTFUL_STR="mEtisalatRestful"
METISALATRESTFUL_REGEX="^(mEtisalatRestful)"      
REGTEMPLATES_STR="etisalat/regtemplates"
REGTEMPLATES_REGEX="^(etisalat/regtemplates)"        
RESTEMPLATES_STR="etisalat/restemplates"
RESTEMPLATES_REGEX="^(etisalat/restemplates)" 

FILECHGBK="filechg_backup"
FILECHGFK="filechg_fallback"

TOMCAT_OWNERS="tomcat:tomcat"
APACHE_OWNERS="apache:apache"


echo "Menu" 
echo "2. Backup filechange"
echo "3. Fallback filechange"
echo "4. deploy app tar file"
echo "5. deploy api tar file"
echo "6. deploy dns tar file"
echo "7. deploy web tar file"

echo "Enter Choice,deployment date,1=tomcat ,2=apache, example 2 20221210 1" 
read Choice CURRENT_TIME Owner

       if [ -z "$CURRENT_TIME" ] ; then 
              echo "Date is empty"
       else 
       
          if [ "1" = "$Owner" ] ; then
            ownershipfile=$TOMCAT_OWNERS
			elif [ "2" = "$Owner" ] ; then 
            ownershipfile=$APACHE_OWNERS
          else 
            ownershipfile=$Owner            
          fi
		#echo $ownershipfile
              case $Choice in 
                     2)
                     while read -r line ; do
                     if [[ "$line" =~ \#.* ]] ; then                        
                        continue                     
                     elif [[ $line =~ $HPL_REGEX ]]; then
                            TEMP=${line#*$HPL_STR}
                            cp $HOME$HPL$TEMP $HOME$HPL$TEMP.$CURRENT_TIME
                            cp $HOME$HPL$TEMP $MIRROR$HPL$TEMP #only keep most recent ver
                            ls -lort $HOME$HPL$TEMP.$CURRENT_TIME >> $FILECHGBK 
                     elif [[ $line =~ $MOBILEWEB_STR_REGEX ]]; then
                            TEMP=${line#*$MOBILEWEB_STR}
                            cp $HOME$MOBILEWEB$TEMP $HOME$MOBILEWEB$TEMP.$CURRENT_TIME
                            cp $HOME$MOBILEWEB$TEMP $MIRROR$MOBILEWEB$TEMP
                            ls -lort $HOME$MOBILEWEB$TEMP.$CURRENT_TIME >> $FILECHGBK                             
                     elif [[ $line =~ $API_REGEX ]]; then
                            TEMP=${line#*$API_STR}
                            cp $HOME$API$TEMP $HOME$API$TEMP.$CURRENT_TIME
                            cp $HOME$API$TEMP $MIRROR$API$TEMP
                            ls -lort $HOME$API$TEMP.$CURRENT_TIME >> $FILECHGBK               
                     elif [[ $line =~ $RESELLER_REGEX ]]; then
                            TEMP=${line#*$RESELLER_STR}
                            cp $HOME$RESELLER$TEMP $HOME$RESELLER$TEMP.$CURRENT_TIME
                            cp $HOME$RESELLER$TEMP $MIRROR$RESELLER$TEMP
                            ls -lort $HOME$RESELLER$TEMP.$CURRENT_TIME >> $FILECHGBK  
                     elif [[ $line =~ $REGISTRAR_REGEX ]]; then
                            TEMP=${line#*$REGISTRAR_STR}
                            cp $HOME$REGISTRAR$TEMP $HOME$REGISTRAR$TEMP.$CURRENT_TIME
                            cp $HOME$REGISTRAR$TEMP $MIRROR$REGISTRAR$TEMP
                            ls -lort $HOME$REGISTRAR$TEMP.$CURRENT_TIME >> $FILECHGBK 
                     elif [[ $line =~ $DNSWS_REGEX ]]; then
                            TEMP=${line#*$DNSWS_STR}
                            cp $HOME$DNSWS$TEMP $HOME$DNSWS$TEMP.$CURRENT_TIME
                            cp $HOME$DNSWS$TEMP $MIRROR$DNSWS$TEMP
                            ls -lort $HOME$DNSWS$TEMP.$CURRENT_TIME >> $FILECHGBK  
                     elif [[ $line =~ $METISALATRESTFUL_REGEX ]]; then
                            restful="true"
                            TEMP=${line#*$METISALATRESTFUL_STR}
                            cp $TOMCAT_PATH$METISALATRESTFUL$TEMP $TOMCAT_PATH$METISALATRESTFUL$TEMP.$CURRENT_TIME 
                            ls -lort $TOMCAT_PATH$METISALATRESTFUL$TEMP.$CURRENT_TIME >> $FILECHGBK 
                     elif [[ $line =~ $REGTEMPLATES_REGEX ]]; then
                            TEMP=${line#*$REGTEMPLATES_STR}
                            cp $HOME$REGTEMPLATES$TEMP $HOME$REGTEMPLATES$TEMP.$CURRENT_TIME
                            cp $HOME$REGTEMPLATES$TEMP $MIRROR$REGTEMPLATES$TEMP
                            ls -lort $HOME$REGTEMPLATES$TEMP.$CURRENT_TIME >> $FILECHGBK  
                     elif [[ $line =~ $RESTEMPLATES_REGEX ]]; then
                            TEMP=${line#*$RESTEMPLATES_STR}
                            cp $HOME$RESTEMPLATES$TEMP $HOME$RESTEMPLATES$TEMP.$CURRENT_TIME
                            cp $HOME$RESTEMPLATES$TEMP $MIRROR$RESTEMPLATES$TEMP
                            ls -lort $HOME$RESTEMPLATES$TEMP.$CURRENT_TIME >> $FILECHGBK  
                     else
                            echo "No match string " $line 
                            $line >> $FILECHGBK 
                     fi
                     done < filechg
                       echo "Backup done"
                       chmod -R 700 $HOME
                       chown -R $ownershipfile $HOME
                     if [[ $restful == "true" ]] ; then
                            chmod -R 700 $TOMCAT_PATH$METISALATRESTFUL
                            chown -R $ownershipfile $TOMCAT_PATH$METISALATRESTFUL
                     fi    
                            ;;
                     3)
                     while read -r line ; do
                     if [[ "$line" =~ \#.* ]] ; then                         
                        continue                     
                     elif [[ $line =~ $HPL_REGEX ]]; then
                            TEMP=${line#*$HPL_STR}
                            mv -f $HOME$HPL$TEMP.$CURRENT_TIME $HOME$HPL$TEMP
                            ls -lort $HOME$HPL$TEMP >> $FILECHGFK 
                     elif [[ $line =~ $MOBILEWEB_STR_REGEX ]]; then
                            TEMP=${line#*$MOBILEWEB_STR}
                            mv -f $HOME$MOBILEWEB$TEMP.$CURRENT_TIME $HOME$MOBILEWEB$TEMP
                            ls -lort $HOME$MOBILEWEB$TEMP >> $FILECHGFK                             
                     elif [[ $line =~ $API_REGEX ]]; then
                            TEMP=${line#*$API_STR}
                            mv -f $HOME$API$TEMP.$CURRENT_TIME $HOME$API$TEMP
                            ls -lort $HOME$API$TEMP >> $FILECHGFK               
                     elif [[ $line =~ $RESELLER_REGEX ]]; then
                            TEMP=${line#*$RESELLER_STR}
                            mv -f $HOME$RESELLER$TEMP.$CURRENT_TIME $HOME$RESELLER$TEMP
                            ls -lort $HOME$RESELLER$TEMP >> $FILECHGFK  
                     elif [[ $line =~ $REGISTRAR_REGEX ]]; then
                            TEMP=${line#*$REGISTRAR_STR}
                            mv -f $HOME$REGISTRAR$TEMP.$CURRENT_TIME $HOME$REGISTRAR$TEMP
                            ls -lort $HOME$REGISTRAR$TEMP >> $FILECHGFK 
                     elif [[ $line =~ $DNSWS_REGEX ]]; then
                            TEMP=${line#*$DNSWS_STR}
                            mv -f $HOME$DNSWS$TEMP.$CURRENT_TIME $HOME$DNSWS$TEMP
                            ls -lort $HOME$DNSWS$TEMP >> $FILECHGFK  
                     elif [[ $line =~ $METISALATRESTFUL_REGEX ]]; then
                            restful="true"                     
                            TEMP=${line#*$METISALATRESTFUL_STR}
                            mv -f $TOMCAT_PATH$METISALATRESTFUL$TEMP.$CURRENT_TIME $TOMCAT_PATH$METISALATRESTFUL$TEMP
                            ls -lort $TOMCAT_PATH$METISALATRESTFUL$TEMP >> $FILECHGFK 
                     elif [[ $line =~ $REGTEMPLATES_REGEX ]]; then
                            TEMP=${line#*$REGTEMPLATES_STR}
                            mv -f $HOME$REGTEMPLATES$TEMP.$CURRENT_TIME $HOME$REGTEMPLATES$TEMP
                            ls -lort $HOME$REGTEMPLATES$TEMP >> $FILECHGFK  
                     elif [[ $line =~ $RESTEMPLATES_REGEX ]]; then
                            TEMP=${line#*$RESTEMPLATES_STR}
                            mv -f $HOME$RESTEMPLATES$TEMP.$CURRENT_TIME $HOME$RESTEMPLATES$TEMP
                            ls -lort $HOME$RESTEMPLATES$TEMP >> $FILECHGFK 
                     else
                            echo "No match string " $line 
                            $line >> $FILECHGFK 
                     fi
                     done < filechg 
                       echo "Revert done"
                       chmod -R 700 $HOME
                       chown -R $ownershipfile $HOME
                     if [[ $restful == "true" ]] ; then
                            chmod -R 700 $TOMCAT_PATH$METISALATRESTFUL
                            chown -R $ownershipfile $TOMCAT_PATH$METISALATRESTFUL
                     fi
                            ;;
                     4)
                     tar -xvf www_app.tar -C / > appfile
                     echo "Done deploy app.tar"
                     chmod -R 700 $HOME*
                     echo "Assign Permission 700 done"
                     chown -R $ownershipfile $HOME
                     echo "Assign Ownersip chown -R $ownershipfile " $HOME " done"                     
                            ;;
                     5)
                     # deploy api
                     tar -xvf www_api.tar -C / > apifile
                     echo "Done deploy api.tar"
                     chmod -R 700 $HOME
                     echo "Assign Permission 700 done"
                     chown -R $ownershipfile $HOME
                     echo "Assign Ownersip chown -R $ownershipfile " $HOME " done" 
                     # deploy restful
                     tar -xvf www_mEtisalatRestful.tar --strip-components=1 -C $TOMCAT_PATH > apifile
                     echo "Done deploy www_mEtisalatRestful.tar"
                     chmod -R 700 $TOMCAT_PATH$METISALATRESTFUL
                     echo "Assign Permission 700 done"
                     chown -R $ownershipfile $TOMCAT_PATH$METISALATRESTFUL
                     echo "Assign Ownersip chown -R $ownershipfile " $TOMCAT_PATH$METISALATRESTFUL " done"                      
                            ;;
                     6)
                     tar -xvf www_dns.tar -C / > dnswsfile
                     echo "Done deploy dns.tar"
                     chmod -R 700 $HOME
                     echo "Assign Permission 700 done"
                     chown -R $ownershipfile $HOME
                     echo "Assign Ownersip chown -R $ownershipfile " $HOME " done"                   
                            ;;        
                     7)
                     tar -xvf www_web.tar -C / > webfile
                     echo "Done deploy web.tar"
                     chmod -R 700 $HOME
                     echo "Assign Permission 700 done"
                     chown -R $ownershipfile $HOME
                     echo "Assign Ownersip chown -R $ownershipfile " $HOME " done"                   
                            ;;                             
              esac
       fi







