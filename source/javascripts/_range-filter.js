/* global noUiSlider */

(
  function initSorter(factory) {
    'use strict';

    var rangeFilters = document.querySelectorAll('[data-filter-type="range"]');

    function handleRangeFilterInit(e) {
      var filter;

      e.preventDefault();

      e.target.removeEventListener(e.type, handleRangeFilterInit);

      filter = this.movielogFilter;

      if (!filter) {
        filter = factory.create(this);
      }

      setTimeout(function redispatchMouseDownEvent() {
        e.target.dispatchEvent(e);
      }, 10);
    }

    Array.prototype.forEach.call(rangeFilters, function addEventListenersToNodeListItem(filterElement) {
      Array.prototype.forEach.call(['mousedown', 'MSPointerDown', 'touchstart'], function bindHandleRangeFilterInit(event) {
        filterElement.addEventListener(event, handleRangeFilterInit, false);
      });

      filterElement.addEventListener('keydown', function handleRangeFilterKeyDown(e) {
        if (e.which !== 9) {
          filterElement.removeEventListener('keydown', handleRangeFilterKeyDown);

          if (this.movielogFilter) {
            factory.create(this);
          }
        }
      });
    });
  }(function buildTextFilterFactory() {
    'use strict';

    function RangeFilter(node) {
      this.node = node;
      this.options = {};
      this.options.filterMinValue = parseInt(node.dataset.filterMinValue || RangeFilter.DEFAULTS.filterMinValue, 10);
      this.options.filterMaxValue = parseInt(node.dataset.filterMaxValue || RangeFilter.DEFAULTS.filterMaxValue, 10);
      this.attribute = node.dataset.filterAttribute || RangeFilter.DEFAULTS.filterAttribute;
      this.slider = node.querySelectorAll('.noUiSlider')[0];
      this.minInput = node.querySelector('.filter-numeric.min');
      this.maxInput = node.querySelector('.filter-numeric.max');

      this.initSlider();
    }

    RangeFilter.prototype.initSlider = function initSlider() {
      var node;
      var minInput;
      var maxInput;
      var slider;

      if (this.slider.noUiSlider) {
        return;
      }

      node = this.node;
      slider = this.slider;
      minInput = this.minInput;
      maxInput = this.maxInput;

      noUiSlider.create(this.slider, {
        range: {
          min: this.options.filterMinValue,
          max: this.options.filterMaxValue
        },
        start: [this.options.filterMinValue, this.options.filterMaxValue],
        step: 1,
        format: {
          to: function formatToValue(value) {
            return value;
          },
          from: function formatFromValue(value) {
            return value;
          }
        }
      });

      this.slider.noUiSlider.on('set', function handleSliderSet() {
        var event;

        if (window.CustomEvent) {
          event = new CustomEvent('filter-changed', {
            'bubbles': true,
            'cancelable': false
          });
        } else {
          event = document.createEvent('CustomEvent');
          event.initCustomEvent('filter-changed', true, true);
        }

        return node.dispatchEvent(event);
      });

      this.slider.noUiSlider.on('update', function handleSliderUpdate(values) {
        minInput.value = values[0];
        maxInput.value = values[1];
      });

      minInput.addEventListener('change', function handleMinInputChange() {
        slider.noUiSlider.set([this.value, null]);
      });

      maxInput.addEventListener('change', function handleMinInputChange() {
        slider.noUiSlider.set([null, this.value]);
      });
    };

    RangeFilter.DEFAULTS = {
      filterAttribute: 'text',
      filterMinValue: 1,
      filterMaxValue: 10
    };

    RangeFilter.prototype.destroy = function destroy() {
      this.node = null;
      this.minInput = null;
      this.maxInput = null;

      if (this.slider) {
        return this.slider.destroy();
      }
    };

    RangeFilter.prototype.getMatcher = function getMatcher() {
      var range;
      var attribute;

      attribute = this.attribute;
      range = this.slider.noUiSlider.get();

      if (range[0] === this.options.filterMinValue && range[1] === this.options.filterMaxValue) {
        return null;
      }

      return function matcher(item) {
        var value;
        value = parseInt(item.getAttribute(attribute), 10);
        return value >= range[0] && value <= range[1];
      };
    };

    // Run the standard initializer
    function initialize(node) {
      var filter = new RangeFilter(node);
      node.movielogFilter = filter;

      return node.movielogFilter;
    }

    // Use an object instead of a function for future expansibility;
    return {
      create: initialize
    };
  }())
);
