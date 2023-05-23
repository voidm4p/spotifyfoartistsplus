<template>
    <div id="app">
      <div v-if="logged"><b-navbar centered type="is-black">
        <template slot="brand">
          <b-navbar-item tag="router-link" :to="{ name: 'Home' }">
            <inline-svg 
                    :src="require(`@/assets/images/spotify-for-artists.svg`)" 
                    @error="svgLoadError($event)"
                    width="300"
                    height="50" 
                    fill="black"
                    aria-label="Logo"
                ></inline-svg>++
          </b-navbar-item>
        </template>
        <template #start>
          <b-navbar-item tag="router-link" :to="{ name: 'Home' }">
                Inicio
          </b-navbar-item>
          <b-navbar-dropdown label="Música">
                <b-navbar-item tag="router-link" :to="{ name: 'MusicSongs' }">
                    Canciones
                </b-navbar-item>
                <b-navbar-item href="#">
                    Álbums
                </b-navbar-item>
                <b-navbar-item href="#">
                    Playlists
                </b-navbar-item>
                <b-navbar-item href="#">
                    Próximos lanzamientos
                </b-navbar-item>
            </b-navbar-dropdown>
          <b-navbar-dropdown label="Audiencia">
                <b-navbar-item href="#">
                    Reproducciones
                </b-navbar-item>
                <b-navbar-item href="#">
                    Oyentes
                </b-navbar-item>
                <b-navbar-item href="#">
                    Seguidores
                </b-navbar-item>
            </b-navbar-dropdown>
          <b-navbar-item tag="router-link" :to="{ name: 'Profile' }">
                Perfil
          </b-navbar-item>
        </template>
        <template #end>
            <b-navbar-item @click="logout">
                Cerrar sesión
            </b-navbar-item>
        </template>
      </b-navbar>
     <br></div>    
    
        <router-view></router-view>
    </div>
</template>

<script>
import InlineSvg from 'vue-inline-svg';
export default {
  name: 'app',
  components: {
    InlineSvg
  },
  data() {
    return {
        logged: false
    }
  },
  mounted() { // Called after the component is mounted (i.e. this is available)
    if(localStorage.getItem('jwt')){
        this.logged = true;
    }
  },
  updated() {
    if(localStorage.getItem('jwt')){
        this.logged = true;
    }
  },
  methods:{
    logout(){
        localStorage.removeItem('jwt')
        this.$router.go()
    }
  }
}
</script>

<style>


</style>
