# Spotify for Artists Plus

Unofficial API for Spotify For Artists built by reverse engineering their endpoints

I also built a custom VueJS Frontend trying to replicate the look of the original but adding some extra features that the API contains but original Frontend is not showing.

## Frontend

![Selection_882](https://github.com/voidm4p/spotifyfoartistsplus/assets/33087100/c4d015ae-f260-43f6-851b-ff5c47239077)

![Selection_881](https://github.com/voidm4p/spotifyfoartistsplus/assets/33087100/6b99b5c4-213c-4f99-8a50-3b4f7b4a2c53)

![Selection_880](https://github.com/voidm4p/spotifyfoartistsplus/assets/33087100/2c9ba3f3-7127-456b-ad50-5a3686e59289)


## API

### Endpoint: https://generic.wg.spotify.com

```
"s4x-me/v0/me"
"marketplace-mgmt/v1/team/manageteam"
"s4x-me/v0/artists"
"marketplace-mgmt/v0/settings"
"s4x-insights-api/v1/artist/{}/permissions".format(artist_id)
"s4x-home-service/v1/artist/{}/home".format(artist_id)
"roster-view-service/v1/artists?offset=0"
"nms-form/v1/artist/{}/album/{}/view?utm_source=home".format(artist_id, album_id)
"s4x-insights-api/v2/artist/{}/recordings".format(artist_id)
"s4x-insights-api/v1/artist/{}/releases/released".format(artist_id)
"s4x-insights-api/v1/artist/{}/playlists/{}".format(artist_id, type)
"upcoming-view-service/v1/artist/{}/catalog".format(artist_id)
"canvaz-view/v1/artist/{}/canvas?uris=spotify:track:{}".format(artist_id, song_id)
"s4x-insights-api/v1/artist/{}/recording/{}/{}".format(artist_id, song_id, fields[field])
"s4x-insights-api/v1/artist/{}/audience/{}/{}".format(artist_id, fields[field], artist_id)
"artist-identity-view/v2/profile/{}".format(artist_id)
```

### Endpoint: https://spclient.wg.spotify.com

```
"track-credits-view/v0/experimental/{}/credits".format(song_id)
"color-lyrics/v2/track/{}/image/{}".format(track_id, quote(image_url, safe=''))
```
    
### Endpoint: https://api.spotify.com/v1

```
"artists/{}".format(artist_id)
"tracks/{}".format(song_id)
"artists/{}/related-artists".format(artist_id)
```

### Endpoint: https://api-partner.spotify.com

```
"operationName": "queryArtistOverview",
```
