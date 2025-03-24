/** @odoo-module **/

import options from "@web_editor/js/editor/snippets.options";
import DilogBoxBody from "../../js/components/collection_dialog/collection_dialog";

options.registry.SelectCollection = options.Class.extend({
    init() {
        this._super(...arguments);
        this.editableMode = true;
    },

    async willStart() {
        await this._super(...arguments);
    },

    onBuilt() {
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
        if (!collectionId) return;

        this.$target[0].dataset.collectionId = collectionId;
        this.$target.attr("data-collection-id", collectionId);
        this._renderSnippetProducts(collectionId);
    },

    async _renderSnippetProducts(collectionId) {
        if (!collectionId) return;

        try {
            const collectionInfo = await this.orm.call(
                "website.product.collection",
                "search_read",
                [[["id", "=", parseInt(collectionId)]]],
                { fields: ["name"] }
            );

            const collectionName =
                collectionInfo && collectionInfo.length > 0
                    ? collectionInfo[0].name
                    : "Product Collection";

            const products = await this.orm.call(
                "website.product.collection",
                "get_collection_products",
                [[parseInt(collectionId)]]
            );

            const container = this.$target[0].querySelector(".container");
            container.innerHTML = ``;

            const titleElement = document.createElement("h2");
            titleElement.className = "collection-title text-center mb-4";
            titleElement.textContent = collectionName;
            container.appendChild(titleElement);

            if (products && products.length) {
                const row = document.createElement("div");
                row.className = "row g-3";

                const isListView = this.$target[0].classList.contains("s_list_view");

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

                row.classList.add("o_animate", "o_animate_in", "o_animate_fade_in", "visible");

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
            const container = this.$target[0].querySelector(".container");
            const errorAlert = document.createElement("div");
            errorAlert.className = "alert alert-danger";
            errorAlert.textContent = "Failed to load products. Please try again.";
            container.innerHTML = "";
            container.appendChild(errorAlert);
        }
    },

    start() {
        const res = this._super(...arguments);
        this.orm = this.bindService("orm");
        return res;
    },

    cleanForSave() {
        const container = this.$target[0].querySelector(".container");
        if (container) {
            const alerts = container.querySelectorAll(".alert");
            alerts.forEach((alert) => alert.remove());

            const collectionId = this.$target[0].dataset.collectionId;
            if (collectionId) {
                this.$target.attr("data-collection-id", collectionId);
            }
        }
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
            const collectionId = this.$target[0].dataset.collectionId;
            if (collectionId) {
                this._renderSnippetProducts(collectionId);
            }
        } else {
            this._super(...arguments);
        }
    },
});
