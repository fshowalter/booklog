(
  function initFilter(factory) {
    'use strict';

    var selectFilterElements = document.querySelectorAll('[data-filter-type="select"]');

    Array.prototype.forEach.call(selectFilterElements, function addEventListenersToNodeListItem(filterElement) {
      filterElement.addEventListener('change', function handleFilterChange(e) {
        var event;

        e.preventDefault();

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
  }(function buildSelectFilterFactory() {
    'use strict';

    function SelectFilter(node) {
      this.node = node;
      this.attribute = node.dataset.filterAttribute || SelectFilter.DEFAULTS.filterAttribute;
    }

    SelectFilter.DEFAULTS = {
      filterAttribute: 'select'
    };

    SelectFilter.prototype.getMatcher = function getMatcher() {
      var attribute = this.attribute;
      var value = this.node.value;

      if (!value) {
        return null;
      }

      return function matcher(item) {
        return item.getAttribute(attribute) === value;
      };
    };


    // Run the standard initializer
    function initialize(node) {
      var filter = new SelectFilter(node);
      node.movielogFilter = filter;

      return node.movielogFilter;
    }

    // Use an object instead of a function for future expansibility;
    return {
      create: initialize
    };
  }())
);
