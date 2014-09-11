from twython import Twython

APP_KEY = '3vojitMRV06dWGdMJDb1eWKI9'
APP_SECRET = 'fGhxVat5cXvro3IzEHyjauduNQpnO26FwD4hKSZwQ64ucnm9SJ'
OAUTH_TOKEN  = '41348505-3eby6GPwQMSkL1Lz2sXVYIKUrf2P2K2gvlabjc9Yr'
OAUTH_TOKEN_SECRET = '8kTWNymhcvmC5HDFphwiZgOH1j0ctVoW8GHbfXsFLCqeH'

api = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

coords                          =   []
MAX_ATTEMPTS                    =   10
COUNT_OF_TWEETS_TO_BE_FETCHED   =   500 

for i in range(0,MAX_ATTEMPTS):

    if(COUNT_OF_TWEETS_TO_BE_FETCHED < len(coords)):
        break # we got 500 tweets... !!

    #----------------------------------------------------------------#
    # STEP 1: Query Twitter
    # STEP 2: Save the returned tweets
    # STEP 3: Get the next max_id
    #----------------------------------------------------------------#

    # STEP 1: Query Twitter
    if(0 == i):
        # Query twitter for data. 
        results    = api.search(q="steelers",count='100')
    else:
        # After the first call we should have max_id from result of previous call. Pass it in query.
        results    = api.search(q="steelers",include_entities='true',max_id=next_max_id)

    # STEP 2: Save the returned tweets
    for result in results['statuses']:
        if result['coordinates'] is not None:
            coords.append(result['coordinates'])
            print(result['coordinates'])

    # STEP 3: Get the next max_id
    try:
        # Parse the data returned to get max_id to be passed in consequent call.
        next_results_url_params    = results['search_metadata']['next_results']
        next_max_id        = next_results_url_params.split('max_id=')[1].split('&')[0]
    except:
        # No more next pages
        break

print('coords')
print(coords)