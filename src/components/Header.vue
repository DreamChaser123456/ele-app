<!-- 导航条组件 -->
<template>
  <div class="header">
    <!-- 左侧返回 -->
    <!-- @click="$emit('backClick') 子组件定义返回事件 -->
    <div class="header-button is-left" v-show="isLeft" @click="$emit('backClick')">
      <i class="fa fa-chevron-left"></i>
      <button>返回</button>
    </div>
    <!-- 中间标题 -->
    <h1 class="header-title">{{title}}</h1>
  </div>
</template>

<script>
export default {
  name: "Header",
  props: {
    title: String,
    // 是否显示返回按钮,默认是false
    isLeft: {
      type: Boolean,
      default: false
    }
  }
}
</script>

<style scoped>
.header {
  align-items: center;
  background-color: #009eef;
  box-sizing: border-box;
  color: #fff;
  display: flex;
  font-size: 16px;
  height: 45px;
  line-height: 1;
  padding: 0 10px;
  position: relative;
  text-align: center;
  white-space: nowrap;
  position: fixed;
  width: 100%;
  top: 0;
  z-index: 99;
}

.header-button button {
  background-color: transparent;
  border: 0;
  box-shadow: none;
  color: inherit;
  display: inline-block;
  padding: 0;
  font-size: inherit;
  outline: none;
}
.header-title {
  flex: 1;
}
.is-left {
  text-align: left;
}
.is-right {
  text-align: right;
}
</style>
