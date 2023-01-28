import pandas as pd
import pathlib

PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath('data').resolve()

df = pd.read_csv(DATA_PATH.joinpath('acled_1.2.2021.csv'))
df = df[['event_date', 'time_precision', 'event_type', 'sub_event_type',
         'actor1', 'assoc_actor_1', 'actor2', 'assoc_actor_2', 'interaction',
         'admin1', 'admin2', 'admin3', 'location', 'latitude', 'longitude',
         'geo_precision', 'source', 'notes', 'fatalities']]
df['event_date'] = pd.to_datetime(df['event_date'])
df['time_precision'] = pd.Categorical(df['time_precision'])
df['geo_precision'] = pd.Categorical(df['geo_precision'])
df['interaction'] = df['interaction'].astype(str)
df = df.set_index(['event_date'])


max_date = max(df.index)
min_date = min(df.index)

total_events = df.shape[0]
total_fatalities = sum(df['fatalities'])

# For Graph (Group By Months and pivot the events)
month_events = df.groupby('event_type')\
    .resample('M')['fatalities']\
    .count()\
    .reset_index()\
    .pivot(index='event_date', columns='event_type', values='fatalities')

month_fatalities = df.groupby('event_type')\
    .resample('M')['fatalities']\
    .sum()\
    .reset_index()\
    .pivot(index='event_date', columns='event_type', values='fatalities')
#

# Total Numbers of Fatalities Groupby event_type
sub_evts = df.groupby(['event_type', 'sub_event_type'])['fatalities']\
    .agg([sum, 'size'])\
    .reset_index()\
    .rename(columns={
        'sum': 'Total Fatalities', 'size': 'Number of Events',
        'event_type': 'Events', 'sub_event_type': 'Sub Events'
    })\
    .sort_values(
    by='Total Fatalities', ascending=False)

sub_evts_dict = sub_evts.to_dict('records')
sub_evts_cols = [{'id': c, 'name': c} for c in sub_evts.columns]

# Total Numbers of Fatalities Groupby location
location = df.groupby(['admin1', 'admin2'])['fatalities']\
    .agg([sum, 'size']).reset_index()\
    .rename(columns={'admin1': 'State/Division', 'admin2': 'Township',
                     'sum': 'Total Fatalities', 'size': 'Total Events'})\
    .sort_values(by='Total Fatalities', ascending=False)
location_dict = location.to_dict('records')
location_cols = [{'id': c, 'name': c} for c in location.columns]


# Total Numbers of Fatalities Groupby Interaction
interaction_lookup = {
    '10': 'Sole Military Action',
    '11': 'Military Vs Military',
    '12': 'Military Vs EAOs',
    '13': 'Military Vs Political Militia',
    '14': 'Military Vs Communal Militia',
    '15': 'Military Vs Rioters',
    '16': 'Military Vs Protesters',
    '17': 'Military Vs Civilians',
    '18': 'Military Vs Other',
    '20': 'Sole Rebel Action',
    '22': 'EAOs Vs EAOs',
    '23': 'EAOs Vs Political Militia',
    '24': 'EAOs Vs Communal Militia',
    '27': 'EAOs Vs Civilians',
    '30': 'Sole Political Militia Action',
    '33': 'Political Militia Vs Political Militia',
    '36': 'Political Militia Vs Protesters',
    '37': 'Political Militia Vs Civilians',
    '38': 'Political Militia Vs Other',
    '45': 'Communal Militia Vs Rioters',
    '47': 'Communal Militia Vs Civilians',
    '50': 'Sole Rioter Action',
    '55': 'Rioters Vs Rioters',
    '56': 'Rioters Vs Protesters',
    '57': 'Rioters Vs Civilians',
    '60': 'Sole Protester Action',
    '66': 'Protesters Vs Protesters',
    '68': 'Protesters Vs Other',
    '70': 'Civilians Displacement and Others'
}

interaction = df.groupby(['interaction'])['fatalities'].agg(
    [sum, 'size']).reset_index()

interaction = interaction.replace(interaction_lookup).rename(columns={
    'interaction': 'Interaction', 'sum': 'Total Fatalities',
    'size': 'Total Events'
}).sort_values(by='Total Fatalities', ascending=False)

interaction_dict = interaction.to_dict('records')
interaction_cols = [{'id': c, 'name': c} for c in interaction.columns]


def find_sub_events(evt):
    return df[df['event_type'] == evt]['sub_event_type'].unique()


######### Events ############
def filter_sub_evt_date(evt,  start, end):
    return df[(df['event_type'] == evt) &
              (df.index > start) &
              (df.index < end)]


# Interactions
def filter_interaction_date(act, start, end):
    return df[(df['interaction'] == act) &
              (df.index > start) &
              (df.index < end)]


def find_total_fatalities_per_month(data):
    return data.groupby('sub_event_type')\
        .resample('M')['fatalities'].sum()\
        .reset_index()\
        .pivot(index='event_date', columns='sub_event_type', values='fatalities')


def find_total_events_per_month(data):
    return data.groupby('sub_event_type')\
        .resample('M')['fatalities'].count()\
        .reset_index()\
        .pivot(index='event_date', columns='sub_event_type', values='fatalities')
