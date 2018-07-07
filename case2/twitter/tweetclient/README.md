# Twitter Data Collection Tool

Program tracks terms with twitters [streaming API](https://developer.twitter.com/en/docs) and saves them into a series of timestamped `.ndjson` ([newline delimited json](http://ndjson.org/)) files.

### Building & Running Locally

To run, first get twitter authentication tokens from their [website](https://developer.twitter.com/en/docs), add them
into a `.env` file then a simple way to init them when you want is to run this command.

    $ for line in $(cat .env); do export $line; done

If the dependencies (`github.com/ChimeraCoder/anaconda`, `github.com/sirupsen/logrus`) are installed
you should be able run simply by:

    $ go run main.go -track "foo,bar,har har"

To see all the command flags just add `-help` for more info.

### Running with systemd on server

Compile `main.go` to the desired system architecture with something like:

    $ GOOS=linux go build -o tweetclient

Now just transfer the binary to your server and create a file like shown in `example.service` adding
you details and twitter authentication tokens. Systemd file also needs putting in the right directory.

    $ sudo mv tweet.service /etc/systemd/system/

Once this is done we can enable the service.

    $ sudo systemctl enable tweet

To check the status of this service:

    $ sudo systemctl status tweet

To `stop`/`start`:

    $ sudo systemctl <your_cmd_here> tweet

Because of the settings described in the `example.service` file the program should
automatically rsetart everytime it crashes.

References: https://github.com/campoy/justforfunc/tree/master/14-twitterbot