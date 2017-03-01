### Getting Started
This is the main repository for the devops.center demo.  The intent is to show how to use our utilities
to bring up a local development environment using docker containers.  

There are two main sections, Creating the development environment and Joining existing development

### Creating the environment

1. Create a directory dcDemo somewhere on your local machine

    - cd $HOME/some/place  (NOTE: this is up to you where you want to put it, regardless you will use it later)
    - mkdir dcDemo
    - cd dcDemo
    - mkdir utils apps

2. Clone the devops.center dcUtils repository into the utils directory

    - cd utils
    - git clone https://github.com/devopscenter/dcUtils.git
    - cd dcUtils

    Next we need to create the directory structure for the application.  This is done by using the
    devops.center manageApp.py utility.  This will create a directory structure at a given directory
    and will contain various configurations appropriate and specific to the application.  The options
    for the create are:

        --appName (-a)       => the application name
        --baseDirectory (-d) => the base directory into which the application will be placed
        --command (-c)       => the command, in this case create

    So type (NOTE: use the path created in step 1):

    - ./manageApp.py -a dcDemoBlog -d $HOME/some/place/dcDemo/apps -c create

        - accept the naming of the web portion of the application (default appName-web => dcDemoBlog-web)
        - enter  000000 as the unique stack name as this is the image that has all the appropriate python/django code already installed

3. Now create the environment variables that are specific to our environment.

    - edit dcDemoBlog-utils/environments/personal.env => change dcUTILS value as appropriate
    - edit dcDemoBlog-utils/environments/personal.env => change LOG_NAME value as appropriate
    - edit dcDemoBlog-utils/environments/local.env => change SYSLOG entries as appropriate
        - we use papertrail for a central logging system so the default values in the SYSLOG_ entries refer to that system but you
          put your logging system in there.  They do need to have something in them, hence the defaults.

    - execute:

        ./deployenv.sh

4. And start the containers:

       ./start.sh

5. When the containers start up, the web container will have the dcDemoBlog/dcDemoBlog-web directory hosted as a volume in the container and
the login directory will correspond with that directory.  

The login directory is: /data/deploy/current   


When you log in there won't be anything in that directory since there isn't anything in the dcDemoBlog/dcDemoBlog-web directory.  At this point,
a good suggestion would be to open another terminal window such that you can log into the web container in one terminal window.  This way you
can run the commands to create the django project inside the container, and then once they are created you can edit the files on your host using
your normal editing tools.  The changes will show up in the container and the hosts because they refer to the same place.

To enter the container:

    - execute:

        ./enter-container.sh
            - Select the web container

For the dcDemoBlog I took a sample django blog tutorial and did all the steps directly in the container.
For this demo a simple django blog will be created from a tutorial found at:

http://www.creativebloq.com/netmag/get-started-django-7132932

NOTE: in order for the django server to show up in the browser, when you execute the runserver add 0.0.0.0:8000:
    python manage.py runserver 0.0.0.0:8000


After getting the blog up and working the next step was to exit the containers
and push the work that was done in dcDemoBlog-web and dcDemoBlog-utils to
github.  


### Joing existing development

1. Create a directory dcDemo somewhere on your local machine

    - cd $HOME/some/place  (NOTE: this is up to you where you want to put it, regardless you will use it later)
    - mkdir dcDemo
    - cd dcDemo
    - mkdir utils apps

2. Clone the devops.center dcUtils repository into the utils directory

    - cd utils
    - git clone https://github.com/devopscenter/dcUtils.git
    - cd dcUtils

    Next we need to create the directory structure for the application.  This is done by using the
    devops.center manageApp.py utility.  This will create a directory structure at a given directory
    and will contain various configurations appropriate and specific to the application.  The options
    for the create are:

        --appName (-a)       => the application name
        --baseDirectory (-d) => the base directory into which the application will be placed
        --command (-c)       => the command, in this case create
        --appURL             => the github URL for the application web content
        --utilsURL           => the github URL for the application utils content

    So type (NOTE: use the path created in step 1):

        ./manageApp.py -a dcDemoBlog -d ~/dcDemo/apps -c join --appURL \
            https://github.com/devopscenter/dcDemoBlog-web.git --utilsURL \
            https://github.com/devopscenter/dcDemoBlog-utils.git


3. Now create the environment variables that are specific to our environment.

    - edit dcDemoBlog-utils/environments/personal.env => change dcUTILS value as appropriate
    - edit dcDemoBlog-utils/environments/personal.env => change LOG_NAME value as appropriate
    - edit dcDemoBlog-utils/environments/local.env => change SYSLOG entries as appropriate
        - we use papertrail for a central logging system so the default values in the SYSLOG_ entries refer to that system but you
          put your logging system in there.  They do need to have something in them, hence the defaults.

    - execute:

        ./deployenv.sh

4. And start the containers:

       ./start.sh


5. When the containers start up, the web container will have the dcDemoBlog/dcDemoBlog-web directory hosted as a volume in the container and
the login directory will correspond with that directory.  The login directory is: /data/deploy/current   
At this point, a good suggestion would be to open another terminal window such that you can log into the web container in one terminal window.
This way you can run the commands to create the django project inside the container, and then once they are created you can edit the files on
your host using your normal editing tools.  The changes will show up in the container and the hosts because they refer to the same place.

    To enter the container:

        ./enter-container.sh
            - Select the web container

    You will need to create the database the very first time you bring down the images and start the containers as the database will be empty.  
    Outside of this demo, you would restore a database from a backup at this point to get it up to speed. In this case we want to start with an
    empty database, but we at least need to create one.  So type:

        echo "create database dcdemoblog" | psql -U postgres

    and then we need to tell the django project about the database, so type:

        - python manage.py syncdb

            - answer yes to create a new superuser for the app
            - Username press return to accept root or type in what you want
            - Press enter for the email to leave blank or put in your email address
            - Password put in something that you will remember

        Now run the server:

            python manage.py runserver 0.0.0.0:8000

6. and when you are done exit from the container and stop the demo containers:
    cd dcUtils
    ./stop.sh
