<!-- segment组件 -->
<template>
  <div class="nav">
    <router-link :to="{ path: '/goods', query: { shop_id: this.$route.query.shop_id } }" class="nav-item">
      点餐
      <i class="line"></i>
    </router-link>
    <!-- <div class="nav-item" @click="click_diancan">
      点餐
      <i class="line"></i>
    </div> -->
    <router-link :to="{ path: '/comments', query: { shop_id: this.$route.query.shop_id } }" class="nav-item">
      评价
      <i class="line"></i>
    </router-link>
    <router-link :to="{ path: '/seller', query: { shop_id: this.$route.query.shop_id } }" class="nav-item">
      商家
      <i class="line"></i>
    </router-link>
  </div>
</template>

<script>
export default {
  name: "NavBar",
  methods: {
    click_diancan() {
      this.$destroy();
      this.$router.push(`/goods?shop_id=${this.$route.query.shop_id}`);
    }
  }
};
</script>
<style scoped>
.nav {
  display: flex;
  width: 100%;
  line-height: 10.666667vw;
  border-bottom: 1px solid #e4e4e4;
  background: #fff;
  /* 设置定位模式是sticky,滚动的时候有悬停的效果 */
  position: sticky;
  top: 0px;
  z-index: 10;
}

.nav .nav-item {
  flex: 1;
  text-align: center;
  font-size: 0.95rem;
  text-decoration: none;
  color: #666;
  position: relative;
}

/* 在路由的index.js文件里面设置了 linkActiveClass: 'active' 当点击<router-link>的时候这个类就会生效 */
.nav .active {
  color: #333;
  font-weight: 700;
}

.nav .active .line {
  width: 30px;
  height: 0.533333vw;
  background: #2395ff;
  display: inline-block;
  position: absolute;
  left: 45%;
  bottom: 0;
  margin-left: -10px;
}
</style>
