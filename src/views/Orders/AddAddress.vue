<!-- 添加/编辑收货地址界面 -->
<template>
  <div class="addAddress">
    <Header @backClick="$router.go(-1)" :isLeft="true" :title="title" />
    <!-- 添加地址 -->
    <div class="viewbody">
      <div class="content">
        <!-- 组件调用使用v-model,组件里面使用:value="value" @input="$emit('input',$event.target.value)"-->
        <!-- 为什么可以这么写?因为v-model的底层原理就是通过绑定value属性，然后通过监听input事件来处理值的变化 -->
        <FormBlock v-model="addressInfo.name" label="联系人" placeholder="姓名" :tags="sexes" :sex="addressInfo.sex"
          @checkSex="checkSex" />
        <FormBlock v-model="addressInfo.phone" label="电话" placeholder="手机号码" />
        <FormBlock v-model="addressInfo.address" @clickSelf="showSearch = true" label="地址" placeholder="小区/写字楼/学校等"
          icon="angle-right" />
        <FormBlock v-model="addressInfo.houseNumber" label="门牌号" placeholder="10号楼5单元404" icon="edit"
          textarea="textarea" />
        <div class="formblock">
          <div class="label-wrap">标签</div>
          <TabTag :tags="tags" :selectTag="addressInfo.tag" @checkTag="checkTag" />
        </div>
      </div>
      <!-- 确定按钮 -->
      <div class="form-button-wrap">
        <button @click="handleSave" class="form-button">确定</button>
      </div>
    </div>
    <!-- 搜索地址组件 -->
    <AddressSearch @close="showSearch = false" :showSearch="showSearch" :addressInfo="addressInfo" />
  </div>
</template>

<script>
import getJsonData from "../../getJsonData.js";
import Header from "../../components/Header";
import FormBlock from "../../components/Orders/FormBlock";
import TabTag from "../../components/Orders/TabTag";
import AddressSearch from "../../components/Orders/AddressSearch";
import { Toast } from "mint-ui";
export default {
  name: "AddAddress",
  components: {
    Header,
    FormBlock,
    TabTag,
    AddressSearch
  },
  data() {
    return {
      title: "", //当前界面标题
      tags: ["家", "学校", "公司"],
      sexes: ["先生", "女士"],
      addressInfo: { //添加的地址对象信息
        name: "",    //姓名
        sex: "", //性别
        phone: "",   //手机号
        address: "", //地址
        houseNumber: "",   //门牌号
        tag: "", //标签
      },
      showSearch: false //是否显示搜索组件
    };
  },
  //接收跳转携带的参数
  beforeRouteEnter(to, from, next) {
    next(vm => {
      vm.addressInfo = to.params.addressInfo;
      vm.title = to.params.title;
    });
  },
  methods: {
    // 点击地址标签
    checkTag(item) {
      // console.log(item);
      this.addressInfo.tag = item;
    },
    // 点击性别标签
    checkSex(item) {
      // console.log(item);
      this.addressInfo.sex = item;
    },
    // 点击确定
    handleSave() {
      // console.log(this.addressInfo);
      if (!this.addressInfo.name) {
        this.showMsg("请输入联系人");
        return;
      }

      if (!this.addressInfo.phone) {
        this.showMsg("请输入手机号");
        return;
      }

      if (!this.addressInfo.address) {
        this.showMsg("请输入收货地址");
        return;
      }

      if (!this.addressInfo.houseNumber) {
        this.showMsg("请输入门牌号");
        return;
      }

      // 存储数据
      if (this.title == "添加地址") {
        this.addAddress();
      } else {
        this.editAddress();
      }
    },
    showMsg(msg) {
      Toast({
        message: msg,
        position: "bottom",
        duration: 2000
      });
    },
    //添加地址
    addAddress() {
      this.addressInfo.user_id = localStorage.getItem("phone_num");

      this.$axios.post('/api/v1/profile/add_address', this.addressInfo)
        .then(() => {
          alert('添加成功');
          this.$store.commit('ADDRESS_INFO', this.addressInfo);
          this.$router.go(-1);
        })
        .catch(() => {
          alert('添加失败');
        })
      // 存到本地
      // let addresssArr = JSON.parse(localStorage.getItem("ele_newAddress"))
      // if (!addresssArr) {
      //   // 将地址对象放到数组中存储
      //   localStorage.setItem("ele_newAddress", JSON.stringify([this.addressInfo]));
      // } else { //取出本地存储的数据,拼接后再存储
      //   let localArr = JSON.parse(localStorage.getItem("ele_newAddress"));
      //   localArr.push(this.addressInfo);
      //   localStorage.setItem("ele_newAddress", JSON.stringify(localArr));
      // }

      //存到vuex中
      // if (!this.$store.getters.addressInfo) {
      //   this.$store.dispatch("setAddressInfo", this.addressInfo);
      // }
      //返回我的地址界面

      return;
      this.$axios
        .post(
          `/api/user/add_address/${localStorage.ele_login}`,
          this.addressInfo
        )
        .then(res => {
          //存到vuex中
          if (!this.$store.getters.userInfo) {
            this.$store.dispatch("setUserInfo", this.addressInfo);
          }
          //返回我的地址界面
          this.$router.push("myAddress");
        })
        .catch(err => {
          console.log(err);
        });
    },
    //编辑地址
    editAddress() {
      this.$axios.post('/api/v1/profile/edit_address', this.addressInfo)
        .then(() => {
          alert('修改成功');
          this.$router.go(-1);
        })
        .catch(() => {
          alert('修改失败');
        });
    }
  },
};
</script>

<style scoped>
.addAddress {
  width: 100%;
  height: 100%;
  box-sizing: border-box;
  padding-top: 45px;
}

.viewbody {
  width: 100%;
  height: 100%;
  overflow: auto;
  box-sizing: border-box;
  background-color: #f5f5f5;
}

.content {
  padding-left: 4vw;
  background: #fff;
  font-size: 0.94rem;
}

.formblock {
  background-color: #fff;
  border-bottom: 1px solid #eee;
  display: flex;
}

.formblock .label-wrap {
  flex-basis: 17.333333vw;
  padding: 3.733333vw 0;
  line-height: 4.8vw;
  color: #333;
  font-weight: 700;
}

/* 确定按钮 */
.form-button-wrap {
  padding: 5.333333vw 4vw;
  display: flex;
}

.form-button-wrap .form-button {
  background: #00d762;
  text-align: center;
  border-radius: 0.533333vw;
  flex: 1;
  font-size: 1.1rem;
  line-height: 5.066667vw;
  color: #fff;
  padding: 3.333333vw 0;
  border: none;
  font-weight: 500;
}
</style>
