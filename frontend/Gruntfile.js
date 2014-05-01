module.exports = function(grunt) {

  // Project configuration.
  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),

    // LESS
    less: {
      debug: {
        options: {
          compile: true,
          paths: ['bower_components/bootstrap/less']
        },
        files: {
          'app/style/main.css': ['app/style/main.less']
        }
      }
    },

    // Watch files
    watch: {
      styles: {
        files: ['app/style/*.less'],
        tasks: 'less'
      }
    },

    // Running the server. Debug doesn't need to keepalive because watch
    connect: {
      debug: {
        options: {
          port: 8888,
          base: ['app', 'bower_components/bootstrap/dist']
        }
      },
    }
  });

  grunt.loadNpmTasks('grunt-contrib-less');
  grunt.loadNpmTasks('grunt-contrib-connect');
  grunt.loadNpmTasks('grunt-contrib-watch');

  grunt.registerTask('serve', ['less', 'connect', 'watch'])

  grunt.registerTask('default', ['debug', 'release']);
};