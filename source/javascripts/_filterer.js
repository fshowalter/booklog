(
  function initFilterer(factory) {
    'use strict';

    var filterControls = document.querySelector('[data-filter-controls]');

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

    filterControls.addEventListener('filter-changed', function handleFilterChanged(e) {
      var filterer;

      filterer = this.movielogFilterer;

      if (!filterer) {
        filterer = factory.create(this);
      }

      filterer.addFilter(e.target.movielogFilter);

      underscoreDebounce(function debouncedFilter() {
        filterer.filter();
      }, 50)();
    });
  }(function buildFiltererFactory() {
    'use strict';

    function Filterer(node) {
      this.itemsSelector = node.dataset.itemsSelector || Filterer.DEFAULTS.itemsSelector;
      this.items = document.querySelectorAll(node.dataset.target + ' ' + this.itemsSelector);
      this.filters = [];
    }

    Filterer.DEFAULTS = {
      itemsSelector: 'li'
    };

    Filterer.nodeListToArray = function nodeListToArray(nodeList) {
      var array = [];
      var i;
      var len;

      for (i = -1, len = nodeList.length; ++i !== len; ) {
        array[i] = nodeList[i];
      }

      return array;
    };

    /*
      Copyright 2009 Nicholas C. Zakas. All rights reserved. MIT Licensed
    */
    Filterer.timedChunk = function timedChunk(items, process, context, callback) {
      var processItem;
      var todo;

      todo = Filterer.nodeListToArray(items);

      processItem = function processItemChunk() {
        var start;
        start = +new Date();

        do {
          process.call(context, todo.shift());
        } while (todo.length > 0 && (+new Date() - start < 50));

        if (todo.length > 0) {
          return setTimeout(processItem, 25);
        } else if (callback) {
          return callback(items);
        }
      };
      return setTimeout(processItem, 25);
    };

    Filterer.prototype.addFilter = function addFilter(filter) {
      if (this.filters.indexOf(filter) === -1) {
        return this.filters.push(filter);
      }
    };

    Filterer.getMatchers = function getMatchers(filters) {
      var filter;
      var i;
      var len;
      var matcher;
      var matchers = [];

      for (i = 0, len = filters.length; i < len; i++) {
        filter = filters[i];
        matcher = filter.getMatcher();

        if (matcher) {
          matchers.push(matcher);
        }
      }

      return matchers;
    };

    Filterer.prototype.filter = function filter() {
      var matcher;
      var matchers = Filterer.getMatchers(this.filters);

      function matchItem(item) {
        var i;
        var len;
        var match = true;

        for (i = 0, len = matchers.length; i < len; i++) {
          matcher = matchers[i];
          if (!matcher(item)) {
            match = false;
            break;
          }
        }
        if (match) {
          item.removeAttribute('style');
        } else {
          item.style.display = 'none';
        }
      }

      Filterer.timedChunk(this.items, matchItem);
    };

    // Run the standard initializer
    function initialize(node) {
      var filterer = new Filterer(node);
      node.movielogFilterer = filterer;

      return node.movielogFilterer;
    }

    // Use an object instead of a function for future expansibility;
    return {
      create: initialize
    };
  }())
);

