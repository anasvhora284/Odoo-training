/** @odoo-module **/

import { Dialog } from "@web/core/dialog/dialog";
import { Component, useState } from "@odoo/owl";

class DilogBoxBody extends Component {
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
      selectedCollection: "",
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

      // Check if already has collection ID from snippet
      if (this.props.snippetEl) {
        const collectionId = this.props.snippetEl.dataset.collectionId;
        if (collectionId) {
          this.state.selectedCollection = collectionId;
        }
      }

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

  onCollectionChange(ev) {
    const collectionId = ev.target.value;
    if (collectionId) {
      this.state.selectedCollection = collectionId;
    } else {
      this.state.selectedCollection = "";
    }
    this.state.error = null;
  }

  applyCollection() {
    if (this.state.selectedCollection && this.props.onCollectionSelected) {
      this.props.onCollectionSelected(this.state.selectedCollection);
    }
    this.props.close();
  }
}

export default DilogBoxBody;
