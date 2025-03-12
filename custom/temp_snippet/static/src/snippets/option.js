/** @odoo-module **/

import options from "@web_editor/js/editor/snippets.options";

console.log("Snippet options loaded");
const AirproofSnippetOptions = options.Class.extend({
  /**
   * @override
   */
  start: function () {
    console.log("Snippet options started");
    alert("Snippet started");
    return this._super(...arguments);
  },

  /**
   * @override
   */
  onBuilt: function () {
    console.log("Snippet built - After drag-drop");
    alert("Snippet built - After drag-drop");
    return this._super(...arguments);
  },

  /**
   * @override
   */
  onFocus: function () {
    console.log("Snippet focused");
    alert("Snippet focused");
    return this._super(...arguments);
  },

  /**
   * @override
   */
  onBlur: function () {
    console.log("Snippet lost focus");
    alert("Snippet lost focus");
    return this._super(...arguments);
  },

  /**
   * @override
   */
  onClone: function () {
    console.log("Snippet cloned");
    alert("Snippet cloned");
    return this._super(...arguments);
  },

  /**
   * @override
   */
  onRemove: function () {
    console.log("Snippet removed");
    alert("Snippet removed");
    return this._super(...arguments);
  },

  /**
   * @override
   */
  cleanForSave: function () {
    console.log("Snippet being saved");
    alert("Snippet being saved");
    return this._super(...arguments);
  },
});

options.registry.s_airproof_snippet_options = AirproofSnippetOptions;

export default AirproofSnippetOptions;
