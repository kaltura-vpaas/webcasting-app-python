# webcasting-integration-python

This is a sample app written in python3 that demonstrates how to integrate the Kaltura Webcasting tool into your application. It includes event creation, working with metadata, launching the Kaltura Webcasting Studio, and most importantly, playing the webcast stream using the Kaltura Player. 

The complete documentation can be found [here](https://github.com/kaltura-vpaas/webcasting-integration)

### Setting Up The Application 

- Make sure you have python3 installed. 
- Install or import the Kaltura [Client Library](https://developer.kaltura.com/api-docs/Client_Libraries)
- Run `pip install -r requirements.txt` from within the project directory to install all dependencies. 

**You'll need to add credentials to the `config.py` file:**

- partner_id (int): this can be found in the [integration settings](https://kmc.kaltura.com/index.php/kmcng/login)
- admin_secret (string): this can be found in the [integration settings](https://kmc.kaltura.com/index.php/kmcng/login)
- admin_email (string): the email address of the admin, most likely the account owner, used for object creation.
- user_id (string): this is any identifying string, such as your name or email address 
- service_url (string): "https://www.kaltura.com/" - can be changed for onprem 
- uiconf_id: this is the ID of the player you'll be using for livestream playback. Can be found in the KMC [Studio](https://kmc.kaltura.com/index.php/kmcng/studio/v3)

- user_id (string) = the identifying string of the end user who will be watching the playback. This value will most likely will come from a different part of the application 
- moderator_user (string) = the identifying string of the moderator who will be managing the Q&A flow. 

- app_name = The name that appears on the Webcasting Studio App
- app_id = Application ID used for analytics 
- app_domain = Domain name of the application

### Running The Application

```python3 main.py```

To use with python2.7, replace the import statement in **view.py**:

```from urllib.parse import urlencode```

with

```from urllib import urlencode```

### About The Application 

#### main.py 

`main.py` contains the application routes. `/create` creates a new webcasting entry and returns webpage with options for the entry. `/view` takes the entry ID as parameter and returns a webpage with the Kaltura Player embedded. `/moderator` takes the entry ID as parameter and returns the URL for the moderator view. 

#### create.py 

A webcast instance is created using the configurations discussed in the guide and an Admin Kaltura Session. Metadata profiles get populated with webcast and event data. Links for downloading the Webcasting Studio are retrieved and created. The parameters for launching the application are prepared and passed in the response. 

#### view.py 

**playback()** takes the entry ID and checks if it is live. If not, the redirect and recorded entry IDs are checked. If those are also empty, the media API is called to look for any recordings that may have resulted from this session, assuming it is complete. If any of these exist, the entry ID is replaced. Otherwise, the entry ID remains the same. 

A user session is created and passed in the response, along with other values needed in order to embed the player with the live entry. 

**moderator_view** takes the entry ID and creates a Kaltura Session that allows for moderation on the entry. The necessary parameters are encoded and added to the moderator view URL which is returned in the response. 