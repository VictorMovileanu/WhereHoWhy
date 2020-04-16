const path = require("path");
const BundleTracker = require('webpack-bundle-tracker');
const { CleanWebpackPlugin } = require('clean-webpack-plugin');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');


module.exports = (env, options) => {
    return {
        context: __dirname,
        entry: ["./static/src/js/index.js", "./static/src/sass/main.scss"],
        output: {
            path: path.resolve("./static/dist/"),
            filename: options.mode === 'production' ? '[name]-[hash].js' : '[name].js'
        },
        plugins: [
            new CleanWebpackPlugin(),
            new BundleTracker(),
            new MiniCssExtractPlugin({
                filename: options.mode === 'production' ? '[name].[hash].css' : '[name].css',
                chunkFilename: options.mode === 'production' ? '[id].[hash].css' : '[id].css'
            })
        ],
        module: {
            rules: [
                {
                    test: /\.m?js$/,
                    exclude: /node_modules/,
                    use: {
                        loader: "babel-loader",
                        options: {
                            presets: ['@babel/preset-env']
                        }
                    }
                },
                {
                    test: /\.s[ac]ss$/i,
                    loader: [
                        options.mode === 'production' ? MiniCssExtractPlugin.loader : 'style-loader',
                        'css-loader',
                        {
                            loader: "sass-loader",
                            options: {
                                sourceMap: options.mode !== 'production'
                            }
                        }
                    ]
                },
                {
                    test: /\.(png|woff|woff2|svg|eot|ttf|gif|jpe?g)$/,
                    loader: 'file-loader'
                }
            ]
        }
    }
};