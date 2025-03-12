/** @odoo-module */
import publicWidget from "@web/legacy/js/public/public_widget";

console.log("Script 000.js loaded");

const AirproofSnippetWidget = publicWidget.Widget.extend({
  selector: ".s_airproof_snippet_another",
  events: {
    click: "_onClick",
    "click .main_1": "_main1",
    "click .as_test1": "_onTest1Click",
    "mouseover .as_test2": "_onTest2Hover",
  },

  /**
   * @override
   */
  start() {
    console.log("AirproofSnippetWidget started");
    return this._super(...arguments);
  },

  //--------------------------------------------------------------------------
  // Handlers
  //--------------------------------------------------------------------------

  /**
   * @private
   */
  _onClick(ev) {
    ev.preventDefault();
    ev.stopPropagation();
    console.log("Snippet clicked");
    alert("Snippet clicked");
  },

  /**
   * @private
   */
  _main1(ev) {
    ev.preventDefault();
    ev.stopPropagation();
    console.log("Main 1 button clicked");
    alert("Main 1 button clicked");
  },

  /**
   * @private
   * @param {Event} ev
   */
  _onTest1Click(ev) {
    ev.preventDefault();
    ev.stopPropagation();
    console.log("Test 1 button clicked");
    alert("Test 1 button clicked");
  },

  /**
   * @private
   * @param {Event} ev
   */
  _onTest2Hover(ev) {
    ev.preventDefault();
    ev.stopPropagation();
    console.log("Test 2 hovered");
    alert("Test 2 hovered");
  },
});

publicWidget.registry.AirproofSnippetWidget = AirproofSnippetWidget;

export default AirproofSnippetWidget;
