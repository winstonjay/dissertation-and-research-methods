
# --- collecting dataset ------------------------------------------------------

TWITTER_ROOT := data/twitter
YOUTUBE_ROOT := data/youtube

dataset: tw_occupy tw_metoo yt_blm
	@echo "INFO: run contentserver.py --help for info on how to run content analysis UI"

yt_blm: yt_dir
	python youtube_search.py -o $(YOUTUBE_ROOT)/blm/blm.ndjson "black lives matter, blm" --limit=200
yt_occupy: yt_dir
	python youtube_search.py -o $(YOUTUBE_ROOT)/occupy/occupy.ndjson "occupy" --limit=500
yt_metoo: yt_dir
	python youtube_search.py -o $(YOUTUBE_ROOT)/metoo/metoo.ndjson "meToo me too" --limit=500

tw_blm: tw_dir
	python twitter_search.py -o $(TWITTER_ROOT)/blm/blm.ndjson "black lives matter, blm" --limit=200
tw_occupy: tw_dir
	python twitter_search.py -o $(TWITTER_ROOT)/occupy/occupy.ndjson "occupy" --limit=500
tw_metoo: tw_dir
	python twitter_search.py -o $(TWITTER_ROOT)/metoo/metoo.ndjson "meToo me too" --limit=500

tw_dir:
	mkdir -p $(TWITTER_ROOT)/blm $(TWITTER_ROOT)/occupy $(TWITTER_ROOT)/metoo
yt_dir:
	mkdir -p $(YOUTUBE_ROOT)/blm $(YOUTUBE_ROOT)/occupy $(YOUTUBE_ROOT)/metoo