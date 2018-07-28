

## Relevence critera

- Name: + 1
    Does the name clearly indicate involvement with the movement.
    e.g. 'Black Lives Matter'
- claiming a Location or official + 2
    Is it a regional branch, specific sector or main organisation?
    e.g. 'Occupy Washington DC'
- Publically affilated activist with resonable size following or
    other activist group that may be related? + 1
- Description: + 3
    Does the description indicated involvment with the movement.
    e.g. 'The Official page for Occupy Washington DC at Freedom Plaza'
- Affliation and multi-issue: + 1
    Does the account reflect involvement with multiple or related campaigns.
- Website: + 2
    Are their affilated website links.
- Activity: + 1 / - 1
    Does the page have a resonable number of posts in light of the platform it is on.
- Image: + 2
    Does the image relate to the movement or is it
- Webpage: + 3 / - 3
    Does the content display active involvement in the movement.

tw_metoo.created_at  = pd.to_datetime(tw_metoo, format='%a %b %d %H:%M:%S +0000 %Y')
tw_blm.created_at    = pd.to_datetime(tw_blm, format='%a %b %d %H:%M:%S +0000 %Y')
tw_occupy.created_at = pd.to_datetime(tw_occupy, format='%a %b %d %H:%M:%S +0000 %Y')


tw_metoo.days  = (now - tw_metoo.created_at).dt.days
tw_blm.days    = (now - tw_blm.created_at).dt.days
tw_occupy.days = (now - tw_occupy.created_at).dt.days