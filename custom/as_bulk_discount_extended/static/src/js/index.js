/** @odoo-module **/

import { registry } from "@web/core/registry";
import { BulkDiscountDialog } from "./components/bulk_discount_dialog/bulk_discount_dialog";

// Register components
registry.category("components").add("BulkDiscountDialog", BulkDiscountDialog);

// Import widgets to ensure they are registered
import "./bulk_discount_button";
