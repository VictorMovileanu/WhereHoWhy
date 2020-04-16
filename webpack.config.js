const path = require("path");
const BundleTracker = require('webpack-bundle-tracker');


module.exports = (env, options) => {
    return {
        context: __dirname,
        entry: ["./static/src/js/index.js", "./static/src/sass/main.scss"],
        output: {
            path: path.resolve("./static/dist/"),
            filename: options.mode === 'production' ? '[name]-[hash].js' : '[name].js'
        },
        plugins: [
            new BundleTracker(),
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
                    use: [
                        {
                            loader: "file-loader",
                            options: {
                                name: options.mode === 'production' ? '[name]-[hash].css' : '[name].css'
                            }
                        },
                        {
                            loader: 'css-loader'
                        },
                        {
                            loader: "postcss-loader"
                        },
                        {
                            loader: 'sass-loader'
                        }
                    ]
                },
                // {
                //     test: /\.(png|woff|woff2|svg|eot|ttf|gif|jpe?g)$/,
                //     loader: 'file-loader'
                // }
            ]
        }
    }
};