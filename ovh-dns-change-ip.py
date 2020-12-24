from configparser import ConfigParser
import os
import sys
import requests
import ovh


def setupOVHConf(ovhEndpoint,ovhApplicationKey,ovhApplicationSecret):
    ###Retrieve the Customer Key
    client = ovh.Client(
        endpoint=ovhEndpoint,
        application_key=ovhApplicationKey,
        application_secret=ovhApplicationSecret
    )
    # Request RO, /me API access
    ck = client.new_consumer_key_request()
    ck.add_rules(ovh.API_READ_ONLY, "/domain/zone/*/record")
    ck.add_rules(ovh.API_READ_WRITE_SAFE, "/domain/zone/*/record/*")


    # Request token
    validation = ck.request()
    print("You need to verify and accept the permission to allow the application to use the OVH APIs")
    print("Please visit %s to authenticate" % validation['validationUrl'])
    input("and press Enter to continue...")


    #Create ovh.conf file for ovh library https://github.com/ovh/python-ovh
    config_ovh = ConfigParser()
    config_ovh["default"]= {"endpoint":ovhEndpoint}
    config_ovh[ovhEndpoint]={}
    config_ovh[ovhEndpoint]["application_key"]=ovhApplicationKey
    config_ovh[ovhEndpoint]["application_secret"]=ovhApplicationSecret
    config_ovh[ovhEndpoint]["consumer_key"]=validation['consumerKey']

    script_dir = os.path.dirname(__file__)
    with open(os.path.join(script_dir,'ovh.conf'), 'w') as configfile_ovh:
        config_ovh.write(configfile_ovh)

script_dir = os.path.dirname(__file__)
conf_file=os.path.join(script_dir, "ovh-dns-change-ip.conf")

#Get the configparser object
config_object = ConfigParser()
config_object.read(conf_file)

ovhInfo=config_object["OVH-INFO"]
ovhEndpoint=ovhInfo["Endpoint"]
ovhApplicationKey=ovhInfo["ApplicationKey"]
ovhApplicationSecret=ovhInfo["ApplicationSecret"]

dnsInfo=config_object["DNS-INFO"]
dnsInfoDomainName=dnsInfo["DomainName"]
dnsInfoSubDomainName=dnsInfo["SubDomainName"]

#Setup OVH Conf
if "--setup" in sys.argv or "-s" in sys.argv:
    setupOVHConf(ovhEndpoint,ovhApplicationKey,ovhApplicationSecret)
    print("SETUP COMPLETE")
    os._exit(status=0)

#Check file ovh.conf exist
if not os.path.isfile(os.path.join(script_dir,"ovh.conf")):
    print("ERROR, you need to do a Setup before execute the script")
    print("Execute the script with a --setup or -s")
    os._exit(status=2)


#Retrieve IP 

IPCurrent=requests.get("https://ifconfig.me").text


#OVH call
try:
    client = ovh.Client(config_file=os.path.join(script_dir,"ovh.conf"))
    ListRecord=client.get('/domain/zone/%s/record' % dnsInfoDomainName,
                        fieldType='A',
                        subDomain=dnsInfoSubDomainName)

    if len(ListRecord) > 1:
        print("Error: We retrieved more than one record")
        print("We will NOT continue")
        print("List of Record:")
        i=1
        for record in ListRecord:
            detailRecord=client.get('/domain/zone/%s/record/%s' % (dnsInfoDomainName,record))
            print("Record %s :" % i)
            print(detailRecord)
        os._exit(status=3)

    record=ListRecord[0]
    detailRecord=client.get('/domain/zone/%s/record/%s' % (dnsInfoDomainName,record))
    targetIpRecord=detailRecord["target"]
    if targetIpRecord==IPCurrent:
        print("IP identical, record will not need to change")
    else:
        print("The local IP is not the DNS IP, we will change the Record")
        detailRecord=client.put('/domain/zone/%s/record/%s' % (dnsInfoDomainName,record),target=IPCurrent)
        print("IP Change OK")
  
except ovh.exceptions.NotGrantedCall:
    print("Permission denied, you need to setup again your grant was revoked")
    print("Execute the script with a --setup or -s")
except Exception  as exception:
    print("ERROR")
    print(type(exception).__name__+" : "+str(exception))

