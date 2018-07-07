/*
Track terms via twitter streaming api.

References:
https://github.com/campoy/justforfunc/tree/master/14-twitterbot
*/
package main

import (
	"bufio"
	"encoding/json"
	"flag"
	"fmt"
	"net/url"
	"os"
	"time"

	"github.com/ChimeraCoder/anaconda"
	"github.com/sirupsen/logrus"
)

var (
	api *anaconda.TwitterApi
	log = &logger{logrus.New()}

	// command-line flags
	tracking string
	filename string
	epochlen int

	// twitter auth
	consumerKey       = getenv("TWITTER_CONSUMER_KEY")
	consumerSecret    = getenv("TWITTER_CONSUMER_SECRET")
	accessToken       = getenv("TWITTER_ACCESS_TOKEN")
	accessTokenSecret = getenv("TWITTER_ACCESS_TOKEN_SECRET")
)

// LiveTweet : tweets structure specified by study group
type LiveTweet struct {
	CreatedAt     string                 `json:"created_at"`
	ExtendedTweet anaconda.ExtendedTweet `json:"extended_tweet"`
}

func init() {
	// init command line args
	flag.StringVar(&tracking, "track", "", "REQUIRED: Keywords to track. Specified by a quoted comma-separated list.")
	flag.StringVar(&filename, "filename", "out", "Filename prefix to save collected tweets to. File exstension not required.")
	flag.IntVar(&epochlen, "epochlen", 5000, "Number of tweets peer file.")
	flag.Parse()
	if tracking == "" {
		log.Fatal("Error: args for command flag `-track` are required. `-help` for more information.\n")
	}

	// init auth and set logger.
	anaconda.SetConsumerKey(consumerKey)
	anaconda.SetConsumerSecret(consumerSecret)
	api = anaconda.NewTwitterApi(accessToken, accessTokenSecret)
	api.SetLogger(log)
}

func main() {
	stream := api.PublicStreamFilter(url.Values{
		"track": []string{tracking},
	})
	defer stream.Stop()

	log.Infof("tracking terms: %s", tracking)

	i := epochlen
	f := newFile(filename)
	w := bufio.NewWriter(f)

	for v := range stream.C {
		tweet, ok := v.(anaconda.Tweet)
		if !ok {
			log.Warningf("recived unexpeted value of type %T", v)
			continue
		}
		// we dont want retweets tbh but also the full text is also
		// checked by the api but for some reason empty json structures
		// keept coming through so we dont want those either. anaconda bug?
		if tweet.RetweetedStatus != nil || tweet.ExtendedTweet.FullText == "" {
			continue
		}
		livetweet := &LiveTweet{
			CreatedAt:     tweet.CreatedAt,
			ExtendedTweet: tweet.ExtendedTweet,
		}
		b, err := json.Marshal(livetweet)
		check(err)
		_, err = w.Write(b)
		check(err)
		err = w.WriteByte('\n')
		check(err)
		w.Flush()
		// limit file sizes by specifying a number of tweets per file.
		// once this is reached here restart with another file.
		i--
		if i <= 0 {
			f.Close()
			i = epochlen
			f = newFile(filename)
			w = bufio.NewWriter(f)
		}
	}
	f.Close() // probally wont ever get here
}

type logger struct {
	*logrus.Logger
}

func (lg *logger) Critical(args ...interface{})                 { lg.Error(args...) }
func (lg *logger) Criticalf(format string, args ...interface{}) { lg.Errorf(format, args...) }
func (lg *logger) Notice(args ...interface{})                   { lg.Info(args...) }
func (lg *logger) Noticef(format string, args ...interface{})   { lg.Infof(format, args...) }

func newFile(filename string) *os.File {
	t := time.Now()
	filename = fmt.Sprintf("%s%d-%02d-%02dT%02d%02d%02d.ndjson",
		filename, t.Year(), t.Month(), t.Day(), t.Hour(), t.Minute(), t.Second())
	outfile, err := os.Create(filename)
	check(err)
	return outfile
}

func getenv(name string) string {
	v := os.Getenv(name)
	if v == "" {
		log.Fatalf("Error: Env variable %q is required.\n", name)
	}
	return v
}

func check(e error) {
	if e != nil {
		log.Fatalf("Error: %v\n", e)
	}
}
