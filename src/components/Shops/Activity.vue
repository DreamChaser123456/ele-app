<!-- 优惠活动信息组件 -->
<template>
  <div class="rst-activity" v-if="activities">
    <!-- 满减文字 -->
    <div class="activity-txt">
      <!-- 满减 -->
      <span :style="{ background: '#' + activities[0].icon_color }">{{ activities[0].icon_name }}</span>
      <!-- 满xx减xx -->
      <span>{{ activities[0].description }}</span>
    </div>
    <!-- 满减数量 -->
    <div class="activity-count" @click="showSheet = true">
      <span>{{ activities.length }}个优惠</span>
      <!-- ⬇️箭头 -->
      <i class="fa fa-caret-down"></i>
    </div>
    <!-- 优惠弹窗 -->
    <transition name="fade">
      <!-- 最大的容器 -->
      <div class="act-model" v-show="showSheet">
        <!-- 弹窗容器 -->
        <div class="activity-sheet">
          <h2>优惠活动</h2>
          <i @click="showSheet = false" class="fa fa-remove"></i>
          <!-- 优惠活动 -->
          <ul>
            <li v-for="(item, index) in activities" :key="index">
              <!-- 颜色 -->
              <span :style="{ background: '#' + item.icon_color }">{{ item.icon_name }}</span>
              <!-- 文字 -->
              <span>{{ item.description }}</span>
            </li>
          </ul>
        </div>
      </div>
    </transition>
  </div>
</template>

<script>
export default {
  name: "Activity",
  data() {
    return {
      showSheet: false
    };
  },
  props: {
    // 优惠信息数组
    activities: Array
  }
};
</script>

<style scoped>
.rst-activity {
  display: flex;
  color: #333;
  margin: 3.2vw auto 0;
  align-items: center;
  font-size: 0.6rem;
  width: 80vw;
}

.rst-activity .activity-txt {
  flex: 1;
  overflow: hidden;
}

.activity-txt span:first-child {
  color: #fff;
  height: 4.466667vw;
  line-height: 3.466667vw;
  font-size: 0.6rem;
  padding: 0.533333vw 1.2vw;
  margin-right: 1.6vw;
  display: inline-block;
  box-sizing: border-box;
  border-radius: 0.266667vw;
}

.activity-count {
  width: 16.266667vw;
  flex-shrink: 0;
  padding-right: 2.933333vw;
  text-align: right;
  color: #999;
}

.activity-count span {
  margin-right: 1vw;
}

.act-model {
  /* 使用固定定位,让弹窗全屏显示 */
  position: fixed;
  width: 100%;
  height: 100%;
  top: 0;
  left: 0;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  background: rgba(0, 0, 0, 0.5);
  /* 使弹窗在最上面 */
  z-index: 99;
}

.activity-sheet {
  position: absolute;
  background-color: #f5f5f5;
  box-shadow: 0 -1px 5px 0 rgba(0, 0, 0, 0.4);
  bottom: 0;
  left: 0;
  right: 0;
  z-index: 100;
  padding: 5.333333vw 6.933333vw;
  box-sizing: border-box;
}

.activity-sheet h2 {
  text-align: center;
  font-size: 1.1rem;
  font-weight: 600;
  margin-bottom: 4.133333vw;
}

.activity-sheet ul {
  height: 50.8vw;
  overflow-y: scroll;
}

.activity-sheet ul li {
  margin-bottom: 3.066667vw;
  display: flex;
  font-size: 0.82rem;
  align-items: center;
}

.activity-sheet ul li span:first-child {
  height: 4.266667vw;
  padding: 0.533333vw 1.6vw;
  margin-right: 1.6vw;
  display: inline-block;
  box-sizing: border-box;
  border-radius: 0.266667vw;
  color: #fff;
  white-space: nowrap;
}

.activity-sheet ul li span:last-child {
  line-height: 1.38;
  flex: 1;
}

.act-model .fa-remove {
  position: absolute;
  font-size: 1.4rem;
  right: 2.666667vw;
  top: 2.666667vw;
  z-index: 1002;
  color: #888;
}

/* 弹窗动画 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.25s ease-out;
}

.fade-enter,
.fade-leave-to {
  opacity: 0;
}
</style>
