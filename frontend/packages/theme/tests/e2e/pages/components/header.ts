import { el } from '../utils/element';

class Header {
  get cart(): Cypress.Chainable {
    return el('app-header-cart');
  }

  get categories(): Cypress.Chainable {
    return cy.get('[data-e2e*="app-header"]');
  }

  get category() {
    return {
      women: () => el('app-header-url_numerai'),
      men: () => el('app-header-url_signals')
    };
  }

  openCart(): Cypress.Chainable {
    const click = $el => $el.click();
    return this.cart.pipe(click).should(() => {
      expect(Cypress.$('[data-e2e="sidebar-cart"]')).to.exist;
    });
  }

  get account(): Cypress.Chainable {
    return cy.get('[name="app-header-account"]');
  }

  openLoginModal(): Cypress.Chainable {
    const click = $el => $el.click();
    return this.account.pipe(click).should(() => {
      expect(Cypress.$('[data-e2e="login-modal"]')).to.exist;
    });
  }
}

export default new Header();
