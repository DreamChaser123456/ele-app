import Vue from 'vue'
import App from './App.vue'
// 引入MintUI全部组件
import MintUI from 'mint-ui';
// 引入MintUI样式
import 'mint-ui/lib/style.css';
import router from './router'
import store from './store'
import axios from 'axios'
import qs from 'qs';

//引入loading框
import { Indicator } from 'mint-ui';

//关闭生产模式下给出的提示
Vue.config.productionTip = false;
//挂载到vue的原型对象上,这样就可以全局直接使用$axios调用
Vue.prototype.$axios = axios;
//使用MintUI
Vue.use(MintUI);

// 根路径
axios.defaults.baseURL = 'http://localhost:5000/';

// 请求拦截
axios.interceptors.request.use(
  config => {
    // 添加loading
    Indicator.open();
    return config;
  },
  error => {
    return Promise.reject(error);
  }
);

// 响应拦截
axios.interceptors.response.use(
  response => {
    //移除loading
    Indicator.close();
    return response;
  },
  error => {
    // 移除loading
    Indicator.close();
    return Promise.reject(error);
  }
);

new Vue({
  router, //挂载路由
  store,  //挂载Vuex
  render: h => h(App)
}).$mount('#app')
