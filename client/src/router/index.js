import Vue from 'vue'
import Router from 'vue-router'

import Home from '@/components/Home/Home'
import Login from '@/components/Home/Login'
import ArtistHome from '@/components/Artist/ArtistHome'
import Music from '@/components/Artist/Music'
import MusicSong from '@/components/Artist/MusicSong'
import MusicSongs from '@/components/Artist/MusicSongs'
import Audience from '@/components/Artist/Audience'
import Profile from '@/components/Artist/Profile'

Vue.use(Router)

let router = new Router({
    mode: 'history',
    routes: [
    {
            path: '/login',
            name: 'Login',
            component: Login,
            meta: {
                requiresAuth: false
            }
    },
    {
            path: '/',
            name: 'Home',
            component: Home,
            meta: {
                requiresAuth: true
            }
    },
	{
            path: '/artist/:id',
            name: 'ArtistHome',
            component: ArtistHome,
            meta: {
                requiresAuth: true
            }
    },
	{
            path: '/artist/:id/music',
            name: 'Music',
            component: Music,
            meta: {
                requiresAuth: true
            }
    },
    {
            path: '/artist/:id/music/song/:song',
            name: 'MusicSong',
            component: MusicSong,
            meta: {
                requiresAuth: true
            }
    },
    {
        path: '/artist/:id/music/songs',
        name: 'MusicSongs',
        component: MusicSongs,
        meta: {
            requiresAuth: true
        }
    },
	{
            path: '/artist/audience',
            name: 'Audience',
            component: Audience,
            meta: {
                requiresAuth: true
            }
    },
	{
            path: '/artist/profile',
            name: 'Profile',
            component: Profile,
            meta: {
                requiresAuth: true
            }
    },
        
    ]
})

router.beforeEach((to, from, next) => {
    const publicPages = ['/login'];
    const authRequired = !publicPages.includes(to.path);
    const loggedIn = localStorage.getItem('jwt');

    console.log(authRequired)
    console.log(loggedIn)
    console.log(authRequired && !loggedIn)

    // trying to access a restricted page + not logged in
    // redirect to login page
    if (authRequired && !loggedIn) {
        next({ path: '/login', query: { next: to.path }});
    }
    if (!authRequired && loggedIn){
        if(to.query.next){
            next({ path: to.query.next });
        }
        else {
            next({name: 'Home'})
        }
    }
    else {
        next();
    }
});

export default router
