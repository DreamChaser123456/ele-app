module.exports = {
  // http://localhost:8080/wxzf/dist/
  // publicPath: '/wxzf/dist/', // 打包文件相对路径,根据服务端的实际路径进行修改
  devServer: {
    open: true, //执行命令之后自动打开浏览器
    host: '0.0.0.0',
    port: 8080, //设置端口
    https: false,
    hotOnly: false,
    // // 因为herokuapp.com服务器已经被开放允许任何人访问,所以我们在这里不需要配置跨域了,直接注释掉,在main.js里面设置baseURL就行了
    // proxy: {
    //   // 配置跨域
    //   '/api': {
    //     // 使用axios请求会自动加上这个前缀
    //     target: 'https://ele-interface.herokuapp.com/api/',
    //     ws: true,
    //     changOrigin: true,
    //     // target地址的别名,/api就相当于target
    //     pathRewrite: {
    //       '^/api': ''
    //     }
    //   }
    // },
    before: app => {}
  }
};
