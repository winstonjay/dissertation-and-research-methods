

## Relevence critera

- Name:
    Does the name clearly indicate involvement with the movement. Is it a regional branch,
    specific sector or main organisation.
    e.g. 'Occupy Washington DC'
- Description:
    Does the description indicated involvment with the movement.
    e.g. 'The Official page for Occupy Washington DC at Freedom Plaza'
- Affliation and multi-issue:
    Does the account reflect involvement with multiple or related campaigns.
- Website:
    Are their affilated website links.
- Activity:
    Does the page have a resonable numer of posts in light of the platform it is on.


tw_metoo.created_at  = pd.to_datetime(tw_metoo, format='%a %b %d %H:%M:%S +0000 %Y')
tw_blm.created_at    = pd.to_datetime(tw_blm, format='%a %b %d %H:%M:%S +0000 %Y')
tw_occupy.created_at = pd.to_datetime(tw_occupy, format='%a %b %d %H:%M:%S +0000 %Y')


tw_metoo.days  = (now - tw_metoo.created_at).dt.days
tw_blm.days    = (now - tw_blm.created_at).dt.days
tw_occupy.days = (now - tw_occupy.created_at).dt.days