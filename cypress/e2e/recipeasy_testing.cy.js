// describe - top level test
// it - what you want to happen


// checking that the app is available by visiting login page
describe('template spec', () => {
  it('App Available', () => {
    cy.visit('/login')
  })
})

// checking that you can register and login to the web app
describe('Authentication', () => {

  // generating random user data: username, email and password
  // used by all tests within Authentication hence declared outside of the its
    var currentUser = {username: (Math.random() + 1).toString(36).substring(5),
                       password: (Math.random() + 1).toString(36).substring(7),
                       email: 'a@b.com'}

  // testing whether the user can register
  it('Register Page', () => {
    // fetching username, password and email as declared in currentUser
    const { username, password, email } = currentUser
    cy.visit('/')
    // getting 'Register' menu item out of the html
    cy.get('a').contains('Register').click()
    cy.url().should('include', '/register')

    // 'type' in username, email and password in corresponding input element
    cy.get('input[id=username]').type(username)
    cy.get('input[id=email]').type(email)
    cy.get('input[id=password]').type(password)

    cy.get('button[type=submit]').click()

    cy.url().should('include', '/homepage')
  }),

  // checking if user already exists
  it('Register Page User Exists', () => {
    const { username, password, email } = currentUser
    cy.visit('/')
    cy.get('a').contains('Register').click()
    cy.url().should('include', '/register')

    cy.get('input[id=username]').type(username)
    cy.get('input[id=email]').type(email)
    cy.get('input[id=password]').type(password)

    cy.get('button[type=submit]').click()
    // confirming still on the Register page
    cy.url().should('include', '/register')
    // checking the validation messages are correct
    // using strong as reference as it is the only identifiable tag in this html element.
    cy.get('strong').contains('Username already taken. Please try again.')
  }),

  // checking for a failed login and that the correct error message shows
  it('Failed Login', () => {
    const { username, password, email } = currentUser
    cy.visit('/')
    cy.get('input[name=username]').type(username)
    cy.get('input[name=password]').type(`${password + 'ZZZ'}{enter}`, { log: false })
    cy.url().should('include', '/login')
    cy.get('strong').contains('Username or Password Incorrect')
  }),

  // checking a successful login
  it('Login', () => {
    const { username, password, email } = currentUser
    cy.visit('/')
    cy.login(username, password)
    cy.url().should('include', '/homepage')
  })
})


// checking the recipe search functionality
describe('Recipe Search', () => {

    var currentUser = {username: 'testing',
                       password: 't3stp455w0rd'}

    // checking the recipe search validation, when no ingredients inputted the validation pop up appears
    it('No Ingredient Search', () => {
    const { username, password} = currentUser
    cy.login(username, password)
    cy.visit('/recipe')
    cy.get('button[type=submit]').click()
    cy.get('input:invalid').should('have.length', 1)
    cy.get('input[name=ingredient1]').then(($input) => {
    expect($input[0].validationMessage).to.eq('Please fill in this field.')
    })
    }),

    // checking a nonsense ingredient, when inputted no data is returned
    it('Nonsense Ingredient Search', () => {
    const { username, password} = currentUser
    cy.login(username, password)
    cy.visit('/recipe')
    cy.get('input[name=ingredient1]').type('zsdgabgzejyz')
    cy.get('button[type=submit]').click()
    cy.get('td[class=select]').should('not.exist')
    }),

    // checking that you can search with one ingredient and that the table populates on the search results page
    it('1 Ingredient Search', () => {
    const { username, password} = currentUser
    cy.login(username, password)
    cy.visit('/recipe')
    cy.get('input[name=ingredient1]').type('Mutton')
    cy.get('button[type=submit]').click()
    cy.get('td[class=select]').should('exist')
    }),

    // checking that you can search with two ingredients and that the table populates on the search results page
    it('2 Ingredient Search', () => {
    const { username, password} = currentUser
    cy.login(username, password)
    cy.visit('/recipe')
    cy.get('input[name=ingredient1]').type('Tofu')
    cy.get('input[name=ingredient2]').type('Noodles')
    cy.get('button[type=submit]').click()
    cy.get('td[class=select]').should('exist')
    }),

    // checking that you can search with three ingredients and that the table populates on the search results page
    it('3 Ingredient Search', () => {
    const { username, password} = currentUser
    cy.login(username, password)
    cy.visit('/recipe')
    cy.get('input[name=ingredient1]').type('Tuna')
    cy.get('input[name=ingredient2]').type('Pasta')
    cy.get('input[name=ingredient3]').type('Cheese')
    cy.get('button[type=submit]').click()
    cy.get('td[class=select]').should('exist')
    }),

    // checking that you can search with four ingredients and that the table populates on the search results page
    it('4 Ingredient Search', () => {
    const { username, password} = currentUser
    cy.login(username, password)
    cy.visit('/recipe')
    cy.get('input[name=ingredient1]').type('Mince Beef')
    cy.get('input[name=ingredient2]').type('Carrot')
    cy.get('input[name=ingredient3]').type('Potato')
    cy.get('input[name=ingredient4]').type('Peas')
    cy.get('button[type=submit]').click()
    cy.get('td[class=select]').should('exist')
    }),

    // checking that you can search with five ingredients and that the table populates on the search results page
    it('5 Ingredient Search', () => {
    const { username, password} = currentUser
    cy.login(username, password)
    cy.visit('/recipe')
    cy.get('input[name=ingredient1]').type('Chicken')
    cy.get('input[name=ingredient2]').type('Pepper')
    cy.get('input[name=ingredient3]').type('Tomato')
    cy.get('input[name=ingredient4]').type('Garlic')
    cy.get('input[name=ingredient5]').type('Onion')
    cy.get('button[type=submit]').click()
    cy.get('td[class=select]').should('exist')
    })

})


// checking the recipe details page
describe('Recipe Details', () => {


    var currentUser = {username: 'testing',
                       password: 't3stp455w0rd'}

    // checking that from the search you can reach the recipe details page and that the page populates data
    it('Get Recipe Details', () => {
    const { username, password } = currentUser
    cy.login(username, password)
    cy.visit('/recipe')
    cy.get('input[name=ingredient1]').type('Mutton')
    cy.get('button[type=submit]').click()
    cy.get('td').first().within(($td)=> {
    cy.get('a').click()
    })
    cy.get('div[class=recipe]').should('exist')
    })

})