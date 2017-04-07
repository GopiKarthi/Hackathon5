var gulp = require('gulp');
var gulputil = require('gulp-util');

var browserSync = require('browser-sync').create();

gulp.task('browser-sync', function() {
    browserSync.init({
        //files: ['static/css/*.css', 'static/js/*.js'],
        files: ['d3/*.css','./*.html'],
        server: {
            baseDir: ""
        }
    });
    gulp.watch(['./*.html']).on('change',function(){
        //gulp.watch('static/css/*.css', ['dest_css']);
        browserSync.reload('./*.html');
    })

});

gulp.task('bs', ['browser-sync'])
