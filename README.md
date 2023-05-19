- [Overview](#overview)
    - [Description](#description)
- [WebApps Overview](#webapps-overview)
  - [API](#api)
  - [Converters](#converters)
  - [CrossDocking](#crossdocking)
  - [HighlightTracker](#highlighttracker)
  - [pmoReporting](#pmoreporting)
  - [cab](#cab)
  - [Investment Request](#investment-request)
- [Deployment](#deployment)
  - [Already configured machine](#already-configured-machine)
  - [New machine](#new-machine)
- [Contributing](#contributing)
# Overview
### Description
This project contains several small webapps that helps different departments in HL  
It is build using [Django](https://www.djangoproject.com/) (version 3.2.4) framework and it is runned on apache2 with mod_wsgi  
# WebApps Overview
## API
**URL**  
/api/get_highlight_data  
/api/get_pmoReporting_data  
/api/get_user_data  
/api/qr_bill  
/api/api_logs  
/api/crossDockingRefresh  
/api/crossDockingSummaryEmail  
/api/cab_refresh  
/api/track_and_trace  

**Description**  
App used for interacting with every application in automated way.  

- get_highlight_data  Endpoint used to gather data from highlight_tracker app. Used to create data file for PowerBI report.  
- get_pmoReporting_data Endpoint used to gather data from pmoReporting app. Used to create data file for PowerBI report.  
- get_user_data Endpoint used to gather info about user profiles from highlight_tracker app.  
- qr_bill Endpoint used to generate and add qr codes to pdf invoices created in jeeves. To use it you need to `POST` below XML file to it and it will be saved on path provided in `<FilePath>` tag. It uses account `poca` and it privilages to save files on file servers mounted in `/media` directory.  

    ```XML
    <root>
        <Account>CH6800761016011773781</Account>
        <Creditor>
            <Name>HL Display Schweiz AG</Name>
            <Street>Rohrerstrasse 102</Street>
            <City>Aarau</City>
            <Pcode>5000</Pcode>
            <Country>CH</Country>
        </Creditor>
        <Debtor>
            <Name>Ladenbau Schmidt AG</Name>
            <Street>Bächliackerstrasse 4a</Street>
            <City>Frenkendorf</City>
            <Pcode>4402</Pcode>
            <Country>CH</Country>
        </Debtor>
        <Amount>3685.9200</Amount>
        <Currency>CHF</Currency>
        <FilePath>/media/qr_bill_prod</FilePath>
        <FaktNr>2030014</FaktNr>
    </root>
    ```
- api_logs Endpoint used to generate statistics from API logs. Works with `GET` method only.  
- crossDockingRefresh Endpoint used to refresh data from Jeeves in Cross Docking app. Runned two times per day from Jenkins.  
- crossDockingSummaryEmail Endpoint used to generate summary email for Cross Docking app. Runned once per week from Jenkins.   
- cab_refresh Endpoint used to refresh data from FreshService in cab app. Run once a day by Jenkins.  
- track_and_trace Endpoint is used to download documents from carriers and save it on file server. You need to `POST` JSON with below structure to work with it.
  ```JSON
  {
    "root": {
        "url": "https://services.schenkerfrance.fr/Tracing/servlet/SEmarge?PARAM=000637026591553407252340",
        "env": "PROD"
    }
  }
  ```
  Response
  ```JSON
  {
    "MessageId": "0",
    "Message": "File saved at /media/TrackAndTrace/TEST/665c2a9e-018f-11ec-a6fd-00505694c9e2.pdf",
    "filename": "665c2a9e-018f-11ec-a6fd-00505694c9e2.pdf"
  }
  ```

## Converters
**URL**  
/converters/db2csv  
/converters/aldi_orders  
/converters/aldi_orders_admin  

**Description**  
- db2csv is used for converting sqlite db from marketing into csv file  
- aldi_orders is used for downloading excel file with Aldi order (only store opening) that can be inserted into jeeves  
- aldi_orders_admin is used for uploading new data (in excel format) into aldi_orders app  

## CrossDocking
**URL**  
/CrossDocking/main  

**Description**  
Application build for logistic department in 1210 and 1810  
It uses network drive `//ew1-fil-101/Public/_LinuxShareFolder/CrossDocking` for file storage  
Due to that it is needed to have alias in project static dir  

## HighlightTracker
**URL**  
/tools/highlight_tracker  

**Description**  
Application build for hr department for tracking down higlight action plans
## pmoReporting
**URL**  
/pmoReporting/main  

**Description**  
Application build for Group Supply Chain

## cab
**URL**  
/cab/main  

**Description**  
Application build for tracking RFC from FreshService

## Investment Request
**URL**  
/InvestmentRequest/main  

**Description**  
Application build for tracking Investment Request used by group controller  
It uses network drive `//ew1-fil-101/Public/_LinuxShareFolder/InvestmentRequest` for file storage  
Due to that it is needed to have alias in project static dir  

# Deployment
## Already configured machine
1. open jenkins project page > http://bma-mte-101:8080/view/Applications/job/AppPortal
2. Run Jenkins job `Deploy_prod_AppPortal`
## New machine
1. Mount drives used by apps in media drive
   1. Create folders in `/media` folder
   2. Add below lines to `/etc/fstab` 
   ```
    //sdl-clu-003/Jeeves/SWAP/TEST/Invoices /media/qr_bill_test  cifs  username=poca,password=<PUT_PASSWORD_HERE>,uid=1001,iocharset=iso8859-1,vers=1.0  0  0
    //sdl-clu-003/Jeeves/SWAP/PROD/Invoices /media/qr_bill_prod  cifs  username=poca,password=<PUT_PASSWORD_HERE>,uid=1001,iocharset=iso8859-1,vers=1.0  0  0
    //ew1-fil-101/Public/_LinuxShareFolder/CrossDocking /media/CrossDocking  cifs  username=s-hlit,password=<PUT_PASSWORD_HERE>,uid=1001,iocharset=iso8859-1,vers=1.0  0  0
    //ew1-fil-101/Public/_LinuxShareFolder/TrackAndTrace /media/TrackAndTrace  cifs  username=s-hlit,password=<PUT_PASSWORD_HERE>,uid=1001,iocharset=iso8859-1,vers=1.0  0  0
    //ew1-fil-101/Public/_LinuxShareFolder/InvestmentRequest /media/InvestmentRequest  cifs  username=s-hlit,password=<PUT_PASSWORD_HERE>,uid=1001,iocharset=iso8859-1,vers=1.0  0  0
   ```
   3. Run command to mount drives
   ```bash
   sudo mount /media/qr_bill_test/
   sudo mount /media/qr_bill_prod/
   sudo mount /media/CrossDocking/
   sudo mount /media/TrackAndTrace/
   sudo mount /media/InvestmentRequest/
   ```
2. Install apache2 and mod_wsgi 
3. Add new config to apache
```bash
sudo nano /etc/apache2/sites-available/AppPortal.conf
```
```
Listen 8300
<VirtualHost *:8300>
    ServerAdmin dawid.wybierek@hl-display.com
    ServerName tools.hl-display.com
    ServerAlias tools.hl-display.com
    DocumentRoot /opt/AppPortal
    ErrorLog ${APACHE_LOG_DIR}/error_appPortal.log
    CustomLog ${APACHE_LOG_DIR}/access_appPortal.log combined

        WSGIDaemonProcess django2 python-path=/opt/AppPortal:/home/ubuntu/virtual_environments/venv_AppPortal2/lib/python3.8/site-packages user=ubuntu group=ubuntu processes=3 maximum-requests=100
        WSGIProcessGroup django2
        WSGIApplicationGroup %{GLOBAL}
        WSGIScriptAlias / /opt/AppPortal/AppPortal/wsgi.py

        Alias /static /opt/AppPortal/static
        Alias /static/admin/ /home/ubuntu/virtual_environments/venv_AppPortal2/lib/python3.6/site-packages/django/contrib/admin/static/admin
        Alias /media/ /opt/AppPortal/media/

        <Directory /opt/AppPortal/media>
                Require all granted
        </Directory>

        <Directory /opt/AppPortal>
                        Require all granted
        </Directory>

        <Directory /opt/AppPortal/AppPortal>
                <Files wsgi.py>
                        Require all granted
                </Files>
        </Directory>
</VirtualHost>
```
4. Add `EnableMMAP off` to apache2.conf file for proper handling of pdf files
5. Disable default site and enable our newly created one
```bash
sudo a2dissite 000-default.conf
sudo a2ensite AppPortal.conf
```
6. Restart apache2
```bash
sudo systemctl restart apache2
```
7. open jenkins project page > http://bma-mte-101:8080/view/Applications/job/AppPortal/job/Deploy_prod_AppPortal/
8. Run Jenkins job `Deploy_prod_AppPortal`  
9. Add admin account (with valid email)
# Contributing
1. Clone repository
2. Create virtual environment
3. Activate virtual environment and install requirements from file `requirements.txt`
4. Mount folders (if needed for development) from `Deployment > New machine` instruction
5. Run project with below command (inside folder `with manage.py` file) 
```bash
python manage.py runserver 0.0.0.0:8002 --settings AppPortal.settings_dev
```  
