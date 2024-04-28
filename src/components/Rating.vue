<!-- 星级组件 -->
<template>
  <div class="Rating-gray">
    <!-- 遍历类名数组,绑定到class上面 -->
    <i v-for="(item,index) in itemClasses" :key="index" class="fa" :class="item"></i>
  </div>
</template>

<script>

// 星星长度
const LENGTH = 5;
// 全星
const CLS_ON = "fa-star";
// 半星
const CLS_HALF = "fa-star-half-empty";
// 没星
const CLS_OFF = "fa-star-o";

export default {
  name: "Rating",
  props: {
    rating: Number
  },
  computed: {
    // 根据星级获取类名数组
    itemClasses() {
      // 4.8   四个全星 1个半星
      let result = [];

      // 对分数进行处理, 向下取0.5的倍数
      // Math.floor 向下取整
      let score = Math.floor(this.rating * 2) / 2;
      // 是否有半星
      let hasDecimal = score % 1 !== 0;
      // 全星数量
      let fullStarCount = Math.floor(score);

      // 全星放入到数组中
      for (let i = 0; i < fullStarCount; i++) {
        result.push(CLS_ON);
      }

      // 半星
      if (hasDecimal) {
        result.push(CLS_HALF);
      }

      // 补齐
      while (result.length < LENGTH) {
        result.push(CLS_OFF);
      }

      return result;
    }
  }
}
</script>

<style scoped>
.Rating-gray {
  margin-right: 1.066667vw;
  color: #ffbe00;
  /* 一行显示 */
  display: inline-block;
}
</style>
