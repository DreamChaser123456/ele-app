import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    // 路由重定向
    redirect:'/home',
    // 如果当前路由有默认的子路由了,就不能设置name了,否则会有警告
    name: 'index', 
    //路由懒加载方式
    component: () => import("../views/Index.vue"),
    children: [
      // 这是设置默认子路由
      // 设置默认子路由和路由重定向都可以达到相同的效果,更推荐路由重定向,因为更容易理解并且没警告
      // {
      //   path: '/',
      //   redirect: '/home'
      // },
      {
        path: '/home',
        name: 'home',
        component: () => import("../views/indexChildren/Home.vue")
      },
      {
        path: '/order',
        name: 'order',
        component: () => import("../views/indexChildren/Order.vue")
      },
      {
        path: '/me',
        name: 'me',
        component: () => import("../views/indexChildren/Me.vue")
      },
      {
        path: '/address',
        name: 'address',
        component: () => import("../views/Address.vue")
      },
      {
        path: '/city',
        name: 'city',
        component: () => import("../views/City.vue")
      }
    ]
  },
  {
    path: '/login',
    name: 'login',
    component: () => import("../views/Login.vue")
  },
  {
    path: '/search',
    name: 'search',
    component: () => import("../views/Search.vue")
  },
  {
    path: '/shop',
    name: 'shop',
    redirect: '/goods',
    component: () => import("../views/Shops/Shop.vue"),
    children: [
      {
        path: '/goods',
        name: 'goods',
        component: () => import('../views/Shops/Goods.vue')
      },
      {
        path: '/comments',
        name: 'comments',
        component: () => import('../views/Shops/Comments.vue')
      },
      {
        path: '/seller',
        name: 'seller',
        component: () => import('../views/Shops/Seller.vue')
      }
    ]
  },
  {
    path: '/myAddress',
    name: 'myAddress',
    component: () => import('../views/Orders/MyAddress.vue')
  },
  {
    path: '/addAddress',
    name: 'addAddress',
    component: () => import('../views/Orders/AddAddress.vue')
  },
  {
    path: '/settlement',
    name: 'settlement',
    component: () => import('../views/Orders/Settlement.vue')
  },
  {
    path: '/remark',
    name: 'remark',
    component: () => import('../views/Orders/Remark.vue')
  },
  {
    path: '/pay',
    name: 'pay',
    component: () => import('../views/Orders/Pay.vue')
  },
  {
    path: '/orderInfo',
    name: 'orderInfo',
    component: () => import('../views/Orders/OrderInfo.vue')
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  // <router-link> 被点击的时候生效的class,在NavBar.vue里面生效
  linkActiveClass: 'active',
  // 路由规则数组
  routes
})

// 路由守卫,判断是进入index还是进入login
router.beforeEach((to, from, next) => {
  const isLogin = localStorage.getItem("ele_login") ? true : false;
  if (to.path == '/login') {
    next();
  } else {
    // 是否在登录状态下
    isLogin ? next() : next('/login');
  }
});

export default router
