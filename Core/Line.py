from random import choice

from numpy import extract
from plotly.graph_objs import Scatter, Margin


def random_color():
    """
    Make a list of colors to picvk from
    :return:
    """
    colors = ["red", "green", "blue", "orange", "purple", "pink", "yellow", "black", "gray", "sliver", "violet",
              "yellowgreen", "turquoise", "sienna", "salmon"]
    color = choice(colors)
    return tuple(color)


def create_curve_line(df, virus_name, min_date, max_date):
    df_group_by_country = df.groupby(['country', 'year']).agg(['count'])['value']
    # Rename the first column in Value
    df_group_by_country.columns = ['value']
    # Move the index values (i.e. Country column) in column and reset index
    df_group_by_country = df_group_by_country.reset_index()
    country_list = df_group_by_country.country.unique()
    p_data, p_name, p_year = [], [], []

    for country_name in country_list:
        country_data = extract(df_group_by_country.country == country_name, df_group_by_country.value)
        country_year = extract(df_group_by_country.country == country_name, df_group_by_country.year)

        if country_year[0] < min_date:
            min_date = country_year[0]
        if country_year[len(country_year) - 1] > max_date:
            max_date = country_year[len(country_year) - 1]

        # Stock country name in array structure
        if len(country_name) != 0:
            p_name.append(country_name)

        # Stock country data in array structure
        if len(country_data) != 0:
            p_data.append(country_data)

        # Stock country year in array structure
        if len(country_year) != 0:
            p_year.append(country_year)

    # Add step in x axe
    step = 1
    if 5 < max_date - min_date <= 10:
        step = 2
    elif 10 < max_date - min_date <= 50:
        step = 5
    elif max_date - min_date > 50:
        step = 10
    marks_data = []
    for i in range(int(min_date), int(max_date + 1), step):
        marks_data.append(str(i))

    if i < int(max_date):
        marks_data.append(str(max_date))

    i = 0
    data = []
    for l_country in p_data:
        trace = Scatter(
            x=p_year[i],
            y=l_country,
            name=p_name[i],
            line=dict(
                color=('rgb(' + str(random_color()) + ')'),
                width=1)
        )
        i = i + 1
        data.append(trace)

    # Edit the layout
    layout = dict(title="Evolution of " + virus_name.title() + " virus <br>Between " + str(min_date) + " and " + str(
        max_date) + " by country.",
                  xaxis=dict(title='Year'),
                  yaxis=dict(title='Number of ' + virus_name.title() + " virus"),
                  legend=dict(overflowY="scroll"),
                  margin=Margin(
                      l=50,
                      r=0,
                      b=100,
                      t=100,
                      pad=0
                  ),
                  )

    fig = dict(data=data, layout=layout)
    return fig
