/** @odoo-module **/
import { useService } from "@web/core/utils/hooks";
import { Component, useState, onMounted } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";
import { _t } from "@web/core/l10n/translation";
import { rpc } from "@web/core/network/rpc";

export class BulkDiscountDialog extends Component {
    static template = "BulkDiscountDialog";
    static props = {
        productId: Number,
        productName: String,
        productImage: { type: String, optional: true },
        quantity: Number,
        close: Function,
    };
    static components = { Dialog };

    setup() {
        this.notificationService = useService("notification");

        this.state = useState({
            fullName: "",
            email: "",
            quantity: Math.max(10, this.props.quantity || 10),
            discount: 10,
            notes: "",
            isLoggedIn: false,
            isLoading: true,
            isSubmitting: false,
            formError: "",
            size: "xl",
            errors: {
                fullName: "",
                email: "",
                quantity: "",
                discount: "",
                notes: "",
            },
        });

        onMounted(() => this.loadUserInfo());
    }

    async loadUserInfo() {
        try {
            const result = await rpc("/sbodr/get_user_info");
            if (result) {
                this.state.fullName = result.name || "";
                this.state.email = result.email || "";
                this.state.isLoggedIn = result.is_logged_in || false;
            }
        } catch (error) {
            console.error("Error loading user info:", error);
        } finally {
            this.state.isLoading = false;
            this.state.size = "md";
        }
    }

    validateAndSubmit() {
        // Reset errors
        this.state.formError = "";
        this.state.errors = {
            fullName: "",
            email: "",
            quantity: "",
            discount: "",
            notes: "",
        };

        let isValid = true;

        // Validate full name
        if (!this.state.fullName.trim()) {
            this.state.errors.fullName = "Full name is required";
            isValid = false;
        }

        // Validate email
        if (!this.state.email.trim()) {
            this.state.errors.email = "Email is required";
            isValid = false;
        } else if (!this._isValidEmail(this.state.email)) {
            this.state.errors.email = "Please enter a valid email address";
            isValid = false;
        }

        // Validate quantity
        if (!this.state.quantity) {
            this.state.errors.quantity = "Quantity is required";
            isValid = false;
        } else if (this.state.quantity < 10) {
            this.state.errors.quantity = "Quantity must be at least 10";
            isValid = false;
        } else if (this.state.quantity > 1000) {
            this.state.errors.quantity = "Quantity cannot exceed 1000";
            isValid = false;
        }

        // Validate discount
        if (!this.state.discount) {
            this.state.errors.discount = "Discount is required";
            isValid = false;
        } else if (this.state.discount < 1) {
            this.state.errors.discount = "Discount must be at least 1%";
            isValid = false;
        } else if (this.state.discount > 70) {
            this.state.errors.discount = "Discount cannot exceed 70%";
            isValid = false;
        }

        // Validate notes
        if (!this.state.notes.trim()) {
            this.state.errors.notes = "Please explain why you need this discount";
            isValid = false;
        } else if (this.state.notes.trim().length < 10) {
            this.state.errors.notes = "Please provide a more detailed explanation";
            isValid = false;
        }

        if (!isValid) {
            this.state.formError = "Please correct the errors in the form";
            return;
        }

        // If validation passes, submit the request
        this.submitRequest();
    }

    _isValidEmail(email) {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(email);
    }

    submitRequest() {
        this.state.isSubmitting = true;

        rpc("/sbodr/submit_request", {
            product_id: this.props.productId,
            product_name: this.props.productName,
            full_name: this.state.fullName,
            email: this.state.email,
            quantity: this.state.quantity,
            discount: this.state.discount,
            notes: this.state.notes,
            create_lead: true,
        })
            .then((result) => {
                this.state.isSubmitting = false;

                if (result && result.success) {
                    this.notificationService.add(
                        _t("Your bulk discount request has been submitted successfully."),
                        {
                            type: "success",
                            title: _t("Request Submitted"),
                            sticky: false,
                        }
                    );
                    this.props.close();
                } else {
                    this.state.formError = result?.error || "Failed to submit request";
                    this.notificationService.add(
                        _t("Failed to submit request. Please try again."),
                        {
                            type: "danger",
                            title: _t("Error"),
                        }
                    );

                    this.props.close();
                }
            })
            .catch((error) => {
                this.state.isSubmitting = false;
                this.state.formError = "Network error. Please try again.";

                this.notificationService.add(_t("Failed to submit request. Please try again."), {
                    type: "danger",
                    title: _t("Error"),
                });

                this.props.close();

                console.error("Error submitting bulk discount request:", error);
            });
    }

    redirectLoginPage() {
        window.location.href = "/web/login";
    }
}
