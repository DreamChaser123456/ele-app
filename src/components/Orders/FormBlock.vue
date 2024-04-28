<!-- 添加地址的输入框组件 -->
<template>
  <!-- 子组件将点击自己的点击事件传递出去 -->
  <div class="formblock" @click="$emit('clickSelf')">
    <!-- 左边标题 -->
    <div class="label-wrap">{{label}}</div>
    <!-- 右边输入部分 -->
    <div class="input-group-wrap">
      <!-- 输入部分 -->
      <div class="input-wrap">
        <!-- 组件调用使用v-model,组件里面使用:value="value" @input="$emit('input',$event.target.value)"-->
        <!-- 为什么可以这么写?因为v-model的底层原理就是通过绑定value属性，然后通过监听input事件来处理值的变化 -->
        <input
          v-if="!textarea"
          :type="type"
          :placeholder="placeholder"
          :value="value"
          @input="$emit('input',$event.target.value)"
        >
        <textarea
          v-else
          :type="type"
          :placeholder="placeholder"
          :value="value"
          @input="$emit('input',$event.target.value)"
          rows="2"
          maxlength="100"
        ></textarea>
        <!-- 右图片 -->
        <i v-if="icon" :class="'fa fa-'+icon"></i>
      </div>
      <!-- 标签部分 -->
      <TabTag v-if="tags" :tags="tags" :selectTag="sex" @checkTag="checkTag"/>
    </div>
  </div>
</template>

<script>
import TabTag from "./TabTag";
export default {
  name: "FormBlock",
  components: {
    TabTag
  },
  props: {
    type: {
      type: String,
      default: "text" //默认值
    },
    label: String,
    value: String,
    placeholder: String,
    icon: String, //右边图标的名称
    textarea: String, //输入域文字
    tags: Array, //tag数组
    sex: String //选中的性别
  },
  methods: {
    checkTag(item) {
      // console.log(item);
      // 将事件再传递给父组件
      this.$emit("checkSex", item);
    }
  },
};
</script>

<style scoped>
.formblock {
  /* border-top: 0.266667vw solid #eee; */
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
.input-group-wrap {
  flex: 1;
}
.input-wrap {
  flex: 1 1 0;
  padding: 3.733333vw 0;
  display: flex;
  align-items: center;
}
.input-wrap input {
  outline: none;
  line-height: 4.8vw;
  color: #333;
  border: none;
  flex: 1;
  padding-right: 4vw;
  padding-left: 0;
  font-size: 0.9rem;
}

.input-wrap textarea {
  outline: none;
  font-size: 0.9rem;
  line-height: 4.8vw;
  color: #333;
  border: none;
  flex: 1;
  padding-right: 4vw;
  padding-left: 0;
}
.input-wrap i {
  margin-right: 3.2vw;
  color: rgb(102, 102, 102);
  font-size: 1.2rem;
}
</style>
