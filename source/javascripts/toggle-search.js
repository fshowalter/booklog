(
  function initSearchToggle() {
    'use strict';

    var toggleElements = document.querySelectorAll('[data-toggle]');

    function hide(menu, toggle) {
      if (menu.classList.contains('js-toggle_off')) {
        return;
      }

      menu.classList.add('js-toggling', 'js-toggle_off');
      menu.setAttribute('aria-expanded', false);
      toggle.setAttribute('aria-expanded', false);

      menu.addEventListener('transitionend', function handleTransitionEnd(event) {
        if (event.propertyName === 'opacity') {
          menu.removeEventListener('transitionend', handleTransitionEnd);
          this.classList.remove('js-toggling');
          toggle.innerHTML = toggle.getAttribute('data-toggle-label');
        }
      });
    }

    function show(menu, toggle) {
      if (!menu.classList.contains('js-toggle_off')) {
        return;
      }

      menu.classList.add('js-toggling');
      menu.classList.remove('js-toggle_off');
      menu.setAttribute('aria-expanded', true);
      toggle.setAttribute('aria-expanded', true);

      menu.addEventListener('transitionend', function handleTransitionEnd(event) {
        if (event.propertyName === 'opacity') {
          menu.removeEventListener('transitionend', handleTransitionEnd);
          this.classList.remove('js-toggling');
          toggle.innerHTML = 'Cancel';
          if (!/iPad|iPhone|iPod/g.test(navigator.userAgent)) {
            return this.querySelectorAll('input[type="text"]')[0].focus();
          }
        }
      });
    }

    function handleSearchToggleClick() {
      var menu;
      menu = this.previousSibling;

      if (!this.getAttribute('data-toggle-label')) {
        this.setAttribute('data-toggle-label', this.innerHTML);
      }

      if (menu.classList.contains('js-toggling')) {
        return;
      }

      if (menu.classList.contains('js-toggle_off')) {
        show(menu, this);
      } else {
        hide(menu, this);
      }
    }

    function addEventListenerToItemsInNodeList(list, event, fn) {
      Array.prototype.forEach.call(list, function addEventListenerToNodeListItem(item) {
        item.addEventListener(event, fn, false);
      });
    }

    document.documentElement.classList.add('js-search');

    document.documentElement.addEventListener('mousedown', function handleMouseDownToRemoveOutline() {
      return document.documentElement.classList.add('js-no_outline');
    });

    document.documentElement.addEventListener('keydown', function handleKeyDownToAddOutline() {
      return document.documentElement.classList.remove('js-no_outline');
    });

    addEventListenerToItemsInNodeList(toggleElements, 'click', handleSearchToggleClick);
  }()
);


