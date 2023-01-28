import plotly.express as px
# import data_process as d

# SUMMARY


def summary_fig(data, ylabel, title):
    fig = px.bar(data, title=title, labels={
                 'event_date': '', 'value': ylabel},)
    fig.update_layout(legend=dict(title_text='Events'))
    fig.update_xaxes(dtick='M1')
    return fig


# def total_fatalities_with_subplots(data):
#     fig = px.bar(data_frame=data, x='event_date',
#                  y='fatalities', facet_row='sub_event_type', height=800, color_discrete_map='red')
#     fig.for_each_annotation(lambda a: a.update(text=a.text.split('=')[1]))
#     fig.update_yaxes(matches=None)
#     fig.update_xaxes(dtick='M1')
#     return fig

def geo_fig(data):
    data = data.reset_index()
    fig = px.scatter_mapbox(data_frame=data, lat='latitude', lon='longitude', color='sub_event_type',
                            hover_data=['admin3', 'location', 'actor1',
                                        'actor2', 'fatalities', 'event_date'],
                            zoom=5, height=800, color_continuous_scale=px.colors.sequential.algae,
                            size=data['fatalities'] + 1,
                            opacity=0.5
                            )

    # carto-positron, carto-darkmatter, stamen-terrain
    # stemen-toner, stemen-watercolor, open-street-map
    fig.update_layout(mapbox_style="carto-positron")
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return fig
