/** @odoo-module **/
import publicWidget from "@web/legacy/js/public/public_widget";
import { _t } from "@web/core/l10n/translation";
import { registry } from "@web/core/registry";
import { BulkDiscountDialog } from "./components/bulk_discount_dialog/bulk_discount_dialog";
import { discountUtils } from "./utils/discount_utils";

publicWidget.registry.BulkDiscountButton = publicWidget.Widget.extend({
    selector: ".js_sbodr_container",
    events: {
        "click .js_sbodr_request": "_onClickBulkDiscountRequest",
    },

    start() {
        return this._super.apply(this, arguments);
    },

    _onClickBulkDiscountRequest(ev) {
        ev.preventDefault();
        const productInfo = discountUtils.getProductInfo();
        console.log("Product Info:", productInfo);

        // Use the service to open the dialog
        const dialogService = this.bindService("dialog");
        dialogService.add(BulkDiscountDialog, {
            productId: productInfo.productId,
            productName: productInfo.productName,
            productImage: productInfo.productImage,
            quantity: productInfo.quantity,
        });
    },
});

publicWidget.registry.BulkDiscountVariantHandler = publicWidget.Widget.extend({
    selector: ".oe_website_sale",

    events: {
        "change form.js_attributes input, form.js_attributes select":
            "_onChangeVariantBulkDiscount",
    },

    start: function () {
        var def = this._super.apply(this, arguments);
        this._handleBulkDiscountVisibility();
        return def;
    },

    _onChangeVariantBulkDiscount: function () {
        this._handleBulkDiscountVisibility();
    },

    _handleBulkDiscountVisibility: function () {
        const $container = $(".js_sbodr_container");
        if (!$container.length) return;

        const productInfo = discountUtils.getProductInfo();

        if (productInfo.productId) {
            discountUtils
                .checkVariantEligibility(productInfo.productId, productInfo.productTemplateId)
                .then((response) => {
                    if (response && response.is_enabled) {
                        $container.removeClass("d-none");
                    } else {
                        // $container.addClass("d-none");
                    }
                })
                .catch(() => {});
        } else {
            // $container.addClass("d-none");
        }
    },
});
