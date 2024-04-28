<template>
  <div class="login">
    <div class="logo">
      <img src="../assets/logo.jpg" alt="my login image">
    </div>
    <!-- 使用组件,传递参数 -->
    <!-- 手机号 -->
    <InputGroup
      type="number"
      v-model="phone"
      placeholder="手机号"
      :btnTitle="btnTitle"
      :disabled="disabled"
      :error="errors.phone"
      @btnClick="getVerifyCode"
    />
    <!-- 验证码 -->
    <InputGroup type="number" v-model="verifyCode" placeholder="验证码" :error="errors.code"/>

    <!-- 用户服务协议 -->
    <div class="login_des">
      <p>
        新用户登录即自动注册，表示已同意
        <span>《用户服务协议》</span>
      </p>
    </div>
    <!-- 登录按钮 -->
    <div class="login_btn">
      <button :disabled="isClicked" @click="handleLogin">登录</button>
    </div>
  </div>
</template>

<script>
// 导入组件
import InputGroup from "../components/InputGroup";
export default {
  name: "login",
  //一定要注册组件
  components: {
    InputGroup
  },
  data() {
    return {
      phone: "",
      verifyCode: "",
      errors: {},
      btnTitle: "获取验证码",
      disabled: false
    };
  },
  //登录按钮是否可用的计算属性
  computed: {
    isClicked() {
      if (!this.phone || !this.verifyCode) return true;
      else return false;
    }
  },
  methods: {
    handleLogin() {

      //假登录, 存储用户id
      localStorage.setItem("ele_login","5cd437fef7a6970017c415fe");
      localStorage.setItem('phone_num', this.phone);
      //push到index界面
      this.$router.push("/");
      return;

      //清空错误信息
      this.errors = {};
      //登录请求
      this.$axios.post("/api/post/sms_back", {
        phone:this.phone,
        code:this.verifyCode
      })
      .then(res => {
        // console.log(res);
        // 检验成功 设置登录状态并且跳转到/
        localStorage.setItem("ele_login", res.data.user._id);
        this.$router.push("/");
      })
      .catch(err => {
        this.errors = {
          code: err.response.data.msg
        };
      });
    },
    //点击获取验证码
    getVerifyCode() {
      if (this.validatePhone()) {
        // 倒计时
        this.validateBtn();
        //发送网络请求
        this.$axios.post("/api/post/sms_send",{
          tpl_id: "140481",
          key: "795be723dd9e88c3ea98e2b6713ab795",
          phone: this.phone
        })
        .then(res => {
          console.log(res);
        });
      }
    },
    //验证手机号码
    validatePhone() {
      if(!this.phone) { //没有手机号
        this.errors = {
          phone: "手机号码不能为空"
        };
        return false;
      } else if (!/^1[345678]\d{9}$/.test(this.phone)) { //手机号码不对
        this.errors = {
          phone: "请填写正确的手机号码"
        };
        return flase;
      } else {
        this.errors = {};
        return true;
      }
    },
    //倒计时60s
    validateBtn() {
      let time = 60;
      let tiemr = setInterval(() => {
        if(time == 0) {
          clearInterval(tiemr);
          this.btnTitle = "获取验证码";
          this.disabled = false;
        } else {
          this.btnTitle = time + "秒后重试";
          this.disabled = true;
          time--;
        }
      }, 1000);
    }
  }
};
</script>

<style scoped>
.login {
  width: 100%;
  height: 100%;
  padding: 30px;
  box-sizing: border-box;
  background: #fff;
}

.logo {
  text-align: center;
}
.logo img {
  width: 150px;
}
.text_group,
.login_des,
.login_btn {
  margin-top: 20px;
}
.login_des {
  color: #aaa;
  line-height: 22px;
}
.login_des span {
  color: #4d90fe;
}
.login_btn button {
  width: 100%;
  height: 40px;
  background-color: #48ca38;
  border-radius: 4px;
  color: white;
  font-size: 14px;
  border: none;
  outline: none;
}
/* 属性选择器,选择disabled为true的button,如果没有disabled,不选中 */
.login_btn button[disabled] {
  background-color: #8bda81;
}
</style>