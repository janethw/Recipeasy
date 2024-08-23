// this is the parent command
Cypress.Commands.add('login', (username, password) => {
    cy.visit('/login')

    cy.get('input[name=username]').type(username)

    // {enter} causes the form to submit
    cy.get('input[name=password]').type(`${password}{enter}`, { log: false })

    // we should be redirected to /homepage
    cy.url().should('include', '/homepage')

    // our auth cookie should be present
    cy.getCookie('session').should('exist')

  })