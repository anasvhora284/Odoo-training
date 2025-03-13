/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";

import { useService } from "@web/core/utils/hooks";

export class CounterComponent extends Component {
  static template = "as_website_airproof.counter_action";

  setup() {
    this.state = useState({ count: 0 });
    this.notification = useService("notification"); // Inject the notification service
  }

  increment() {
    this.state.count++;
    this.notification.add(`Count increased to ${this.state.count}`, {
      type: "info",
    });
  }

  decrement() {
    if (this.state.count > 0) {
      this.state.count--;
      this.notification.add(`Count decreased to ${this.state.count}`, {
        type: "info",
      });
    }
  }
}

// Register the component in the registry for use in the website & in actions for the use in backend(admin_side)!

registry
  .category("public_components")
  .add("as_website_airproof.CounterComponentCustom", CounterComponent);

registry
  .category("actions")
  .add("as_website_airproof.CounterComponentCustom", CounterComponent);
