const webpack = require('webpack');

const javascriptPath = __dirname + '/src/js';

module.exports = {
  entry: [
    'babel-polyfill',
    './app.jsx'
  ],
  context: javascriptPath,
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
    }, {
      test: /\.less$/,
      use: [
        {loader: 'style-loader'},
        {loader: 'css-loader'},
        {loader: 'less-loader'}
      ]
    }]
  },
  resolve: {
    extensions: ['.js', '.jsx'],
    modules: [
      javascriptPath,
      __dirname + '/node_modules'
    ]
  },
  devServer: {
    contentBase: './dist'
  }
};
