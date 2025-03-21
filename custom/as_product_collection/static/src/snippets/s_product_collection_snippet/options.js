/** @odoo-module **/

import options from "@web_editor/js/editor/snippets.options";
import CollectionDialog from "../../js/components/collection_dialog/collection_dialog";

options.registry.SelectCollection = options.Class.extend({
  init() {
    this._super(...arguments);
    this.editableMode = true;

    if (!options.registry.SelectCollection._instances) {
      options.registry.SelectCollection._instances = new Set();
    }

    this._instanceId = Date.now() + Math.random().toString(36).substring(2, 9);
    options.registry.SelectCollection._instances.add(this._instanceId);
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
    if (options.registry.SelectCollection._primaryInstance === undefined) {
      options.registry.SelectCollection._primaryInstance = this._instanceId;
    }

    if (
      options.registry.SelectCollection._primaryInstance === this._instanceId
    ) {
      this._openCollectionDialog();
    }
  },

  _openCollectionDialog() {
    if (options.registry.SelectCollection._activeDialog) {
      return;
    }

    const dialogService = this.bindService("dialog");

    const closeCallback = () => {
      options.registry.SelectCollection._activeDialog = null;
    };
    options.registry.SelectCollection._activeDialog = dialogService.add(
      CollectionDialog,
      {
        title: "Select Product Collection",
        snippetEl: this.$target[0],
        onCollectionSelected: (collectionId) => {
          this._setCollectionId(collectionId);
        },
      },
      {
        onClose: closeCallback,
      }
    );
  },

  _setCollectionId(collectionId) {
    if (!collectionId) return;

    this.$target[0].dataset.collectionId = collectionId;
    this.$target.attr("data-collection-id", collectionId);
    this._renderSnippetProducts(collectionId);
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

    const productLink = `/shop/product/${product.product_tmpl_id}`;

    col.innerHTML = `
    <div class="card border-1 rounded-2 h-100 w-100 oe_product_cart js_product" data-product-id="${product.id}" data-product-template-id="${product.product_tmpl_id}">
      <form class="js_add_cart_variants" action="/shop/cart/update" method="POST">
        <input type="hidden" name="csrf_token" value="${odoo.csrf_token}"/>
        <input type="hidden" name="product_id" value="${product.id}"/>
        <input type="hidden" name="product_template_id" value="${product.product_tmpl_id}"/>
        <a href="${productLink}" class="text-decoration-none">
          <img src="${product.image_url}" class="card-img-top object-fit-cover px-0 p-lg-0" alt="${product.name}"/>
        </a>
        <div class="card-body">
          <a href="${productLink}" class="text-decoration-none">
            <h5 class="card-title text-dark">${product.name}</h5>
          </a>
          <div class="row justify-content-between align-items-center px-3">
            <div class="col-auto p-0">
              <span class="card-text text-primary">${product.price_formatted}</span>
            </div>
            <div class="col-auto p-0">
              <div class="o_wsale_product_btn d-flex align-items-center gap-2">
                <button type="button" class="btn btn-light o_add_wishlist" 
                  data-product-template-id="${product.product_tmpl_id}" 
                  data-product-product-id="${product.id}" 
                  data-action="o_wishlist" 
                  title="Add to Wishlist">
                  <i class="fa fa-heart" aria-label="Add to wishlist"></i>
                </button>
                <button type="submit" class="btn btn-primary a-submit js_add_cart" title="Add to Cart">
                  <i class="fa fa-shopping-cart"></i>
                </button>
                <button type="button" class="btn btn-light o_add_compare d-none d-md-inline-block" 
                  data-product-product-id="${product.id}" 
                  data-action="o_comparelist" 
                  title="Compare">
                  <i class="fa fa-exchange" aria-label="Compare"></i>
                </button>
              </div>
            </div>
          </div>
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

  destroy() {
    if (options.registry.SelectCollection._instances) {
      options.registry.SelectCollection._instances.delete(this._instanceId);
    }

    if (
      options.registry.SelectCollection._primaryInstance === this._instanceId
    ) {
      options.registry.SelectCollection._primaryInstance = undefined;
    }

    this._super(...arguments);
  },
});
