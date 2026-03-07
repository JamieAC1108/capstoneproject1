#imports
import dash

#Title
html.Header([
    html.Title('Information System Search')
)]

#Page Body
html.Body([
    html.H2('Welcome to the website!')
    html.P("Using this website, you'll be able search through the CMCC information database!")
    html.P('Simply navigate using the buttons')
    html.H3('Press continue to get started!')
)]

#Footer
html.Footer([
    html.nav([
        html.A('Continue!' href='search.html')
    ])
)]