<!-- 我的界面 -->
<template>
  <div class="me">
    <!-- 个人信息 -->
    <div class="headInfo">
      <!-- 头像 -->
      <div class="head-img"></div>
      <div class="head-profile">
        <!-- 用户id -->
        <p class="user-id" v-if="phone_num">{{ phone_num }}</p>
        <!-- 登录/注册 -->
        <p v-else class="user-id" @click="handleLogin">登录/注册</p>
        <!-- 手机号 -->
        <!-- <p class="user-phone">
          <i class="fa fa-mobile"></i>
          <span v-if="userInfo">{{ phone_num }}</span>
          <span v-else>登录后享受更多特权</span>
        </p> -->
      </div>
      <!-- 右箭头 -->
      <i class="fa fa-angle-right"></i>
    </div>
    <!-- 我的地址 -->
    <div v-if="phone_num">
      <div class="address-cell">
        <i class="fa fa-map-marker"></i>
        <div class="address-index" @click="clickMyAddress">
          <span>我的地址</span>
          <i class="fa fa-angle-right"></i>
        </div>
      </div>
      <button @click="handleLogout" class="loginOut-btn">退出登录</button>
    </div>
  </div>
</template>

<script>
import getJsonData from "../../getJsonData.js";
export default {
  name: "me",
  data() {
    return {
      //用户信息
      userInfo: "",
      phone_num: null,
    };
  },
  // 每次进来都重新获取用户信息,刷新界面
  // beforeRouteEnter(to, from, next) {
  //   next(vm => vm.getData());
  // },
  created() {
    this.phone_num = localStorage.getItem("phone_num");
  },
  methods: {
    //push登录界面
    handleLogin() {
      this.$router.push("/login");
    },
    // 退出登录
    handleLogout() {
      localStorage.removeItem("ele_login");
      this.$router.push("/login");
    },
    //点击我的地址
    clickMyAddress() {
      // 有地址跳转到我的地址界面
      this.$router.push("/myAddress");
    }
  }
};
</script>

<style scoped>
.me {
  width: 100%;
  height: 100%;
  overflow: auto;
  box-sizing: border-box;
}

.headInfo {
  display: flex;
  background-image: linear-gradient(90deg, #0af, #0085ff);
  padding: 6.666667vw 4vw;
  color: #fff;
  align-items: center;
}

.head-img {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background-position: 0px 0px;
  background-size: 60px;
  background-image: url(https://shadow.elemecdn.com/faas/h5/static/sprite.3ffb5d8.png);
}

.head-profile {
  overflow: hidden;
  margin-left: 4.8vw;
  flex-grow: 1;
}

.head-profile .user-id {
  max-width: 40vw;
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
  font-size: 1.3rem;
  margin-bottom: 2.133333vw;
  font-weight: 700;
  display: flex;
  align-items: center;
}

.head-profile .user-phone {
  display: flex;
  align-items: center;
  font-size: 0.8rem;
}

.user-phone>i {
  margin-right: 0.666667vw;
  font-size: 1rem;
}

.headInfo>i {
  font-size: 1.2rem;
}

.address-cell {
  margin-top: 2.666667vw;
  border-top: 1px solid #ddd;
  border-bottom: 1px solid #ddd;
  font-size: 1rem;
  line-height: 4.533333vw;
  background: #ffffff;
  display: flex;
  align-items: center;
  padding-left: 6.666667vw;
  color: #333;
}

.address-cell>i {
  font-size: 1.3rem;
  color: rgb(74, 165, 240);
  margin-right: 2.666667vw;
}

.address-index {
  display: flex;
  justify-content: space-between;
  width: 100%;
  padding: 3.733333vw 2.666667vw 3.733333vw 0;
  align-content: center;
}

.address-index>i {
  font-size: 1.3rem;
  color: #ccc;
}

.loginOut-btn {
  display: block;
  width: 100%;
  text-align: center;
  padding: 3.733333vw 0;
  margin: 5.333333vw 0;
  color: #ff5339;
  border-radius: 0.8vw;
  font-size: 1rem;
  font-weight: 700;
  background-color: #fff;
  border: 0;
}
</style>