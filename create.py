from KalturaClient import *
from KalturaClient.Plugins.Core import *
from KalturaClient.Plugins.Metadata import *
from datetime import datetime, timedelta
import ks
import json
import config 
from time import time 

class Livestream:

    @staticmethod
    def create():

        client  = ks.client_for_admin(config.admin_email, "")

        # CREATE LIVESTREAM ENTRY

        live_stream_entry = KalturaLiveStreamEntry()
        live_stream_entry.name = "Webcast Tutorial"
        live_stream_entry.description = "This is a test webcast"
        live_stream_entry.mediaType = KalturaMediaType.LIVE_STREAM_FLASH
        live_stream_entry.dvrStatus = KalturaDVRStatus.ENABLED
        live_stream_entry.dvrWindow = 60
        live_stream_entry.sourceType = KalturaSourceType.LIVE_STREAM
        live_stream_entry.adminTags = "vpaas-webcast"
        live_stream_entry.pushPublishEnabled = KalturaLivePublishStatus.DISABLED
        live_stream_entry.explicitLive = KalturaNullableBoolean.TRUE_VALUE
        live_stream_entry.recordStatus = KalturaRecordStatus.PER_SESSION
        live_stream_entry.conversionProfileId = 0000000
        live_stream_entry.recordingOptions = KalturaLiveEntryRecordingOptions()
        live_stream_entry.recordingOptions.shouldCopyEntitlement = KalturaNullableBoolean.TRUE_VALUE
        live_stream_entry.recordingOptions.shouldMakeHidden = KalturaNullableBoolean.TRUE_VALUE
        live_stream_entry.recordingOptions.shouldAutoArchive = KalturaNullableBoolean.TRUE_VALUE

        source_type = KalturaSourceType.LIVE_STREAM

        result = client.liveStream.add(live_stream_entry, source_type)

        live_stream_entry = result.id

        # LIVESTREAM METADATA 

        ## retrieve profile ID for KMS_WEBCAST2

        pager = KalturaFilterPager()
        filter = KalturaMetadataProfileFilter()
        filter.systemNameEqual = "KMS_KWEBCAST2"

        result = client.metadata.metadataProfile.list(filter, pager)
        kms_metadata_profile_id = result.objects[0].id

        ## add data to profile 

        xml_data = '<?xml version="1.0"?><metadata><SlidesDocEntryId></SlidesDocEntryId>' \
        '<IsKwebcastEntry>1</IsKwebcastEntry><IsSelfServe>1</IsSelfServe></metadata>'

        object_type = KalturaMetadataObjectType.ENTRY

        result = client.metadata.metadata.add(kms_metadata_profile_id, object_type, live_stream_entry, xml_data)

        kms_metadata_record_id = result.id

        ## retrieve profile ID for KMS_EVENTS3

        pager = KalturaFilterPager()
        filter = KalturaMetadataProfileFilter()
        filter.systemNameEqual = "KMS_EVENTS3"
        result = client.metadata.metadataProfile.list(filter, pager)
        events_metadata_profile_id = result.objects[0].id

        presenter_name = "John Doe"
        webcast_start_date = datetime.now()+timedelta(minutes=2)
        webcast_end_date = datetime.now()+timedelta(minutes=10)

        xml_data = '<?xml version="1.0"?><metadata><StartTime>{}</StartTime>' \
        '<EndTime>{}</EndTime><Timezone>Asia/Jerusalem</Timezone>' \
        '<Presenter><PresenterId>8723792</PresenterId><PresenterName>{}</PresenterName>' \
        '<PresenterTitle>CEO and Chairman</PresenterTitle><PresenterBio>Awesome biography here</PresenterBio>' \
        '<PresenterLink>https://www.linkedin.com/in/john.doe</PresenterLink>' \
        '<PresenterImage>https://speakerheadshot.com/image.png</PresenterImage></Presenter></metadata>' \
        .format(int(webcast_start_date.strftime("%s")), int(webcast_end_date.strftime("%s")), presenter_name)

        object_type = KalturaMetadataObjectType.ENTRY
        result = client.metadata.metadata.add(events_metadata_profile_id, object_type, live_stream_entry, xml_data)

        event_metadata_record_id = result.id

        ## get download links 

        filter = KalturaUiConfFilter()
        filter.objTypeEqual = KalturaUiConfObjType.WEBCASTING
        pager = KalturaFilterPager()

        result = client.uiConf.listTemplates(filter, pager)
        first = result.objects[0]
        configuration = json.loads(first.config)

        mac_download_url = configuration['osx']['recommendedVersionUrl']
        win_download_url = configuration['windows']['recommendedVersionUrl']

        # PREPARE LAUNCH PARAMS 

        ## kaltura session for launch 

        privileges = "setrole:WEBCAST_PRODUCER_DEVICE_ROLE,sview:*,list:{},download:{}" \
            .format(live_stream_entry, live_stream_entry)

        kaltura_session = ks.ks_for_user(config.moderator_user, privileges)

        ## conversion profile ID

        filter = KalturaConversionProfileFilter()
        pager = KalturaFilterPager()
        result = client.conversionProfile.list(filter, pager)

        conversion_profile_id = result.objects[0].id

        ## player ui conf ID 

        filter = KalturaUiConfFilter()
        filter.nameLike = "MediaSpace Webcast Player"
        pager = KalturaFilterPager()

        result = client.uiConf.list(filter, pager)
        player_ui_conf_id = result.objects[0].id

        ## CREATE LAUNCH PARAMS DICT

        launch_params = {
            "ks": kaltura_session,
            "ks_expiry": (datetime.now()+timedelta(days=1)).strftime("%Y-%d-%d%Z%H:%M:%S%z"),
            "MediaEntryId": live_stream_entry,
            "serverAddress": config.service_url,
            "eventsMetadataProfileId": events_metadata_profile_id,
            "kwebcastMetadataProfileId": kms_metadata_profile_id,
            "appName": config.app_name,
            "logoUrl": "https://picsum.photos/200",
            "fromDate": webcast_start_date,
            "toDate": webcast_end_date,
            "userId": config.moderator_user,
            "QnAEnabled": True,
            "pollsEnabled": True,
            "userRole": "adminRole", 
            "playerUIConf": player_ui_conf_id,
            "presentationConversionProfileId": conversion_profile_id,
            "referer": config.app_domain,
            "debuggingMode": False, 
            "verifySSL": True,
            "selfServeEnabled": True,
            "appHostUrl": '',
            "instanceProfile": config.app_name
        }

        data = {
            "entry_id": live_stream_entry,
            "mac_download": mac_download_url,
            "windows_download": win_download_url,
            "launch_params": launch_params
        }

        return data



