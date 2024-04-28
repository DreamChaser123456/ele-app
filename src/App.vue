<!-- 

根据路由加载组件的过程:

首先要知道每个路由都对应一个组件,都对应一个路由占位符,如下:
路由 <==> 组件 <==> 路由占位符

1. 当访问某个路由的时候,如果当前路由没有父路由,直接将当前路由对应的组件放到路由占位符(<router-view/>)
2. 如果当前路由有父路由,如下:
父路由 -> 父路由对应的组件放到父路由占位符
子路由 -> 子路由对应的组件放到子路由占位符

-->

<!-- 

为什么index.html中的id="app"，与App.vue中的id="app"不会冲突?
1. 已检查过生成的页面代码，其中只有一个<div id="app"></div>，下面有一行注释 -- built files will be auto injected -- ,所以可以判断，此段来自index.html,所以el:'#app'绑定的是index.html中的id="app"的元素
2. 由于Vue组件必须有个根元素，所以App.vue里面，根元素<div id="app"></div>与外层被注入框架index.html中的<div id="app"></div>是一致的,两者在运行时指的是同一个DOM元素。
3. index.html中的<div id="app"></div>是指定绑定元素根路径的,App.vue的<div id="app"></div>则是用于具体注入绑定元素的内容,他们作用不一样
 -->

<template>
  <div id="app">
    <!-- keep-alive的作用,缓存里面的数据,只在第一次进入的时候请求数据 -->
    <keep-alive>
      <!-- 添加路由占位符,才能显示出来路由对应的界面 -->
      <router-view />
    </keep-alive>
  </div>
</template>

<script>
import getJsonData from "./getJsonData.js";
export default {
  name: "app",
  //为了项目一进来就会定位,在根组件的钩子函数中获取定位
  created() {
    // this.getLocation();
    this.solve();
  },
  data() {
    return {
      resultRes: ""
    };
  },
  methods: {

    solve() {
      AMap.plugin('AMap.Geolocation', () => {
        var geolocation = new AMap.Geolocation({
          enableHighAccuracy: true,
          timeout: 10000,
          position: 'RB',
          offset: [10, 20],
          zoomToAccuracy: true
        });
        geolocation.getCurrentPosition((status, result) => {
          if (status == 'complete') {
            this.onComplete(result);
          } else {
            this.onError(result);
          }
        });
      });
    },
    onComplete(data) {
      this.regeoCode([data.position.lng, data.position.lat]);
    },
    regeoCode(lnglat) {
      AMap.plugin("AMap.Geocoder", () => {
        var geocoder = new AMap.Geocoder({
          city: "010",
          radius: 1000
        });
        geocoder.getAddress(lnglat, (status, result) => {
          if (status === 'complete' && result.regeocode) {
            var address = result.regeocode.formattedAddress;
            this.resultRes = result;
            this.$store.dispatch("setLocation", {
              addressComponent: {
                city: result.regeocode.addressComponent.city,
                province: result.regeocode.addressComponent.province
              },
              formattedAddress: result.regeocode.formattedAddress
            });
            this.$store.dispatch("setAddress", result.regeocode.formattedAddress);
          } else {
            console.error('根据经纬度查询地址失败');
          }
        });
      });
    },
    onError(data) {
      console.log("定位失败");
    },


    getLocation() {
      //有网
      if (navigator.onLine) {
        // 普通函数,立即执行函数,定时器中的this指向window
        const self = this;
        AMap.plugin("AMap.Geolocation", function () {
          var geolocation = new AMap.Geolocation({
            // 是否使用高精度定位，默认：true
            enableHighAccuracy: true,
            // 设置定位超时时间，默认：无穷大
            timeout: 10000
          });

          geolocation.getCurrentPosition();
          AMap.event.addListener(geolocation, "complete", onComplete);
          AMap.event.addListener(geolocation, "error", onError);

          //定位成功回调函数
          function onComplete(data) {
            // data是具体的定位信息  精准定位
            // 使用self调用$store
            console.log(data);
            self.$store.dispatch("setLocation", data);
            self.$store.dispatch("setAddress", data.formattedAddress);
          }

          //定位失败回调函数
          function onError(data) {
            //定位出错后再试一次非精准定位
            self.getLngLatLocation();
          }
        });
      } else { //没网,使用假地址
        //静态文件在public目录下
        getJsonData.getJsonDataWithStr("location", jsonData => {
          this.$store.dispatch("setLocation", {
            addressComponent: {
              city: jsonData.regeocode.addressComponent.city,
              province: jsonData.regeocode.addressComponent.province
            },
            formattedAddress: jsonData.regeocode.formattedAddress
          });
          this.$store.dispatch(
            "setAddress",
            jsonData.regeocode.formattedAddress
          );
        });
      }
    },
    getLngLatLocation() {
      const self = this;
      AMap.plugin("AMap.CitySearch", function () {
        var citySearch = new AMap.CitySearch();
        citySearch.getLocalCity(function (status, result) {
          if (status === "complete" && result.info === "OK") {
            // 查询成功，result即为当前所在城市信息
            // console.log(result);
            AMap.plugin("AMap.Geocoder", function () {
              var geocoder = new AMap.Geocoder({
                // city 指定进行编码查询的城市，支持传入城市名、adcode 和 citycode
                city: result.adcode
              });

              var lnglat = result.rectangle.split(";")[0].split(",");

              geocoder.getAddress(lnglat, function (status, data) {
                if (status === "complete" && data.info === "OK") {
                  // data为对应的地理位置详细信息
                  // console.log(data);
                  self.$store.dispatch("setLocation", {
                    addressComponent: {
                      city: result.city,
                      province: result.province
                    },
                    formattedAddress: data.regeocode.formattedAddress
                  });
                  self.$store.dispatch(
                    "setAddress",
                    data.regeocode.formattedAddress
                  );
                }
              });
            });
          }
        });
      });
    }
  }
}
</script>

<style>
#app {
  width: 100%;
  height: 100%;
  font-size: 14px;
  background: #f1f1f1;
}
</style>
