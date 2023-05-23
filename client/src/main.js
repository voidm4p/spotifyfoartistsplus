import Vue from 'vue'
import App from './App.vue'
import Buefy from 'buefy'
import 'buefy/dist/buefy.css'
import router from './router'

Vue.config.productionTip = false


// Buefy
import './assets/css/styles.scss'
Vue.use(Buefy, {
    defaultIconPack: 'fas',
})

// API endpoints
const endpoint = process.env.VUE_APP_API_ENDPOINT_URL

Vue.prototype.$api = {
    'login': endpoint + "/login",
    'team': endpoint + "/manage-team",
    'roster': endpoint + "/roster-view",
    'artist_home': endpoint + "/home",
    'artist_info_public': endpoint + "/artist/public",
    'song': endpoint + "/song",
    'songs': endpoint + "/music/songs",
    'song_public': endpoint + "/song/public",
    'song_credits': endpoint + "/song/public/credits",
    'song_lyrics': endpoint + "/song/public/lyrics"
}

Vue.prototype.getImgUrl = function (filename) {
    var images = require.context('@/assets/', false, /\.png$/)
    return images('./' + filename + ".png")
}

Vue.prototype.$vueEventBus = new Vue(); // Global event bus

Vue.prototype.clone = function(obj)  {
    return JSON.parse(JSON.stringify(obj))
}

Vue.filter('lineBreaks', (value) => {
    return value.replace(/\n/g, '<br />').replace(/\t/g, '&tab;').replace(/\s\s/g, '&nbsp;&nbsp;')
})

Vue.filter('round', function(value, decimals) {
  console.log(value)
  console.log(decimals)
  if(!value) {
    value = 0;
  }

  if(!decimals) {
    decimals = 0;
  }

  value = Math.round(value * Math.pow(10, decimals)) / Math.pow(10, decimals);
  return value;
});

Vue.filter('capitalize', function (value) {
    if (!value) return ''
    value = value.toString()
    return value.charAt(0).toUpperCase() + value.slice(1)
})

new Vue({
    router,
    render: h => h(App),
}).$mount('#app')
