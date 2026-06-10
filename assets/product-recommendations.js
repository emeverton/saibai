if (!customElements.get("product-recommendations")){
  class ProductRecommendations extends HTMLElement {
    observer = undefined;

    constructor() {
      super();
    }

    connectedCallback() {
      this.initializeRecommendations(this.dataset.productId);
    }

    initializeRecommendations(productId) {
      this.observer?.unobserve(this);
      this.observer = new IntersectionObserver(
        (entries, observer) => {
          if (!entries[0].isIntersecting) return;
          observer.unobserve(this);
          this.loadRecommendations(productId);
        },
        { rootMargin: "0px 0px 400px 0px" }
      );
      this.observer.observe(this);
    }

    refreshSwiperHeight() {
      var swiperComponents = this.querySelectorAll("swiper-component");
      swiperComponents.forEach(function (component) {
        var swiperEl = component.querySelector(".swiper");
        var swiperInstance =
          component.initSwiper || (swiperEl && swiperEl.swiper ? swiperEl.swiper : null);

        if (swiperInstance && typeof swiperInstance.updateAutoHeight === "function") {
          swiperInstance.updateAutoHeight(0);
        } else if (swiperInstance && typeof swiperInstance.update === "function") {
          swiperInstance.update();
        }
      });
    }

    scheduleSwiperHeightRefresh() {
      var self = this;
      var delays = [0, 120, 400, 900, 1800, 3200];

      delays.forEach(function (delay) {
        window.setTimeout(function () {
          self.refreshSwiperHeight();
        }, delay);
      });
    }

    markLoaded(html) {
      if (
        html.querySelector(".grid__item") ||
        html.querySelector(".swiper-slide") ||
        html.querySelector(".product-card-wrapper")
      ) {
        this.classList.add("product-recommendations--loaded");
      }
    }

    loadRecommendations(productId) {
      fetch(
        `${this.dataset.url}&product_id=${productId}&section_id=${this.dataset.sectionId}`
      )
        .then((response) => response.text())
        .then((text) => {
          const html = document.createElement("div");
          html.innerHTML = text;
          const recommendations = html.querySelector("product-recommendations");

          if (recommendations?.innerHTML.trim().length) {
            this.innerHTML = recommendations.innerHTML;
          }

          if (this.classList.contains("complementary-products")) {
            this.remove();
            return;
          }

          this.markLoaded(html);
          this.scheduleSwiperHeightRefresh();

          this.querySelectorAll(".product-card-wrapper img").forEach((img) => {
            if (img.complete) return;
            img.addEventListener(
              "load",
              () => {
                this.scheduleSwiperHeightRefresh();
              },
              { once: true }
            );
          });
        })
        .catch((e) => {
          console.error(e);
        });
    }
  }

  customElements.define("product-recommendations", ProductRecommendations);
}
