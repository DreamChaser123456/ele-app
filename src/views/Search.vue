<!-- 搜索界面 -->
<template>
  <div class="search">
    <Header :isLeft="true" title="搜索" @backClick="$router.push('/home')" />
    <div class="search_header">
      <form class="search_wrap">
        <i class="fa fa-search"></i>
        <input type="text" v-model="key_word" placeholder="请输入商家,商品信息" ref="input">
        <!-- <button>搜索</button> -->
      </form>
    </div>

    <div v-if="empty" class="empty_wrap">
      <img src="https://fuss10.elemecdn.com/d/60/70008646170d1f654e926a2aaa3afpng.png" alt>
      <div class="empty_txt">
        <h4>附近没有搜索结果</h4>
        <span>换个关键词试试吧</span>
      </div>
    </div>
    <div v-else-if="showShop" class="container">
      <!-- 筛选外卖门店组件 -->
      <FilterView :filterData="filterData" @update="update" />
      <!-- 使用了InfiniteScroll自动加载更多数据 -->
      <div v-infinite-scroll="loadDataAndMore" :infinite-scroll-disabled="loading">
        <IndexShop v-for="(item, index) in restaurants" :key="index" :restaurant="item.restaurant" />
      </div>
    </div>
    <div v-else>
      <!-- 餐馆 -->
      <SearchIndex :data="result.restaurants" />
      <!-- 关键字 -->
      <!-- <SearchIndex @clickItem="shopItemClick" :data="result.words" /> -->
    </div>
  </div>
</template>

<script>
import getJsonData from "../getJsonData.js";
import Header from '../components/Header.vue'
import SearchIndex from '../components/SearchIndex.vue'
import FilterView from "../components/FilterView";
import IndexShop from "../components/IndexShop";
//这个控件有点类似于上拉加载,但是不需要松手,直接会加载数据
import { InfiniteScroll } from "mint-ui";
export default {
  name: "Search",
  components: {
    Header,
    SearchIndex,
    FilterView,
    IndexShop
  },
  data() {
    return {
      key_word: "", //搜索关键字
      result: null, //搜索结果,包括商家和关键字
      showShop: false, //是否显示商家信息列表页面
      filterData: null, //过滤组件数据
      restaurants: [], //根据关键字搜索到的商家信息列表数据
      page: 0,
      size: 7,
      loading: false, //是否加载完毕
      data: null, //搜索条件
      cancel: null, //取消网络请求
    }
  },
  computed: {
    //搜索内容是否为空
    empty() {
      if (this.result) {
        if (this.result.restaurants.length <= 0 && this.result.words.length <= 0) {
          return true;
        } else {
          return false;
        }
      } else {
        return true;
      }
    }
  },
  watch: {
    key_word() {
      if (!this.key_word) {
        this.result = null;
        return;
      }
      this.showShop = false;
      this.keyWordChange();
    }
  },
  created() {
    // this.getFilterData();
    // console.log("created");

  },
  // 路由跳转之前的钩子函数,用于获取跳转参数
  beforeRouteEnter(to, from, next) {
    // 路由跳转之前清空界面的数据
    next(vm => {
      vm.key_word = ""; //搜索关键字
      vm.result = null; //搜索结果,包括商家和关键字
      vm.showShop = false; //是否显示商家信息列表页面
      vm.filterData = null; //过滤组件数据
      vm.restaurants = []; //根据关键字搜索到的商家信息列表数据
      vm.page = 0;
      vm.size = 7;
      vm.loading = false; //是否加载完毕
      vm.data = null; //搜索条件
      vm.cancel = null; //取消网络请求

      //每次进入都自动聚焦
      vm.$nextTick(() => {
        vm.$refs.input.focus();
      });
    });
  },
  methods: {
    getFilterData() {
      this.$axios("/api/profile/filter").then(res => {
        // console.log(res.data);
        this.filterData = res.data;
      })
        .catch(res => {
          //获取假数据
          getJsonData.getJsonDataWithStr("filter", jsonData => {
            this.filterData = jsonData;
          });
        });
    },
    //文字改变,进行搜索  支持搜索:汉堡 炸鸡
    keyWordChange() {
      this.$axios.get(`/api/v1/profile/search?key_word=${this.key_word}`)
        .then(res => {
          if (this.key_word) { //搜索框有内容的时候才是真正的搜索结果,否则可能是搜索框清空了,但是返回的还是上次的结果
            this.result = res.data;
          }
        })
    },
    // searchHandle() {
    //   if (!this.key_word) return;
    //   // 搜索
    //   if (
    //     this.result &&
    //     (this.result.restaurants.length > 0 || this.result.words.length)
    //   ) {
    //     this.shopItemClick();
    //   }
    // },
    //点击某个推荐关键字
    shopItemClick() {
      this.page = 0;
      this.restaurants = []; //先清空
      this.getFilterData(); //获取过滤数据
      this.showShop = true; //显示
    },
    update(condation) {
      // console.log(condation);
      this.data = condation;
      this.shopItemClick();
      this.loadDataAndMore();
    },
    //加载数据/更多
    loadDataAndMore() {
      this.page++;
      this.$axios
        .post(`/api/profile/restaurants/${this.page}/${this.size}`, this.data)
        .then(res => {
          if (res.data.length > 0) {
            res.data.forEach(item => {
              this.restaurants.push(item);
            });
          } else {
            this.loading = true;
          }
        })
        .catch(res => {
          //加载假数据
          getJsonData.getJsonDataWithStr("restaurantsLoadMore", jsonData => {
            if (jsonData.length > 0) {
              jsonData.forEach(item => {
                this.restaurants.push(item);
              });
            } else {
              this.loading = true;
            }
          });
        });
    },
  }
}
</script>

<style scoped>
/* 
这里为什么不使用/deep/或>>>,父组件直接修改子组件的样式也能生效呢? 
如果是自己写的类,可以直接修改类的样式,因为父类的会覆盖子类的,如果是第三方组件的或者是层级很深的,可以使用 /deep/或>>>
*/
.header {
  height: 54px;
}

.search {
  width: 100%;
  height: 100%;
  overflow: auto;
  box-sizing: border-box;
}

.search_header {
  margin-top: 54px;
  background: #fff;
  padding: 0 4.266667vw;
}

.search_header .search_wrap {
  padding: 2.933333vw 2.933333vw 2.933333vw 0;
  display: flex;
  align-items: center;
  position: relative;
}

.search_wrap .fa-search {
  width: 2.933333vw;
  height: 2.933333vw;
  color: #888;
  position: absolute;
  top: 4.6666666vw;
  left: 2.933333vw;
}

.search_wrap input {
  flex-grow: 1;
  border-radius: 0.266667vw;
  background-color: #f8f8f8;
  padding: 1.733333vw 4vw 1.733333vw 8.8vw;
  color: #666;
  outline: none;
  border: none;
}

.search_wrap button {
  outline: none;
  border: none;
  color: #333;
  font-size: 0.426667rem;
  background: #fff;
  font-weight: 700;
  margin-left: 2.933333vw;
  font-size: 14px;
}

.shop {
  width: 100%;
  /* 95是导航条+搜索条的高度 */
  height: calc(100% - 95px);
  overflow: auto;
}

.empty_wrap {
  width: 100%;
  height: 100%;
  overflow: hidden;
  background: #fff;
  display: flex;
  justify-content: center;
}

.empty_wrap img {
  width: 35vw;
  height: 35vw;
}

.empty_txt h4 {
  color: #666;
  font-size: 1rem;
  margin: 12vw 0 2vw 0;
}

.empty_txt span {
  color: #999;
  font-size: 0.8rem;
}
</style>
