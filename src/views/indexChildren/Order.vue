<!-- 订单界面 -->
<template>
  <div class="order">
    <!-- 每个cell -->
    <div class="order-card-body" v-for="(order, index) in orderlist" :key="index">
      <!-- 订单信息 -->
      <div class="order-card-wrap" @click="$router.push({ name: 'orderInfo', params: order })">
        <!-- 左图片 -->
        <img :src="order.order_info.restaurant_info.image_path" alt>
        <!-- 右内容 -->
        <div class="order-card-content">
          <!-- 第一行,头部 -->
          <div class="order-card-head">
            <!-- 名字 -->
            <div class="title">
              <a>
                <span>{{ order.order_info.restaurant_info.name }}</span>
                <i class="fa fa-angle-right"></i>
              </a>
              <p>订单已完成</p>
            </div>
            <!-- 时间 -->
            <p class="date-time">{{ formatDate(order.created_at) }}</p>
          </div>
          <!-- 第二行,详情 -->
          <div class="order-card-detail">
            <p v-for="(item, index) in order.order_info.selectFoods" class="detail" :key="index">{{ item.name }}</p>
            <p class="price">¥{{ order.total_price }}</p>
          </div>
        </div>
      </div>
      <!-- 再来一单 -->
      <!-- <div class="order-card-bottom">
        <button class="cardbutton" @click="$router.push('/shop')">再来一单</button>
      </div> -->
    </div>
  </div>
</template>

<script>
import dayjs from 'dayjs';
export default {
  name: "order",
  data() {
    return {
      orderlist: [], //订单列表
    };
  },
  beforeRouteEnter(to, from, next) {
    next(vm => {
      vm.getData();
    });
  },
  beforeRouteUpdate(to, from, next) {
    // 执行刷新操作
    this.getData();
    next();
  },
  methods: {
    formatDate(timestamp) {
      // 使用day.js
      return dayjs(parseInt(timestamp, 10)).format('YYYY-MM-DD');
    },
    getData() {
      this.$axios.get(`/api/v1/profile/order_list?user_id=${localStorage.getItem("phone_num")}`)
        .then(res => {
          this.orderlist = res.data
            .map(order => {
              // 对order_info字段进行JSON.parse转换，如果它存在
              if (order.order_info) {
                order.order_info = JSON.parse(order.order_info);
              }
              // 对address_info字段进行JSON.parse转换，如果它存在
              if (order.address_info) {
                order.address_info = JSON.parse(order.address_info);
              }
              // 对remark_info字段进行JSON.parse转换，如果它存在
              if (order.remark_info) {
                order.remark_info = JSON.parse(order.remark_info);
              }
              // 返回更新后的订单对象
              return order;
            })
            // 在这里进行排序
            .sort((a, b) => b.created_at - a.created_at);
        })
        .catch(error => {
          console.error('Error fetching order list:', error);
        });
    }
  }
};
</script>

<style scoped>
.order {
  width: 100%;
  height: 100%;
  overflow: auto;
  box-sizing: border-box;
  margin-bottom: 2.666667vw;
}

.order-card-body {
  margin-top: 2.666667vw;
  background-color: #fff;
  padding: 3.733333vw 0 0 4vw;
}

.order-card-wrap {
  display: flex;
}

.order-card-wrap>img {
  height: 8.533333vw;
  border-radius: 0.533333vw;
  border: 1px solid #eee;
  width: 8.533333vw;
  margin-right: 2.666667vw;
}

.order-card-content {
  flex: 1;
}

.order-card-head {
  border-bottom: 1px solid #eee;
  padding-right: 3.466667vw;
  padding-bottom: 2.666667vw;
}

.order-card-head .title {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.order-card-head .title>a {
  font-size: 1rem;
  line-height: 1.5em;
  color: #333;
  text-decoration: none;
}

.order-card-head .title>a>span {
  display: inline-block;
  max-width: 10em;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.order-card-head .title>a>i {
  margin-left: 1.333333vw;
  color: #ccc;
  vertical-align: super;
}

.order-card-head .title>p {
  font-size: 0.8rem;
  text-align: right;
  color: #333;
  max-width: 14em;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.date-time {
  font-size: 0.6rem;
  color: #999;
}

.order-card-detail {
  display: flex;
  flex-direction: column;

  justify-content: space-between;
  padding: 4vw 3.466667vw 4vw 0;
  font-size: 0.8rem;
}

.order-card-detail .detail {
  color: #666;
  display: flex;
  align-items: center;
}

.order-card-detail .price {
  flex-basis: 16vw;
  text-align: right;
  color: #333;
  font-weight: 700;
}

.order-card-bottom {
  display: flex;
  border-top: 1px solid #eee;
  padding: 2.666667vw 4.266667vw;
  justify-content: flex-end;
}

.cardbutton {
  padding: 1.333333vw 2.666667vw;
  border: 1px solid #2395ff;
  border-radius: 0.533333vw;
  background-color: transparent;
  outline: none;
  font-size: 0.8rem;
  color: #2395ff;
  margin-left: 2vw;
}
</style>
