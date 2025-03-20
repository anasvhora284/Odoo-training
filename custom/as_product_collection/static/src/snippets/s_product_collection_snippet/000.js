/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";
import { rpc } from "@web/core/network/rpc";

publicWidget.registry.ProductCollectionSnippet = publicWidget.Widget.extend({
  selector: ".s_product_collection_snippet",
  disabledInEditableMode: false,

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

  async _renderProducts() {
    if (!this.collectionId) return;

    try {
      const data = await this._getCollectionData();
      this._renderCollectionUI(data);
    } catch (error) {
      this._showErrorMessage();
    }
  },

  async _getCollectionData() {
    try {
      const collectionId = parseInt(this.collectionId);
      const result = await rpc(
        "/web/dataset/call_kw/website.product.collection/get_collection_data",
        {
          model: "website.product.collection",
          method: "get_collection_data",
          args: [[collectionId]],
          kwargs: {},
        }
      );

      return {
        collectionInfo: { name: result.name || "Product Collection" },
        products: result.products || [],
      };
    } catch (error) {
      return {
        collectionInfo: { name: "Product Collection" },
        products: [],
      };
    }
  },

  _renderCollectionUI(data) {
    const container = this.el.querySelector(".container");
    container.innerHTML = "";

    // Add collection title
    const titleElement = document.createElement("h2");
    titleElement.className = "collection-title text-center mb-4";
    titleElement.textContent = data.collectionInfo
      ? data.collectionInfo.name
      : "Product Collection";
    container.appendChild(titleElement);

    if (data.products && data.products.length) {
      this._renderProductCards(container, data.products);
    } else {
      this._showNoProductsMessage(container);
    }
  },

  _renderProductCards(container, products) {
    const row = document.createElement("div");
    row.className = "row g-3";

    products.forEach((product) => {
      console.log(product, "products 000");
      const col = this._createProductCard(product);
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
  },

  _createProductCard(product) {
    const col = document.createElement("div");
    col.className = "col-12 col-sm-6 col-md-4 col-lg-3 card-column";

    const productLink = `/shop/product/${product.product_template_id}`;

    col.innerHTML = `
      <div class="card h-100 w-100 oe_product_cart">
        <form class="js_add_cart_variants" action="/shop/cart/update" method="POST">
          <input type="hidden" name="csrf_token" value="${odoo.csrf_token}"/>
          <input type="hidden" name="product_id" value="${product.id}"/>
          <input type="hidden" name="product_template_id" value="${product.product_template_id}"/>
          <a href="${productLink}" class="text-decoration-none">
            <img src="${product.image_url}" class="card-img-top" alt="${product.name}"/>
            <div class="card-body">
              <h5 class="card-title text-dark">${product.name}</h5>
              <p class="card-text text-primary">${product.price_formatted}</p>
            </div>
          </a>
          <div class="o_wsale_product_btn w-100 mb-2 d-flex justify-content-center align-items-center gap-1">
            <a role="button" class="btn btn-secondary o_add_wishlist" data-product-template-id="${product.product_template_id}" title="Add to Wishlist">
              <i class="fa fa-heart"></i>
            </a>
            <button type="submit" class="btn btn-primary a-submit js_add_cart" title="Add to Cart">
              <i class="fa fa-shopping-cart"></i>
            </button>
            <a role="button" class="btn btn-secondary o_add_compare" data-product-template-id="${product.product_template_id}" title="Compare">
              <i class="fa fa-exchange"></i>
            </a>
          </div>
        </form>
      </div>
    `;

    return col;
  },

  _showNoProductsMessage(container) {
    const alert = document.createElement("div");
    alert.className = "alert alert-info";
    alert.textContent = "No products found in this collection.";
    container.appendChild(alert);
  },

  _showErrorMessage() {
    const container = this.el.querySelector(".container");
    const errorAlert = document.createElement("div");
    errorAlert.className = "alert alert-danger";
    errorAlert.textContent = "Failed to load products. Please try again.";
    container.innerHTML = "";
    container.appendChild(errorAlert);
  },
});
