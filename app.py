import numpy as np
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px

import rad_pattern as rp

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


title1 = html.Div([
    html.H1('Antenna Radiation Pattern'),
    html.Div([
        html.P('Simple tool to calculate the radiation pattern of a dipole antenna')
    ])
])

title2 = dcc.Markdown(
    '''
    [Home](/)

    # Antenna Radiation Pattern

    This is a simple tool that calculates the radiation pattern of a **dipole antenna**, given the radio of transmitting/receiving wavelength to antenna length
    '''
)

footer = dcc.Markdown(
    '''
    This was also my first time using [Dash](https://dash.plotly.com/).
    '''
)
#fig = px.line(x=theta, y=np.sin(theta))
plot = dcc.Graph(id='my-graph', style={'height': '70vh', 'width': '50vw'})

min_val = 1
max_val=20
start_val = int((min_val+max_val)/2)

slider1 =  html.Div([
    html.H3('Wavelength (m):'),
    html.Div(
        dcc.Slider(
            id='wavelength-slider',
            min = min_val,
            max=max_val,
            step=0.1,
            value=start_val,
            vertical=False,
            updatemode='drag',
            marks={i:'{}'.format(i) for i in range(min_val,max_val)},
        ),
        style={'height': '5vh', 'width': '50vw'}
    ),
    html.Div(id='slider-output-container1')
])

d_min = 0.1
d_max = 10
d_start = int((d_min+d_max)/2)

slider2 =  html.Div([
    html.H3('Dipole Length (m):'),
    html.Div(
        dcc.Slider(
            id='length-slider',
            min = d_min,
            max=d_max,
            step=0.01,
            value=d_start,
            vertical=False,
            updatemode='drag',
            marks={i:'{}'.format(i) for i in range(d_max)},
        ),
        style={'height': '5vh', 'width': '50vw'}
    ),
    html.Div(id='slider-output-container2')
])


app = dash.Dash(__name__, url_base_pathname='/radpattern/', external_stylesheets=external_stylesheets)
server = app.server
app.layout = html.Div([title2, slider1, slider2, plot, footer])

def get_wave(k):
    theta = np.linspace(0, 2*np.pi, 1000)
    return np.sin(k*theta)

@app.callback(
    dash.dependencies.Output('slider-output-container1', 'children'),
    [dash.dependencies.Input('wavelength-slider', 'drag_value'), dash.dependencies.Input('wavelength-slider', 'value')])
def update_output(drag_value, value):
    if drag_value is None:
        return "{} m / {} MHz".format(value, round(300/value, 2))
    else:
        return "{} m / {} MHz".format(value, round(300/value))

@app.callback(
    dash.dependencies.Output('slider-output-container2', 'children'),
    [dash.dependencies.Input('length-slider', 'drag_xvalue'), dash.dependencies.Input('length-slider', 'value')])
def update_output(drag_xvalue, value):
    if drag_xvalue is None:
        return "{} metre dipole antenna".format(value)
    return "{} metre dipole antenna".format(drag_xvalue)

@app.callback(
    dash.dependencies.Output('my-graph', 'figure'),
    [dash.dependencies.Input('wavelength-slider', 'drag_value'),
    dash.dependencies.Input('wavelength-slider', 'value'),
    dash.dependencies.Input('length-slider', 'drag_value'),
    dash.dependencies.Input('length-slider', 'value')])
def update_output(drag_wave, wave, drag_length, length):

    if drag_wave is None or drag_length is None:
        d1 = rp.DipoleAntenna(float(300/wave), length)
        yx = d1.E / np.nanmax(d1.E)
        fig = px.line_polar(theta=np.degrees(d1.theta)+90, r=yx, title="Radiation Pattern", labels={'x': 'X', 'y':'Y'}, template="plotly_dark")
    else:
        d1 = rp.DipoleAntenna(300/drag_wave, drag_length)
        yx = d1.E / np.nanmax(d1.E)
        fig = px.line_polar(theta=np.degrees(d1.theta)+90, r=yx, title="Radiation Pattern", labels={'x': 'X', 'y':'Y'}, template="plotly_dark")

    return fig

if __name__ == '__main__':
    app.run_server()
