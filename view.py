from KalturaClient import *
from KalturaClient.Plugins.Core import *
import ks
import config
from urllib.parse import urlencode
from datetime import datetime, timedelta

class View:

    @staticmethod
    def playback(entry_id):

        client  = ks.client_for_admin(config.admin_email, "")

        livestream = client.liveStream.get(entry_id)

        is_live = client.liveStream.isLive(entry_id, KalturaPlaybackProtocol.AUTO)
        if (is_live == False):
            if ((livestream.redirectEntryId) and livestream.redirectEntryId != ''):
                entry_id = livestream.redirectEntryId
            elif ((livestream.recordedEntryId) and livestream.recordedEntryId != ''):
                entry_id = livestream.recordedEntryId
            ## for entries with PER_SESSION recording, the recordedEntryId is wiped
            ## we find the recorded entry by filtering on the root entry 
            else:
                filter = KalturaBaseEntryFilter()
                filter.rootEntryIdEqual = entry_id
                pager = KalturaFilterPager()

                result = client.baseEntry.list(filter, pager)
                if (result.objects):
                    entry_id = result.objects[0].id

        privileges = "sview:{},restrictexplicitliveview:{},enableentitlement,appid:{},appdomain:{},sessionkey:{}" \
            .format(entry_id, entry_id, config.app_id, config.app_domain, config.user_id)

        kaltura_session = ks.ks_for_user(config.user_id, privileges)
        
        data = {
            "ks": kaltura_session, 
            "partner_id": config.partner_id,
            "uiconf_id": config.uiconf_id,
            "user_id": config.user_id, 
            "entry_id": entry_id
        }

        return data

    @staticmethod
    def moderator_view(entry_id): 
        
        privileges = "setrole:WEBCAST_PRODUCER_DEVICE_ROLE,sview:*,list:{},download:{}" \
            .format(entry_id, entry_id)
        kaltura_session = ks.ks_for_user(config.moderator_user, privileges)

        base_url =  "https://www.kaltura.com/apps/webcast/vlatest/index.html?"

        params = {
            "MediaEntryId": entry_id,
            "ks":kaltura_session,
            "ks_expiry": datetime.now()+timedelta(days=1),
            "qnaModeratorMode": True,
            "serverAddress": config.service_url, 
            "fromDate": datetime.now()+timedelta(minutes=2),
            "toDate":datetime.now()+timedelta(minutes=8)
        }

        moderator_url = base_url+urlencode(params)
        return(moderator_url)
