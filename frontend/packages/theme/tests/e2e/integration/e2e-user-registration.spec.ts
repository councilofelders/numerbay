import page from '../pages/factory';
import requests from '../api/requests';
import generator from '../utils/data-generator';

context(['regression'], 'User registration', () => {
  beforeEach(() => {
    // eslint-disable-next-line func-names
    cy.fixture('test-data/e2e-user-registration').then(function (fixture) {
      this.fixtures = {
        data: fixture
      };
    });
  });

  // eslint-disable-next-line func-names
  it('Should successfully register', function () {
    const data = this.fixtures.data[this.test.title];
    data.user.username = generator.email;
    page.home.visit();
    cy.wait(150);
    page.home.header.openLoginModal();
    page.components.loginModal.loginOptionsTab.then($item => {
      $item[0].__vue__.toggle($item[0].__vue__.$children[1]._uid);
    });
    page.components.loginModal.registerOptionButton.click();
    page.components.loginModal.fillForm(data.user);
    page.components.loginModal.submitButton.click();
    page.components.loginModal.container.should('not.exist');
    page.home.header.account.click();
    page.myAccount.sidebar.heading.should('be.visible');
  });

  // eslint-disable-next-line func-names
  it('Existing user - should display an error', function () {
    const data = this.fixtures.data[this.test.title];
    data.user.username = generator.email;
    requests.signUpUser(data.user).then(() => {
      cy.clearCookies();
    });
    page.home.visit();
    cy.wait(150);
    page.home.header.openLoginModal();
    page.components.loginModal.loginOptionsTab.then($item => {
      $item[0].__vue__.toggle($item[0].__vue__.$children[1]._uid);
    });
    page.components.loginModal.registerOptionButton.click();
    page.components.loginModal.fillForm(data.user);
    page.components.loginModal.submitButton.click();
    page.components.loginModal.container.contains(data.errorMessage).should('be.visible');
  });
});
