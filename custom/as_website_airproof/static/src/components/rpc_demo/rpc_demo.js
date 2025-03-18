/** @odoo-module **/

import { Component, useState, onWillStart } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

/**
 * Component demonstrating various ways to use RPC in Odoo 18.0 JavaScript
 */
export class RPCDemoComponent extends Component {
  static template = "as_website_airproof.rpc_demo_component";

  setup() {
    // Use the built-in RPC service
    this.rpc = useService("rpc");

    // Use the notification service for displaying results
    this.notification = useService("notification");

    // State for the component
    this.state = useState({
      menuItems: {
        backend: [],
        frontend: [],
      },
      products: [],
      isLoading: {
        menus: false,
        products: false,
      },
      selectedMenuType: "both",
    });

    // Load initial data on component start
    onWillStart(async () => {
      await this.fetchProducts();
    });
  }

  /**
   * Fetch products using direct RPC service call
   */
  async fetchProducts() {
    try {
      this.state.isLoading.products = true;

      // Direct RPC call to model method
      const result = await this.rpc("/simple_rpc/products", {});

      if (result && result.success) {
        this.state.products = result.products;
        this.notification.add("Products loaded successfully", {
          type: "success",
        });
      } else {
        this.notification.add("Failed to load products", { type: "danger" });
      }
    } catch (error) {
      this.notification.add(`Error: ${error.message || "Unknown error"}`, {
        type: "danger",
      });
      console.error("RPC Error:", error);
    } finally {
      this.state.isLoading.products = false;
    }
  }

  /**
   * Fetch menu items using the RPC service
   */
  async fetchMenuItems() {
    try {
      this.state.isLoading.menus = true;

      // Example of calling a controller endpoint with parameters
      const result = await this.rpc("/simple_rpc/menus", {
        menu_type: this.state.selectedMenuType,
      });

      if (result && result.success) {
        // Update state with received data
        if (result.menu_items.backend_menus) {
          this.state.menuItems.backend = [
            ...result.menu_items.backend_menus.airproof_menus,
            ...result.menu_items.backend_menus.main_menus.slice(0, 5),
          ];
        }

        if (result.menu_items.frontend_menus) {
          this.state.menuItems.frontend = [
            ...result.menu_items.frontend_menus.airproof_menus,
            ...result.menu_items.frontend_menus.all_menus.slice(0, 5),
          ];
        }

        this.notification.add("Menu items loaded successfully", {
          type: "success",
        });
      } else {
        this.notification.add(
          `Failed to load menu items: ${result.error || "Unknown error"}`,
          { type: "danger" }
        );
      }
    } catch (error) {
      this.notification.add(`Error: ${error.message || "Unknown error"}`, {
        type: "danger",
      });
      console.error("RPC Error:", error);
    } finally {
      this.state.isLoading.menus = false;
    }
  }

  /**
   * Alternative method using a different RPC call pattern
   * This demonstrates calling a model method directly
   */
  async fetchMenuItemsAlternative() {
    try {
      this.state.isLoading.menus = true;

      // Example of calling a model method directly with the service
      // This approach requires proper permissions and is common in backend components
      const result = await this.rpc(
        "/web/dataset/call_kw/as_website_airproof.rpc_demo/get_menu_items",
        {
          model: "as_website_airproof.rpc_demo",
          method: "get_menu_items",
          args: [],
          kwargs: {
            menu_type: this.state.selectedMenuType,
          },
        }
      );

      if (result && result.success) {
        // Process result similar to the other method
        // ... (implementation similar to above)
        this.notification.add("Menu items loaded using alternative method", {
          type: "success",
        });
      } else {
        this.notification.add(
          "Failed to load menu items with alternative method",
          { type: "danger" }
        );
      }
    } catch (error) {
      this.notification.add(
        `Error in alternative method: ${error.message || "Unknown error"}`,
        { type: "danger" }
      );
      console.error("RPC Error (alternative):", error);
    } finally {
      this.state.isLoading.menus = false;
    }
  }

  /**
   * Handle menu type selection change
   */
  onMenuTypeChange(ev) {
    this.state.selectedMenuType = ev.target.value;
  }
}

// Register the component in the registry for use in the frontend
registry
  .category("public_components")
  .add("as_website_airproof.RPCDemoComponent", RPCDemoComponent);

// Register for backend use as well
registry
  .category("actions")
  .add("as_website_airproof.rpc_demo_action", RPCDemoComponent);

export default RPCDemoComponent;
