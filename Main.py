from io import open
import json
import arrow
import datetime
from pprint import pprint
import plotly.graph_objects as go
import humanize
import locale
import calendar
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import numpy as np
import Calendar_heatmap
import logging

language = locale.getdefaultlocale()

locale.setlocale(locale.LC_ALL, language[0])
humanize.activate(language[0])

logging.basicConfig(filename='Time-Tracker-Logging.log', level=logging.DEBUG, format='%(asctime)s %(name)-12s: %(levelname)-8s %(funcName)-4s (line %(lineno)d) : %(message)s')

console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(funcName)-4s (line %(lineno)d) : %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)


class full_data():

	def __init__(self):
		data = []
		with open(r"C:\Users\Adrien\Dropbox\time-tracker.txt", mode="r", encoding="utf8") as file:
			file_content = file.read()

		for line in file_content.split('\n'):
			result = line.split(" - ")
			data.append({"time": result[0], "position": result[1], "Activity": result[2]})

		# ADD DURATION

		for i, (v, w) in enumerate(zip(data[:-1], data[1:])):
			duration = arrow.get(w["time"]) - arrow.get(v["time"])
			data[i]["duration"] = duration

		self.data = data

	def raw(self):
		return self.data

	def to_dataframe(self):

		data = self.data
		for item in data:
			time = item["time"]
			arrow_time = arrow.get(time).datetime

			item["time"] = arrow_time

		to_remove = []
		for [v, w] in zip(data, data[1:]):
			if v["Activity"] == w["Activity"]:
				to_remove.append(w)
		for x in to_remove:
			data.remove(x)

		dataframe = pd.DataFrame(data)
		dataframe["endtime"] = dataframe["time"] + dataframe["duration"]
		return dataframe

	def make_list_of_days(self):

		list_of_days = []
		dataframe = self.to_dataframe()
		for idc, day in dataframe.groupby(dataframe.time.dt.date):
			calendar_day = day.iloc[0]["time"].date()
			list_of_days.append(calendar_day)
		return list_of_days

	def activities(self):

		activities = []

		for datapoint in self.data:
			if datapoint["Activity"] not in activities:
				activities.append(datapoint["Activity"])
		return activities

	def time_by_activities(self):

		time_by_activities = []

		sorted_data = sorted(self.data, key=lambda k: k['Activity'])

		for activity in self.activities():
			total_time = datetime.timedelta(0)
			for datapoint in sorted_data:
				if activity in datapoint["Activity"]:
					if "duration" in datapoint:
						total_time += datapoint["duration"]
			time_by_activities.append([activity, total_time])

		return time_by_activities

	def datetime_to_hours(self):
		df = self.to_dataframe()
		df["hour_start"] = df["time"].dt.time
		df["hour_end"] = df["endtime"].dt.time
		return df

	def geopoints(self):

		geopoints = []

		for datapoint in self.data:

			if datapoint["position"] not in geopoints:
				position = datapoint["position"].split("/")
				approx_position = []
				for chiffre in position:
					approx_position.append(round(float(chiffre), 3))
				if approx_position not in geopoints:
					geopoints.append(approx_position)
		return geopoints

	def list_by_geo(self):
		sorted_data = sorted(self.data, key=lambda k: k['Activity'])

		list_by_geo = []
		time_by_activities = []
		for geopoint in self.geopoints():
			list_by_geo.append({"position": geopoint})

			for activity in self.activities():
				total_time = datetime.timedelta(0)
				for datapoint in sorted_data:
					if activity in datapoint["Activity"]:
						if str(geopoint[0]) in str(round(float(datapoint["position"].split("/")[0]), 3)):
							if "duration" in datapoint:
								total_time += datapoint["duration"]
				time_by_activities.append([activity, total_time])
				for time in time_by_activities:
					for position in list_by_geo:
						if str(geopoint) in str(position["position"]):
							if total_time.total_seconds() != 0.0:
								position[activity] = total_time.total_seconds()
		return list_by_geo

	def time_data_by_date(self, activity):

		time_data = []

		for datapoint in self.data:
			if datapoint["Activity"] == activity:
				date = arrow.get(datapoint["time"]).date()
				if "duration" in datapoint:
					time_data.append({"date": date, "duration": datapoint["duration"]})

		for i, (v, w) in enumerate(zip(time_data[:-1], time_data[1:])):  # Additionne les deux qui tombent à la même date
			if v["date"] == w["date"]:
				v["duration"] = w["duration"] + v["duration"]
				time_data.remove(w)

		return time_data

	def time_data_by_weekday(self, activity):

		weekly_sleep = []
		activity_data = self.time_data_by_date(activity)

		for datapoint in activity_data:
			weekday = calendar.day_name[arrow.get(datapoint["date"]).weekday()]
			duration_in_hours = datapoint["duration"].seconds // 3600
			weekly_sleep.append({"weekday": weekday, "duration": duration_in_hours})

		for i, (v, w) in enumerate(zip(weekly_sleep[:-1], weekly_sleep[1:])):  # Additionne les deux qui tombent à la même date
			if v["weekday"] == w["weekday"]:
				v["duration"] = w["duration"] + v["duration"]
				activity_data.remove(w)

		# print("Weekly sleep", weekly_sleep)

		sleep_duration_weekly = []

		for days in weekly_sleep:
			duration = days["duration"]
			sleep_duration_weekly.append(duration)

		weekly_sleep = pd.DataFrame(weekly_sleep)
		return weekly_sleep

	def year_span(self):
		year_span = []
		for datapoint in self.data:
			year = arrow.get(datapoint["time"]).year
			year_span.append(year)

		year_span = list(set(year_span))

		return year_span

	def full_sleep_calendar_dataframe(self, activity):
		full_sleep_calendar = []
		full_sleep_calendar_dataframe = pd.DataFrame(full_sleep_calendar)
		for year in self.year_span():
			year_dataframe = pd.DataFrame([])
			start = datetime.datetime(year, 1, 1)
			end = datetime.datetime(year, 12, 31)

			if calendar.isleap(year):
				sleep_calendar = np.full((366,), fill_value=np.inf)
			else:
				sleep_calendar = np.full((365,), fill_value=np.inf)

			for datapoint in self.time_data_by_date(activity):
				for i, days in enumerate(pd.date_range(start, end)):

					if datapoint["date"] == days:
						np.put(sleep_calendar, i, int(datapoint["duration"].seconds))
					else:
						if sleep_calendar[i] == np.inf:
							np.put(sleep_calendar, i, 0)
			year_dataframe[year] = sleep_calendar

			full_sleep_calendar_dataframe = pd.concat([full_sleep_calendar_dataframe, year_dataframe], axis=1)

		return full_sleep_calendar_dataframe

	def year_activity_calendar(self, activity, year_arg):
		try:
			year_activity_calendar = self.full_sleep_calendar_dataframe(activity)[year_arg]
		except Exception as e:
			logging.error("Year out of span for data")
			year_activity_calendar = []
		return year_activity_calendar


class make_graph():
	def global_geo_map(self):
		mapfig = go.Figure(data=[go.Scattergeo(lon=[full_data().list_by_geo()[0]["position"][0]], lat=[full_data().list_by_geo()[0]["position"][1]])])

		mapfig.update_layout(
			title_text='Activities by position',
			showlegend=True,
			geo=dict(
				scope='europe',
				landcolor='rgb(217, 217, 217)',
			),

		)
		return mapfig

	def global_piefig(self):
		activity_for_graph = [x for x, v in full_data().time_by_activities()]
		duration_for_graph = [v.total_seconds() for x, v in full_data().time_by_activities()]
		humanized_duration_for_graph = [humanize.naturaldelta(v.total_seconds()) for x, v in full_data().time_by_activities()]
		piefig = go.Figure(data=[go.Pie(labels=activity_for_graph, values=duration_for_graph, text=humanized_duration_for_graph, hole=.3, texttemplate="%{label}: %{text} <br>(%{percent})", hovertemplate="%{label}: %{text} <br>(%{percent})")])
		return piefig

	def global_barfig(self):
		activity_for_graph = [x for x, v in full_data().time_by_activities()]
		duration_for_graph = [v.seconds /3600 for x, v in full_data().time_by_activities()]
		humanized_duration_for_graph = [humanize.naturaldelta(v.total_seconds()) for x, v in full_data().time_by_activities()]
		barfig = go.Figure(data=[go.Bar(y=activity_for_graph, x=duration_for_graph, text=humanized_duration_for_graph, orientation="h", texttemplate="%{label}: %{text} <br>(%{percent})", hovertemplate="%{label}: %{text}")])

		return barfig

	def week_activity_barfig(self, activity):
		time_data_by_weekday = full_data().time_data_by_weekday(activity)

		week_activity_barfig = px.bar(time_data_by_weekday, x=time_data_by_weekday.weekday, y=time_data_by_weekday.duration, color=time_data_by_weekday.duration)
		return week_activity_barfig

	def yearly_heatmap(self, activity, year):
		yearly_heatmap = Calendar_heatmap.display_year(full_data().year_activity_calendar(activity, year), year=year, activity=activity)
		return yearly_heatmap

#DASH

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],suppress_callback_exceptions=True)


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


sidebar_list = [dbc.NavLink("Home", href="/", active="exact")]
for activity in full_data().activities():
	sidebar_list.append(dbc.NavLink(activity, href=str("/" + activity), active="exact"))


sidebar = html.Div(
    [
        html.H2("Time Tracker", className="display-4"),
        html.Hr(),
        html.P(
            "Welcome, here's your days at a glance.", className="lead"
        ),
        dbc.Nav(

            sidebar_list,
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", style=CONTENT_STYLE)

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])


def render_activity_page(activity):
	container = dbc.Container(

		[html.H1(f"{activity} data"),
		 html.Hr(),
		 # Hidden div inside the app that stores the intermediate value
		 dcc.Input(id="activity", value=activity, style={"display" : "none"})
			,

		 dbc.Row([

			 dbc.Col(dcc.Graph(
				 id='Activity bars',
				 figure=make_graph().week_activity_barfig(activity)))
		 ]

		 ),

		 html.H3(f"Yearly {activity} data"),
		 html.Hr(),
		 dcc.Dropdown(
			 id="year_input",
			 options=[
				 {"label": col, "value": col} for col in full_data().full_sleep_calendar_dataframe(activity).columns
			 ],
			 value=datetime.datetime.now().year,

		 ),
		 dbc.Row([

			 dbc.Col([dcc.Graph(
				 id='Heatmap'
			 )]),

		 ])

		 ]
	)
	return container

@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
	if pathname == "/":
		return dbc.Container(

	[html.H1("Total data"),
        html.Hr(),


dbc.Row([

	dbc.Col(dcc.Graph(
		id='Time pie',
		figure=make_graph().global_piefig())),

	dbc.Col(dcc.Graph(
		id='Time bar',
		figure=make_graph().global_barfig()))
]

	),

dbc.Row([
	dbc.Col([dcc.Graph(
		id='Map',
		figure=make_graph().global_geo_map(),
	style={"height":1200}
	)]),

	])

	]
)
	else:
		for activity in full_data().activities():
			if pathname == "/" + activity:
				return render_activity_page(activity)
	# If the user tries to reach a different page, return a 404 message
	return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )


@app.callback(
    Output(component_id='Heatmap', component_property='figure'),
    Input(component_id='year_input', component_property='value'),
	Input(component_id='activity', component_property='value')

)
def make_heatmap_graph(year, activity):
	fig = make_graph().yearly_heatmap(activity, year)
	return fig

app.run_server(debug=False, use_reloader=False)