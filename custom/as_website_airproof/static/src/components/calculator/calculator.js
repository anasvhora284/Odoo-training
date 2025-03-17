/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";

export class CalculatorComponent extends Component {
  static template = "as_website_airproof.calculator_component";

  setup() {
    this.state = useState({
      display: "0",
      firstOperand: null,
      operator: null,
      waitingForSecondOperand: false,
      clearDisplay: false,
    });
  }

  inputDigit(ev) {
    let digit = ev.target.dataset.val; // Use dataset to get the value

    const { display, waitingForSecondOperand } = this.state;

    if (waitingForSecondOperand) {
      this.state.display = digit;
      this.state.waitingForSecondOperand = false;
    } else {
      this.state.display = display === "0" ? digit : display + digit;
    }
  }

  inputDecimal(ev) {
    if (this.state.waitingForSecondOperand) {
      this.state.display = "0.";
      this.state.waitingForSecondOperand = false;
      return;
    }

    if (!this.state.display.includes(".")) {
      this.state.display += ".";
    }
  }

  handleOperator(ev) {
    const nextOperator = ev.currentTarget.dataset.val;
    const { firstOperand, display, operator } = this.state;
    const inputValue = parseFloat(display);

    if (firstOperand === null) {
      this.state.firstOperand = inputValue;
    } else if (operator) {
      const result = this.performCalculation(operator, inputValue);
      this.state.display = String(result);
      this.state.firstOperand = result;
    }

    this.state.waitingForSecondOperand = true;
    this.state.operator = nextOperator;
  }

  performCalculation(operator, secondOperand) {
    if (operator === "+") {
      return this.state.firstOperand + secondOperand;
    } else if (operator === "-") {
      return this.state.firstOperand - secondOperand;
    } else if (operator === "*") {
      return this.state.firstOperand * secondOperand;
    } else if (operator === "/") {
      return this.state.firstOperand / secondOperand;
    }

    return secondOperand;
  }

  resetCalculator() {
    this.state.display = "0";
    this.state.firstOperand = null;
    this.state.operator = null;
    this.state.waitingForSecondOperand = false;
  }
}

registry
  .category("public_components")
  .add("as_website_airproof.CalculatorComponent", CalculatorComponent);

registry
  .category("actions")
  .add("as_website_airproof.calculator_action", CalculatorComponent);

export { CalculatorComponent };
