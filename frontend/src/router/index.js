import { createRouter, createWebHistory } from 'vue-router'
import LandingPage from '../views/LandingPage.vue'
import EditorPage from '../views/EditorPage.vue'
import BlogFeed from '../views/BlogFeed.vue'
import ProfilePage from '../views/ProfilePage.vue'
import ChatPage from '../views/ChatPage.vue'
import LoginPage from '../views/LoginPage.vue'
import SignupPage from '../views/SignupPage.vue'
import DraftsPage from '../views/DraftsPage.vue'

const routes = [
  { path: '/', component: LandingPage },
  { path: '/write', component: EditorPage },
  { path: '/blog-explore', component: BlogFeed },
  { path: '/profile', component: ProfilePage },
  { path: '/chat', component: ChatPage },
  { path: '/login', component: LoginPage },
  { path: '/signup', component: SignupPage },
  { path: '/drafts', component: DraftsPage },
{ path: '/blog/:id', name: 'BlogDetail', component: () => import('../views/BlogDetail.vue') },

]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, from, next)=>{
  
  const publicRoutes = ['/login', '/signup', '/'];
  const authRequired = !publicRoutes.includes(to.path)
  const loggedIn = localStorage.getItem('user_id');

  if(authRequired && !loggedIn){
    return next('/login')
  }

  next()

})

export default router
