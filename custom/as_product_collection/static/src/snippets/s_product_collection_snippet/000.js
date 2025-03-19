/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";
import { debounce } from "@web/core/utils/timing";
import { rpc } from "@web/core/network/rpc";

publicWidget.registry.ProductCollectionSnippet = publicWidget.Widget.extend({
  selector: ".s_product_collection_snippet",
  disabledInEditableMode: false,

  /**
   * @override
   */
  start() {
    this.collectionId =
      this.el.dataset.collectionId ||
      this.el.getAttribute("data-collection-id") ||
      false;
    if (this.collectionId && !this.editableMode) {
      return this._renderProducts();
    }
    return this._super(...arguments);
  },

  /**
   *
   * @private
   */
  _renderProducts: debounce(async function () {
    if (!this.collectionId) return;

    try {
      const collectionInfo = await rpc(
        "/product_collection/get_collection_info",
        { collection_id: this.collectionId }
      );

      const collectionName =
        collectionInfo && collectionInfo.name
          ? collectionInfo.name
          : "Product Collection";

      const products = await rpc(
        "/product_collection/get_collection_products",
        { collection_id: this.collectionId }
      );

      const container = this.el.querySelector(".container");
      container.innerHTML = "";

      const titleElement = document.createElement("h2");
      titleElement.className = "collection-title text-center mb-4";
      titleElement.textContent = collectionName;
      container.appendChild(titleElement);

      if (products && products.length) {
        const row = document.createElement("div");
        row.className = "row g-3";

        const isListView = this.el.classList.contains("s_list_view");

        products.forEach((product) => {
          const col = document.createElement("div");
          col.className = "col-12 col-sm-6 col-md-4 col-lg-3 card-column";

          const productLink = `/shop/product/${product.id}`;

          col.innerHTML = `
            <div class="card h-100">
              <a href="${productLink}" class="text-decoration-none">
                <img src="${product.image_url}" class="card-img-top" alt="${product.name}"/>
                <div class="card-body">
                  <h5 class="card-title text-dark">${product.name}</h5>
                  <p class="card-text text-primary">${product.price_formatted}</p>
                </div>
              </a>
            </div>
          `;

          row.appendChild(col);
        });

        container.appendChild(row);

        row.classList.add(
          "o_animate",
          "o_animate_in",
          "o_animate_fade_in",
          "visible"
        );

        const placeholder = container.querySelector(".collection-placeholder");
        if (placeholder) {
          placeholder.remove();
        }
      } else {
        const alert = document.createElement("div");
        alert.className = "alert alert-info";
        alert.textContent = "No products found in this collection.";
        container.appendChild(alert);
      }
    } catch (error) {
      console.error("Failed to load products:", error);
      const container = this.el.querySelector(".container");
      const errorAlert = document.createElement("div");
      errorAlert.className = "alert alert-danger";
      errorAlert.textContent = "Failed to load products. Please try again.";
      container.innerHTML = "";
      container.appendChild(errorAlert);
    }
  }, 300),
});
