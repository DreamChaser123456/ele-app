<template>
  <div class="pay">
    <Header title="在线支付" />
    <div class="main" v-if="orderInfo">
      <div class="tip">
        <p class="countdown-title">支付剩余时间</p>
        <h3 class="countdown-text">{{ countDown }}</h3>
      </div>
      <section class="home">
        <!-- 订单地址列表 -->
        <ul class="list info-list">
          <li>
            <span class="order-name">{{ orderInfo.restaurant_info.name }}</span>
            <span class="text-highlight">¥{{ totalPrice }}</span>
          </li>
        </ul>
        <div class="title">在线支付</div>
        <!-- 支付方式列表 -->
        <ul class="list payment-list">
          <li class="payment-list-item">
            <div class="icon">
              <img src="../../assets/wechart.jpg" alt>
              <span>微信</span>
            </div>
            <i class="fa fa-check-circle selected"></i>
          </li>
        </ul>
      </section>
      <!-- 超时之后不可用 -->
      <button @click="pay" :disabled="timeOut" class="btn-submit">确认支付</button>
    </div>
  </div>
</template>

<script>
import Header from "../../components/Header";
import { setInterval, clearInterval } from "timers";
export default {
  name: "Pay",
  data() {
    return {
      countDown: "00:15:00", //倒计时
      timer: null, //定时器
      timeOut: false,  //已超时
    };
  },
  components: {
    Header
  },
  // 路由一进来就显示倒计时
  beforeRouteEnter(to, from, next) {
    next(vm => {
      vm.countTimeDown();
    });
  },
  beforeRouteLeave(to, from, next) {
    clearInterval(this.timer); // 清除定时器
    next();
  },
  computed: {
    orderInfo() {
      return this.$store.getters.orderInfo;
    },
    totalPrice() {
      return this.$store.getters.totalPrice;
    },
    addressInfo() {
      return this.$store.getters.addressInfo;
    },
    remarkInfo() {
      return this.$store.getters.remarkInfo;
    }
  },
  methods: {
    countTimeDown() {
      let minute = 14;
      let second = 59;

      this.timer = setInterval(() => {
        second--;

        if (second == "00" && minute == "00") {
          this.countDown = "订单已超时";
          clearInterval(this.timer);
          this.timeOut = true;
          return;
        }

        if (second == "00") {
          second = 59;
          minute--;

          // 09  08
          if (minute < 10) {
            minute = "0" + minute;
          }
        }

        if (second < 10) {
          second = "0" + second;
        }

        this.countDown = "00:" + minute + ":" + second;
      }, 1000);
    },
    pay() {
      this.addOrder();
    },
    onBridgeReady(data) {
      //将data传递到这里面
      WeixinJSBridge.invoke("getBrandWCPayRequest", data, res => {
        //这是回调函数
        if (res.err_msg == "get_brand_wcpay_request:ok") {
          // 使用以上方式判断前端返回,微信团队郑重提示：
          // res.err_msg将在用户支付成功后返回ok，但并不保证它绝对可靠。
          // 支付成功, 生成订单
          this.addOrder();
        }
      });
    },
    addOrder() {
      let orderlist = {
        orderInfo: this.orderInfo,
        totalPrice: this.totalPrice,
        addressInfo: this.addressInfo,
        remarkInfo: this.remarkInfo,
        created_at: new Date().getTime().toString(),
        user_id: localStorage.getItem("phone_num"),
        user_addresses_phone: this.addressInfo.phone
      };
      this.$axios.post('/api/v1/profile/add_orders', orderlist, {
        headers: {
          'Content-Type': 'application/json',
        },
      })
        .then((() => {
          alert('订单支付成功！');
          this.$store.dispatch("setOrderInfo", null);
          this.$router.push({ path: "order", force: true });
        }))
        .catch(() => {
          alert('订单支付失败！');
        });

      // this.orderInfo.selectFoods.forEach(element => {
      //   element.count = 0;
      // });
    }
  },
};
</script>

<style scoped>
.pay {
  width: 100%;
  height: 100%;
  box-sizing: border-box;
  padding-top: 45px;
}

.main {
  width: 100%;
  height: 100%;
  overflow: auto;
  box-sizing: border-box;
}

.tip {
  display: block;
  text-align: center;
  background-color: #fff;
  color: #333;
  padding: 2rem;
  line-height: 2rem;
}

countdown-title {
  font-size: 0.88rem;
  color: #999;
}

.countdown-text {
  height: 2rem;
  color: #333;
  font-size: 1.8rem;
}

down-text {
  height: 2rem;
  color: #333;
  font-size: 1.8rem;
}

.list {
  border-bottom: 0.5px solid #eee;
  background: #fff;
}

.info-list {
  padding: 0 1.5rem;
}

.info-list li {
  border-top: 0.5px solid #eee;
  display: flex;
  padding: 1.5rem 0;
  font-size: 1rem;
  line-height: 1rem;
  justify-content: space-between;
}

.info-list li .order-name {
  color: #333;
  display: inline-block;
  vertical-align: bottom;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  margin-right: 16px;
  max-width: 60%;
}

.text-highlight {
  color: #ff6000;
}

.title {
  background-color: #f5f5f5;
  font-size: 0.88rem;
  padding: 1.2rem 1.2rem 1rem;
  color: #999;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.payment-list-item {
  border-bottom: 0.5px solid #eee;
  padding: 0.9rem 1rem;
  font-size: 1.1rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.icon {
  display: flex;
  align-items: center;
}

.payment-list-item img {
  width: 2.4rem;
  height: 2.4rem;
  margin-right: 20px;
}

.payment-list-item>i {
  font-size: 1.5rem;
  color: #eee;
}

.selected {
  color: #4cd964 !important;
}

.btn-submit-wrap {
  margin: 1rem auto;
  width: 90%;
}

.btn-submit {
  font-size: 1.1rem;
  line-height: 1.5rem;
  background-color: #4cd964;
  width: 100%;
  outline: none;
  border: none;
  color: #fff;
  border-radius: 5px;
  padding: 0.5rem;
  box-sizing: border-box;
}

/* 不可点击btn */
.btn-submit[disabled] {
  background-color: #bbb !important;
}
</style>
