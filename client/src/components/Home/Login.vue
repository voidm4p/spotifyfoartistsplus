<template>
    <section class="hero is-primary is-fullheight">
      <div class="hero-body">
        <div class="container">
          <div class="columns is-centered">
            <div class="column is-6-tablet is-6-desktop is-5-widescreen">
                
              <div class="box">
              <figure style="text-align: center">
              <inline-svg 
                    :src="require(`@/assets/images/spotify-for-artists.svg`)" 
                    @error="svgLoadError($event)"
                    width="300" 
                    fill="black"
                    aria-label="Logo"
                ></inline-svg></figure>
              
                
                <b-field label="Correo electrónico o nombre de usuario" >
                      <b-input v-model="username" required placeholder="Correo electrónico o nombre de usuario"></b-input>
                </b-field>
                <b-field label="Contraseña">
                      <b-input
                          type="password"
                          placeholder="Contraseña"
                          v-model="password" required></b-input>
                </b-field>
                <div class="field">
                    <button class="button is-dark" @click="handleSubmit()">
                      Login
                    </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
</template>

<script>
import InlineSvg from 'vue-inline-svg';

export default {
  name: 'Login',
  components: {
    InlineSvg
  },
  data() {
    return {
      username: "",
      password: ""
    }
  },
  methods:{
    svgLoadError(){
        console.log("Error cargando svg")
    },
    handleSubmit(){
      if (this.username && this.password) {
        let body = {
          username: this.username,
          password: this.password
        }
        const navigate = this.$router;
        const url = this.$route;
        fetch(this.$api.login, {
          method: 'POST',
          body: JSON.stringify(body),
          headers:{
            'Content-Type': 'application/json'
          },
          credentials: 'include'
        })
            .then(response => {
              return response.json()
            })
            .then((json) => {
              console.log(json)
              if(json.meta.code == 200 && json.data){
                  localStorage.setItem('jwt',json.data.token)
                  if (localStorage.getItem('jwt') !== null){
                    this.$emit('loggedIn')
                    if(url.query.next){
                      navigate.push({ path: url.query.next })
                    }
                    else {
                      navigate.push({ name: 'Home' })
                    }
                  }
              } else {
                console.error(json.meta.error_message)
              }
            })
            .catch(function (error) {
              console.error(error);
            });
      }
    }
  },
  mounted() {
    
  },
  updated(){

  },
  watch:{

  }
}
</script>

<style scoped>

</style>
