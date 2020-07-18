# webcasting-integration-python

This is a sample Python app that demonstrates how to integrate the Kaltura Webcasting tool into your application. It includes event creation, working with metadata, launching the Kaltura Webcasting Studio, and most importantly, playing the webcast stream using the Kaltura Player. 

The complete documentation can be found [here](https://github.com/kaltura-vpaas/webcasting-integration).

### Setting Up The Application 

- Make sure you have Python 3 installed. 
- Install or import the Kaltura [Client Library](https://developer.kaltura.com/api-docs/Client_Libraries)
- Run `pip install -r requirements.txt` from within the project directory to install all dependencies. 

**Copy `config.template.py` onto `config.py` and set the below values**

- **partner_id (int)**: this can be found in the [integration settings](https://kmc.kaltura.com/index.php/kmcng/login)
- **admin_secret (string)**: this can be found in the [integration settings](https://kmc.kaltura.com/index.php/kmcng/login)
- **admin_email (string)**: the email address of the admin, most likely the account owner, used for object creation
- **service_url (string)**: Kaltura API endpoint ("https://www.kaltura.com/" for SaaS)
- **player_v2 (boolean)**: determines whether the application will use player v2 for playback - in the scenario that presentation slides are required in the live stream
- **uiconf_id (int)**: the ID of the v7 player to be used for playback. Can be found in the KMC [**TV STUDIO**](https://kmc.kaltura.com/index.php/kmcng/studio/v3) (can be left blank if `player_v2` is set to `True`)
- **uiconf_idv2 (int)**: the ID of the v2 player to be used for playback. Can be found in the KMC [**Universal STUDIO**](https://kmc.kaltura.com/index.php/kmcng/studio/v2). (Can be left blank if `player_v2` is set to `False`)

- **user_id (string)** = the identifying string of the end user who will be watching the stream. This value will most likely will come from a different part of the application 
- **moderator_user (string)** = the identifying string of the moderator who will be managing the Q&A flow

- **app_name (string)** = the name that appears on the Webcasting Studio App
- **app_id (string)** = application ID (used for analytics)
- **app_domain (string)** = domain name of the application

### Running The Application

`python3 main.py`

To use with Python 2.7, change the import statement in `view.py` from:

```python
from urllib.parse import urlencode
```

to:

```python
from urllib import urlencode
```


### About The Application 

#### main.py 

`main.py` contains the application routes. `/create` creates a new webcasting entry and returns webpage with options for the entry. `/view` takes the entry ID as a parameter and returns a webpage with the Kaltura Player embedded. `/moderator` takes the entry ID as a parameter and returns the URL for the moderator view. 

#### create.py 

A webcast instance is created using the configurations discussed in the guide and an Admin Kaltura Session. Metadata profiles are populated with webcast and event data. Links for downloading the Webcasting Studio are retrieved and displayed. The parameters for launching the application are populated and passed in the response. 

#### view.py 

`playback()` accepts an entry ID and checks whether it is live. If not, `livestream.redirectEntryId` and `livestream.recordedEntryId` are checked. If those members are also empty, the `media` API service is called to locate any recordings that were created from the live entry ID in question. If found, the entry ID is replaced. Otherwise, the entry ID remains the same. 

A user session is created and passed in the response, along with other values needed in order to embed the player with the live entry. 

`moderator_view()` takes the entry ID and creates a Kaltura Session (KS) that allows for moderation on the entry. The necessary parameters are encoded and added to the moderator view URL which is returned in the response. 
