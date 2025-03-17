/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

export class RainbowMenuButton extends Component {
  static template = "as_website_airproof.rainbow_menu_button";
  static props = {};

  setup() {
    this.state = useState({
      messages: [
        "Rainbow Power!",
        "Colors of Joy!",
        "Vibrant Energy!",
        "Colorful Magic!",
        "Rainbow Vibes!",
      ],
    });

    // Use the effect service
    this.effectService = useService("effect");

    // Bind methods to preserve 'this' context
    this.showRainbowMan = this.showRainbowMan.bind(this);
  }

  showRainbowMan() {
    // Get a random message from the list
    const randomIndex = Math.floor(Math.random() * this.state.messages.length);
    const message = this.state.messages[randomIndex];

    // Show the rainbow man effect
    this.effectService.add({
      type: "rainbow_man",
      message: message,
      fadeout: "medium",
    });
  }
}

// Register the component for use in the user menu
registry.category("systray").add("rainbow_button", {
  Component: RainbowMenuButton,
  sequence: 100,
});

export { RainbowMenuButton };
