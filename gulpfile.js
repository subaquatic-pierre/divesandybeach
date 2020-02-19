const gulp = require('gulp');
var UglifyJS = require("uglify-es");
var pipeline = require('readable-stream').pipeline;

gulp.task('default', done => {
    gulp.src('core/static/core/js/main.js')
        .pipe(UglifyJS.minify())
    gulp.dest('dist')
    done()
});

