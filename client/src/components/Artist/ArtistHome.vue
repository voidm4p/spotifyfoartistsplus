<template>
    <section class="container is-fluid main-container">
      <h1 class="title is-1">{{artist_info.name}}</h1>
      <h5 class="subtitle is-5 has-text-centered"><strong>Popularidad</strong><b-progress :value="artist_info.popularity" show-value></b-progress></h5>
      <div class="columns reverse-row-order">
          <div class="column is-3">
            <h3 class="title is-3">Últimos 7 días</h3>
            <h4 class="title is-4">Audiencia</h4>
            <table class="table is-fullwidth">
                <tbody>
                    <tr>
                        <th>Oyentes</th>
                        <td class="has-text-right">{{artist_home.data.homestats.s4xinsightsapi.overview.listeners.deltaPct > 0 ? "+" : "" }}{{artist_home.data.homestats.s4xinsightsapi.overview.listeners.deltaPct | round(2) }}% ({{artist_home.data.homestats.s4xinsightsapi.overview.listeners.total}})</td>
                    </tr>
                    <tr>
                        <th>Reproducciones</th>
                        <td class="has-text-right">{{artist_home.data.homestats.s4xinsightsapi.overview.streams.deltaPct > 0 ? "+" : "" }}{{artist_home.data.homestats.s4xinsightsapi.overview.streams.deltaPct | round(2) }}% ({{artist_home.data.homestats.s4xinsightsapi.overview.streams.total}})</td>
                    </tr>
                    <tr>
                        <th>Seguidores</th>
                        <td class="has-text-right">{{artist_home.data.homestats.s4xinsightsapi.overview.followers.delta > 0 ? "+" : "" }}{{artist_home.data.homestats.s4xinsightsapi.overview.followers.delta}} ({{artist_home.data.homestats.s4xinsightsapi.overview.followers.total}})</td>
                    </tr>
                </tbody>
            </table>
            <h4 class="title is-4">Canciones TOP</h4>
            <b-table :data="artist_home.data.homestats.s4xinsightsapi.recordingStatsTable.recordingStatsList" :mobile-cards="false">
                <b-table-column field="picture" width="80" colspan="2">
                    <template v-slot:header="">
                        Nombre
                    </template>
                    <template v-slot="props">
                        <img class="image is-48x48" :src="props.row.pictureUri"/>
                    </template>
                </b-table-column>
                <b-table-column field="trackName" v-slot="props">
                    <router-link :to="{ name: 'MusicSong', params: { id: $route.params.id, song: props.row.trackUri.split(':')[2] }}">{{props.row.trackName}}</router-link>
                </b-table-column>
                <b-table-column field="numStreams">
                    <template v-slot:header="">
                        <b-tooltip label="Reproducciones" position="is-left">
                            <b-icon icon="play"></b-icon>
                        </b-tooltip>
                    </template>
                    <template v-slot="props">
                        {{props.row.numStreams}}
                    </template>
                </b-table-column>
                <b-table-column field="numListeners">
                    <template v-slot:header="">
                        <b-tooltip label="Oyentes" position="is-left">
                            <b-icon icon="user"></b-icon>
                        </b-tooltip>
                    </template>
                    <template v-slot="props">
                        {{props.row.numListeners}}
                    </template>
                </b-table-column>
                <b-table-column field="listenRate">
                    <template v-slot:header="">
                        <b-tooltip label="Ratio reproducciones/oyente" position="is-left">
                            <b-icon icon="percentage"></b-icon>
                        </b-tooltip>
                    </template>
                    <template v-slot="props">
                        {{props.row.numStreams/props.row.numListeners | round(2) }}
                    </template>
                </b-table-column>
                <b-table-column field="trend">
                    <template v-slot:header="">
                        <b-tooltip label="Trend" position="is-left">
                            <b-icon icon="chart-line"></b-icon>
                        </b-tooltip>
                    </template>
                    <template v-slot="props">
                        {{props.row.trend}}
                    </template>
                </b-table-column>
            </b-table>
            <h4 class="title is-4">Playlists donde más te escuchan</h4>
            <b-table :data="artist_home.data.homestats.s4xinsightsapi.playlistCollection.dataList" :mobile-cards="false">
                <b-table-column field="picture" width="80" colspan="2">
                    <template v-slot:header="">
                        Nombre
                    </template>
                    <template v-slot="props">
                        <img class="image is-48x48" :src="props.row.thumbnailUrl"/>
                    </template>
                </b-table-column>
                <b-table-column field="title" v-slot="props">
                    <a :href="`https://open.spotify.com/playlist/${props.row.uri.split(':')[2]}`" target="_blank">{{props.row.title}}</a>
                    <p>{{props.row.followers == -1 ? "-" : `${props.row.followers} seguidores`}}</p>
                </b-table-column>
                <b-table-column field="numStreams">
                    <template v-slot:header="">
                        <b-tooltip label="Reproducciones" position="is-left">
                            <b-icon icon="play"></b-icon>
                        </b-tooltip>
                    </template>
                    <template v-slot="props">
                        {{props.row.streams}}
                    </template>
                </b-table-column>
                <b-table-column field="numListeners">
                    <template v-slot:header="">
                        <b-tooltip label="Oyentes" position="is-left">
                            <b-icon icon="user"></b-icon>
                        </b-tooltip>
                    </template>
                    <template v-slot="props">
                        {{props.row.listeners}}
                    </template>
                </b-table-column>
                <b-table-column field="listenRate">
                    <template v-slot:header="">
                        <b-tooltip label="Ratio reproducciones/oyente" position="is-left">
                            <b-icon icon="percentage"></b-icon>
                        </b-tooltip>
                    </template>
                    <template v-slot="props">
                        {{props.row.streams/props.row.listeners | round(2) }}
                    </template>
                </b-table-column>
            </b-table>
          </div>
          <div class="column is-9">
              <div class="columns is-multiline">
                <div class="column is-4" v-for="card in artist_home.data.homestats.cards.cardsList" :key="card">
                    <div class="card">
                        <div class="card-image">
                            <figure class="image is-3by3">
                              <img :src="card.displayCard.header">
                            </figure>
                        </div>
                        <div class="card-content">
                            <div class="media">
                              <div class="media-content">
                                <p class="title is-4">{{card.displayCard.title}}</p>
                                <p class="subtitle is-6">{{card.displayCard.subtitle}}</p>
                                <p>Fuente: {{card.cardSource}}</p>
                                <p>Tipo: {{card.cardType}}</p>
                              </div>
                            </div>
                            <a :href="card.displayCard.callToAction.url" target="_blank">{{card.displayCard.callToAction.text}}</a>

                        </div>
                    </div>
                </div>
              </div>
          </div>
      </div>
  </section>
</template>

<script>

export default {
  name: 'Search',
  data() {
    return {
        artist_home: null,
        artist_info: null
    }
  },
  methods:{
  },
  mounted() {
    console.log("mounted")
    let url = new URL(this.$api.artist_home);
    url.searchParams.append("id", this.$route.params.id)

    fetch(url, { credentials: 'include' })
          .then(response => {
            return response.json();
          })
          .then(data => {
            if(data.meta.code == 200)
                this.artist_home = data.data
            else
                this.team_error = data.meta
          })
          .catch(errors => {
            console.error(errors)
          })
          
    url = new URL(this.$api.artist_info_public);
    url.searchParams.append("id", this.$route.params.id)

    fetch(url, { credentials: 'include' })
          .then(response => {
            return response.json();
          })
          .then(data => {
            if(data.meta.code == 200)
                this.artist_info = data.data
            else
                this.team_error = data.meta
          })
          .catch(errors => {
            console.error(errors)
          })
  },
  updated(){
    console.log("updated")
    
  },
  watch:{

  }
}
</script>

<style scoped>
@media only screen and (min-width: 769px) {
   .reverse-row-order{
     flex-direction:row-reverse;
   }
}
.b-table .table th .th-wrap .icon {
    margin-left: 0;
}
</style>
