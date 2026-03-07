#imports
import dash

#Title
html.Header([
    html.Title('Information System Search')
)]

#Page Body
html.Body([
    #buttons
button = html.Button('top')

@app.callback(
    input(button, "n_clicks")
    )

button2 = html.Button('bottom')

@app.callback(
    input(button2, "n_clicks")
    )

button3 = html.Button('a-z')

@app.callback(
input(button3, "n_clicks")
)

button4 = html.Button('z-a')

@app.callback(
input(button4, "n_clicks")
)
)]

#Footer
html.Footer([
    html.P('Created by ') html.A('Jamie Aaron Cole' href='mailto:jamie.cole@mainecc.edu')
       html.P('and ') html.A('Theodore (Teddy) Robillard' href='mailto:theodore.robillar@mainecc.edu')
    html.nav([
        html.A('Give us some feedback!' href='feedback.html')
    ])
)]