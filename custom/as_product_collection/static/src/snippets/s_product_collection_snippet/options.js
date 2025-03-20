/** @odoo-module **/

import options from "@web_editor/js/editor/snippets.options";
import CollectionDialog from "../../js/components/collection_dialog/collection_dialog";

options.registry.SelectCollection = options.Class.extend({
  init() {
    this._super(...arguments);
    this.editableMode = true;
  },

  async willStart() {
    await this._super(...arguments);
  },

  start() {
    const res = this._super(...arguments);
    this.orm = this.bindService("orm");
    return res;
  },

  onBuilt() {
    this._openCollectionDialog();
  },

  buildSnippetMenuOptions() {
    this._super(...arguments);
    this.$el.find(".dropdown-menu").append(
      $(`
      <a href="#" class="dropdown-item" data-name="select_collection">
        <i class="fa fa-list me-2"></i>Select Collection
      </a>
    `)
    );
  },

  onOptionClick(ev) {
    const optionName = ev.target.dataset.name;
    if (optionName === "select_collection") {
      this._openCollectionDialog();
    } else if (
      optionName === "grid_view_opt" ||
      optionName === "list_view_opt" ||
      optionName.startsWith("cards_per_row_")
    ) {
      this._refreshProductDisplay();
    } else {
      this._super(...arguments);
    }
  },

  cleanForSave() {
    const container = this.$target[0].querySelector(".container");
    if (container) {
      this._removeAlerts(container);
      this._ensureDataAttributeIsSet();
    }
  },

  _openCollectionDialog() {
    const dialogService = this.bindService("dialog");
    dialogService.add(CollectionDialog, {
      title: "Select Product Collection",
      snippetEl: this.$target[0],
      onCollectionSelected: (collectionId) => {
        this._setCollectionId(collectionId);
      },
    });
  },

  _setCollectionId(collectionId) {
    if (!collectionId) return;

    this.$target[0].dataset.collectionId = collectionId;
    this.$target.attr("data-collection-id", collectionId);
    this._renderSnippetProducts(collectionId);
  },

  _refreshProductDisplay() {
    const collectionId = this.$target[0].dataset.collectionId;
    if (collectionId) {
      this._renderSnippetProducts(collectionId);
    }
  },

  async _renderSnippetProducts(collectionId) {
    if (!collectionId) return;

    try {
      const collectionData = await this._getCollectionData(collectionId);
      this._updateSnippetUI(collectionData);
    } catch (error) {
      this._showErrorMessage();
    }
  },

  async _getCollectionData(collectionId) {
    collectionId = parseInt(collectionId);

    try {
      const data = await this.orm.call(
        "website.product.collection",
        "get_collection_data",
        [[collectionId]]
      );

      return {
        name: data.name || "Product Collection",
        products: data.products || [],
      };
    } catch (error) {
      return {
        name: "Product Collection",
        products: [],
      };
    }
  },

  _updateSnippetUI(collectionData) {
    const container = this.$target[0].querySelector(".container");
    container.innerHTML = "";

    this._addCollectionTitle(container, collectionData.name);

    if (collectionData.products && collectionData.products.length) {
      this._renderProductsGrid(container, collectionData.products);
    } else {
      this._showNoProductsMessage(container);
    }
  },

  _addCollectionTitle(container, title) {
    const titleElement = document.createElement("h2");
    titleElement.className = "collection-title text-center mb-4";
    titleElement.textContent = title;
    container.appendChild(titleElement);
  },

  _renderProductsGrid(container, products) {
    const row = document.createElement("div");
    row.className = "row g-3";

    products.forEach((product) => {
      console.log(product, "product options.js");
      const col = this._createProductCard(product);
      row.appendChild(col);
    });

    container.appendChild(row);
    this._applyAnimationClasses(row);
    this._removePlaceholder(container);
  },

  _createProductCard(product) {
    const col = document.createElement("div");
    col.className = "col-12 col-sm-6 col-md-4 col-lg-3 card-column";

    const productLink = `/shop/product/${product.product_template_id}`;

    col.innerHTML = `
      <div class="card h-100 w-100 oe_product_cart">
        <form class="js_add_cart_variants" action="/shop/cart/update" method="POST">
          <input type="hidden" name="csrf_token" value="${odoo.csrf_token}"/>
          <a href="${productLink}" class="text-decoration-none">
            <img src="${product.image_url}" class="card-img-top" alt="${product.name}"/>
            <div class="card-body">
              <h5 class="card-title text-dark">${product.name}</h5>
              <p class="card-text text-primary">${product.price_formatted}</p>
            </div>
          </a>
          <div class="o_wsale_product_btn w-100 mb-2 d-flex justify-content-center align-items-center gap-1">
            <input type="hidden" name="product_id" value="${product.id}"/>
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

  _applyAnimationClasses(element) {
    element.classList.add(
      "o_animate",
      "o_animate_in",
      "o_animate_fade_in",
      "visible"
    );
  },

  _removePlaceholder(container) {
    const placeholder = container.querySelector(".collection-placeholder");
    if (placeholder) {
      placeholder.remove();
    }
  },

  _showNoProductsMessage(container) {
    const alert = document.createElement("div");
    alert.className = "alert alert-info";
    alert.textContent = "No products found in this collection.";
    container.appendChild(alert);
  },

  _showErrorMessage() {
    const container = this.$target[0].querySelector(".container");
    const errorAlert = document.createElement("div");
    errorAlert.className = "alert alert-danger";
    errorAlert.textContent = "Failed to load products. Please try again.";
    container.innerHTML = "";
    container.appendChild(errorAlert);
  },

  _removeAlerts(container) {
    const alerts = container.querySelectorAll(".alert");
    alerts.forEach((alert) => alert.remove());
  },

  _ensureDataAttributeIsSet() {
    const collectionId = this.$target[0].dataset.collectionId;
    if (collectionId) {
      this.$target.attr("data-collection-id", collectionId);
    }
  },
});
