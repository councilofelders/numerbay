import { User } from '../../types/types';
import { el } from '../utils/element';

class LoginModal {

  get container(): Cypress.Chainable {
    return el('login-modal', '.sf-modal__container');
  }

  get loginOptionsTab(): Cypress.Chainable {
    return el('login-options-tab');
  }

  get registerOptionButton(): Cypress.Chainable {
    return el('register-option-button');
  }

  get username(): Cypress.Chainable {
    return el('login-modal-username');
  }

  get password(): Cypress.Chainable {
    return el('login-modal-password');
  }

  get submitButton(): Cypress.Chainable {
    return el('login-modal-submit');
  }

  get loginToAccountButton(): Cypress.Chainable {
    return el('login-modal-login-to-your-account');
  }

  get loginBtn(): Cypress.Chainable {
    return el('login-modal-submit');
  }

  fillForm(user: User): void {
    if (user.username) this.username.type(user.username);
    if (user.password) this.password.type(user.password);
  }

}

export default new LoginModal();
