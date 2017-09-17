'use strict'

var gulp = require('gulp');
var pug = require('gulp-pug');
var sass = require('gulp-sass');
var sourcemaps = require('gulp-sourcemaps');
var autoprefixer = require('gulp-autoprefixer');
var babel = require('gulp-babel');
var concat = require('gulp-concat');
var eslint = require('gulp-eslint');
var sourcemaps = require('gulp-sourcemaps');
var browserify = require("browserify");
var source =  require("vinyl-source-stream");

// Lint JS/JSX files
gulp.task('eslint', function() {
    return gulp.src('/dest/script/*.js')
        .pipe(eslint({
            baseConfig: {
                "ecmaFeatures": {
                    "jsx": true
                }
            }
        }))
        .pipe(eslint.format())
        .pipe(eslint.failAfterError());
});

gulp.task('views', function() {
    gulp.src('./src/views/*.pug')
        .pipe(pug({pretty: true}).on('error', sass.logError))
        .pipe(gulp.dest('./dest/templates'))
});

// Compile Sass to CSS
gulp.task('sass', function() {
    var autoprefixerOptions = {
        browsers: ['last 2 versions'],
    };
    var filterOptions = '**/*.css';
    var reloadOptions = {
        stream: true,
    };
    return gulp.src('src/style/*.sass')
        .pipe(sourcemaps.init())
        .pipe(sass({outputStyle: 'compressed'}))
        .pipe(autoprefixer(autoprefixerOptions))
        .pipe(sourcemaps.write('./'))
        .pipe(gulp.dest('dest/css'));
});

var paths = {
    main_js: ['./src/script/new.js','./src/script/demo.js','./src/script/info.js','./src/script/blog.js'],
};

gulp.task("babel", function() {
    return browserify(paths.main_js)
        .transform("babelify", {presets: ["es2015", "react"]})
        .bundle()
        .pipe(source("bundle.js"))
        .pipe(gulp.dest("./dest/script"));
});

gulp.task('watch', function() {
    gulp.watch('./src/views/*.pug', ['views'])
    gulp.watch('./src/style/*.sass', ['sass'])
    gulp.watch('./src/script/*.js', ['babel']);
});

gulp.task('build', ['sass', 'views', 'babel']);
gulp.task('default', ['build', 'watch']);
