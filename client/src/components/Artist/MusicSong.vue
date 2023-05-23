<template>
    <div>
    <b-loading is-full-page active v-if="loading_songs || loading_song || loading_song_public || loading_song_credits">
        <p>Songs:{{loading_songs}}</p> <br>
        <p>Song:{{loading_song}}</p> <br>
        <p>Song public:{{loading_song_public}}</p> <br>
        <p>Song credits:{{loading_song_credits}}</p>
    </b-loading>
    <div class="sidebar-page" v-else>
        <section class="sidebar-layout">
             <b-sidebar
                position="static"
                fullheight
                type="is-light"
                open
            >
                <div class="p-1">
                    <b-menu class="is-custom-mobile">
                        <b-menu-list>
                            <div v-for="(s, key) in songs.recordingStats" :key="key">

                                <b-menu-item>
                                    <template slot="label">
                                        <router-link :to="{ name: 'MusicSong', params: { id: $route.params.id, song: s.trackUri.split(':')[2] }}">
                                            <img class="image is-48x48" :src="s.pictureUri"/>
                                            {{ s.trackName }}
                                        </router-link>
                                    </template>
                                </b-menu-item>
                            </div>
                        </b-menu-list>
                    </b-menu>
                </div>
            </b-sidebar>

                <div class="p-1">
                    <div>
                        <h5 class="subtitle is-5 has-text-centered"><strong>Popularidad</strong><b-progress :value="song_public.popularity" show-value></b-progress></h5>
                        <div class="media">
                          <div class="media-left">
                            <figure class="image is-128x128">
                              <img :src="song_public.album.images[1].url" alt="Cover">
                            </figure>
                          </div>
                          <div class="media-content">
                            <p class="title is-4">{{song_public.name}}</p>
                            <p class="subtitle is-6">{{ main_artists.join(", ") }} <template v-if="feat_artists.length != 0">feat. {{ feat_artists.join(", ")}}</template></p>
                            <p class="subtitle is-6">{{ song.streams.totalStreams | toUSD }} reproducciones</p>
                          </div>
                        </div>
                        

                        <b-tabs position="is-centered" class="block">
                            <b-tab-item label="Canción">
                                <section>
                                    <h2 class="title is-2">Reproducciones en este periodo</h2>
                                    <p>{{song.graph}}</p>
                                    <p>{{song.summary}}</p>
                                </section>
                                
                                <section>
                                    <h2 class="title is-2">Fuente de las reproducciones (28 días)</h2>
                                    <p>{{song.source}}</p>
                                </section>
                                
                                <section>
                                    <h2 class="title is-2">Paises (28 días)</h2>
                                    <p>{{song.country}}</p>
                                </section>
                                
                                <section>
                                    <h2 class="title is-2">Ciudades (28 días)</h2>
                                    <p>{{song.city}}</p>
                                </section>
                                
                                {{song.canonical}}
                            </b-tab-item>
                            <b-tab-item label="Playlists">
                                <section>
                                    <h2 class="title is-2">Recientes</h2>
                                    <p>{{song["recent-playlists"]}}</p>
                                </section>
                                
                                <section>
                                    <h2 class="title is-2">TOP</h2>
                                    <p>{{song["top-playlists"]}}</p>
                                </section>
                            </b-tab-item>
                            <b-tab-item label="Credits">
                                <section>
                                    <div v-for="(role, key) in song_credits.roleCredits" :key="key">
                                        <h2 class="title is-2">{{role.roleTitle}}</h2>
                                        <div v-for="(artist, key2) in role.artists" :key="key2">
                                            <p>{{artist}}</p>
                                        </div>
                                    </div>
                                    <h2 class="title is-2">Label</h2>
                                    <p>{{song_credits.sourceNames.join(",")}}</p>
                                    <div v-if="song_credits.extendedCredits.length !== 0">
                                        <h2 class="title is-2">Extended credits</h2>
                                        <p>{{song_credits.extendedCredits}}</p>
                                    </div>
                                </section>
                            </b-tab-item>
                            <b-tab-item label="Lyrics">
                                <section>
                                    <p>{{song_lyrics}}</p>
                                </section>
                            </b-tab-item>
                        </b-tabs>
                      </div>

                </div>
        </section>
    </div>
    </div>


</template>

<script>

export default {
  name: 'MusicSong',
  data() {
    return {
        song: {},
        song_public: null,
        song_credits: null,
        song_lyrics: null,
        song_error: null,
        song_public_error: null,
        song_credits_error: null,
        song_lyrics_error: null,
        main_artists: null,
        feat_artists: null,
        loading_song: true,
        loading_song_public: true,
        loading_song_credits: true,
        loading_song_lyrics: true,
        fields: [
            'graph',
            'summary',
            'source',
            'country',
            'city',
            'streams',
            'canonical',
            'top-playlists',
            'recent-playlists'
        ],
        songs: null,
        loading_songs: true
    }
  },
  methods:{
  },
  mounted() {
    console.log("mounted")
    
    // SONG STATS
    let url = new URL(this.$api.song);
    url.searchParams.append("id", this.$route.params.id)
    url.searchParams.append("song", this.$route.params.song)
    url.searchParams.append("field", "")
       
    let requests = this.fields.map((field) => {
        url.searchParams.set("field", field)
        return new Promise((resolve) => {
          fetch(url, { credentials: 'include' })
              .then(response => {
                return response.json();
              })
              .then(data => {
                if(data.meta.code === 200){
                    this.song[field] = data.data
                } else
                    this.song_error = data.meta
                return resolve()
              })
              .catch(errors => {
                console.error(errors)
              }) 
        });
    })

    Promise.all(requests).then(() => this.loading_song = false).catch(errors => { 
        console.log(errors)
        this.loading_song = false
    });
    
    // SONG PUBLIC INFO
    url = new URL(this.$api.song_public)
    url.searchParams.append("id", this.$route.params.song)

    fetch(url, { credentials: 'include' })
      .then(response => {
        return response.json();
      })
      .then(data => {
        if(data.meta.code === 200){
            this.song_public = data.data
            
            let album_artists = data.data.album.artists.map((artist) => { return artist.name })
            let single_artists = data.data.artists.map((artist) => { return artist.name })
            
            this.main_artists = album_artists.filter(x => single_artists.includes(x));
            this.feat_artists = album_artists
                 .filter(x => !single_artists.includes(x))
                 .concat(single_artists.filter(x => !album_artists.includes(x)));
                 
        } else
            this.song_public_error = data.meta
        this.loading_song_public = false
      })
      .catch(errors => {
        console.error(errors)
      })
    
    // SONG CREDITS INFO
    url = new URL(this.$api.song_credits)
    url.searchParams.append("id", this.$route.params.song)
    fetch(url, { credentials: 'include' })
      .then(response => {
        return response.json();
      })
      .then(data => {
        if(data.meta.code === 200){
            this.song_credits = data.data
        } else
            this.song_credits_error = data.meta
        this.loading_song_credits = false
      })
      .catch(errors => {
        console.error(errors)
      })
      
    // SONG LYRICS INFO
    url = new URL(this.$api.song_lyrics)
    url.searchParams.append("id", this.$route.params.song)
    fetch(url, { credentials: 'include' })
      .then(response => {
        return response.json();
      })
      .then(data => {
        if(data.meta.code === 200){
            this.song_lyrics = data.data
        } else
            this.song_lyrics_error = data.meta
        this.loading_song_lyrics = false
      })
      .catch(errors => {
        console.error(errors)
      })
    
    // ARTIST SONGS LIST
    url = new URL(this.$api.songs)
    url.searchParams.append("id", this.$route.params.id)

    fetch(url, { credentials: 'include' })
      .then(response => {
        return response.json();
      })
      .then(data => {
        if(data.meta.code === 200){
            this.songs = data.data
            
            url = new URL(this.$api.song_public)
            let r = this.songs.recordingStats.map((song) => {
                url.searchParams.set("id", song.trackUri.split(":")[2])
                
                return new Promise((resolve) => {
                    fetch(url, { credentials: 'include' })
                      .then(response => {
                        return response.json();
                      })
                      .then(data => {
                        if(data.meta.code === 200){
                            song.releaseDate = data.data.album.release_date
                            return resolve()
                        }
                      })
                      .catch(errors => {
                        console.error(errors)
                      })
                  });
            });
            Promise.all(r).then(() => {
                this.songs.recordingStats.sort(function(first, second) {
                    return new Date(second.releaseDate) - new Date(first.releaseDate);
                })
                this.loading_songs = false
            });
                 
        } else {
            this.songs_error = data.meta
            this.loading_songs = false
        }
      })
      .catch(errors => {
        console.error(errors)
      })
  },
  updated(){
    console.log("updated")
    
  },
  watch:{

  },
  filters: {
    toUSD (value) {
      return Number(value).toLocaleString()
    }
  }
}
</script>
<style lang="scss">
.p-1 {
  padding: 1em;
}
.sidebar-page {
    display: flex;
    flex-direction: column;
    width: 100%;
    min-height: 100%;
    // min-height: 100vh;
    .sidebar-layout {
        display: flex;
        flex-direction: row;
        min-height: 100%;
        // min-height: 100vh;
    }
}
@media screen and (max-width: 1023px) {
    .b-sidebar {
        .sidebar-content {
            &.is-mini-mobile {
                &:not(.is-mini-expand),
                &.is-mini-expand:not(:hover) {
                    .menu-list {
                        li {
                            a {
                                span:nth-child(2) {
                                    display: none;
                                }
                            }
                            ul {
                                padding-left: 0;
                                li {
                                    a {
                                        display: inline-block;
                                    }
                                }
                            }
                        }
                    }
                    .menu-label:not(:last-child) {
                        margin-bottom: 0;
                    }
                }
            }
        }
    }
}
@media screen and (min-width: 1024px) {
    .b-sidebar {
        .sidebar-content {
            &.is-mini {
                &:not(.is-mini-expand),
                &.is-mini-expand:not(:hover) {
                    .menu-list {
                        li {
                            a {
                                span:nth-child(2) {
                                    display: none;
                                }
                            }
                            ul {
                                padding-left: 0;
                                li {
                                    a {
                                        display: inline-block;
                                    }
                                }
                            }
                        }
                    }
                    .menu-label:not(:last-child) {
                        margin-bottom: 0;
                    }
                }
            }
        }
    }
}
.is-mini-expand {
    .menu-list a {
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
}
</style>
