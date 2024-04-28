<!-- 购物车组件 -->
<template>
  <div class="shopcar">
    <transition name="fade">
      <!-- 灰色蒙版 -->
      <div class="cartview-cartmask" @click.self="showCartView = false" v-if="showCartView && !isEmpty">
        <div class="cartview-cartbody">
          <div class="cartview-cartheader">
            <span>已选商品</span>
            <button @click="clearFoods">
              <i class="fa fa-trash-o"></i>
              <span>清空</span>
            </button>
          </div>
          <div class="entityList-cartbodyScroller">
            <ul class="entityList-cartlist">
              <!-- 商品列表 -->
              <li class="entityList-entityrow" v-for="(food, index) in selectFoods" :key="index">
                <h4>
                  <span>{{ food.name }}</span>
                </h4>
                <span class="entityList-entitytotal">{{ food.fixed_price }}</span>
                <!-- 结算控件 -->
                <CartControl :food="food" />
              </li>
            </ul>
          </div>
        </div>
      </div>
    </transition>
    <!-- 底部的商品选择框 -->
    <div class="bottomNav-cartfooter" :class="{ 'bottomNav-carticon-empty': isEmpty }">
      <span class="bottomNav-carticon" @click="showCartView = !showCartView">
        <!-- 购物车图标 -->
        <i class="fa fa-cart-plus"></i>
        <!-- 角标数量 -->
        <span v-if="totalCount">{{ totalCount }}</span>
      </span>
      <!-- 中间文字区域 -->
      <div class="bottomNav-cartInfo" @click="showCartView = !showCartView">
        <!-- 第一行文字 -->
        <p class="bottomNav-carttotal">
          <span v-if="isEmpty">未选购商品</span>
          <!-- toFixed保留两位小数 -->
          <span v-else>¥{{ totalPrice.toFixed(2) }}</span>
        </p>
        <!-- 第二行文字 -->
        <!-- <p class="bottomNav-cartdelivery">另需配送费{{ shopInfo.float_delivery_fee }}元</p> -->
      </div>
      <!-- 结算按钮 -->
      <button class="submit-btn" v-if="restaurant_info">
        <span v-if="isEmpty">¥{{ restaurant_info.float_delivery_fee }}元起送</span>
        <span @click="settlement" v-else>去结算</span>
      </button>
    </div>
  </div>
</template>

<script>
import CartControl from "../../components/Shops/CartControl";
export default {
  name: "ShopCar",
  props: {
    menuWithFoods: ""
  },
  components: {
    CartControl
  },
  created() {
    this.get_float_delivery_fee();
  },
  data() {
    return {
      totalCount: 0, //商品总数
      totalPrice: 0, //商品总价
      selectFoods: [], //选中的商品数组,用于展示
      showCartView: false, //是否显示带有蒙版的已选商品
      restaurant_info: null,
    };
  },
  computed: {
    // 购物车是否为空
    isEmpty() {
      let empty = true;
      this.totalCount = 0;
      this.totalPrice = 0;
      this.selectFoods = [];

      // 右侧列表数据
      if (this.menuWithFoods) {
        this.menuWithFoods.forEach(item => {
          item.foods.forEach(food => {
            if (food.count) {
              empty = false;
              this.totalCount += food.count;
              this.totalPrice += food.fixed_price * food.count;
              this.selectFoods.push(food);
            }
          });
        });
      }
      return empty;
    }
  },
  methods: {
    get_float_delivery_fee() {
      this.$axios.get(`/api/v1/profile/restaurants_detail?shop_id=${this.$route.query.shop_id}`)
        .then(res => {
          this.restaurant_info = res.data;
        })
    },
    // 清空商品
    clearFoods() {
      if (this.menuWithFoods) {
        this.menuWithFoods.forEach(item1 => {
          item1.foods.forEach(item2 => {
            item2.count = 0;
          });
        });
      }

    },
    //点击结算,将信息存到vuex中
    settlement() {
      // 如果使用子父组件传值,需要ShopCar.vue -> Goods.vue -> Shop.vue 层级比较多,所以我们使用vuex传值
      this.$store.dispatch("setOrderInfo", {
        restaurant_info: this.restaurant_info,
        selectFoods: this.selectFoods
      });
      this.$destroy();
      this.$router.push("/settlement");
    }
  },
};
</script>

<style scoped>
.bottomNav-cartfooter {
  position: fixed;
  right: 0;
  bottom: 0;
  left: 0;
  display: flex;
  align-items: center;
  padding-left: 21.066667vw;
  background-color: rgba(61, 61, 63, 0.9);
  height: 12.8vw;
  z-index: 1000;
}

.bottomNav-carticon {
  position: absolute;
  left: 3.2vw;
  bottom: 2vw;
  width: 13.333333vw;
  height: 13.333333vw;
  box-sizing: border-box;
  border-radius: 100%;
  background-color: #3190e8;
  border: 1.333333vw solid #444;
  box-shadow: 0 -0.8vw 0.533333vw 0 rgba(0, 0, 0, 0.1);
}

.bottomNav-carticon>i {
  position: absolute;
  top: 7px;
  right: 0;
  bottom: 0;
  left: 7px;
  color: #fff;
  font-size: 1.6rem;
}

.bottomNav-cartInfo {
  flex: 1;
}

.bottomNav-carttotal {
  font-size: 0.8rem;
  line-height: normal;
  color: #fff;
}

.bottomNav-cartdelivery {
  color: #999;
  font-size: 0.6rem;
}

.submit-btn {
  height: 100%;
  width: 28vw;
  background-color: #38ca73;
  color: #fff;
  text-align: center;
  text-decoration: none;
  font-size: 0.9rem;
  font-weight: 600;
  line-height: 12.8vw;
  border: none;
  outline: none;
}

.bottomNav-carticon-empty>span {
  background-image: radial-gradient(circle, #363636 6.266667vw, #444 0);
}

.bottomNav-carticon-empty>span>i {
  color: #606065 !important;
}

.bottomNav-carticon-empty .bottomNav-carttotal>span {
  color: #999;
}

.bottomNav-carticon-empty .submit-btn {
  background-color: #535356 !important;
}

.bottomNav-carticon>span {
  position: absolute;
  right: -1.2vw;
  top: -1.333333vw;
  line-height: 1;
  background-image: linear-gradient(-90deg, #ff7416, #ff3c15 98%);
  color: #fff;
  border-radius: 3.2vw;
  padding: 0.833333vw 1.333333vw;
  font-size: 0.6rem;
}

.cartview-cartmask {
  position: fixed;
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
  background-color: rgba(0, 0, 0, 0.4);
  z-index: 200;
}

.cartview-cartbody {
  position: fixed;
  left: 0;
  width: 100%;
  background-color: #fff;
  bottom: 12.8vw;
  z-index: 201;
  opacity: 1;
  font-size: 1rem;
}

.cartview-cartheader {
  display: flex;
  align-items: center;
  padding: 0 4vw;
  border-bottom: 0.133333vw solid #ddd;
  background-color: #eceff1;
  color: #666;
  height: 10.666667vw;
}

.cartview-cartheader>span {
  flex: 1;
  display: flex;
  align-items: center;
}

.cartview-cartheader>button {
  border: none;
  outline: none;
  flex: none;
  display: flex;
  align-items: center;
  padding-left: 4vw;
  color: #666;
  text-decoration: none;
  font-size: 0.8rem;
  line-height: 4vw;
  background: none;
}

.cartview-cartheader>button>span {
  margin-left: 0.8vw;
}

.entityList-cartbodyScroller {
  overflow: auto;
  max-height: 80vw;
}

.entityList-entityrow {
  border-bottom: 0.133333vw solid #eee;
  display: flex;
  align-items: center;
  padding: 2vw 3.333333vw 2vw 0;
  min-height: 12.666667vw;
  margin-left: 3.333333vw;
}

.entityList-entityrow>h4 {
  flex: 5.5;
  line-height: normal;
}

.entityList-entityrow>h4>span {
  display: inline-block;
  font-style: normal;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  vertical-align: middle;
  max-width: 46.666667vw;
}

.entityList-entitytotal {
  color: rgb(255, 83, 57);
  flex: 2.5;
  text-align: left;
  white-space: nowrap;
  font-weight: 700;
}

.entityList-entitytotal::before {
  content: "\A5";
  font-size: 0.6rem;
  color: currentColor;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.25s ease-out;
}

.fade-enter,
.fade-leave-to {
  opacity: 0;
}
</style>
