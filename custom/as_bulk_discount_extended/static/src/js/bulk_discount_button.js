/** @odoo-module **/
import publicWidget from "@web/legacy/js/public/public_widget";
import { rpc } from "@web/core/network/rpc";
import { _t } from "@web/core/l10n/translation";
import { browser } from "@web/core/browser/browser";
import { useService } from "@web/core/utils/hooks";
import { Component, xml } from "@odoo/owl";

class BulkDiscountDialog extends Component {
    setup() {
        this.dialog = useService("dialog");
    }

    static template = xml`
        <div class="bulk_discount_form p-3">
            <div class="row mb-4">
                <div class="col-md-4">
                    <img t-att-src="props.productImage || '/web/static/img/placeholder.png'" class="img-fluid" t-att-alt="props.productName"/>
                </div>
                <div class="col-md-8">
                    <h5 t-esc="props.productName"/>
                    <p><strong>Quantity:</strong> <t t-esc="props.quantity"/></p>
                </div>
            </div>
            <div class="form-group mb-3">
                <label for="bulk_discount_qty" class="form-label">Bulk Order Quantity</label>
                <input type="number" class="form-control" id="bulk_discount_qty" min="1" t-att-value="props.quantity"/>
            </div>
            <div class="form-group mb-3">
                <label for="bulk_discount_percent" class="form-label">Requested Discount (%)</label>
                <input type="number" class="form-control" id="bulk_discount_percent" min="1" max="90" value="10"/>
            </div>
            <div class="form-group mb-3">
                <label for="bulk_discount_notes" class="form-label">Additional Notes</label>
                <textarea class="form-control" id="bulk_discount_notes" rows="3" placeholder="Explain why you need this discount"></textarea>
            </div>
        </div>
    `;

    static props = {
        productId: Number,
        productName: String,
        productImage: { type: String, optional: true },
        quantity: Number,
        close: Function,
    };
}

publicWidget.registry.BulkDiscountButton = publicWidget.Widget.extend({
    selector: ".js_sbodr_container",
    events: {
        "click .js_sbodr_request": "_onClickBulkDiscountRequest",
    },

    /**
     * @override
     */
    start() {
        return this._super.apply(this, arguments);
    },

    /**
     * @private
     * @param {MouseEvent} ev
     */
    _onClickBulkDiscountRequest(ev) {
        console.log(".js_sbodr_container");
        ev.preventDefault();

        // Get product information
        const $form = $(".js_product");
        const productId = parseInt(
            $form.find('input[name="product_id"], input.js_product_change:checked').val() || 0,
            10
        );
        const productName = $(".product_detail h1").text().trim();
        const productImage = $(".product_detail img.product_detail_img").first().attr("src");
        const quantity = parseInt($form.find('input[name="add_qty"]').val() || 1, 10);

        // Create HTML content for the dialog
        const dialogContent = `
            <div class="bulk_discount_form p-3">
                <div class="row mb-4">
                    <div class="col-md-4">
                        <img src="${
                            productImage || "/web/static/img/placeholder.png"
                        }" class="img-fluid" alt="${productName}"/>
                    </div>
                    <div class="col-md-8">
                        <h5>${productName}</h5>
                        <p><strong>Quantity:</strong> ${quantity}</p>
                    </div>
                </div>
                <div class="form-group mb-3">
                    <label for="bulk_discount_qty" class="form-label">Bulk Order Quantity</label>
                    <input type="number" class="form-control" id="bulk_discount_qty" min="1" value="${quantity}">
                </div>
                <div class="form-group mb-3">
                    <label for="bulk_discount_percent" class="form-label">Requested Discount (%)</label>
                    <input type="number" class="form-control" id="bulk_discount_percent" min="1" max="90" value="10">
                </div>
                <div class="form-group mb-3">
                    <label for="bulk_discount_notes" class="form-label">Additional Notes</label>
                    <textarea class="form-control" id="bulk_discount_notes" rows="3" placeholder="Explain why you need this discount"></textarea>
                </div>
            </div>
        `;

        // Create simple jQuery modal
        const $modal = $(
            '<div class="modal" role="dialog"><div class="modal-dialog"><div class="modal-content">' +
                '<div class="modal-header"><h5 class="modal-title">' +
                _t("Request Bulk Discount") +
                "</h5>" +
                '<button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button></div>' +
                '<div class="modal-body">' +
                dialogContent +
                "</div>" +
                '<div class="modal-footer">' +
                '<button type="button" class="btn btn-secondary cancel-btn">' +
                _t("Cancel") +
                "</button>" +
                '<button type="button" class="btn btn-primary submit-btn">' +
                _t("Submit Request") +
                "</button>" +
                "</div></div></div></div>"
        );

        // Add to body
        $modal.appendTo("body");

        // Show using vanilla JS
        $modal[0].classList.add("show");
        $modal[0].style.display = "block";
        document.body.classList.add("modal-open");

        // Add backdrop
        const backdrop = document.createElement("div");
        backdrop.className = "modal-backdrop fade show";
        document.body.appendChild(backdrop);

        // Function to close the modal
        const closeModal = () => {
            $modal[0].classList.remove("show");
            $modal[0].style.display = "none";
            document.body.classList.remove("modal-open");
            backdrop.remove();
            setTimeout(() => {
                $modal.remove();
            }, 300);
        };

        // Handle close button clicks
        $modal.find(".btn-close, .cancel-btn").on("click", closeModal);

        // Handle submit button click
        $modal.find(".submit-btn").on("click", () => {
            const quantity = parseInt(document.getElementById("bulk_discount_qty").value, 10);
            const discount = parseFloat(document.getElementById("bulk_discount_percent").value);
            const notes = document.getElementById("bulk_discount_notes").value;

            this._submitBulkDiscountRequest(productId, quantity, discount, notes, closeModal);
        });
    },

    /**
     * Submit the bulk discount request
     *
     * @private
     * @param {Number} productId
     * @param {Number} quantity
     * @param {Number} discount
     * @param {String} notes
     * @param {Function} closeCallback
     */
    _submitBulkDiscountRequest(productId, quantity, discount, notes, closeCallback) {
        // Submit the request via RPC
        rpc("/sbodr/submit_request", {
            product_id: productId,
            quantity: quantity,
            discount: discount,
            notes: notes,
        })
            .then((result) => {
                if (result && result.success) {
                    // Show success message
                    this.displayNotification({
                        type: "success",
                        title: _t("Request Submitted"),
                        message: _t("Your bulk discount request has been submitted successfully."),
                        sticky: false,
                    });

                    // Close the modal
                    closeCallback();
                } else {
                    console.error("Failed to submit request:", result?.error || "Unknown error");
                }
            })
            .catch((error) => {
                console.error("Error submitting request:", error);
            });
    },
});

// Add a separate widget for handling variant changes
publicWidget.registry.BulkDiscountVariantHandler = publicWidget.Widget.extend({
    selector: ".oe_website_sale",

    /**
     * Events object to track variant changes
     */
    events: {
        "change form.js_attributes input, form.js_attributes select":
            "_onChangeVariantBulkDiscount",
    },

    /**
     * @override
     */
    start: function () {
        var def = this._super.apply(this, arguments);
        this._handleBulkDiscountVisibility();
        return def;
    },

    /**
     * Custom method to handle variant changes for bulk discount button
     *
     * @private
     */
    _onChangeVariantBulkDiscount: function () {
        this._handleBulkDiscountVisibility();
    },

    /**
     * Handles the visibility of the bulk discount button based on the selected variant
     *
     * @private
     */
    _handleBulkDiscountVisibility: function () {
        const $container = $(".js_sbodr_container");
        if ($container.length) {
            console.log(".js_sbodr_container - variant changed");

            // Get the current product ID from the form
            const $form = $(".js_product");

            let productId = null;
            // Try to get product ID from the form
            const $productInput = $form.find(
                'input[name="product_id"], input.js_product_change:checked'
            );
            if ($productInput.length) {
                productId = parseInt($productInput.val(), 10);
            }

            // Get the product template ID
            const productTemplateId = parseInt(
                $form.find('input[name="product_template_id"]').val(),
                10
            );

            if (productId) {
                console.log("Product ID:", productId, "Template ID:", productTemplateId);

                rpc("/sbodr/check_variant", {
                    product_id: productId,
                    template_id: productTemplateId,
                })
                    .then((response) => {
                        if (response && response.is_enabled) {
                            $container.removeClass("d-none");
                        } else {
                            // $container.addClass("d-none");
                        }
                    })
                    .catch((error) => {
                        console.error("Error checking variant status:", error);
                    });
            } else {
                // No product selected yet, hide the button
                // $container.addClass("d-none");
            }
        }
    },
});
