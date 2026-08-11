const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  // 關閉全套件庫 Babel 重複轉譯（大幅加速啟動與編譯）
  transpileDependencies: false,

  devServer: {
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        pathRewrite: { '^/api': '' }
      }
    }
  },

  configureWebpack: {
    // 啟用 Webpack 5 本地磁碟快取，大幅加速 pnpm run serve 的二次啟動速度
    cache: {
      type: 'filesystem',
    },
  },

  pluginOptions: {
    vuetify: {
			// https://github.com/vuetifyjs/vuetify-loader/tree/next/packages/vuetify-loader
		}
  }
})
