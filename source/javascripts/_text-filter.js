(
  function initSorter(factory) {
    'use strict';

    var textFilterElements = document.querySelectorAll('[data-filter-type="text"]');

    Array.prototype.forEach.call(textFilterElements, function addEventListenersToNodeListItem(filterElement) {
      filterElement.addEventListener('keyup', function handleTextFilterKeyUp() {
        var event;

        if (!this.movielogFilter) {
          factory.create(this);
        }

        if (window.CustomEvent) {
          event = new CustomEvent('filter-changed', {
            'bubbles': true,
            'cancelable': false
          });
        } else {
          event = document.createEvent('CustomEvent');
          event.initCustomEvent('filter-changed', true, true);
        }

        this.dispatchEvent(event);
      });
    });
  }(function buildTextFilterFactory() {
    'use strict';

    function TextFilter(node) {
      this.node = node;
      this.attribute = node.dataset.filterAttribute || TextFilter.DEFAULTS.filterAttribute;
    }

    TextFilter.DEFAULTS = {
      filterAttribute: 'text'
    };

    TextFilter.escapeRegExp = function escapeRegExp(str) {
      return str.replace(/[\-\[\]\/\{\}\(\)\*\+\?\.\\\^\$\|]/g, '\\$&');
    };

    TextFilter.prototype.getMatcher = function getMatcher() {
      var attribute = this.attribute;
      var regex;
      var value = this.node.value;

      if (!value) {
        return null;
      }

      regex = new RegExp(TextFilter.escapeRegExp(value), 'i');

      return function matcher(item) {
        return regex.test(item.getAttribute(attribute));
      };
    };


    // Run the standard initializer
    function initialize(node) {
      var filter = new TextFilter(node);
      node.movielogFilter = filter;

      return node.movielogFilter;
    }

    // Use an object instead of a function for future expansibility;
    return {
      create: initialize
    };
  }())
);
