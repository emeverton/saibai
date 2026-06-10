(function () {
  'use strict';

  var activateTab;

  activateTab = function (root, tabId) {
    var tabs = root.querySelectorAll('.saibai-pdp-tabs__tab');
    var panels = root.querySelectorAll('.saibai-pdp-tabs__panel');
    var i;

    for (i = 0; i < tabs.length; i++) {
      var isActive = tabs[i].getAttribute('data-saibai-tab') === tabId;
      tabs[i].classList.toggle('is-active', isActive);
      tabs[i].setAttribute('aria-selected', isActive ? 'true' : 'false');
      tabs[i].setAttribute('tabindex', isActive ? '0' : '-1');
    }

    for (i = 0; i < panels.length; i++) {
      var panelActive = panels[i].getAttribute('data-saibai-panel') === tabId;
      panels[i].classList.toggle('is-active', panelActive);
      if (panelActive) {
        panels[i].removeAttribute('hidden');
      } else {
        panels[i].setAttribute('hidden', '');
      }
    }
  };

  function bindTabs(root) {
    var tabRoot = root.querySelector('[data-saibai-pdp-tabs]');
    if (!tabRoot) return;

    var tabs = tabRoot.querySelectorAll('.saibai-pdp-tabs__tab');
    var i;

    for (i = 0; i < tabs.length; i++) {
      tabs[i].addEventListener('click', function (event) {
        event.preventDefault();
        var tabId = event.currentTarget.getAttribute('data-saibai-tab');
        if (!tabId || event.currentTarget.classList.contains('is-active')) return;
        activateTab(tabRoot, tabId);
      });

      tabs[i].addEventListener('keydown', function (event) {
        var currentIndex = -1;
        var nextIndex = 0;
        var j;

        if (event.key !== 'ArrowLeft' && event.key !== 'ArrowRight' && event.key !== 'Home' && event.key !== 'End') {
          return;
        }

        for (j = 0; j < tabs.length; j++) {
          if (tabs[j] === event.currentTarget) {
            currentIndex = j;
            break;
          }
        }

        if (currentIndex < 0) return;

        event.preventDefault();

        if (event.key === 'ArrowLeft') {
          nextIndex = currentIndex > 0 ? currentIndex - 1 : tabs.length - 1;
        } else if (event.key === 'ArrowRight') {
          nextIndex = currentIndex < tabs.length - 1 ? currentIndex + 1 : 0;
        } else if (event.key === 'Home') {
          nextIndex = 0;
        } else if (event.key === 'End') {
          nextIndex = tabs.length - 1;
        }

        tabs[nextIndex].focus();
        activateTab(tabRoot, tabs[nextIndex].getAttribute('data-saibai-tab'));
      });
    }
  }

  function hasJudgeMeReviews(widget) {
    if (!widget) return false;
    return !!(
      widget.querySelector('.jdgm-rev')
      || widget.querySelector('.jdgm-rev-widg__reviews .jdgm-rev')
    );
  }

  function checkReviewsWidget() {
    var widgetRoot = document.querySelector('[data-saibai-pdp-reviews-widget]');
    if (!widgetRoot) return;

    function updateReviewsState() {
      var widget = widgetRoot.querySelector('.jdgm-review-widget');
      var reviewsTab = document.getElementById('saibai-tab-avaliacoes');
      var reviewsPanel = document.getElementById('saibai-panel-avaliacoes');
      var tabRoot = document.querySelector('[data-saibai-pdp-tabs]');
      var hasReviews = hasJudgeMeReviews(widget);

      widgetRoot.classList.toggle('saibai-pdp-reviews-widget--has-reviews', hasReviews);
      widgetRoot.classList.toggle('saibai-pdp-reviews-widget--empty', !hasReviews);

      var reviewsSummary = document.querySelector('[data-saibai-pdp-reviews-summary]');

      if (reviewsTab) {
        if (hasReviews) {
          reviewsTab.removeAttribute('hidden');
        } else {
          reviewsTab.setAttribute('hidden', '');
        }
      }

      if (reviewsSummary) {
        if (hasReviews) {
          reviewsSummary.removeAttribute('hidden');
        } else {
          reviewsSummary.setAttribute('hidden', '');
        }
      }

      if (!hasReviews && reviewsPanel && reviewsPanel.classList.contains('is-active') && tabRoot && activateTab) {
        activateTab(tabRoot, 'detalhes');
      }
    }

    updateReviewsState();
    window.setTimeout(updateReviewsState, 800);
    window.setTimeout(updateReviewsState, 2000);
    window.setTimeout(updateReviewsState, 4500);

    if (typeof MutationObserver === 'function') {
      var observer = new MutationObserver(function () {
        updateReviewsState();
      });
      observer.observe(widgetRoot, { childList: true, subtree: true });
      window.setTimeout(function () {
        observer.disconnect();
      }, 12000);
    }
  }

  function init() {
    var sections = document.querySelectorAll('.saibai-pdp-details');
    var i;
    for (i = 0; i < sections.length; i++) {
      bindTabs(sections[i]);
    }
    checkReviewsWidget();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
  document.addEventListener('shopify:section:load', init);
})();
