/** @odoo-module **/

import { registry } from "@web/core/registry";
import { debounce } from "@web/core/utils/timing";
import publicWidget from "@web/website/js/public_widget";

publicWidget.registry.ProductCollectionSnippet = publicWidget.Widget.extend({
  selector: ".s_product_collection_snippet",
  disabledInEditableMode: false,

  /**
   * @override
   */
  start() {
    // Try to get collection ID from both dataset and attribute to ensure compatibility
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
   * Fetch products for the selected collection and render them
   *
   * @private
   */
  _renderProducts: debounce(async function () {
    if (!this.collectionId) return;

    try {
      const products = await this._rpc({
        route: "/product_collection/get_collection_products",
        params: { collection_id: this.collectionId },
      });

      // Clear existing content
      const container = this.el.querySelector(".container");
      container.innerHTML = "";

      // Create product grid
      if (products && products.length) {
        const row = document.createElement("div");
        row.className = "row g-3";

        // Check if list view is enabled
        const isListView = this.el.classList.contains("s_list_view");

        products.forEach((product) => {
          const col = document.createElement("div");
          col.className = "col-12 col-sm-6 col-md-4 col-lg-3 card-column";

          // Determine if there's a link to the product page
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

        // Add fade-in animation
        row.classList.add("o_animate", "o_animate_in", "o_animate_fade_in");

        // Remove placeholder if exists
        const placeholder = container.querySelector(".collection-placeholder");
        if (placeholder) {
          placeholder.remove();
        }
      } else {
        // No products message
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
