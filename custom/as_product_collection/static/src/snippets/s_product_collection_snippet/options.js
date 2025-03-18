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
}

options.registry.SelectCollection = options.Class.extend({
  init() {
    this._super(...arguments);
    console.log("=========Snippet init=============");
  },

  async willStart() {
    await this._super(...arguments);
    console.log("=========Snippet willStart=============");
  },

  onBuilt() {
    console.log("=========Snippet Built (Dropped on Page)==========");
    const dialogService = this.bindService("dialog");
    dialogService.add(DilogBoxBody, {
      title: "Select Product List",
    });
  },
});
