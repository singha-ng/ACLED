import dash
from dash import dcc, html, ctx
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import data_process as d
import layouts
from datetime import datetime
import graphs as g

app = dash.Dash(__name__, title='ACLED Myanmar',
                external_stylesheets=[dbc.themes.MORPH])

server = app.server


app.layout = html.Div([
    # html.Header([layouts.header], className='header'),
    dbc.Tabs([
        dbc.Tab(
            label="Summary",
            children=[layouts.summary]
        ),
        dbc.Tab(
            label="Sub-events",
            children=[
                html.Main([
                    layouts.events_aside,
                    layouts.events_mainContainer
                ], className='container')
            ]
        ),
        dbc.Tab(
            label="Interactions",
            children=[
                html.Main([
                    layouts.interaction_aside,
                    layouts.interaction_mainContainer
                ], className='container')
            ]
        ),
        dbc.Tab(
            label='About',
            children=[layouts.about]
        )
    ], className='tabs'),

])


# ====================
# callbacks
# ====================
# ====================
# SUB _EVENTS
# ====================

# sub-events graph
@ app.callback((Output('events_fatalities_plot', 'figure')),
               (Output('events_events_plot', 'figure')),
               (Output('events_geo_plot', 'figure')),
               (State('event', 'value')),
               #    (State('sub-events', 'value')),
               (State('date_range_event', 'start_date')),
               (State('date_range_event', 'end_date')),
               (Input('btn-search-event', 'n_clicks')),
               (Input('btn-reset-event', 'n_clicks'))
               )
def output_subevents_graph(evt, start, end, btn_search, btn_reset):
    start_date = datetime.strptime(start.split('T')[0], '%Y-%m-%d')
    end_date = datetime.strptime(end.split('T')[0], '%Y-%m-%d')

    if (ctx.triggered_id == 'btn-reset-event') or (evt is None):
        fat_plot = g.summary_fig(
            d.month_fatalities, 'Number of Fatalities', 'Total Numbers of Fatalities Occurred')
        evt_plot = g.summary_fig(
            d.month_events, 'Number of Events', 'Total Numbers of Events Occurred')
        geo_plot = g.geo_fig(d.df)
        return fat_plot, evt_plot, geo_plot

    filtered_df = d.filter_sub_evt_date(evt, start, end)
    fatalities_per_month = d.find_total_fatalities_per_month(filtered_df)
    events_per_month = d.find_total_events_per_month(filtered_df)

    fat_plot = g.summary_fig(
        fatalities_per_month, 'Number of Fatalities', 'Total Number of Fatalities')
    evt_plot = g.summary_fig(
        events_per_month, 'Number of Events', 'Total Number of Events')
    geo_plot = g.geo_fig(filtered_df)
    return fat_plot, evt_plot, geo_plot

# btn-reset


# ====================
# INTERACTIONS
# ====================

# sub-events graph
@ app.callback((Output('interaction_fatalities_plot', 'figure')),
               (Output('interaction_events_plot', 'figure')),
               (Output('interaction_geo_plot', 'figure')),
               (State('interaction', 'value')),
               (State('date_range_interaction', 'start_date')),
               (State('date_range_interaction', 'end_date')),
               (Input('btn-search-interaction', 'n_clicks')),
               (Input('btn-reset-interaction', 'n_clicks'))
               )
def output_subevents_graph(evt, start, end, btn_search, btn_reset):
    start_date = datetime.strptime(start.split('T')[0], '%Y-%m-%d')
    end_date = datetime.strptime(end.split('T')[0], '%Y-%m-%d')

    if (ctx.triggered_id == 'btn-reset-interaction') or (evt is None):
        fat_plot = g.summary_fig(
            d.month_fatalities, 'Number of Fatalities', 'Total Numbers of Fatalities Occurred')
        evt_plot = g.summary_fig(
            d.month_events, 'Number of Events', 'Total Numbers of Events Occurred')
        geo_plot = g.geo_fig(d.df)
        return fat_plot, evt_plot, geo_plot

    filtered_df = d.filter_interaction_date(evt, start, end)
    fatalities_per_month = d.find_total_fatalities_per_month(filtered_df)
    events_per_month = d.find_total_events_per_month(filtered_df)

    fat_plot = g.summary_fig(
        fatalities_per_month, 'Number of Fatalities', 'Total Number of Fatalities')
    evt_plot = g.summary_fig(
        events_per_month, 'Number of Events', 'Total Number of Events')
    geo_plot = g.geo_fig(filtered_df)
    return fat_plot, evt_plot, geo_plot


if __name__ == '__main__':
    app.run_server(dev_tools_hot_reload=True, debug=True)
