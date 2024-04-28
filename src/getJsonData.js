import axios from 'axios'

//根据文件名获取文件数据
function getJsonDataWithStr(str, callBack) {
  if (str) {
    //获取假数据
    axios.get('http://localhost:8080/json/' + str + '.json').then(res => {
      if (callBack) {
        callBack(res.data);
      }
    });
  }
}

export default {getJsonDataWithStr}