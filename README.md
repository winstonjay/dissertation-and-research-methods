# Dissertation

## Contents

* 4 - Reactions to data scandals
    * 4.1.2 - data selection and reduction
    * 4.1.3 - analysis.
* 5 - Social movements
    * 5.1.2 - Platform search
    * 5.1.3 - Co-link analysis
    * 5.1.4 - Content analysis

## Setting up environment

Requires

    TWITTER_CONSUMER_KEY=your_twitter_consumer_key
    TWITTER_CONSUMER_SECRET=your_twitter_consumer_secret
    TWITTER_ACCESS_TOKEN=your_twitter_access_token
    TWITTER_ACCESS_TOKEN_SECRET=your_twitter_access_token_secret
    YOUTUBE_DEVELOPER_KEY=your_youtube_developer_key
    GUARDIAN_API_KEY=your_guardian_api_key


**Environment varibles** are needed to access specfic api's.

    $ for line in $(cat .env); do export $line; done

