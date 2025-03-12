/** @odoo-module **/
import { Component, useState } from "@odoo/owl";

export class CounterComponent extends Component {
  static template = "as_website_airproof.CounterComponent";

  setup() {
    this.state = useState({ count: 0 });
  }

  increment() {
    this.state.count++;
  }

  decrement() {
    if (this.state.count > 0) {
      this.state.count--;
    }
  }
}

// Register the component
import { registry } from "@web/core/registry";
registry
  .category("website_components")
  .add("CounterComponent", CounterComponent);
