from dash import dcc, html, dash_table
import data_process as d
import plotly.express as px
import graphs as g
# Application HTMLs/Layouts

header = html.Div(children=[
    html.H1(['ACLED Myanmar'],  className='header-title'),
    html.H3(
        [f'From {d.min_date.strftime("%d-%m-%Y")} to {d.max_date.strftime("%d-%m-%Y")}'])
])


####################################
## SUMMARY #########################
####################################
summary = html.Div([
    html.Div([
        html.Div([
            html.H2(f'{d.total_fatalities}'),
            html.H5('Fatalities')
        ], className='show-numbers'),
        html.Div([
            html.H2(f'{d.total_events}'),
            html.H5('Events')
        ], className='show-numbers'),
    ], className='number-container'),
    # Graphs
    html.Div([
        dcc.Graph(figure=g.summary_fig(
            d.month_fatalities, 'Number of Fatalities', 'Total Numbers of Fatalities Occurred')),
        dcc.Graph(figure=g.summary_fig(
            d.month_events, 'Number of Events', 'Total Numbers of Events Occurred')),
    ], className='graph-container'),

    # Tables
    html.H2('Number of Events and Fatalities According to Events'),
    dash_table.DataTable(data=d.sub_evts_dict,
                         columns=d.sub_evts_cols,
                         style_cell_conditional=[{
                             'if': {'column_id': 'Events'},
                             'textAlign': 'left',
                             'font-weight': 'normal',
                             'color': '#444'
                         }, {
                             'if': {'column_id': 'Sub Events'},
                             'textAlign': 'left',
                             'font-weight': 'normal',
                             'color': '#444',
                         }],
                         #  style_as_list_view=True,
                         style_table={'overflowX': 'auto'},
                         style_cell={'padding': '5px',
                                     'font-weight': 'bold',
                                     'color': 'red'},
                         style_header={
                             'backgroundColor': '#222',
                             'fontWeight': 'bold',
                             'color': '#fff'
                         },
                         style_data={'height': 'auto', 'whiteSpace': 'normal'},
                         style_data_conditional=[{
                             'if': {'row_index': 'odd'},
                             'backgroundColor': 'rgb(220, 220, 220)',
                         }],
                         sort_action="native",
                         page_size=10,
                         ),

    html.H2('Number of Events and Fatalities According to Locations'),
    dash_table.DataTable(data=d.location_dict,
                         columns=d.location_cols,
                         style_table={'overflowX': 'auto'},
                         style_cell_conditional=[{
                             'if': {'column_id': 'State/Division'},
                             'textAlign': 'left',
                             'font-weight': 'normal',
                             'color': '#444',
                         }, {
                             'if': {'column_id': 'Township'},
                             'textAlign': 'left',
                             'font-weight': 'noraml',
                             'color': '#444',
                         }],
                         #  style_as_list_view=True,
                         style_data={'height': 'auto', 'whiteSpace': 'normal'},
                         style_cell={'padding': '5px',
                                     'font-weight': 'bold', 'color': 'red'},
                         style_header={
                             'backgroundColor': '#222',
                             'fontWeight': 'bold',
                             'color': '#fff'
                         },
                         style_data_conditional=[{
                             'if': {'row_index': 'odd'},
                             'backgroundColor': 'rgb(220, 220, 220)',
                         }],
                         sort_action="native",
                         sort_mode='multi',
                         page_size=10,


                         ),

    html.H2('Number of Events and Fatalities According to Interactions'),
    dash_table.DataTable(data=d.interaction_dict,
                         columns=d.interaction_cols,
                         style_table={'overflowX': 'auto'},
                         style_cell_conditional=[{
                             'if': {'column_id': 'Interaction'},
                             'textAlign': 'left',
                             'font-weight': 'normal',
                             'color': '#444',
                         }],
                         #  style_as_list_view=True,
                         style_cell={'padding': '5px',
                                     'font-weight': 'bold', 'color': 'red'},
                         style_header={
                             'backgroundColor': '#222',
                             'fontWeight': 'bold',
                             'color': '#fff'
                         },
                         style_data_conditional=[{
                             'if': {'row_index': 'odd'},
                             'backgroundColor': 'rgb(220, 220, 220)',
                         }],
                         sort_action="native",
                         page_size=10,
                         ),

], className='summary')

####################################
## EVENTS ##########################
####################################
# aside
events_aside = html.Aside(
    [html.Div([
        html.H2('Filter'),

        # Event type
        html.Label('Event Type'),
        dcc.Dropdown(id='event', options=[{'label': event, 'value': event}
                     for event in d.df['event_type'].unique()],
                     ),

        # Date Range
        html.Label('Date'),
        dcc.DatePickerRange(
            id='date_range_event',
            start_date=d.min_date,
            end_date=d.max_date,
            min_date_allowed=d.min_date,
            max_date_allowed=d.max_date,
        ),

        # Buttons
        html.Div([
            html.Button('Search', id='btn-search-event',
                        n_clicks=0, className='btn-search'),
            html.Button('Reset', id='btn-reset-event',
                        n_clicks=0, className='btn-reset')
        ], className='input-btns')

    ], className='input-group')], className='aside')

events_mainContainer = html.Div([
    dcc.Graph(id='events_fatalities_plot'),
    dcc.Graph(id='events_events_plot'),
    dcc.Graph(id='events_geo_plot')
], className='main', id='main')


####################################
## Interactions ####################
####################################
# aside
interaction_aside = html.Aside(
    [html.Div([
        html.H2('Filter'),

        # Event type
        html.Label('Interaction Type'),
        dcc.Dropdown(id='interaction', options=[{'label': d.interaction_lookup[act], 'value': act}
                     for act in d.df['interaction'].unique()],
                     ),


        # Date Range
        html.Label('Date'),
        dcc.DatePickerRange(
            id='date_range_interaction',
            start_date=d.min_date,
            end_date=d.max_date,
            min_date_allowed=d.min_date,
            max_date_allowed=d.max_date,
        ),

        # Buttons
        html.Div([
            html.Button('Search', id='btn-search-interaction',
                        n_clicks=0, className='btn-search'),
            html.Button('Reset', id='btn-reset-interaction',
                        n_clicks=0, className='btn-reset')
        ], className='input-btns')

    ], className='input-group')], className='aside')

interaction_mainContainer = html.Div([
    dcc.Graph(id='interaction_fatalities_plot'),
    dcc.Graph(id='interaction_events_plot'),
    dcc.Graph(id='interaction_geo_plot')
], className='main')


####################################
## About ###########################
####################################
about = html.Div([
    html.Ul([
        html.Li('ACLED data selected for Myanmar'),
        html.Li(f'Start from {d.min_date} to {d.max_date}'),
        html.Li('Not mobile responsive yet!'),
        html.Li('Development in Progress')
    ], style={'max-width': '80%', 'margin': '40px auto', 'font-weight': 'bold'})
])
