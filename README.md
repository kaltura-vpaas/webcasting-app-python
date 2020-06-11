# webcasting-integration-python

This is a sample app written in python3 that demonstrates how to integrate the Kaltura Webcasting tool into your application. It includes event creation, working with metadata, launching the Kaltura Webcasting Studio, and most importantly, playing the webcast stream using the Kaltura Player. 

The complete documentation can be found [here](https://github.com/kaltura-vpaas/webcasting-integration)

### Running The Application 

- Make sure you have python3 installed. 
- Install or import the Kaltura [Client Library](https://developer.kaltura.com/api-docs/Client_Libraries)
- Run `pip install -r requirements.txt` from within the project directory to install all dependencies. 

**You'll need to add credentials to the `config.py` file:**

- partner_id: this can be found in the [integration settings](https://kmc.kaltura.com/index.php/kmcng/login)
- admin_secret: this can be found in the [integration settings](https://kmc.kaltura.com/index.php/kmcng/login)
- user_id: this is any identifying string, such as your name or email address 
- service_url: "https://www.kaltura.com/" - can be changed for onprem 
- uiconf_id: this is the ID of the player you'll be using for livestream playback. Can be found in the KMC [Studio](https://kmc.kaltura.com/index.php/kmcng/studio/v3)

- app_name = The name that appears on the Webcasting Studio App
- app_id = Application ID used for analytics 
- app_domain = Domain name of the application

You can run the application with `python3 main.py`
