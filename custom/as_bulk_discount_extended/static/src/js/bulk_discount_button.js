/** @odoo-module **/
import publicWidget from "@web/legacy/js/public/public_widget";
import { _t } from "@web/core/l10n/translation";
import { BulkDiscountDialog } from "./components/bulk_discount_dialog/bulk_discount_dialog";
import { discountUtils } from "./utils/discount_utils";
import { rpc } from "@web/core/network/rpc";

console.log("Bulk Discount Button Loaded");

publicWidget.registry.BulkDiscountButton = publicWidget.Widget.extend({
    selector: ".js_sbodr_container",
    events: {
        "click .js_sbodr_request": "_onClickBulkDiscountRequest",
    },

    start() {
        console.log("Bulk Discount Button Widget Loaded Inside");
        const bulkOrderButton = $(".js_sbodr_container");
        bulkOrderButton.addClass("d-none");
        return this._super.apply(this, arguments);
    },

    _onClickBulkDiscountRequest(ev) {
        ev.preventDefault();
        const productInfo = discountUtils.getProductInfo();
        console.log("Product Info:", productInfo);

        const dialogService = this.bindService("dialog");
        dialogService.add(BulkDiscountDialog, {
            productId: productInfo.productId,
            productName: productInfo.productName,
            productImage: productInfo.productImage,
            quantity: productInfo.quantity,
        });
    },
});

publicWidget.registry.WebsiteSale.include({
    async _getCombinationInfo() {
        const result = await this._super.apply(this, arguments);
        const productInfo = discountUtils.getProductInfo();
        this.checkBulkOrderButtonVisible(productInfo.productId);
        return result;
    },

    async checkBulkOrderButtonVisible(productId) {
        const isBulkOrderButtonVisible = await rpc("/sbodr/check_variant", {
            product_id: productId,
        });

        if (isBulkOrderButtonVisible.is_enabled) {
            const bulkOrderButton = $(".js_sbodr_container");
            bulkOrderButton.removeClass("d-none");
        } else {
            const bulkOrderButton = $(".js_sbodr_container");
            bulkOrderButton.addClass("d-none");
        }
    },
});
