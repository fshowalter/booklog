// = require _nouislider-8.0.1
// = require _sorter
// = require _filterer
// = require _text-filter
// = require _range-filter
// = require _select_filter

(
  function setFiltersFromQueryString() {
    'use strict';

    var filter;
    var key;
    var keyUpevent;
    var params;
    var value;

    function getQueryParameters() {
      var map = {};
      var query;
      var queryString = document.location.search;

      queryString.replace(/(^\?)/, '').split('&').map(function mapQueryString(q) {
        query = q.split('=');
        map[query[0]] = query[1];
      });

      return map;
    }

    params = getQueryParameters();

    for (key in params) {
      if ({}.hasOwnProperty.call(params, key)) {
        value = params[key];
        filter = document.querySelector('[data-filter-attribute=data-' + key.toLowerCase() + ']');

        if (filter) {
          filter.value = decodeURI(value);

          keyUpevent = document.createEvent('HTMLEvents');
          keyUpevent.initEvent('keyup', true, false);
          filter.dispatchEvent(keyUpevent);
        }
      }
    }

    document.documentElement.classList.add('js-filters');
  }()
);
