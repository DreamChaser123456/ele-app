<!-- 城市列表组件 -->
<template>
  <!-- v-if="cityInfo" 当有嵌套循环的时候,需要判断外层有数据才进行渲染,否则会报错 -->
  <!-- ref="area_scroll"设置引用,用于标记是哪个控件滚动 -->
  <div class="area" ref="area_scroll" v-if="cityInfo">
    <!-- 使用better-scroll的时候,必须外层div和内层div都有,少一个滚动都不生效 -->
    <div class="scroll_wrap">
      <!-- 热门城市 -->
      <div class="hot_wrap citylist">
        <div class="title">热门城市</div>
        <ul class="hot_city">
          <!-- 子组件给父组件传值 -->
          <li @click="$emit('selectCity',item)" v-for="(item,index) in cityInfo.hotCities" :key="index">{{item.name}}</li>
        </ul>
      </div>
      <!-- 所有城市 -->
      <div class="city_wrap">
        <!-- 循环字母表排序的key -->
        <div class="city_content citylist" v-for="(item,index) in keys" :key="index">
          <!-- 字母头key -->
          <div class="title">{{item}}</div>
          <!-- 根据字母头key展示城市名 -->
          <ul>
            <!-- 循环里面嵌套循环,遍历的是cityInfo对应的当前item对应的数组 -->
            <!-- 子组件给父组件传值 -->
            <li @click="$emit('selectCity',city)" v-for="(city,index) in cityInfo[item]" :key="index">{{city.name}}</li>
          </ul>
        </div>
      </div>
    </div>
    <!-- 索引组件 -->
    <div class="area_keys">
      <ul>
        <li @click="selectKey(0)">#</li>
        <li @click="selectKey(index+1)" v-for="(item,index) in keys" :key="index">{{item}}</li>
      </ul>
    </div>
  </div>
</template>

<script>
import BScroll from "better-scroll";
export default {
  name: "Alphabet",
  props: {
    cityInfo: Object,
    keys: Array
  },
  data(){
    return {
      scroll: null
    }
  },
  methods: {
    //实例化BScroll
    initScroll() {
      // 第一个传递哪个控件滚动,第二个传递参数
      this.scroll = new BScroll(this.$refs.area_scroll, {
        click: true //可以被点击
      });
    },
    selectKey(index) {
      // console.log(index);
      // console.log(this.$refs.area_scroll.getElementsByClassName("citylist"));
      // 热门城市和所有城市都有共同的citylist类名
      const citylist = this.$refs.area_scroll.getElementsByClassName("citylist");
      // 根据下标,滚动到相对应的元素上
      let el = citylist[index];

      // 滚动到对应的位置上  better-scroll的方法
      this.scroll.scrollToElement(el, 250);
    }
  }
}
</script>

<style scoped>
.area {
  margin-top: 10px;
  box-sizing: border-box;
  padding: 0 16px;
  background: #fff;
  height: calc(100% - 65px);
  overflow: hidden;
}
.scroll_wrap {
  background: #fff;
  overflow: auto;
}
.title {
  color: #aaa;
  padding: 15px 0;
}
.hot_city {
  padding: 0 16px;
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
}
.hot_city li {
  width: 30%;
  background: #f1f1f1;
  margin: 0 10px 10px 0;
  text-align: center;
  padding: 10px;
  box-sizing: border-box;
}
.city_content li {
  padding: 10px;
  border-bottom: 1px solid #eee;
}
.area_keys {
  position: fixed;
  right: 0;
  top: 25%;
  color: #aaa;
  font-size: 12px;
  line-height: 1.4;
  text-align: center;
  padding: 0 5px;
}
</style>
