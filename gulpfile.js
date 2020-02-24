// Initialize Modules

// const autoprefixer = require('autoprefixer');
// const cssnano = require('cssnano');
const gulp = require('gulp');
const concat = require('gulp-concat');
// const postcss = require('gulp-postcss');
// const replace = require('gulp-replace');
// const sass = require('gulp-sass');
// const sourcemaps = require('gulp-sourcemaps');
const terser = require('gulp-terser');

// File path variables
// Be sure to add directories for different apps
const files = {
    // coreScssPath: 'core/static/core/scss/main.scss',
    // coreJsPath: 'core/static/core/js/main.js',
    // cssFolder: 'core/static/core/css/build/main.css',
    jsFolder: 'core/static/core/js/'
    // htmlFolder: 'core/templates/core/**/*.html',
}

// // Sass Task

// function scssTask() {
//     return gulp.src(files.coreScssPath)
//         .pipe(sourcemaps.init())
//         .pipe(sass())
//         .pipe(postcss([autoprefixer(), cssnano()]))
//         .pipe(sourcemaps.write('.'))
//         .pipe(gulp.dest('./dist')
//         );
// }

// // Cachebusting

// const cbString = new Date().getTime();
// function cacheCssBustTask() {
//     return gulp.src('core/templates/core/style_links.html')
//         .pipe(replace(/cd=\d+/g, 'cb=' + cbString))
//         .pipe(gulp.dest('.')
//         );
// }

// function cacheJsBustTask() {
//     return gulp.src('core/templates/core/scripts.html')
//         .pipe(replace(/cd=\d+/g, 'cb=' + cbString))
//         .pipe(gulp.dest('.')
//         );
// }

// JS task

function jsTask() {
    return gulp.src(files.jsFolder + 'main.js')
        .pipe(concat('main.min.js'))
        .pipe(terser())
        .pipe(gulp.dest(files.jsFolder)
        );
}

// Watch Task

function watchTask() {
    gulp.watch([files.jsFolder + 'main.js'],
        gulp.parallel(jsTask)
    );
}

// Default Task

exports.default = gulp.series(
    gulp.parallel(jsTask),
    watchTask
);
