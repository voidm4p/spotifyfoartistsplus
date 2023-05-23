<template>
  <div v-if="searchResults">
    {{search}}
    {{$route.params.search}}
    <h2 class="subtitle">Resultado principal:</h2>
    <div class="columns is-mobile is-centered">
      <div class="column is-4">
      </div>
    </div>

    <div class="columns is-mobile is-multiline">
      <div class="column is-6">
        <h2 class="subtitle">Canciones:</h2>
        <div class="columns is-multiline">
          <div v-for="match in searchResults.tracks.items" v-bind:key="match.id" class="column is-6">
            <article class="media">
              <figure class="media-left">
                <p class="image is-64x64">
                  <img :src="match.album.images[match.album.images.length - 1].url">
                </p>
              </figure>
              <div class="media-content">
                <div class="content">
                  <p>
                    <strong>{{match.name}}</strong>
                    <br>
                    {{match.artists.map((item) => { return item.name}).join(", ")}}
                  </p>
                </div>
              </div>
            </article>
          </div>
        </div>
      </div>
      <div class="column is-6" v-if="searchResults.artists.items.length !== 0">
        <h2 class="subtitle">Artistas:</h2>
        <div class="columns is-multiline">
          <div v-for="match in searchResults.artists.items" v-bind:key="match.id" class="column is-2">
            <article class="has-text-centered">
              <figure class="thumbnail has-image-centered is-rounded">
                <img class="portrait" :src="match.images[match.images.length - 1].url">
              </figure>
              <p>{{match.name}}</p>
            </article>
          </div>
        </div>
      </div>


      <div class="column is-6" v-if="searchResults.albums.items.length !== 0">
        <h2 class="subtitle">Albums:</h2>
        <div class="columns is-multiline">
          <div v-for="match in searchResults.albums.items" v-bind:key="match.id" class="column is-4">
            <article class="media">
              <figure class="media-left">
                <p class="image is-64x64">
                  <img :src="match.images[match.images.length - 1].url">
                </p>
              </figure>
              <div class="media-content">
                <div class="content">
                  <p>
                    <strong>{{match.name}}</strong>
                    <br>
                    {{match.artists.map((item) => { return item.name}).join(", ")}}
                  </p>
                </div>
              </div>
            </article>
          </div>
        </div>
      </div>

      <div class="column is-6" v-if="searchResults.playlists.items.length !== 0">
        <h2 class="subtitle">Playlists:</h2>
        <div class="columns is-multiline">
          <div v-for="match in searchResults.playlists.items" v-bind:key="match.id" class="column is-4">
            <article class="media">
              <figure class="media-left">
                <p class="image is-64x64">
                  <img :src="match.images[match.images.length - 1].url">
                </p>
              </figure>
              <div class="media-content">
                <div class="content">
                  <p>
                    <strong>{{match.name}}</strong>
                    <br>
                    {{match.owner.display_name}}
                    <br>
                    <small class="is-italic">@{{match.owner.id}}</small>
                  </p>
                </div>
              </div>
            </article>
          </div>
        </div>
      </div>
    </div>

  </div>

</template>

<script>

export default {
  name: 'Search',
  data() {
    return {
      search: "",
      awaitingSearch: false,
      searchResults: null
    }
  },
  methods:{
  },
  mounted() {
    console.log("mounted")
    this.search = this.$route.params.search
  },
  updated(){
    console.lof("updated")
    this.search = this.$route.params.search

    if(this.search !== "" && this.search !== undefined){
      if (!this.awaitingSearch) {
        setTimeout(() => {
          fetch("http://127.0.0.1:5000/spotify/search?q=" + this.search)
              .then(response => {
                return response.json();
              })
              .then(data => {
                this.searchResults = data
                this.awaitingSearch = false;
              })
              .catch(errors => {
                console.error(errors)
                this.awaitingSearch = false;
              })
        }, 2000); // 1 sec delay
      }
      this.awaitingSearch = true;
    }
  },
  watch:{
    '$route.arams.search': function (search) {
      console.log(search)
    }
  }
}
</script>

<style scoped>

</style>