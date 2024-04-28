<!-- tabbar组件 -->
<template>
  <div class="tabbar">
    <!-- 跳转子路由链接 -->
    <router-link 
      class="tab-item"
      :key="index"
      v-for="(item,index) in data" 
      :to="item.path"
      active-class="is-selected" 
    >
    <!-- 小图标,使用的是公共图标 -->
    <div class="tab-item-icon">
      <i :class="'fa fa-' + item.icon"></i>
    </div>
    <!-- 文字 -->
    <div class="tab-item-label">{{item.title}}</div>
    </router-link>
  </div>
</template>

<script>
export default {
  name: "tabbar",
  props: {
    data: Array
  }
};
</script>

<style scoped>
.tabbar {
  height: 45px;
  box-sizing: border-box;
  width: 100%;
  /* 固定定位到最下面 */
  position: fixed;
  bottom: 0;
  background-image: linear-gradient(
    180deg,
    #d9d9d9,
    #d9d9d9 50%,
    transparent 0
  );
  background-size: 100% 1px;
  background-repeat: no-repeat;
  background-position: 0 0;
  background-color: #fafafa;
  display: flex;
  text-align: center;
}
.tab-item {
  display: block;
  padding: 3px 0;
  flex: 1;
}
.tab-item-icon {
  width: 20px;
  height: 20px;
  margin: 0 auto 5px;
}
.tab-item-icon i {
  font-size: 16px;
}
.tab-item-label {
  color: inherit;
  font-size: 10px;
  line-height: 1;
}
a {
  text-decoration: none;
  color: #999;
}
.is-selected {
  color: #009eef;
}
</style>