<template>
  <div class="index">
    <!-- 添加路由占位符,路由对应的界面才能显示 -->
    <router-view/>
    <TabBar :data="tabbarData"/>
  </div>
</template>

<script>
// 导入组件
import TabBar from "../components/TabBar";
export default {
  name: "index",
   //一定要注册组件
  components: {
    TabBar
  },
  data() {
    return {
      //tabbar的数据
      tabbarData:[
        {title:"首页",icon:"home",path:"/home"},
        {title:"订单",icon:"file-text-o",path:"/order"},
        {title:"我的",icon:"user",path:"/me"}
      ]
    }
  }
}
</script>

<style>
.index {
  /* 设置首页的宽高,45px是tabbar的高度 */
  width: 100%;
  /* calc()函数用于动态计算长度值 */
  height: calc(100% - 45px);
}
</style>
