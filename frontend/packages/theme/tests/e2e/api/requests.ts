import { User, Product } from '../types/types';

export type CreateCartResponse = {
  body: {
    data: {
      cart: {
        id: string;
      }
    }
  }
}

const requests = {

  addToCart(cartId: string, product: Product, quantity?: number): Cypress.Chainable {
    const options = {
      url: '/api/numerbay/addToCart',
      method: 'POST',
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json'
      },
      body: [
        {id: cartId, version: 1},
        {id: product.id, sku: product.sku },
        quantity ?? 1,
        null
      ]
    };
    return cy.request(options);
  },

  createCart(): Cypress.Chainable {
    const options = {
      url: '/api/numerbay/createCart',
      method: 'POST',
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json'
      },
      body: [{}, null]
    };
    return cy.request(options);
  },

  signUpUser(user: User): Cypress.Chainable {
    const options = {
      url: '/api/numerbay/signUpUser',
      method: 'POST',
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json'
      },
      body: [
        {
          username: user.username,
          password: user.password
        }
      ]
    };
    return cy.request(options);
  },

  getMe(): Cypress.Chainable {
    const options = {
      url: '/api/numerbay/getMe',
      method: 'POST',
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json'
      },
      body: [
        {customer: false}, null
      ]
    };
    return cy.request(options);
  }
};

export default requests;
