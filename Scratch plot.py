from io import open
import json
import arrow
import datetime
from pprint import pprint
import plotly.graph_objects as go
import humanize
import locale

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

language = locale.getdefaultlocale()
humanize.activate(language[0])
# GET AND FORMAT DATA
data = []
with open(r"C:\Users\Adrien\Dropbox\time-tracker.txt", mode="r", encoding="utf8") as file:
	file_content = file.read()

for line in file_content.split('\n'):
	result = line.split(" - ")
	data.append({"time": result[0], "position":result[1], "Activity":result[2]})

# ADD DURATION

for i, (v, w) in enumerate(zip(data[:-1], data[1:])):
	duration = arrow.get(w["time"])-arrow.get(v["time"])
	data[i]["duration"]= duration

# print("Data : ", data)

#GET ACTIVITIES

activities = []

for datapoint in data:
	if datapoint["Activity"] not in activities:
		activities.append(datapoint["Activity"])

print("activities : ", activities)

# ADD DURATION BY ACTIVITIES

time_by_activities = []

sorted_data = sorted(data, key=lambda k: k['Activity'])

for activity in activities:
	total_time = datetime.timedelta(0)
	for datapoint in sorted_data:
		if activity in datapoint["Activity"]:
			if "duration" in datapoint:
				total_time += datapoint["duration"]
	time_by_activities.append([activity, total_time])

print("time by activities : ", time_by_activities)


# MAKE GEO LIST

geopoints = []

for datapoint in data:

	if datapoint["position"] not in geopoints:
		position = datapoint["position"].split("/")
		approx_position = []
		for chiffre in position:
			approx_position.append(round(float(chiffre), 3))
		if approx_position not in geopoints:
			geopoints.append(approx_position)

print("Geopoints : ", geopoints)


list_by_geo = []
time_by_activities = []
for geopoint in geopoints:
	list_by_geo.append({"position":geopoint})

	for activity in activities:
		total_time = datetime.timedelta(0)
		for datapoint in sorted_data:
			if activity in datapoint["Activity"]:
				if str(geopoint[0]) in str(round(float(datapoint["position"].split("/")[0]),3)):
					if "duration" in datapoint:
						total_time += datapoint["duration"]
		time_by_activities.append([activity, total_time])
		for time in time_by_activities:
			for position in list_by_geo:
				if str(geopoint) in str(position["position"]):
					if total_time.total_seconds() != 0.0:
						position[activity] = total_time.total_seconds()



print("list by geo : " , list_by_geo)
# MAKE THE LISTS FOR GRAPHS
activity_for_graph = [x for x, v in time_by_activities]
duration_for_graph = [v.total_seconds() for x, v in time_by_activities]
humanized_duration_for_graph = [humanize.naturaldelta(v.total_seconds()) for x, v in time_by_activities]
print("humanized_duration_for_graph : ", humanized_duration_for_graph)



#GRAPHING

piefig = go.Figure(data=[go.Pie(labels=activity_for_graph, values=duration_for_graph, text= humanized_duration_for_graph, hole=.3, texttemplate ="%{label}: %{text} <br>(%{percent})", hovertemplate="%{label}: %{text} <br>(%{percent})")])


barfig = go.Figure(data=[go.Bar(y=activity_for_graph, x=duration_for_graph, text= humanized_duration_for_graph, orientation="h", texttemplate ="%{label}: %{text} <br>(%{percent})", hovertemplate="%{label}: %{text}")])

mapfig = go.Figure(data=[go.Scattergeo(lon=[list_by_geo[0]["position"][0]], lat=[list_by_geo[0]["position"][1]], )])
mapfig.update_layout(
        title_text = 'Activities by position',
        showlegend = True,
	geo=dict(
		scope='europe',
		landcolor='rgb(217, 217, 217)',
	),


)


#DASH

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])


# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "18rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}


sidebar = html.Div(
    [
        html.H2("Time Tracker", className="display-4"),
        html.Hr(),
        html.P(
            "Welcome, here's your days at a glance.", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", active="exact"),
                dbc.NavLink("Sleep", href="/page-1", active="exact"),
                dbc.NavLink("Page 2", href="/page-2", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", style=CONTENT_STYLE)

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])

@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return dbc.Container(

	[html.H1("Total data"),
        html.Hr(),


dbc.Row([

	dbc.Col(dcc.Graph(
		id='Time pie',
		figure=piefig)),

	dbc.Col(dcc.Graph(
		id='Time bar',
		figure=barfig))
]

	),

dbc.Row([
	dbc.Col([dcc.Graph(
		id='Map',
		figure=mapfig,
	style={"height":1200}
	)]),

	], style=CONTENT_STYLE)

	]
)
    elif pathname == "/page-1":
        return html.P("This is the content of page 1. Yay!")
    elif pathname == "/page-2":
        return html.P("Oh cool, this is page 2!")
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )

app.run_server(debug=True, use_reloader=False)