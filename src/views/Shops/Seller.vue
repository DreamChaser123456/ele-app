<!-- 商家组件 -->
<template>
  <div class="seller" v-if="sellerInfo">
    <!-- 类似于tableview的section -->
    <section>
      <img :src="sellerInfo.header_image" alt>
      <h3>{{sellerInfo.title}}</h3>
      <p>{{sellerInfo.brief}}</p>
      <div>查看品牌故事</div>
    </section>
  </div>
</template>

<script>
import getJsonData from "../../getJsonData.js";
export default {
  name: "Seller",
  data() {
    return {
      // 商家信息
      sellerInfo: null
    };
  },
  created() {
    this.getData();
  },
  methods: {
    getData() {
      this.$axios(`/api/v1/profile/seller_info?restaurant_id=${this.$route.query.shop_id}`).then(res => {
        console.log(res.data);
        this.sellerInfo = res.data[0];
      })
      .catch(res => {
        // 获取假数据
        getJsonData.getJsonDataWithStr("seller", jsonData => {
          this.sellerInfo = jsonData;
        });
      });
    }
  }
};
</script>

<style scoped>
.seller section {
  margin-bottom: 2.666667vw;
  padding: 4.266667vw 4vw 4vw;
  font-size: 0.9rem;
  background-color: #fff;
  color: #666;
  border-bottom: 1px solid #eee;
}
section > img {
  width: 92vw;
  height: 52vw;
  margin-bottom: 4.266667vw;
}
section > h3 {
  color: #333;
  font-weight: 700;
  font-size: 1rem;
  margin-bottom: 1.066667vw;
}
section > p {
  height: 40px;
  line-height: 1.4;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}
section > div {
  margin: 4vw 0 -4vw;
  text-align: center;
  font-size: 0.346667rem;
  padding: 4vw 0;
}
</style>
