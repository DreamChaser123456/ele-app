<!-- 店铺根界面 -->
<template>
  <div class="shop" v-if="shopInfo">
    <!-- 头部 -->
    <nav class="header-nav">
      <!-- 背景图片 -->
      <div class="nav_bg">
        <img :src="shopInfo.background_image_path" alt>
      </div>
      <!-- 返回按钮 -->
      <div class="nav_back">
        <!-- <i @click="$router.go(-1)" class="fa fa-chevron-left"></i> -->
        <i @click="destroyComponent" class="fa fa-chevron-left"></i>
      </div>
      <!-- 店铺头像 -->
      <div class="shop_image">
        <img :src="shopInfo.image_path" alt>
      </div>
    </nav>
    <!-- 商家信息 -->
    <div class="index-rst">
      <!-- 标题 -->
      <div class="rst-name">
        <!-- 点击显示弹窗 -->
        <span @click="showInfoModel = true">{{ shopInfo.name }}</span>
        <i class="fa fa-caret-right"></i>
      </div>
      <!-- 弹窗信息 -->
      <!-- 父组件接收子组件的close事件 -->
      <ShopAlert @close="showInfoModel = false" :rst="shopInfo" :showInfoModel="showInfoModel" />
      <!-- 评分月售 -->
      <div class="rst-order">
        <span>评分{{ shopInfo.rating }}</span>
        <span>月售{{ shopInfo.recent_order_num }}单</span>
        <span>蜂鸟专送约{{ shopInfo.order_lead_time }}分钟</span>
      </div>
      <!-- 优惠信息 -->
      <Activity :activities="shopInfo.activities" />
      <!-- 公告 -->
      <p class="rst-promotion">公告: {{ shopInfo.promotion_info }}</p>
    </div>
    <!-- 导航 -->
    <NavBar />
    <!-- keep-alive的作用,缓存里面的数据,只在第一次进入的时候请求数据 -->
    <!-- 举例就是,如果添加了keep-alive,点餐里面添加了商品到购物车,切换到评价,再切到点餐,购物车的数据会还在 -->
    <!-- 如果不加keep-alive,点餐里面添加了商品到购物车,切换到评价,再切到点餐,点餐界面会重新请求数据,这时候购物车的数据就没了 -->
    <keep-alive>
      <!-- 路由占位符 -->
      <router-view></router-view>
    </keep-alive>
  </div>
</template>

<script>
import getJsonData from "../../getJsonData.js";
import ShopAlert from "../../components/Shops/ShopAlert";
import Activity from "../../components/Shops/Activity";
import NavBar from "../../components/Shops/NavBar";
import { Indicator } from 'mint-ui';
export default {
  name: "Shop",
  components: {
    ShopAlert,
    Activity,
    NavBar
  },
  data() {
    return {
      shopInfo: null, //店铺信息数据
      showInfoModel: false, //是否显示商铺信息弹窗
      shop_id: '',
    };
  },
  activated() {
    this.getData();
  },
  methods: {
    destroyComponent() {
      this.$router.go(-1);
      this.$destroy();
    },
    getData() {
      // Indicator.open();
      this.$axios(`/api/v1/profile/restaurants_detail?shop_id=${this.$route.query.shop_id}`).then(res => {
        this.shopInfo = res.data;
        getJsonData.getJsonDataWithStr("batch_shop", jsonData => {
          this.$set(this.shopInfo, 'activities', jsonData.rst.activities)
        });
        // Indicator.close();
      });
    }
  }
}
</script>

<style scoped>
.shop {
  width: 100%;
  height: 100%;
  overflow: auto;
  box-sizing: border-box;
}

.header-nav {
  position: relative;
}

.nav_bg img {
  width: 100%;
  height: 26.666667vw;
}

.nav_back {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 26.666667vw;
  background: rgba(0, 0, 0, 0.5);
}

.nav_back i {
  color: #fff;
  font-size: 1.3rem;
  margin-left: 1.333333vw;
  margin-top: 1.333333vw;
}

.shop_image {
  position: absolute;
  top: 0;
  left: 50%;
  margin-left: -10vw;
  margin-top: 11vw;
}

.shop_image img {
  width: 20vw;
  height: 20vw;
  border-radius: 0.8vw;
}

.index-rst {
  padding: 8vw 0 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  background: #fff;
  box-shadow: inset 0 -0.666667vw 0.666667vw hsla;
}

.index-rst .rst-name {
  flex: 1;
  width: 72vw;
  font-size: 1.3rem;
  font-weight: 700;
  white-space: nowrap;
  padding-right: 2.666667vw;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 1.6vw 0;
}

.rst-name span {
  text-align: left;
  overflow: hidden;
  text-overflow: ellipsis;
}

.index-rst .rst-order {
  white-space: nowrap;
  height: 3.2vw;
  margin-top: 1.733333vw;
  color: #666;
  text-align: center;
  font-size: 0.6rem;
}

.rst-order span {
  margin: 0 3px;
}

.index-rst .rst-promotion {
  width: 80vw;
  font-size: 0.6rem;
  color: #999;
  overflow: hidden;
  text-overflow: ellipsis;
  margin: 2.266667vw auto 2.666667vw;
  padding: 0;
  white-space: nowrap;
}
</style>