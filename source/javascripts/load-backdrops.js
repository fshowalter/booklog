(
  function initMovielogBackdrops() {
    'use strict';

    var debouncedUpdate;

    function retinaWidth(node, retinaMultiplier) {
      return Math.ceil(node.offsetWidth * retinaMultiplier);
    }

    function updateWidthInImageUrl(baseUrl, width) {
      return baseUrl.replace(/w\d*-l75-rj/, 'w' + width + '-l75-rj');
    }

    function backgroundImageUrlForNode(node, retinaMultiplier) {
      var url = node.getAttribute('data-backdrop');
      var width = retinaWidth(node, retinaMultiplier);

      return updateWidthInImageUrl(url, width);
    }

    function updateBackgroundImageForNode(node, retinaMultiplier) {
      var imageUrl = backgroundImageUrlForNode(node, retinaMultiplier);
      var image = new Image();

      image.onload = function cacheImage() {
        node.style.backgroundImage = 'url(' + imageUrl + ')';
        node.classList.add('loaded');
        image = null;
      };

      image.src = imageUrl;
    }

    function updateBackgroundImages() {
      var i;
      var nodes = document.querySelectorAll('[data-backdrop]');
      var retinaMultiplier = window.devicePixelRatio || 1;

      // cache nodelist length
      var nodesLength = nodes.length;

      // loop through nodes
      for (i = 0; i < nodesLength; i++) {
        // cache node
        updateBackgroundImageForNode(nodes[i], retinaMultiplier);
      }
    }

    function underscoreDebounce(func, wait, immediate) {
      var args;
      var context;
      var result;
      var timeout;
      var timestamp;

      var later = function later() {
        var last = (new Date() - timestamp);

        if (last < wait && last >= 0) {
          timeout = setTimeout(later, wait - last);
        } else {
          timeout = null;
          if (!immediate) {
            result = func.apply(context, args);
            if (!timeout) context = args = null;
          }
        }
      };

      return function debouncedFunction() {
        var callNow = immediate && !timeout;

        context = this;
        args = arguments;
        timestamp = new Date();

        if (!timeout) timeout = setTimeout(later, wait);
        if (callNow) {
          result = func.apply(context, args);
          context = args = null;
        }

        return result;
      };
    }

    debouncedUpdate = underscoreDebounce(function getDebouncedUpdate() {
      requestAnimationFrame(updateBackgroundImages);
    }, 250);

    window.addEventListener('resize', debouncedUpdate, false);
    window.addEventListener('load', function updateBackgroundImagesOnLoad() {
      updateBackgroundImages();
    }, false);

    function update() {
      requestAnimationFrame(updateBackgroundImages);
    }

    window.MovielogBackdrops = {
      update: update
    };
  }()
);
