/** @odoo-module **/

import { ListRenderer } from "@web/views/list/list_renderer";
import { useService } from "@web/core/utils/hooks";
import { patch } from "@web/core/utils/patch";
import { onWillRender, onWillUpdateProps } from "@odoo/owl";

const originalSetup = ListRenderer.prototype.setup;

patch(ListRenderer.prototype, {
    setup() {
        originalSetup.call(this);
        this.orm = useService("orm");
        this.colorConditionsEnabled = true;

        onWillRender(() => this.applyColorConditions());
        onWillUpdateProps(() => this.applyColorConditions());
    },

    async applyColorConditions() {
        if (!this.props?.list?.records?.length || !this.colorConditionsEnabled) {
            return;
        }

        try {
            const model = this.props.list.resModel; //current opened model name
            const conditions = await this.orm.call("color.condition", "get_color_conditions", [
                model,
            ]);

            if (!conditions?.length) {
                return;
            }

            await new Promise((resolve) => setTimeout(resolve, 100));

            //all rows from the list view
            const rows = document.querySelectorAll(".o_list_view .o_data_row");
            if (!rows?.length) {
                return;
            }

            const recordMap = new Map();
            for (const record of this.props.list.records) {
                recordMap.set(record.id, record);
            }

            for (const row of rows) {
                const dataId = row.getAttribute("data-id");
                if (!dataId) continue;

                const record = recordMap.get(dataId);
                if (!record) continue;

                for (const condition of conditions) {
                    try {
                        if (this.matchDomain(condition.domain, record.data)) {
                            row.style.color = condition.text_color || "#000000";
                            row.style.backgroundColor = condition.background_color || "#FFFFFF";

                            const cells = row.querySelectorAll("td");
                            cells.forEach((cell) => {
                                cell.style.color = condition.text_color || "#000000";
                                cell.style.backgroundColor =
                                    condition.background_color || "#FFFFFF";
                            });

                            break;
                        }
                    } catch (e) {
                        console.error("Error applying condition:", e);
                    }
                }
            }
        } catch (error) {
            console.error("Error in applyColorConditions:", error);
            this.colorConditionsEnabled = false;
        }
    },

    matchDomain(domain, recordData) {
        if (!domain || !domain.length) return true;

        if (Array.isArray(domain) && domain.length === 3 && typeof domain[1] === "string") {
            const [field, operator, value] = domain;
            const fieldValue = recordData[field];

            switch (operator) {
                case "=":
                    return fieldValue === value;
                case "!=":
                    return fieldValue !== value;
                case ">":
                    return fieldValue > value;
                case ">=":
                    return fieldValue >= value;
                case "<":
                    return fieldValue < value;
                case "<=":
                    return fieldValue <= value;
                case "in":
                    return Array.isArray(value) && value.includes(fieldValue);
                case "not in":
                    return !Array.isArray(value) || !value.includes(fieldValue);
                default:
                    return false;
            }
        }

        if (domain[0] === "&") {
            return (
                this.matchDomain(domain[1], recordData) && this.matchDomain(domain[2], recordData)
            );
        } else if (domain[0] === "|") {
            return (
                this.matchDomain(domain[1], recordData) || this.matchDomain(domain[2], recordData)
            );
        } else if (domain[0] === "!") {
            return !this.matchDomain(domain[1], recordData);
        }

        if (Array.isArray(domain[0])) {
            return domain.every((condition) => this.matchDomain(condition, recordData));
        }

        return false;
    },
});
