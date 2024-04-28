<!-- 展示定位信息组件 -->
<template>
  <div class="location">
    <div class="title">当前定位</div>
    <div class="des">
      <i class="fa fa-location-arrow"></i>
      <span>{{address}}</span>
    </div>
  </div>
</template>

<script>
//显示当前定位信息的组件

export default {
  name: "location",
  props: {
    address: String
  }
};
</script>

<style scoped>
.location {
  /* background-color: white; */
  /* width: 100%; */
}

.title {
  margin: 10px 0;
  font-size: 12px;
}
.des i {
  color: #009eef;
}
.des span {
  color: #333;
  font-weight: bold;
  margin-left: 5px;
  display: inline-block;
  width: 90%;
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
}
</style>
