<template>
  <div>
    <b-loading is-full-page active v-if="loading_songs">
      <p>Songs:{{loading_songs}}</p> <br>
    </b-loading>
    <div v-else-if="songs_error">
      {{songs_error}}
    </div>
    <div v-else>
      <section>
        <h2 class="title is-2">Canciones</h2>
        <b-tabs position="is-left" class="block">
          <b-tab-item label="Canciones">
            <section>
              <b-select v-model="filter_selected" placeholder="Selecciona una fecha">
                <option
                    v-for="option in filters"
                    :value="option.value"
                    :key="option.value">
                  {{ option.label }}
                </option>
              </b-select>

              <b-table :data="songs.recordingStats">
                <b-table-column field="pictureUri" v-slot="props">
                  <figure class="image is-64x64">
                    <img :src="props.row.pictureUri" alt="Cover">
                  </figure>
                </b-table-column>
                <b-table-column field="trackName" label="Título" v-slot="props" sortable width="45%">
                  <router-link :to="{ name: 'MusicSong', params: { id: $route.params.id, song: props.row.trackUri.split(':')[2] }}">{{ props.row.trackName }}</router-link>
                </b-table-column>
                <b-table-column field="numListeners" label="Reproducciones" v-slot="props" sortable>
                  {{ props.row.numStreams }}
                </b-table-column>
                <b-table-column field="numListeners" label="Oyentes" v-slot="props" sortable>
                  {{ props.row.numListeners }}
                </b-table-column>
                <b-table-column label="Ratio Play/Oyente" v-slot="props" sortable>
                  {{ (props.row.numStreams / props.row.numListeners).toFixed(2) }}
                </b-table-column>
                <b-table-column field="numSavers" label="Saves" v-slot="props" sortable>
                  {{ props.row.numSavers }}
                </b-table-column>
                <b-table-column label="Ratio Save/Oyente" v-slot="props" sortable>
                  {{ ((props.row.numSavers / props.row.numListeners) * 100).toFixed(2) }}%
                </b-table-column>
                <b-table-column field="numCanvasViews" label="Reproducciones del canvas" v-slot="props">
                  {{ props.row.numCanvasViews }}
                </b-table-column>
                <b-table-column field="releaseDate" label="Fecha de lanzamientos" v-slot="props" sortable>
                  {{ props.row.releaseDate }}
                </b-table-column>
                <b-table-column field="trend" label="Trend" v-slot="props">
                  {{ props.row.trend }}
                </b-table-column>
              </b-table>

            </section>
          </b-tab-item>
          <b-tab-item label="Lanzamientos">
            <section>
            </section>
          </b-tab-item>
          <b-tab-item label="Playlists">
            <section>
            </section>
          </b-tab-item>
          <b-tab-item label="Próximamente">
            <section>
            </section>
          </b-tab-item>
        </b-tabs>
      </section>
      {{songs}}
    </div>
  </div>
</template>

<script>

export default {
  name: 'MusicSongs',
  data() {
    return {
      songs: null,
      loading_songs: true,
      songs_error: null,
      filters: [
        {
          label: 'Últimas 24h',
          value: '1day'
        },
        {
          label: 'Últimos 7d',
          value: '7day'
        },
        {
          label: 'Últimos 28d',
          value: '28day'
        },
        {
          label: 'Desde 2015',
          value: 'last5years'
        },
        {
          label: 'Todo el tiempo',
          value: 'all'
        }
      ],
      filter_selected: null
    }
  },
  methods:{
  },
  mounted() {
    this.filter_selected = this.filters[3].value

    let url = new URL(this.$api.songs)
    url.searchParams.append("id", this.$route.params.id)
    url.searchParams.append("filter", this.filter_selected)

    fetch(url, { credentials: 'include' })
        .then(response => {
          return response.json();
        })
        .then(data => {
          if(data.meta.code === 200) {
            this.songs = data.data
            this.loading_songs = false
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

  },
  watch:{
  }
}
</script>

<style scoped>

</style>
