<!-- 城市选择界面 -->
<template>
  <div class="city">
    <div class="search_wrap">
      <div class="search">
        <i class="fa fa-search"></i>
        <input v-model="city_val" type="text" placeholder="输入城市名">
      </div>
      <!-- 点击取消将当前城市传过去,携带城市 不能直接go(-1),这样没参数 -->
      <button @click="$router.push({name:'address',params:{city:city}})">取消</button>
    </div>
    <!-- 原来是因为盒子的高度超出屏幕了,所以会有滚动效果,它只是超出屏幕了,我们并没有添加实际滚动的东西 -->
    <!-- 我们可以设置height: 100%,然后使用better-scroll实现滚动 -->
    <!-- v-if="searchList.length == 0 城市列表和搜索结果列表只显示一个 -->
    <!-- overflow:hidden; 可以去掉右边的滑动指示条 -->
    <div style="height:100%; overflow:hidden;" v-if="searchList.length == 0">
      <!-- 上面的定位 -->
      <!-- 绑定点击事件 -->
      <Location @click="selectCity({name:city})" :address="city"/>
      <!-- 下面的城市列表 -->
      <!-- 父组件接收子组件传递过来的值 -->
      <Alphabet @selectCity="selectCity" ref="allcity" :cityInfo="cityInfo" :keys="keys"/>
    </div>
    <!-- 搜索结果列表 -->
    <div class="search_list" v-else>
      <ul>
        <!-- 绑定点击事件 -->
        <li @click="selectCity(item)" v-for="(item,index) in searchList" :key="index">{{item.name}}</li>
      </ul>
    </div>
  </div>
</template>

<script>
import getJsonData from "../getJsonData.js";
import Location from "../components/Location";
import Alphabet from "../components/Alphabet";
export default {
  name: "City",
  components: {
    Location,
    Alphabet
  },
  data() {
    return {
      city_val: "", //输入框的内容
      cityInfo: {}, //城市信息模型
      keys: [], //首字母key
      allCities: [], //所有城市数组
      searchList: [] //搜索城市数组
    };
  },
  computed: {
    city() {
      return (
        this.$store.getters.location.addressComponent.city ||
        this.$store.getters.location.addressComponent.province
      );
    }
  },
  watch: {
    city_val() {
      this.searchCity();
    }
  },
  created() {
    this.getCityInfo();
  },
  methods: {
    getCityInfo() {
      this.$axios("/api/posts/cities")
      .then(res => {
        // console.log(res.data);
        this.cityInfo = res.data;
        // 处理key 计算key
        this.keys = Object.keys(res.data);
        // hotcities这个key移除掉
        this.keys.pop();
        // keys 排序
        this.keys.sort();
        this.$nextTick(() => {
          this.$refs.allcity.initScroll();
        });

        // 存储所有城市, 用来搜索过滤
        this.keys.forEach(key => {
          // console.log(key);
          this.cityInfo[key].forEach(city => {
            // console.log(city);
            this.allCities.push(city);
          });
        });
      })
      .catch(err => {
        // 如果数据请求失败,就使用假数据
        getJsonData.getJsonDataWithStr("cities", jsonData => {
          this.cityInfo = jsonData;
          // 处理key 计算key
          this.keys = Object.keys(jsonData);
          // hotcities这个key移除掉
          this.keys.pop();
          // keys 排序
          this.keys.sort();
          this.$nextTick(() => {
            this.$refs.allcity.initScroll();
          });

          // 存储所有城市, 用来搜索过滤
          this.keys.forEach(key => {
            // console.log(key);
            this.cityInfo[key].forEach(city => {
              // console.log(city);
              this.allCities.push(city);
            });
          });
        });
      });
    },
    selectCity(city) {
      // console.log(city);
      this.$router.push({ name: "address", params: { city: city.name } });
    },
    searchCity() {
      if(this.city_val) {
        // 根据输入框的关键字检索城市 并存入到searchList数组中
        this.searchList = this.allCities.filter(item => {
          // 过滤搜索的结果
          return item.name.indexOf(this.city_val) != -1;
        });
      } else {
        // 如果搜索框为空, 数组置空
        this.searchList = [];
        //重新实例化BScroll,否则滚动会失效
        this.$nextTick(() => {
          this.$refs.allcity.initScroll();
        });
      }
    }
  }
}
</script>

<style scoped>
.city {
  width: 100%;
  height: 100%;
  overflow: auto;
  box-sizing: border-box;
  padding-top: 45px;
}
.search_wrap {
  position: fixed;
  top: 0;
  height: 45px;
  width: 100%;
  background: #fff;
  box-sizing: border-box;
  padding: 3px 16px;
  display: flex;
  justify-content: space-between;
  /* 清除外边距塌陷问题 */
  overflow: hidden;
}
.search {
  background-color: #eee;
  border-radius: 10px;
  line-height: 40px;
  width: 85%;
  box-sizing: border-box;
  padding: 0 16px;
}
.search input {
  background: #eee;
  outline: none;
  border: none;
  margin-left: 5px;
}
.search_wrap button {
  outline: none;
  color: #009eef;
}

.location {
  background: #fff;
  padding: 8px 16px;
  height: 73px;
  box-sizing: border-box;
}

.search_list {
  background: #fff;
  padding: 5px 16px;
}
.search_list li {
  padding: 10px;
  border-bottom: 1px solid #eee;
}
</style>
