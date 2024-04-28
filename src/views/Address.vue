<!-- 选择收货地址界面 -->
<template>
  <div class="address">
    <!-- @backClick="$router.push('/home')" 监听子组件的返回,返回到home界面 -->
    <Header @backClick="$router.push('/home')" :isLeft="true" title="选择收货地址"></Header>
    <div class="city_search">
      <div class="search">
        <span class="city" @click="$router.push('/city')">
          {{ city }}
          <i class="fa fa-angle-down"></i>
          |
        </span>
        <i class="fa fa-search"></i>
        <input type="text" v-model="search_val" placeholder="小区/写字楼/学校">
      </div>
      <!-- 不传参数,使用定位的地址 -->
      <div @click="selectAddress">
        <Location :address="address" />
      </div>
    </div>
    <div class="area">
      <!-- 一个ul是一个组 -->
      <ul class="area_list" v-for="(item, index) in areaList" :key="index">
        <!-- 添加点击事件 -->
        <li @click="selectAddress(item)">
          <h4>{{ item.name }}</h4>
          <!-- item.address.join('') 将数组转成字符串 -->
          <p>{{ item.district }}{{ item.address }}</p>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import getJsonData from "../getJsonData.js";
// 1.先导入
import Header from "../components/Header.vue"
import Location from "../components/Location"
export default {
  name: "Address",
  //2.后注册
  components: {
    Header,
    Location//注册
  },
  data() {
    return {
      city: "武汉市", //当前城市
      search_val: "",
      areaList: [] //搜索结果数组
    }
  },
  // mounted(){
  //   console.log("我是address.vue,我要输出address",this.$store.getters.location.formattedAddress)
  // },
  computed: {
    address() {
      return this.$store.getters.location.formattedAddress;
    }
  },
  //监听
  watch: {
    //监听输入文字的改变
    search_val() {
      this.searchPlace();
    }
  },
  methods: {
    //搜索位置
    searchPlace() {
      //使用假数据
      // getJsonData.getJsonDataWithStr("searchPlace", jsonData => {
      //   this.areaList = jsonData;
      // });
      // return;
      const self = this;
      AMap.plugin("AMap.AutoComplete", function () {
        // 实例化Autocomplete
        var autoOptions = {
          //city 限定城市，默认全国
          city: self.city
        };
        var autoComplete = new AMap.Autocomplete(autoOptions);
        // 这里使用的是function,所以要用self,如果是箭头函数就可以直接用this
        autoComplete.search(self.search_val, function (status, result) {
          // 搜索成功时，result即是对应的匹配数据
          //console.log(result);
          self.areaList = result.tips;
        });
      });
    },
    selectAddress(item) {
      console.log('点击新地址')
      // 设置地址
      if (item) {
        //如果有新地址,在vuex中设置新的地址
        this.$store.dispatch(
          "setAddress",
          item.district + item.address + item.name
        );
      } else {
        //如果没有新地址,就点击的是当前定位,使用定位的地址到vuex中
        this.$store.dispatch("setAddress", this.address);
      }

      // 跳转home
      this.$router.push("/home");
    }
  },
  // 路由跳转之前的钩子函数,用于获取跳转参数
  // beforeRouteEnter(to, from, next) {
  //   // console.log(to);
  //   next(vm => {
  //     vm.city = to.params.city;
  //   });
  // }
}
</script>

<style scoped>
.address {
  width: 100%;
  height: 100%;
  overflow: auto;
  box-sizing: border-box;
  padding-top: 45px;
}

.city_search {
  background-color: #fff;
  padding: 10px 20px;
  color: #333;
}

.search {
  background-color: #eee;
  height: 40px;
  border-radius: 10px;
  box-sizing: border-box;
  line-height: 40px;
  display: flex;
  align-items: center;
}

.search .city {
  padding: 0 10px;
}

.city i {
  margin-right: 10px;
}

.search input {
  flex: 1;
  margin-left: 5px;
  background-color: #eee;
  outline: none;
  border: none;
}

.area {
  margin-top: 16px;
  background: #fff;
}

.area li {
  border-bottom: 1px solid #eee;
  padding: 8px 16px;
  color: #aaa;
}

.area li h4 {
  font-weight: bold;
  color: #333;
  margin-bottom: 5px;
}
</style>
