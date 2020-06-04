
from KalturaClient import *
from KalturaClient.Plugins.Core import *
import os
import config

def client_for_admin(username, privileges): 

    kaltura_config = KalturaConfiguration(config.partner_id)
    kaltura_config.serviceUrl = "https://www.kaltura.com/"
    client = KalturaClient(kaltura_config)
    ks = client.session.start(
        config.admin_secret,
        username,
        KalturaSessionType.ADMIN,
        config.partner_id, 
        86400,
        privileges)
    client.setKs(ks)

    return client 

def client_for_user(username, privileges): 
    kaltura_config = KalturaConfiguration(config.partner_id)
    kaltura_config.serviceUrl = "https://www.kaltura.com/"
    client = KalturaClient(kaltura_config)
    ks = client.session.start(
        config.admin_secret,
        username,
        KalturaSessionType.USER,
        config.partner_id, 
        86400,
        privileges)
    client.setKs(ks)

    return  client 

def ks_for_user(username, privileges):
    kaltura_config = KalturaConfiguration(config.partner_id)
    kaltura_config.serviceUrl = config.service_url
    client = KalturaClient(kaltura_config)
    ks = client.session.start(
        config.admin_secret,
        username,
        KalturaSessionType.USER,
        config.partner_id, 
        86400,
        privileges)

    return ks