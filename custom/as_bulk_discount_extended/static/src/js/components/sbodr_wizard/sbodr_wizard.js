/** @odoo-module **/

import { useService } from "@web/core/utils/hooks";
import { Component, useState } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";

export class SBODRWizard extends Component {
    static template = "as_bulk_discount_extended.SBODRWizard";
    static props = { close: { type: Function } };
    static components = { Dialog };

    setup() {
        this.rpcService = useService("rpc");
        this.notificationService = useService("notification");
        this.userService = useService("user");

        this.state = useState({
            fullName: this.userService.name || "Please Login first to continue",
            email: this.userService.email || "Please Login first to continue",
            quantity: 10,
            discount: 1.0,
            description: "",
        });
    }

    async sendRequest() {
        try {
            const result = await this.rpcService("/sbodr/request", {
                full_name: this.state.fullName,
                email: this.state.email,
                quantity: this.state.quantity,
                discount: this.state.discount,
                description: this.state.description,
            });

            if (result && result.effect) {
                // Rainbow man effect is handled by the backend
                this.props.close();
            } else {
                // Fallback notification
                this.notificationService.add("Thank you! We will get back to you shortly.", {
                    type: "success",
                    title: "Request Sent",
                    sticky: false,
                });
                this.props.close();
            }
        } catch (error) {
            this.notificationService.add("Failed to send request. Please try again.", {
                type: "danger",
            });
        }
    }
}
