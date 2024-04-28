<!-- 筛选外卖门店组件 -->
<template>
  <!-- @click.self 点击自己的时候才触发事件 -->
  <!-- isSort 是否显示蒙版 -->
  <div :class="{ 'open': isSort || isScreen }" @click.self="hideView">
    <!-- 筛选条 -->
    <div v-if="filterData" class="filter_wrap">
      <nav class="filter">
        <div class="filter-nav" v-for="(item, index) in filterData.navTab" :key="index"
          :class="{ 'filter-bold': currentFilter == index }" @click="filterSort(index)">
          <span>{{ item.name }}</span>
          <!-- 有图标才显示 -->
          <i v-if="item.icon" :class="'fa fa-' + item.icon"></i>
        </div>
      </nav>
    </div>
    <!-- 排序模块 -->
    <section class="filter-extend" v-if="isSort">
      <ul>
        <!-- @click="selectSort(item,index) 点击 -->
        <li v-for="(item, index) in filterData.sortBy" :key="index" @click="selectSort(item, index)">
          <span :class="{ 'selectName': currentSort == index }">{{ item.name }}</span>
          <i v-show="currentSort == index" class="fa fa-check"></i>
        </li>
      </ul>
    </section>
    <!-- 筛选模块 -->
    <section class="filter-extend" v-if="isScreen">
      <div class="filter-sort">
        <div v-for="(screen, index) in filterData.screenBy" :key="index" class="morefilter">
          <!-- 标题 -->
          <p class="title">{{ screen.title }}</p>
          <!-- item列表 -->
          <ul>
            <li v-for="(item, i) in screen.data" :key="i" :class="{ 'selected': item.select }"
              @click="selectScreen(item, screen)">
              <img v-if="item.icon" :src="item.icon" alt="">
              <span>{{ item.name }}</span>
            </li>
          </ul>
        </div>
      </div>
      <!-- 清空和确定按钮 -->
      <div class="morefilter-btn">
        <span :class="{ 'canClear': canClear }" class="morefilter-clear" @click="clearFilter">清空</span>
        <span class="morefilter-ok" @click="filterOK">确定</span>
      </div>
    </section>
  </div>

</template>

<script>
export default {
  name: "FilterView",
  props: {
    filterData: Object
  },
  created() {
    // console.log("filterview输出了filterdata",this.filterData)
  },
  data() {
    return {
      currentFilter: 0, //当前选中的下标
      isSort: false, //是否点击了综合排序
      isScreen: false, //是否点击了筛选
      currentSort: 0, //默认选择的排序方式
    };
  },
  computed: {
    //是否可以清空 计算属性
    canClear() {
      let clear = false;
      this.filterData.screenBy.forEach(ele => {
        ele.data.forEach(item => {
          if (item.select) {
            clear = true;
          }
        });
      });
      return clear;
    }
  },
  methods: {
    // 点击segment
    filterSort(index) {
      this.currentFilter = index;
      switch (index) {
        case 0: //点击综合排序
          this.isSort = true;
          this.isScreen = false;
          // 让父控件的搜索框固定定位,显示最上面
          this.$emit("searchFixed", true);
          break;
        case 1: //点击距离最近
          this.$emit("update", {
            //将排序条件传给父控件
            condition: this.filterData.navTab[1].condition
          });
          this.hideView();
          break;
        case 2: //点击品牌
          this.$emit("update", {
            //将排序条件传给父控件
            condition: this.filterData.navTab[2].condition
          });
          this.hideView();
          break;
        case 3: //点击筛选
          this.isScreen = true;
          this.isSort = false;
          this.$emit("searchFixed", true);
          break;
        default:
          this.hideView();
          break;
      }
    },
    // 隐藏蒙版
    hideView() {
      this.isSort = false;
      this.isScreen = false;
      //通知父控件恢复原状
      this.$emit("searchFixed", false);
    },
    selectSort(item, index) {
      //点谁选中谁
      this.currentSort = index;
      // 修改数据
      this.filterData.navTab[0].nameStr = this.filterData.sortBy[index].nameStr;
      this.hideView();

      // 通知父控件更新数据
      this.$emit("update", { condition: item.code });
    },
    selectScreen(item, screen) {
      if (screen.id !== "MPI") { //非商家服务 单选
        //先烦反选
        screen.data.forEach(ele => {
          //再选中
          ele.select = false;
        });
        item.select = true;
      } else { //商家服务 多选
        item.select = !item.select;
      }
    },
    // 点击清空按钮
    clearFilter() {
      this.filterData.screenBy.forEach(ele => {
        ele.data.forEach(item => {
          item.select = false;
        });
      });
    },
    // 点击确定按钮
    filterOK() {
      let screenData = {
        //商家服务
        MPI: "",
        // 优惠活动
        offer: "",
        // 人均消费
        per: ""
      };
      let mpiStr = "";
      this.filterData.screenBy.forEach(ele => {
        ele.data.forEach((item, index) => {
          if (item.select) {
            //两种情况  1.多选  2.单选
            if (ele.id !== "MPI") { //单选
              if (item.code.length !== 0) {
                screenData[ele.id] = item.code;
              }
            } else { //多选 商家服务
              if (item.code.length !== 0) {
                mpiStr += item.code + ",";
              }
              // 赋值
              screenData[ele.id] = mpiStr;
            }
          }
        });
      });
      //多选去掉末尾的,
      screenData.MPI = screenData.MPI.substr(0, screenData.MPI.length - 1);
      // 通知父控件更新数据
      this.$emit("update", { condition: screenData });
      // console.log(screenData);
      this.hideView();
    }
  }
}
</script>

<style scoped>
.filter_wrap {
  background: #fff;
  /* sticky 是粘性的意思,设置position: sticky;和top: 54px;可以实现上滑头部停留的效果 */
  position: sticky;
  left: 0;
  right: 0;
  top: 14vw;
  z-index: 10;
}

/* 如果有蒙版,就修改定位方式 */
.open .filter_wrap {
  position: relative;
}

.filter {
  position: relative;
  border-bottom: 1px solid #ddd;
  line-height: 10.4vw;
  z-index: 101;
  height: 10.666667vw;
  display: flex;
  justify-content: space-around;
}

.filter-nav {
  flex: 1;
  text-align: center;
  color: #666;
  font-size: 0.8333rem;
}

.filter-nav i {
  width: 1.6vw;
  height: 0.8vw;
  margin-left: 1.333333vw;
  margin-bottom: 0.533333vw;
  fill: #333;
  will-change: transform;
}

.filter-bold {
  font-weight: 600;
  color: #333;
}

/* 固定定位,全屏显示 */
.open {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  transition: all 0.3s ease-in-out;
  z-index: 3;
}

.filter-extend {
  background-color: #fff;
  color: #333;
  padding-top: 2.133333vw;
  position: absolute;
  width: 100%;
  z-index: 4;
  left: 0;
  top: 24.533333vw;
}

.filter-extend li {
  position: relative;
  padding-left: 5.333333vw;
  line-height: 10.666667vw;
  overflow: hidden;
}

.fa-check {
  float: right;
  color: #009eef;
  margin-right: 3.733333vw;
  line-height: 10.666667vw;
}

/* 选中文字的颜色 */
.selectName {
  color: #009eef;
}

/* 筛选 */
.filter-sort {
  background: #fff;
  padding: 0 2.666667vw;
  line-height: normal;
}

.morefilter {
  margin: 2.666667vw 0;
  overflow: hidden;
}

.morefilter .title {
  margin-bottom: 2vw;
  color: #666;
  font-size: 0.5rem;
}

.morefilter ul {
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  font-size: 0.8rem;
}

.morefilter li {
  box-sizing: border-box;
  width: 30%;
  height: 9.333333vw;
  line-height: 9.333333vw;
  margin: 0.8vw 1%;
  background: #fafafa;
}

.morefilter li img {
  width: 3.466667vw;
  height: 3.466667vw;
  vertical-align: middle;
  margin-right: 0.8vw;
}

.morefilter li span {
  margin-left: 2%;
  vertical-align: middle;
}

.morefilter-btn {
  display: flex;
  justify-content: space-around;
  align-items: center;
  background-color: #fafafa;
  box-shadow: 0 -0.266667vw 0.533333vw 0 #ededed;
  line-height: 11.466667vw;
  box-sizing: border-box;
}

.morefilter-btn span {
  font-size: 0.826667rem;
  text-align: center;
  text-decoration: none;
  flex: 1;
}

.morefilter-clear {
  color: #ddd;
  background: #fff;
}

.morefilter-ok {
  color: #fff;
  background: #00d762;
  border: 0.133333vw solid #00d762;
}

.selected {
  color: #3190e8 !important;
  background-color: #edf5ff !important;
}

.canClear {
  color: #333 !important;
}
</style>
