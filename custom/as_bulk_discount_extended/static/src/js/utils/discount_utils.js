/** @odoo-module **/
import { rpc } from "@web/core/network/rpc";

export const discountUtils = {
  checkVariantEligibility: function (productId, templateId) {
    return rpc("/sbodr/check_variant", {
      product_id: productId,
      template_id: templateId,
    });
  },

  getProductInfo: function () {
    const $form = $(".js_product");

    let productId = null;
    const $productInput = $form.find(
      'input[name="product_id"], input.js_product_change:checked'
    );
    if ($productInput.length) {
      productId = parseInt($productInput.val(), 10);
    }

    const productTemplateId = parseInt(
      $form.find('input[name="product_template_id"]').val(),
      10
    );

    const productName = $(".product_detail h1").text().trim();
    const productImage = $(".product_detail_img").first().attr("src");
    const quantity = parseInt(
      $form.find('input[name="add_qty"]').val() || 1,
      10
    );

    return {
      productId,
      productTemplateId,
      productName,
      productImage,
      quantity,
    };
  },
};
