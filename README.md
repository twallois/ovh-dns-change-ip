# ovh-dns-change-ip
Python Script to automaticaly change IP of a DNS A record for a OVH 
Can update root Domain Record or SubDomain Record

# Setup
#### 1 - Create Application for interact with OVH
Go inside the corresponding URL and create an application to interact with your OVH Account:

  - [OVH Europe]
  - [OVH US]
  - [OVH North-America]
  - [So you Start Europe]
  - [So you Start North America]
  - [Kimsufi Europe]
  - [Kimsufi North America]


   [OVH Europe]: <https://eu.api.ovh.com/createApp/>
   [OVH US]: <https://api.us.ovhcloud.com/createApp/> 
   [OVH North-America]: <https://ca.api.ovh.com/createApp/>
   [So you Start Europe]: <https://eu.api.soyoustart.com/createApp/>
   [So you Start North America]: <https://ca.api.soyoustart.com/createApp/>
   [Kimsufi Europe]: <https://eu.api.kimsufi.com/createApp/>
   [Kimsufi North America]: <https://ca.api.kimsufi.com/createApp/>
   
#### 2 - Fill ovh-dns-change-ip.conf file
Complete the file `ovh-dns-change-ip.conf` with your Endpoint, Application Key, Secret and the URL of your Domain and SubDomain (if neccesary)

    [OVH-INFO]
    Endpoint=ovh-eu
    #To create an application go to https://eu.api.ovh.com/createApp/ (for OVH Europe)
    ApplicationKey = [APPLICATION_KEY]
    ApplicationSecret = [APPLICATION_SECRET]
    
    [DNS-INFO]
    DomainName = twallois.fr
    SubDomainName = 

#### 3 - Setup requirement and configuration file
Install the python3 requirements:

    pip3 install -r requirements.txt

Run the Python Script with `--setup` argument to ask to OVH to allow your application for some OVH APIs

    python3 ./ovh-dns-change-ip.py --setup 
    
You will need to go inside a website to allow the application

Configuration is Done 

# Execution
To modify the IP inside the OVH DNS Record you just need to run the script

    python3 ./ovh-dns-change-ip.py
If the IP inside OVH DNS is not your current IP, the DNS record will be update
Add the script inside a cron to automaticaly update your IP

Enjoy,

[Thibaut Wallois](https://twallois.fr/)
