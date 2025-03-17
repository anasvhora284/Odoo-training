/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

export class RainbowComponent extends Component {
  static template = "as_website_airproof.rainbow_component";

  setup() {
    this.state = useState({
      activeMessage: "",
      messages: [
        "Rainbow Power!",
        "Colors of Joy!",
        "Vibrant Energy!",
        "Colorful Magic!",
        "Rainbow Vibes!",
      ],
      fadeoutOptions: ["slow", "medium", "fast", "no"],
      selectedFadeout: "medium",
      messageIsHtml: false,
    });

    // Use the effect service
    this.effectService = useService("effect");

    // Bind methods to preserve 'this' context
    this.setFadeout = this.setFadeout.bind(this);
    this.toggleHtml = this.toggleHtml.bind(this);
    this.showRainbowMan = this.showRainbowMan.bind(this);
    this.showCustomMessage = this.showCustomMessage.bind(this);
  }

  showRainbowMan() {
    // Get a random message from the list
    const randomIndex = Math.floor(Math.random() * this.state.messages.length);
    const message = this.state.messages[randomIndex];
    this.state.activeMessage = message;

    // Show the rainbow man effect
    this.effectService.add({
      type: "rainbow_man",
      message: message,
      fadeout: this.state.selectedFadeout,
      messageIsHtml: this.state.messageIsHtml,
    });
  }

  setFadeout(fadeout) {
    return function () {
      this.state.selectedFadeout = fadeout;
    };
  }

  toggleHtml() {
    this.state.messageIsHtml = !this.state.messageIsHtml;
  }

  showCustomMessage() {
    const customMessage = this.state.activeMessage || "Custom Rainbow Message!";

    this.effectService.add({
      type: "rainbow_man",
      message: customMessage,
      fadeout: this.state.selectedFadeout,
      messageIsHtml: this.state.messageIsHtml,
    });
  }
}

registry
  .category("public_components")
  .add("as_website_airproof.RainbowComponent", RainbowComponent);

registry
  .category("actions")
  .add("as_website_airproof.rainbow_action", RainbowComponent);

export { RainbowComponent };
