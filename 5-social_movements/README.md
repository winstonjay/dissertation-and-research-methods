
## Requirements

From root directory of this repository if you have python and pip you can install all the requirements as follows:

    $ pip install -r py-requirements.txt

## Rebuilding dataset

**Authentication**

First get Twitter and YouTube authentication tokens from their [website](https://developer.twitter.com/en/docs), add them
into a `.env` file then a simple way to init them when you want is to run this command. This will need to be done each session.

    $ for line in $(cat .env); do export $line; done

**Collection**

Once authentication is set up and requirements are installed you can collect the data by running:

    $ make dataset

This will peform the same search queries to the platform API's.

**Content Analysis**

In the study pages were then filtered for relevence using human content analysis. There is a GUI application that helps to do this,
a basic interface is given in the gui to perform actions and more information is printed to the calling terminal.

    $ python contentserver.py <filepath> <platform>