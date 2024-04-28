<!-- 点餐组件 -->
<template>
  <div class="goods">
    <!-- 商家推荐 -->
    <div class="recommend" v-if="is_fetched">
      <!-- 标题 -->
      <p class="recommend-name">商家推荐</p>
      <!-- collectionView -->
      <div class="recommend-wrap">
        <ul>
          <!-- collectionViewCell -->
          <li v-for="(item, index) in recommends" :key="index">
            <img :src="item.image_path" alt>
            <div class="recommend-food">
              <p class="recommend-food-name">{{ item.name }}</p>
              <p class="recommend-food-zm">月售{{ item.month_sales }} 好评率{{ item.satisfy_rate }}</p>
            </div>
            <!-- 价格 -->
            <div class="recommend-food-price">
              <p>¥{{ item.fixed_price }}</p>
              <!-- 计算价格的➕ -->
              <CartControl :food="item" />
            </div>
          </li>
        </ul>
      </div>
    </div>

    <!-- 商品分类 -->
    <div class="menuview">
      <!-- 左侧分类列表 -->
      <div class="menu-wrapper" ref="menuScroll">
        <ul>
          <li :class="{ 'current': currentIndex === index }" @click="selectMenu(index)"
            v-for="(item, index) in menuWithFoods" :key="index">
            <!-- <img v-if="item.icon_url" :src="item.icon_url" alt> -->
            <span>{{ item.category_name }}</span>
          </li>
        </ul>
      </div>

      <!-- 右侧商品内容 -->
      <div class="foods-wrapper" ref="foodScroll">
        <ul>
          <li class="food-list-hook" v-for="(item, index) in menuWithFoods" :key="index">
            <!-- 标题 -->
            <div class="category-title">
              <!-- 加粗文字 -->
              <strong>{{ item.category_name }}</strong>
              <span>{{ item.category_description }}</span>
            </div>
            <!-- 遍历cell数据  -->
            <div @click="handleFood(food)" class="fooddetails" v-for="(food, i) in item.foods" :key="i">
              <!-- 左图片 -->
              <img :src="food.image_path" alt>
              <!-- 右文字 -->
              <section class="fooddetails-info">
                <h4>{{ food.name }}</h4>
                <p class="fooddetails-des">{{ food.description }}</p>
                <p class="fooddetails-sales">月售{{ food.month_sales }}份 好评率{{ food.satisfy_rate }}</p>
                <div class="fooddetails-price">
                  <span class="price">¥{{ food.fixed_price }}</span>
                  <!-- 商品数量组件组件 -->
                  <CartControl :food="food" />
                </div>
              </section>
            </div>
          </li>
        </ul>
      </div>
    </div>
    <!-- 购物车 -->
    <ShopCar :menuWithFoods="menuWithFoods" />
    <!-- 商品详情 -->
    <Food :food="selectedFood" :showFood="showFood" @close="showFood = false" />
  </div>
</template>

<script>
import getJsonData from "../../getJsonData.js";
import CartControl from "../../components/Shops/CartControl";
// 为什么使用better-scroll,因为在手机上没有滚轮,所以我们用better-scroll改为触摸的形式滚动
import BScroll from "better-scroll";
import ShopCar from "./ShopCar";
import Food from "./Food";
export default {
  name: "Goods",
  components: {
    CartControl,
    ShopCar,
    Food,
  },
  data() {
    return {
      shopInfo: null, //店铺信息数据
      menuScroll: {}, // 左侧滚动对象
      foodScroll: {}, // 右侧滚动对象
      scrollY: 0, // 右侧菜单当前滚动到的y值
      listHeight: [], // 12个区列表高度
      selectedFood: null, //点击商品详情的商品
      showFood: false, //是否显示商品详情,
      shop_id: null,
      menuWithFoods: null,
      recommends: [],
      is_fetched: false,
    };
  },
  computed: {
    // 根据右侧滚动的位置, 确定对应的索引下标
    currentIndex() {
      for (let i = 0; i < this.listHeight.length; i++) {
        let height1 = this.listHeight[i];
        let height2 = this.listHeight[i + 1];

        // 判断是否在两个高度之间
        if (this.scrollY >= height1 && this.scrollY < height2) {
          return i;
        }
      }
      return 0;
    }
  },
  activated() {
    this.recommends = [];
    this.menuWithFoods = null;
    this.getData();
  },
  methods: {
    async getData() {
      try {
        // 请求菜单信息
        const menusResponse = await this.$axios(`/api/v1/profile/restaurants_menus?shop_id=${this.$route.query.shop_id}`);
        const menus = menusResponse.data.menus;

        // 初始化一个空数组来存储最终的菜单和食物信息
        const tmp_menuWithFoods = [];

        for (const menu of menus) {
          // 对于每个菜单，请求其下的食物信息
          const foodsResponse = await this.$axios(`/api/v1/profile/restaurants_menus_foods?menu_id=${menu.id}`);
          const foods = foodsResponse.data.foods.map(food => ({
            ...food,
            count: 0 // 为每个食物项添加count字段
          }));

          // 将菜单和其对应的食物作为一个对象存储
          tmp_menuWithFoods.push({
            ...menu,
            foods // 将处理过的食物信息添加到菜单对象中
          });
        }

        this.menuWithFoods = tmp_menuWithFoods;

        this.menuWithFoods.forEach(e => {
          e.foods.forEach(f => {
            if (f.is_recommended) {
              this.recommends.push(f);
            }
          });
        });
        this.is_fetched = true;
      } catch (err) {
        console.error("Error fetching menu or foods data:", err);
      }

      this.$nextTick(() => {
        //初始化better-scroll
        this.initScroll();
        // 计算12个区的高度
        this.calculateHeight();
      });
    },
    initScroll() {
      // 左侧tableview
      this.menuScroll = new BScroll(this.$refs.menuScroll, {
        click: true
      });
      // 右侧tableview
      this.foodScroll = new BScroll(this.$refs.foodScroll, {
        // 1 监听事件的触发时间  3 延迟到事件完毕后触发
        probeType: 3,
        // 是否启用click事件
        click: true
      });

      // 监听滚动过程中实时的Y  往下滑动是正值,往下滑动是正值
      this.foodScroll.on("scroll", pos => {
        // console.log(pos.y); abs绝对值   round四舍五入
        this.scrollY = Math.abs(Math.round(pos.y));
      });
    },
    // 选中左侧菜单
    selectMenu(index) {
      // console.log(index);
      let foodlist = this.$refs.foodScroll.getElementsByClassName(
        "food-list-hook"
      );

      let el = foodlist[index];
      // console.log(el);
      // 滚动到对应元素的位置 时间250ms
      this.foodScroll.scrollToElement(el, 250);
    },
    // 计算每个区域的高度
    calculateHeight() {
      let foodlist = this.$refs.foodScroll.getElementsByClassName(
        "food-list-hook"
      );
      // 每个区的高度添加到数组中
      let height = 0;
      this.listHeight.push(height);

      for (let i = 0; i < foodlist.length - 1; i++) {
        let item = foodlist[i];
        // 累加
        height += item.clientHeight;
        this.listHeight.push(height);
      }
      // console.log(this.listHeight);
    },
    //点击某个商品
    handleFood(food) {
      this.selectedFood = food;
      this.showFood = true;
    },
  },
}
</script>

<style scoped>
.goods {
  position: relative;
  /* 减去的高度是导航条的高度 */
  height: calc(100% - 10.666667vw);
}

.recommend {
  padding-top: 4.266667vw;
  background-color: #fff;
}

.recommend-name {
  padding-left: 4.266667vw;
  color: #333;
  font-size: 1rem;
  font-weight: 700;
  margin-bottom: 2.666667vw;
}

.recommend-wrap {
  overflow-x: scroll;
  display: flex;
  width: 100%;
}

.recommend-wrap ul {
  display: flex;
  padding-left: 4.266667vw;
}

.recommend-wrap ul li {
  flex: none;
  width: 32vw;
  margin-right: 2.666667vw;
}

.recommend-wrap li img {
  display: block;
  width: 32vw;
  height: 32vw;
  border-top-left-radius: 0.8vw;
  border-top-right-radius: 0.8vw;
  max-width: 100%;
}

.recommend-food .recommend-food-name {
  color: #333;
  font-size: 0.8rem;
  margin: 1.866667vw 0 1.233333vw;
  white-space: nowrap;
  text-overflow: ellipsis;
  overflow: hidden;
}

.recommend-food .recommend-food-zm {
  color: #999;
  font-size: 0.6rem;
  margin-bottom: 1.866667vw;
  min-height: 1em;
}

.recommend-food-price {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-right: 0.266667vw;
}

.recommend-food-price p {
  font-size: 1rem;
  color: #ff5339;
}

/* 隐藏横向滚动条 */
::-webkit-scrollbar {
  width: 0 !important;
}

.menuview {
  box-sizing: border-box;
  height: 100%;
  padding-bottom: 10.8vw;
  background-color: #fff;
  display: flex;
}

.menu-wrapper {
  /* 不让滚轮生效,使用better-scroll实现手动上下滚动 */
  overflow-y: hidden;
  /* 减去的高度是底部购物车的高度 */
  height: calc(100% - 12.8vw);
  background-color: #f8f8f8;
  padding-bottom: 10.666667vw;
  width: 20.533333vw;
}

.menu-wrapper li {
  padding: 4.666667vw 2vw;
  font-size: 0.6rem;
  color: #666;
  line-height: 1.2;
}

.menu-wrapper li img {
  max-width: 100%;
  width: 3.466667vw;
  height: 3.466667vw;
  vertical-align: top;
  margin-right: 0.8vw;
}

.foods-wrapper {
  /* 不让滚轮生效,使用better-scroll实现手动上下滚动 */
  overflow-y: hidden;
  /* height: 100%; */
  height: calc(100% - 12.8vw);
  width: 79.466667vw;
  padding-bottom: 10.666667vw;
}

.category-title {
  margin-left: 2.666667vw;
  padding: 2vw 8vw 2vw 0;
  display: flex;
  align-items: center;
  overflow: hidden;
}

.category-title strong {
  margin-right: 1.333333vw;
  font-weight: 700;
  font-size: 0.8rem;
  color: #666;
  flex: none;
}

.category-title span {
  flex: 1;
  color: #999;
  font-size: 0.6rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.fooddetails {
  min-height: 30.666667vw;
  padding: 2.666667vw 0 2.666667vw 2.666667vw;
  margin-bottom: 0.133333vw;
  display: flex;
}

.fooddetails img {
  width: 25.333333vw;
  height: 25.333333vw;
  flex: none;
  margin-right: 2.666667vw;
  border-radius: 0.533333vw;
}

.fooddetails-info {
  flex: 1;
  padding-bottom: 6.666667vw;
  padding-right: 4vw;
}

.fooddetails-info h4 {
  padding-right: 4vw;
  font-weight: 700;
  overflow: hidden;
  font-size: 1rem;
  white-space: nowrap;
  width: 40vw;
  text-overflow: ellipsis;
  color: #333;
}

.fooddetails-des {
  margin: 1.333333vw 0;
  font-size: 0.6rem;
  color: #999;
  width: 42.666667vw;
  /* 下面三个属性控制文本一行显示,显示不完的用...代替 */
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.fooddetails-sales {
  margin: 1.733333vw 0 !important;
  color: #999;
  font-size: 0.6rem;
  line-height: 1;
  min-height: 1em;
}

.fooddetails-price {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 3.733333vw;
}

.fooddetails-price .price {
  font-size: 1rem;
  line-height: 4.266667vw;
  color: #ff5339;
  padding-bottom: 0.933333vw;
  display: flex;
  align-items: baseline;
}

.menu-wrapper .current {
  background-color: #fff !important;
  color: #333 !important;
}
</style>
