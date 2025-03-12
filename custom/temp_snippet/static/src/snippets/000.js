/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";

console.log("===============================11");
console.log("loading 000.js");
console.log("===============================11");

publicWidget.registry.s_airproof_snippet = publicWidget.Widget.extend({
  selector: ".s_airproof_snippet",
  events: {
    click: "_onClick",
  },
  start() {
    console.log("Widget started");
    return this._super(...arguments);
  },
  _onClick: function (ev) {
    console.log("Clicked!");
    alert("working snippet");
  },
});

export default publicWidget.registry.s_airproof_snippet;
