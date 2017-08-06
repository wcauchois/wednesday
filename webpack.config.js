const webpack = require('webpack');
const DashboardPlugin = require('webpack-dashboard/plugin');

module.exports = {
  entry: [
    './src/js/app.jsx'
  ],
  output: {
    path: __dirname + '/dist',
    publicPath: '/',
    filename: 'bundle.js'
  },
  module: {
    loaders: [{
      test: /\.jsx?$/,
      exclude: /node_modules/,
      loader: 'babel-loader',
      query: {
        presets: ["es2015", "react"]
      }
    }]
  },
  resolve: {
    extensions: ['.js', '.jsx']
  },
  plugins: [
    new DashboardPlugin()
  ],
  devServer: {
    contentBase: './dist'
  }
};
