<!-- 首页界面 -->
<template>
  <div class="home">
    <!-- 头部定位 -->
    <div class="header">
      <div class="address_map" @click="pushAddress">
        <i class="fa fa-map-marker"></i>
        <!-- 三目运算符和||效果一样,默认地址杭州市 -->
        <span style="width: 80%;">{{ address ? address : '定位中' }}<i class="fa fa-sort-desc"></i></span>
      </div>
    </div>
    <!-- 搜索框 -->
    <div class="search_wrap" :class="{ 'fixedview': showFilter }" @click="$router.push('/search')">
      <div class="shop_search">
        <i class="fa fa-search"></i>
        搜索商家 商家名称
      </div>
    </div>
    <div id="container">
      <!-- 轮播 -->
      <!-- 4000是4秒一次自动轮播 -->
      <mt-swipe :auto="4000" class="swiper">
        <!-- 每一个轮播图item -->
        <mt-swipe-item v-for="(img, index) in swipeImgs" :key="index">
          <img :src="img" alt>
        </mt-swipe-item>
      </mt-swipe>
      <!-- 分类的轮播数据 -->
      <!-- :auto="0" 手动滑动轮播 -->
      <div class="goods_swipe">
        <mt-swipe :auto="0" class="entries">
          <!-- 先看有多少页 -->
          <mt-swipe-item v-for="(entry, i) in entries" :key="i" class="entry_wrap">
            <!-- 再看每一页多少数据 -->
            <div class="foodentry" v-for="(item, index) in entry" :key="index">
              <!-- 图片 -->
              <div class="img_wrap">
                <img :src="item.image" alt>
              </div>
              <!-- 文字 -->
              <span style="font-size: 13px;">{{ item.name }}</span>
            </div>
          </mt-swipe-item>
        </mt-swipe>
      </div>
    </div>
    <!-- 推荐商家标签 -->
    <div class="shoplist-title">推荐商家</div>
    <!-- 筛选外卖门店组件 -->
    <!-- @searchFixed 接收子控件传递的参数,让搜索框固定定位到头部 -->
    <FilterView :filterData="filterData" @searchFixed="showFilterView" @update="update" />

    <!-- 商家信息 -->
    <mt-loadmore :top-method="loadData" :bottom-method="loadMore" :bottom-all-loaded="allLoaded" :auto-fill="false"
      :bottomPullText="bottomPullText" ref="loadmore">
      <!-- 外卖店铺组件 -->
      <IndexShop v-for="(item, index) in restaurants" :key="index" :restaurant="item" />
    </mt-loadmore>
  </div>
</template>

<script>
import getJsonData from "../../getJsonData.js";
import { Swipe, SwipeItem, Loadmore } from "mint-ui";
import FilterView from "../../components/FilterView.vue";
import IndexShop from "../../components/IndexShop.vue";

export default {
  name: "home",
  components: {
    FilterView,
    IndexShop
  },
  data() {
    return {
      swipeImgs: [], //轮播图数组
      entries: [], //分类数组
      filterData: null, //筛选条件数据
      showFilter: false, //搜索条是否固定到头部
      page: 1, //请求的页码
      size: 10, //请求的条数
      restaurants: [], //存放所有商家的数组
      allLoaded: false, //上拉数据是否都加载完了
      bottomPullText: "上拉加载更多",
      sortParamsData: "" //排序的条件
    };
  },
  computed: {
    address() {
      return this.$store.getters.address ? this.$store.getters.address : this.$store.getters.location.formattedAddress;
    }
  },
  activated() {
    this.$store.dispatch("setOrderInfo", null);
  },
  created() {
    // 获取数据
    this.getData();
  },
  methods: {
    // 请求数据
    getData() {
      //获取轮播/分类数据
      getJsonData.getJsonDataWithStr("shopping", jsonData => {
        // 轮播图数据
        this.swipeImgs = jsonData.swipeImgs;
        //分类数据
        this.entries = jsonData.entries;
      });
      //获取过滤数据
      getJsonData.getJsonDataWithStr("filter", jsonData => {
        this.filterData = jsonData;
      });
      // 获取商家信息
      this.loadData();
    },
    // 下拉刷新
    loadData() {
      this.page = 1;
      this.allLoaded = false;
      this.bottomPullText = "上拉加载更多";
      // 拉取商家信息
      this.$axios
        // this.sortParamsData 排序规则
        .get(`/api/v1/profile/restaurants?page=${this.page}&size=${this.size}&sortParamsData=${this.sortParamsData}`)
        .then(res => {
          // 下拉加载完了,隐藏下拉控件
          this.$refs.loadmore.onTopLoaded();
          this.restaurants = res.data.restaurants;
        })
        .catch(res => {
          console.error(err);
          this.$refs.loadmore.onTopLoaded();
        });
    },
    // 上拉加载
    loadMore() {
      if (!this.allLoaded) { // 检查是否还有数据可以加载
        this.page++; // 请求下一页数据
        this.$axios.get(`/api/v1/profile/restaurants?page=${this.page}&size=${this.size}`)
          .then(res => {
            this.$refs.loadmore.onBottomLoaded(); // 结束上拉加载动作

            if (res.data.restaurants.length > 0) {
              this.restaurants = [...this.restaurants, ...res.data.restaurants]; // 将新数据追加到列表中

              if (res.data.restaurants.length < this.size) {
                // 如果返回的数据少于请求的数量，标记为所有数据已加载
                this.allLoaded = true;
                this.bottomPullText = "没有更多了哦";
              }
            } else {
              // 如果没有返回数据，标记为所有数据已加载
              this.allLoaded = true;
              this.bottomPullText = "没有更多了哦";
            }
          })
          .catch(err => {
            console.error(err);
            this.$refs.loadmore.onBottomLoaded(); // 出错时也要结束上拉加载动作
          });
      }
    },
    // 根据排序更新数据
    update(condition) {
      // 保存排序条件
      this.sortParamsData = condition.condition;
      // 重新加载数据
      this.loadData();
    },
    pushAddress() {
      // 通过名称跳转,并且把城市传递过去
      this.$router.push({ name: 'address', params: { city: this.city } })
    },
    showFilterView(isShow) {
      this.showFilter = isShow;
    },
  }
}
</script>

<style scoped>
.home {
  width: 100%;
  height: 100%;
  overflow: auto;
  box-sizing: border-box;
}

.header,
.search_wrap {
  background-color: #009eef;
  padding: 10px 10px;
}

.header .address_map {
  color: #fff;
  font-weight: bold;
}

.address_map i {
  margin: 0 3px;
  font-size: 18px;
}

.address_map span {
  display: inline-block;
  /* width: 80%; */
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
}

.search_wrap .shop_search {
  background-color: #fff;
  padding: 10px 0;
  border-radius: 4px;
  text-align: center;
  color: #aaa;
}

.search_wrap {
  /* sticky 是粘性的意思,设置position: sticky;和top: 0px;可以实现上滑头部停留的效果 */
  position: sticky;
  top: 0px;
  z-index: 999;
  box-sizing: border-box;
}

.swiper {
  height: 100px;
}

.swiper img {
  width: 100%;
  height: 100px;
}

.entries {
  background: #fff;
  height: 47.2vw;
  text-align: center;
  overflow: hidden;
}

.foodentry {
  width: 20%;
  float: left;
  position: relative;
  margin-top: 2.933333vw;
}

.foodentry .img_wrap {
  position: relative;
  display: inline-block;
  width: 12vw;
  height: 12vw;
}

.img_wrap img {
  width: 100%;
  height: 100%;
}

.foodentry span {
  display: block;
  color: #666;
  font-size: 0.32rem;
}

/* 不生效 */
/* .mint-swipe-indicator .is-active {
  background: red !important;
} */

/* 
vue组件中的style标签标有scoped属性时表明style里的css样式只适用于当前组件元素,所以我们使用原来的类+!important并不生效,如上:

在vue的开发中，我们需要引用子组件，包括ui组件（element、iview）。但是在父组件中添加scoped之后，在父组件中书写子组件的样式是无效果的。去掉scoped之后，样式可以覆盖。但这样会污染全局样式，为了解决这个问题，vue-loader新增书写方式: /deep/ 和 >>>,需要在组件外层包裹一下,然后使用/deep/或>>>穿透到里面,使用/deep/和>>>效果都是一样的,都是穿透的意思,使用如下:
*/

/* 更改轮播图原始小圆点颜色 */
.goods_swipe /deep/ .mint-swipe-indicator.is-active {
  background: red;
}

/* 更改轮播图原选中的小圆点透明度 */
.goods_swipe>>>.mint-swipe-indicator {
  width: 8px;
  height: 8px;
  display: inline-block;
  border-radius: 100%;
  background: gray;
  opacity: 0.9;
  margin: 0 3px;
}

/* 推荐商家 */
.shoplist-title {
  display: flex;
  align-items: flex;
  justify-content: center;
  height: 9.6vw;
  line-height: 9.6vw;
  font-size: 16px;
  color: #333;
  background: #fff;
}

/* 前后的--使用伪元素 */
.shoplist-title:after,
.shoplist-title:before {
  display: block;
  content: "--";
  width: 5.333333vw;
  height: 0.266667vw;
  color: #999;
}

.shoplist-title:before {
  margin-right: 3.466667vw;
}

.shoplist-title:after {
  margin-left: 3.466667vw;
}

.fixedview {
  width: 100%;
  position: fixed;
  top: 0px;
  z-index: 999;
}

.mint-loadmore {
  height: calc(100% - 95px);
  overflow: auto;
}
</style>