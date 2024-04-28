import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

// types对象
// 设置types的目的是便于我们在vue调试工具中调试的时候看到名字
const types = {
  SET_LOCATION: 'SET_LOCATION', //定位信息
  SET_ADDRESS: 'SET_ADDRESS',   //地址
  ORDER_INFO: 'ORDER_INFO',     //订单信息
  ADDRESS_INFO: 'ADDRESS_INFO', //选中地址信息
  REMARK_INFO: 'REMARK_INFO',   //餐具信息 + 订单备注都存在这一个vuex中
};

// state
const state = {
  location: {},
  address: '',
  orderInfo: null,
  addressInfo: null,
  remarkInfo: {
    tableware: '',
    remark: ''
  }
};

// getters
// Getter 用于对 Store 中的数据进行加工处理形成新的数据，类似 Vue 的计算属性。 Store 中数据发生变化，Getter 的数据也会跟着变化。 
const getters = {
  //不加工,直接返回
  location: state => state.location,
  address: state => state.address,
  orderInfo: state => state.orderInfo,
  addressInfo: state => state.addressInfo,
  //根据订单信息计算总价,所以只有getter方法在,没有state
  totalPrice: state => {
    let price = 0;
    if (state.orderInfo) {
      const selectFoods = state.orderInfo.selectFoods;
      selectFoods.forEach(food => {
        price += food.fixed_price * food.count;
      });
      price += state.orderInfo.restaurant_info.float_delivery_fee;
    }
    return price;
  },
  remarkInfo: state => state.remarkInfo
};

// 定义mutations
const mutations = {
  [types.SET_LOCATION](state, location) {
    if (location) {
      state.location = location;
    } else {
      state.location = null;
    }
  },
  [types.SET_ADDRESS](state, address) {
    if (address) {
      state.address = address;
    } else {
      state.address = '';
    }
  },
  [types.ORDER_INFO](state, orderInfo) {
    if (orderInfo) {
      state.orderInfo = orderInfo;
    } else {
      state.orderInfo = null;
    }
  },
  [types.ADDRESS_INFO](state, addressInfo) {
    if (addressInfo) {
      state.addressInfo = addressInfo;
    } else {
      state.addressInfo = null;
    }
  },
  [types.REMARK_INFO](state, remarkInfo) {
    if (remarkInfo) {
      state.remarkInfo = remarkInfo;
    } else {
      state.remarkInfo = null;
    }
  }
};

// actions
const actions = {
  setLocation: ({ commit }, location) => {
    // 触发mutations的方式间接变更数据
    // 第一个参数是mutations函数名,第二个参数是mutations函数的参数
    commit(types.SET_LOCATION, location);
  },
  setAddress: ({ commit }, address) => {
    commit(types.SET_ADDRESS, address);
  },
  setOrderInfo: ({ commit }, orderInfo) => {
    commit(types.ORDER_INFO, orderInfo);
  },
  setAddressInfo: ({ commit }, addressInfo) => {
    commit(types.ADDRESS_INFO, addressInfo);
  },
  setRemarkInfo: ({ commit }, remarkInfo) => {
    commit(types.REMARK_INFO, remarkInfo);
  }
};

export default new Vuex.Store({
  state,
  getters,
  mutations,
  actions
});
