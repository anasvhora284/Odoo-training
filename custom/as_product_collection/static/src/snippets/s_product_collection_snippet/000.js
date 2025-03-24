/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";
import { rpc } from "@web/core/network/rpc";
import { ProductConfiguratorDialog } from "@sale/js/product_configurator_dialog/product_configurator_dialog";
import wSaleUtils from "@website_sale/js/website_sale_utils";

publicWidget.registry.ProductCollectionSnippet = publicWidget.Widget.extend({
    selector: ".s_product_collection_snippet",
    events: {
        "click .js_add_cart_custom": "openConfigDialog",
    },
    disabledInEditableMode: false,

    start() {
        this.collectionId =
            this.el.dataset.collectionId || this.el.getAttribute("data-collection-id") || false;
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
            const col = this._createProductCard(product);
            row.appendChild(col);
        });

        container.appendChild(row);
        row.classList.add("o_animate", "o_animate_in", "o_animate_fade_in", "visible");

        const placeholder = container.querySelector(".collection-placeholder");
        if (placeholder) {
            placeholder.remove();
        }
    },

    _createProductCard(product) {
        const col = document.createElement("div");
        col.className = "col-12 col-sm-6 col-md-4 col-lg-3 card-column";

        const productLink = `/shop/product/${product.product_tmpl_id}`;

        col.innerHTML = `
      <div class="card border-1 rounded-2 h-100 w-100 oe_product_cart js_product o_carousel_product_card" data-product-id="${product.id}" data-product-template-id="${product.product_tmpl_id}">
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
                  <button type="button" class="btn btn-light o_add_wishlist o_add_wishlist_dyn" 
                    data-product-template-id="${product.product_tmpl_id}" 
                    data-product-product-id="${product.id}" 
                    data-action="o_wishlist" 
                    aria-label="Add to wishlist"
                    title="Add to Wishlist">
                    <i class="fa fa-heart"></i>
                  </button>
                  <button type="submit" class="btn btn-primary a-submit js_add_cart_custom" 
                    data-product-id="${product.id}"
                    data-product-template-id="${product.product_tmpl_id}"
                    data-action="o_add_cart" 
                    title="Add to Cart" 
                    aria-label="Add to Cart">
                    <i class="fa fa-shopping-cart"></i>
                  </button>
                  <button type="button" class="btn btn-light o_add_compare d-none d-md-inline-block" 
                    data-product-product-id="${product.id}" 
                    data-action="o_comparelist" 
                    aria-label="Compare"
                    title="Compare">
                    <i class="fa fa-exchange"></i>
                  </button>
                </div>
              </div>
            </div>
          </div>
      </div>
    `;

        return col;
    },

    openConfigDialog(event) {
        event.preventDefault();
        event.stopPropagation();

        const productId = parseInt(event.currentTarget.dataset.productId);
        const productTemplateId = parseInt(event.currentTarget.dataset.productTemplateId);
        this.notification = this.bindService("notification");

        const getCurrencyId = () => {
            if (
                document.body.dataset.mainObject === "website" &&
                document.body.dataset.websiteCurrencyId
            ) {
                return parseInt(document.body.dataset.websiteCurrencyId);
            }
            if (odoo?.session_info?.user_context?.currency_id) {
                return odoo.session_info.user_context.currency_id;
            }
            return null;
        };

        this.call("dialog", "add", ProductConfiguratorDialog, {
            productTemplateId: productTemplateId,
            ptavIds: [],
            customPtavs: [],
            quantity: 1,
            soDate: luxon.DateTime.now().toISO(),
            currencyId: getCurrencyId(),
            edit: false,
            isFrontend: true,
            options: {
                isMainProductConfigurable: true,
                showQuantity: true,
                showPrice: true,
            },
            save: async (mainProduct, optionalProducts, options) => {
                try {
                    const mainProductData = {
                        product_id: productId,
                        product_template_id: productTemplateId,
                        quantity: mainProduct.quantity || 1,
                        product_custom_attribute_values:
                            mainProduct.customPtavs?.map((ptav) => ({
                                custom_product_template_attribute_value_id: ptav.id,
                                custom_value: ptav.value,
                            })) || [],
                        no_variant_attribute_value_ids: mainProduct.ptavIds || [],
                    };

                    const optionalProductsData = optionalProducts
                        .map((product) => {
                            const variantId = product.id || product.productId || product.product_id;
                            const templateId =
                                product.product_tmpl_id ||
                                product.productTemplateId ||
                                product.product_template_id;

                            if (!variantId || !templateId) {
                                console.warn("Missing required IDs for optional product:", product);
                                return null;
                            }

                            return {
                                product_id: variantId,
                                product_template_id: templateId,
                                parent_product_template_id: productTemplateId,
                                quantity: product.quantity || 1,
                                product_custom_attribute_values:
                                    product.customPtavs?.map((ptav) => ({
                                        custom_product_template_attribute_value_id: ptav.id,
                                        custom_value: ptav.value,
                                    })) || [],
                                no_variant_attribute_value_ids: product.ptavIds || [],
                            };
                        })
                        .filter(Boolean);

                    const values = await rpc("website_sale/product_configurator/update_cart", {
                        main_product: mainProductData,
                        optional_products: optionalProductsData,
                    });

                    this._onConfigured(options, values);
                } catch (error) {
                    console.error("Error adding product to cart:", error);
                    this.notification?.add("Failed to add product to cart. Please try again.", {
                        type: "danger",
                    });
                }
            },
            discard: () => {},
            close: () => {},
        });
    },

    _onConfigured(options, values) {
        if (options && options.goToCart) {
            window.location.pathname = "/shop/cart";
        } else {
            wSaleUtils.updateCartNavBar(values);
            wSaleUtils.showCartNotification(this.call.bind(this), values.notification_info);
        }
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
