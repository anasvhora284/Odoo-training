/** @odoo-module **/

import options from "@web_editor/js/editor/snippets.options";
import { Dialog } from "@web/core/dialog/dialog";
import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";

console.log("=========Snippet options loading=============");

export class DilogBoxBody extends Component {
  static components = { Dialog };
  static template = "as_product_collection.DilogBoxBody";
  static props = {
    title: { type: String, optional: true },
    close: { type: Function },
    snippetEl: { optional: true },
    onCollectionSelected: { type: Function, optional: true },
  };

  setup() {
    this.state = useState({
      collections: [],
      products: [],
      selectedCollection: null,
      loading: false,
      error: null,
    });

    this._loadCollections();
  }

  async _loadCollections() {
    try {
      this.state.loading = true;
      this.state.error = null;
      const result = await this.env.services.orm.call(
        "website.product.collection",
        "search_read",
        [[]],
        { fields: ["id", "name"] }
      );
      this.state.collections = result || [];
      if (this.state.collections.length === 0) {
        this.state.error =
          "No collections found. Please create a collection first.";
      }
    } catch (error) {
      console.error("Failed to load collections:", error);
      this.state.error = "Failed to load collections. Please try again.";
    } finally {
      this.state.loading = false;
    }
  }

  async onCollectionChange(ev) {
    const collectionId = ev.target.value;
    this.state.selectedCollection = collectionId;
    this.state.products = [];
    this.state.error = null;

    if (collectionId) {
      try {
        this.state.loading = true;

        const products = await this.env.services.orm.call(
          "website.product.collection",
          "get_collection_products",
          [[parseInt(collectionId)]]
        );

        this.state.products = products || [];
        if (this.state.products.length === 0) {
          this.state.error = "No products found in this collection.";
        }
      } catch (error) {
        console.error("Failed to load products:", error);
        this.state.error = "Failed to load products. Please try again.";
      } finally {
        this.state.loading = false;
      }
    }
  }

  applyCollection() {
    if (this.state.selectedCollection && this.props.onCollectionSelected) {
      this.props.onCollectionSelected(this.state.selectedCollection);
    }
    this.props.close();
  }
}

options.registry.SelectCollection = options.Class.extend({
  init() {
    this._super(...arguments);
    console.log("=========Snippet init=============");
    this.editableMode = true; // Always true in options context
  },

  async willStart() {
    await this._super(...arguments);
    console.log("=========Snippet willStart=============");
  },

  onBuilt() {
    console.log("=========Snippet Built (Dropped on Page)==========");
    this._openCollectionDialog();
  },

  _openCollectionDialog() {
    const dialogService = this.bindService("dialog");
    dialogService.add(DilogBoxBody, {
      title: "Select Product Collection",
      snippetEl: this.$target[0],
      onCollectionSelected: (collectionId) => {
        this._setCollectionId(collectionId);
      },
    });
  },

  _setCollectionId(collectionId) {
    this.$target[0].dataset.collectionId = collectionId;
    this.$target.attr("data-collection-id", collectionId);
    this._renderSnippetProducts(collectionId);
  },

  async _renderSnippetProducts(collectionId) {
    if (!collectionId) return;

    try {
      const products = await this.orm.call(
        "website.product.collection",
        "get_collection_products",
        [[parseInt(collectionId)]]
      );

      // Clear existing content
      const container = this.$target[0].querySelector(".container");
      container.innerHTML = "";

      // Create product grid
      if (products && products.length) {
        const row = document.createElement("div");
        row.className = "row g-3";

        // Check if list view is enabled
        const isListView = this.$target[0].classList.contains("s_list_view");

        products.forEach((product) => {
          const col = document.createElement("div");
          col.className = "col-12 col-sm-6 col-md-4 col-lg-3 card-column";

          // Determine product link
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

        // Add fade-in animation in non-edit mode
        if (!this.editableMode) {
          row.classList.add("o_animate", "o_animate_in", "o_animate_fade_in");
        }

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
      const container = this.$target[0].querySelector(".container");
      const errorAlert = document.createElement("div");
      errorAlert.className = "alert alert-danger";
      errorAlert.textContent = "Failed to load products. Please try again.";
      container.innerHTML = "";
      container.appendChild(errorAlert);
    }
  },

  /**
   * @override
   */
  start() {
    const res = this._super(...arguments);
    this.orm = this.bindService("orm");
    return res;
  },

  /**
   * @override
   */
  cleanForSave() {
    // Remove any UI elements that shouldn't be saved
    const container = this.$target[0].querySelector(".container");
    if (container) {
      // Only keep important attributes and remove unnecessary UI elements
      const alerts = container.querySelectorAll(".alert");
      alerts.forEach((alert) => alert.remove());

      // Make sure collection ID is properly saved
      const collectionId = this.$target[0].dataset.collectionId;
      if (collectionId) {
        this.$target.attr("data-collection-id", collectionId);
      }
    }
  },

  /**
   * Add buttons to the options
   *
   * @override
   */
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

  /**
   * Handles option button clicks
   *
   * @override
   */
  onOptionClick(ev) {
    const optionName = ev.target.dataset.name;
    if (optionName === "select_collection") {
      this._openCollectionDialog();
    } else if (
      optionName === "grid_view_opt" ||
      optionName === "list_view_opt" ||
      optionName.startsWith("cards_per_row_")
    ) {
      // When view options change, refresh the products display
      const collectionId = this.$target[0].dataset.collectionId;
      if (collectionId) {
        this._renderSnippetProducts(collectionId);
      }
    } else {
      this._super(...arguments);
    }
  },
});
