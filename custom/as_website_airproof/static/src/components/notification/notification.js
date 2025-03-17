/** @odoo-module **/

import { Component, useState, onWillDestroy } from "@odoo/owl";
import { registry } from "@web/core/registry";

export class NotificationComponent extends Component {
  static template = "as_website_airproof.notification_component";

  setup() {
    this.state = useState({
      message: "Click the button to show a notification",
      type: "info",
    });

    // Bind methods to preserve 'this' context
    this.showNotification = this.showNotification.bind(this);

    // Keep track of active notifications to clean them up
    this.activeNotifications = [];

    // Clean up any remaining notifications when component is destroyed
    onWillDestroy(() => {
      this.activeNotifications.forEach((el) => {
        if (el && document.body.contains(el)) {
          el.remove();
        }
      });
    });
  }

  showNotification(type) {
    // Update state
    this.state.type = type;
    this.state.message = `This is a ${type} notification!`;

    try {
      // Create notification element
      const notificationElement = document.createElement("div");
      notificationElement.className = `alert alert-${type} notification-popup`;
      notificationElement.textContent = this.state.message;
      notificationElement.style.position = "fixed";
      notificationElement.style.top = "20px";
      notificationElement.style.right = "20px";
      notificationElement.style.zIndex = "9999";
      notificationElement.style.minWidth = "250px";
      notificationElement.style.padding = "15px";
      notificationElement.style.boxShadow = "0 4px 8px rgba(0,0,0,0.1)";

      // Add to document and track it
      document.body.appendChild(notificationElement);
      this.activeNotifications.push(notificationElement);

      // Remove after 3 seconds
      setTimeout(() => {
        if (document.body.contains(notificationElement)) {
          notificationElement.remove();
          // Remove from tracking array
          const index = this.activeNotifications.indexOf(notificationElement);
          if (index > -1) {
            this.activeNotifications.splice(index, 1);
          }
        }
      }, 3000);
    } catch (error) {
      console.error("Error showing notification:", error);
    }
  }
}

registry
  .category("public_components")
  .add("as_website_airproof.NotificationComponent", NotificationComponent);

registry
  .category("actions")
  .add("as_website_airproof.notification_action", NotificationComponent);

export { NotificationComponent };
