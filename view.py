from KalturaClient import *
from KalturaClient.Plugins.Core import *
import ks
import config

class View:

    @staticmethod
    def playback_for(user_id, entry_id, user_role):

        client  = ks.client_for_admin(user_id, "")

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
            .format(entry_id, entry_id, config.app_id, config.app_domain, user_id)

        kaltura_session = ks.ks_for_user(user_id, privileges)
        
        data = {
            "ks": kaltura_session, 
            "partner_id": config.partner_id,
            "uiconf_id": config.uiconf_id,
            "app_name": config.app_name,
            "user_id": user_id, 
            "user_role": user_role,
            "entry_id": entry_id
        }

        return data
