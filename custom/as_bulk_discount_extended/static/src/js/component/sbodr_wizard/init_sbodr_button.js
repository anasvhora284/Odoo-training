/** @odoo-module **/

import { registry } from "@web/core/registry";
import { SBODRWizard } from "./sbodr_wizard";
import { dialogService } from "@web/core/dialog/dialog_service";

/**
 * Initializes the SBODR feature on website pages
 */
function setupSBODRButton() {
    // Wait for DOM to be ready
    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", initSBODR);
    } else {
        // DOM already loaded, initialize immediately
        initSBODR();
    }
}

/**
 * Initialize SBODR button handlers once DOM is ready
 */
function initSBODR() {
    // Find all SBODR buttons
    const sbodrButtons = document.querySelectorAll(".sbodr-request");

    // Check if we're on a product page
    const isProductPage = window.location.pathname.includes("/shop/product/");
    if (isProductPage) {
        verifySBODRVisibility();
    }

    if (sbodrButtons.length) {
        // Setup click handlers
        sbodrButtons.forEach((button) => {
            button.addEventListener("click", (event) => {
                event.preventDefault();
                try {
                    // Show the SBODR dialog using the imported service
                    const env = owl.Component.env;
                    if (env && env.services && env.services.dialog) {
                        env.services.dialog.add(SBODRWizard, {});
                    }
                } catch (error) {
                    // Fail silently
                }
            });
        });
    }
}

/**
 * Verify if SBODR should be visible for the current product
 */
function verifySBODRVisibility() {
    // Get the product ID from the page
    const productId = getProductIdFromPage();

    if (!productId) {
        return;
    }

    // Call the controller to check if SBODR is enabled
    fetch("/sbodr/check_enabled", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            jsonrpc: "2.0",
            id: Math.random().toString(),
            method: "call",
            params: {
                product_id: productId,
            },
        }),
    })
        .then((response) => response.json())
        .then((data) => {
            if (data.result && !data.result.enabled) {
                hideButtons();
            }
        })
        .catch(() => {
            // Fail silently
        });
}

/**
 * Helper function to get product ID from the page
 */
function getProductIdFromPage() {
    // Try multiple methods to find the product ID

    // Method 1: Try getting from URL parameters
    const urlParams = new URLSearchParams(window.location.search);
    let productId = urlParams.get("product_id");
    if (productId) {
        return productId;
    }

    // Method 2: Try getting from hidden input field
    const productInput = document.querySelector('input[name="product_id"]');
    if (productInput && productInput.value) {
        return productInput.value;
    }

    // Method 3: Try getting from data attribute in add to cart form
    const addToCartForm = document.getElementById("add_to_cart");
    if (addToCartForm && addToCartForm.dataset.productId) {
        return addToCartForm.dataset.productId;
    }

    // Method 4: Try extracting from URL path (e.g., /shop/product/product-name-123)
    const pathMatch = window.location.pathname.match(/\/shop\/product\/[^/]+-(\d+)/);
    if (pathMatch && pathMatch[1]) {
        return pathMatch[1];
    }

    return null;
}

/**
 * Hide all SBODR buttons on the page
 */
function hideButtons() {
    const buttons = document.querySelectorAll(".sbodr-request");
    buttons.forEach((button) => {
        const container = button.closest(".d-inline-flex");
        if (container) {
            container.style.display = "none";
        } else {
            button.style.display = "none";
        }
    });
}

// Register the startup function
registry.category("public_components").add("sbodr_init", {
    start() {
        setupSBODRButton();
        return true;
    },
});
