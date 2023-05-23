<template>
 <div>
    <section class="container is-fluid main-container">
          <h1 class="title is-1">Todos tus artistas</h1>
          <div v-if="roster_error">
            <b-notification
                icon-pack="fas"
                type="is-danger"
                has-icon
                aria-close-label="Close notification"
                role="alert">
                <h4 class="title is-4">{{this.roster_error.code}} - {{this.roster_error.error_type}}</h4>
                <p>{{this.roster_error.error_message}}</p>
            </b-notification>

          </div>
          <div v-else>
            <h4 class="subtitle is-4">Tienes acceso a los datos de {{this.roster.total}} artistas</h4>
            <b-table :data="this.roster.artists" focusable>
                <b-table-column field="image_url" v-slot="props" width="60" label="Artista">
                    <img :src="props.row.image_url"/>
                </b-table-column>
                <b-table-column field="name" v-slot="props">
                    <router-link :to="{ name: 'ArtistHome', params:{ id: props.row.id } }">{{props.row.name}}</router-link>
                </b-table-column>
                <b-table-column field="actions" v-slot="props" label="Pitch">
                    <div v-for="action in props.row.actions" :key="action.action">
                        <b-button v-if="action.action != 'NO_ELIGIBLE_MUSIC'" rounded tag="router-link"
                        :to="`${action.url}`">{{action.action}}</b-button>
                        <p v-else>{{action.action}}</p>
                    </div>
                </b-table-column>
                <b-table-column field="display_date" v-slot="props" label="Próximo lanzamiento">
                    {{props.row.display_date}}
                </b-table-column>
            </b-table>
          </div>
          <br>
          <h1 class="title is-1">Equipos que administras</h1>
          <div v-if="team_error">
            <b-notification
                icon-pack="fas"
                type="is-danger"
                has-icon
                aria-close-label="Close notification"
                role="alert">
                <h4 class="title is-4">{{this.team_error.code}} - {{this.team_error.error_type}}</h4>
                <p>{{this.team_error.error_message}}</p>
            </b-notification>

          </div>
          <div v-else>
            <h4 class="subtitle is-4">Administras {{this.team.length}} equipos</h4>
            <b-table :data="this.team" focusable>
                <b-table-column field="imageUrl" v-slot="props" width="60">
                    <img :src="props.row.imageUrl"/>
                </b-table-column>
                <b-table-column field="name" v-slot="props">
                    {{props.row.name}}
                </b-table-column>
            </b-table>
          </div>
    </section>
    </div>
</template>

<script>

export default {
  name: 'Home',

  data() {
    return {
      team: null,
      team_error: null,
      roster: null,
      roster_error: null
    }
  },
  methods:{
  },
  mounted() {
    console.log("mounted")
      fetch(this.$api.team, { credentials: 'include' })
          .then(response => {
            return response.json();
          })
          .then(data => {
            if(data.meta.code == 200)
                this.team = data.data
            else
                this.team_error = data.meta
          })
          .catch(errors => {
            console.error(errors)
          })
          
      fetch(this.$api.roster, { credentials: 'include' })
          .then(response => {
            return response.json();
          })
          .then(data => {
            if(data.meta.code == 200)
                this.roster = data.data
            else
                this.roster_error = data.meta
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
.table td, .table th {
    vertical-align: middle;
}
</style>
