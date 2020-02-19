var UglifyJS = require("uglify-es");
var fs = require('fs');

file = fs.readFileSync('core/static/core/js/main.js', 'utf8')

result = UglifyJS.minify(file)

fs.writeFile('./core/static/core/js/main.js', , function (err) {
    if (err) throw err;
    console.log('Saved!');
});
