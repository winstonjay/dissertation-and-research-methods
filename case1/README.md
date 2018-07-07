# INFORMATION SHOULD GO IN MY APPENDIXES

https://www.issuecrawler.net/svg2/issue4.php?id_session=o6apsjrknn3c9p42umfj990h54networkid347926

init env:

    $ for line in $(cat .env); do export $line; done

Used 'clean accounts' for searches to minimise personalisation.

### searches

    python twitter_search.py -o blm.ndjson "black lives matter OR blm" --limit=500
    python twitter_search.py -o occupy.ndjson "occupy" --limit=500
    python twitter_search.py -o metoo.ndjson  "meToo OR 'me too'" --limit=500

    python youtube_search.py -o blm.ndjson "black lives matter | blm" --limit=500
    python youtube_search.py -o occupy.ndjson "occupy" --limit=500
    python youtube_search.py -o metoo.ndjson "meToo | me too" --limit=500


    twitter_date_format = "Fri Jun 22 15:05:42 +0000 2018"
    youtube_date_format = "2007-03-07T15:08:16.000Z"

    twitter_date_format = '%a %b %d %H:%M:%S +0000 %Y'
    youtube_date_format = "%Y-%m-%dT%H:%M:%S.000Z"

## Twitter data sharing requiremnts:
https://developer.twitter.com/en/developer-terms/agreement-and-policy.html

section. 1:F.2 states that:

> "If you provide Twitter Content to third parties, including downloadable datasets of Twitter Content or an API that returns Twitter Content, you will only distribute or allow download of Tweet IDs, Direct Message IDs, and/or User IDs."

## Youtube data sharing policies:

https://developers.google.com/youtube/terms/api-services-terms-of-service

Less clear, concerns are around being transparent with the service.
Here we are using public data mainly from organisations that are tring to
promote a cause. Even so datasets will be provided as channel ID's to keep in
line with twitter.

## Facebook data sharing
https://developers.facebook.com/docs/graph-api/changelog/breaking-changes#search-4-4

https://developers.facebook.com/blog/post/2018/04/04/facebook-api-platform-product-changes/


## Wikipedia

https://en.wikipedia.org/wiki/Occupy_movement
https://en.wikipedia.org/wiki/Black_Lives_Matter
https://en.wikipedia.org/wiki/Me_Too_movement

