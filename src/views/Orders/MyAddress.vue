<!-- 我的地址界面 -->
<template>
  <div class="myAddress">
    <Header @backClick="$router.go(-1)" :isLeft="true" :title="title" />

    <!-- 显示收货地址 -->
    <div class="address-view">
      <!-- cell -->
      <div class="address-card" v-for="(address, index) in allAddress" :key="index">
        <!-- ✅ -->
        <div class="address-card-select">
          <i class="fa fa-check-circle" v-if="selectIndex == index"></i>
        </div>
        <!-- 主体 -->
        <div class="address-card-body" @click="setAddressInfo(address, index)">
          <!-- 第一行 -->
          <p class="address-card-title">
            <span class="username">{{ address.name }}</span>
            <span v-if="address.sex" class="gender">{{ address.sex }}</span>
            <span class="phone">{{ address.phone }}</span>
          </p>
          <!-- 第二行 -->
          <p class="address-card-address">
            <span class="tag" v-if="address.tag">{{ address.tag }}</span>
            <span class="address-text">{{ address.address }}</span>
          </p>
        </div>
        <!-- 编辑 -->
        <div class="address-card-edit">
          <i @click="handleEdit(address)" class="fa fa-edit"></i>
          <i @click="handleDelete(address, index)" class="fa fa-close"></i>
        </div>
      </div>
    </div>

    <!-- 新增收货地址 -->
    <div class="address-view-bottom" @click="addAddress">
      <i class="fa fa-plus-circle"></i>
      <span>新增收货地址</span>
    </div>
  </div>
</template>

<script>
import getJsonData from "../../getJsonData.js";
import Header from "../../components/Header";
import { Toast } from "mint-ui";
export default {
  name: "MyAddress",
  components: {
    Header
  },
  data() {
    return {
      title: "我的地址",
      allAddress: [], //所有收货地址
      selectIndex: 0, //选中的地址
    };
  },
  // 页面一进入就获取所有收货地址
  beforeRouteEnter(to, from, next) {
    next(vm => vm.getData());
  },
  methods: {
    showMsg(msg) {
      Toast({
        message: msg,
        position: "bottom",
        duration: 2000
      });
    },
    // 新增收货地址
    addAddress() {
      this.$router.push({
        name: "addAddress",
        params: {
          title: "添加地址",
          addressInfo: {
            name: "",    //姓名
            sex: "", //性别
            phone: "",   //手机号
            address: "", //地址
            houseNumber: "",   //门牌号
            tag: "", //标签
          }
        }
      });
    },
    getData() {
      this.$axios.get(`/api/v1/profile/user_address?user_id=${localStorage.getItem("phone_num")}`)
        .then(res => {
          this.allAddress = res.data.addresses;
        });
    },
    // 编辑
    handleEdit(address) {
      this.$router.push({
        name: "addAddress",
        params: { //路由传参
          title: "编辑地址",
          addressInfo: address
        }
      });
    },
    // 删除
    handleDelete(address, index) {
      this.$axios.post('/api/v1/profile/delete_address', { id: address.id })
        .then(() => {
          alert('删除成功');
          this.getData();
        })
        .catch(() => {
          alert('删除失败');
        })
    },
    //选择某个地址
    setAddressInfo(address, index) {
      // 当前选中的地址
      this.selectIndex = index;
      if (this.$route.query.can_click)
      // 将选中的地址对象存储到vuex中
      {
        this.$store.dispatch("setAddressInfo", address);
        this.$router.push("/settlement");
      }
    }
  },
};
</script>

<style scoped>
.myAddress {
  width: 100%;
  height: 100%;
  box-sizing: border-box;
  padding-top: 45px;
}

.address-view-bottom {
  position: fixed;
  height: 13.866667vw;
  bottom: 0;
  width: 100%;
  background: #fff;
  display: flex;
  justify-content: center;
  align-items: center;
  border-top: 0.266667vw solid #ddd;
  color: #3190e8;
  font-size: 1rem;
}

.address-view-bottom>i {
  font-size: 1.3rem;
  margin-right: 8px;
}

.address-view {
  height: 100%;
  overflow-y: auto;
  padding-bottom: 13.866667vw;
}

.address-card {
  background-color: #fff;
  padding: 4vw;
  border-bottom: 1px solid #ddd;
  display: flex;
  min-height: 18.133333vw;
}

.address-card-body {
  flex: 1;
  overflow: hidden;
}

.address-card-title {
  font-size: 1rem;
  color: #666;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  padding-bottom: 1.066667vw;
}

.address-card-title .username {
  color: #333;
  font-weight: 700;
}

.address-card-title .gender {
  padding: 0 1.6vw 0 0.8vw;
}

.address-card-address {
  color: #666;
  font-size: 0.84rem;
  display: flex;
  align-items: center;
}

.address-card-address .tag {
  display: inline-block;
  position: relative;
  margin-right: 0.8vw;
  padding: 0.533333vw;
  color: #ff5722;
  white-space: nowrap;
  border: 1px solid #ff5722;
  border-radius: 0.133333vw;
  font-size: 0.6rem !important;
  line-height: 2.666667vw;
}

.address-text {
  line-height: 4.533333vw;
}

/* 编辑和删除 */
.address-card-edit {
  flex-basis: 13.066667vw;
  display: flex;
  justify-content: space-around;
  align-items: center;
}

.address-card-edit>i {
  color: #aaa;
  font-size: 1.2rem;
}

/*  选中图标 */
.address-card-select {
  flex-basis: 7.333333vw;
  min-width: 7.333333vw;
  display: flex;
  align-items: center;
}

.address-card-select>i {
  font-size: 1.5rem;
  color: #4cd964;
}
</style>
