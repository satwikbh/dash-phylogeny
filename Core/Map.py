from collections import Counter

from pandas import read_csv
from plotly.graph_objs import Margin


def create_map_bubble_year(virus_name, metadata_file_stat, map_choice, min_date, max_date):
    df = read_csv(metadata_file_stat)
    # To select only the data between min_date and max_date
    df = df[df["year"] >= min_date]
    df = df[df["year"] <= max_date]
    # min_date, max_date = min_max_date(df)
    df.head()

    cases = []
    colors = ['rgb(231,229,204)', 'rgb(255,255,204)', 'rgb(255,178,102)', 'rgb(255,153,51)',
              'rgb(204,0,0)', 'rgb(189,215,231)', 'rgb(107,174,214)', 'rgb(33,113,181)',
              'rgb(255,102,255)', 'rgb(189,15,255)', 'rgb(121,74,244)', 'rgb(133,13,181)',
              'rgb(239,243,255)', 'rgb(189,215,231)', 'rgb(107,174,214)', 'rgb(33,113,181)']
    months = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug', 9: 'Sept', 10: 'Oct',
              11: 'Nov', 12: 'Dec'}

    if map_choice == 2:
        df_old = df
        counter = Counter(df_old["country"])
        df = read_csv('data/country_codes_iso_3.csv')
        for country, count in counter.items():
            df.loc[df["COUNTRY"] == country, "OCCURRENCE"] += count

        data = [dict(
            type='choropleth',
            locations=df['CODE'],
            z=df['OCCURRENCE'],
            text=df['COUNTRY'],
            colorscale=[
                # Let first 10% (0.1) of the values have color rgb(0, 0, 0)
                [0, "rgb(0, 0, 0)"],
                [0.1, "rgb(0, 0, 0)"],

                # Let values between 10-20% of the min and max of z
                # have color rgb(20, 20, 20)
                [0.1, "rgb(20, 20, 20)"],
                [0.2, "rgb(20, 20, 20)"],

                # Values between 20-30% of the min and max of z
                # have color rgb(40, 40, 40)
                [0.2, "rgb(40, 40, 40)"],
                [0.3, "rgb(40, 40, 40)"],

                [0.3, "rgb(60, 60, 60)"],
                [0.4, "rgb(60, 60, 60)"],

                [0.4, "rgb(80, 80, 80)"],
                [0.5, "rgb(80, 80, 80)"],

                [0.5, "rgb(100, 100, 100)"],
                [0.6, "rgb(100, 100, 100)"],

                [0.6, "rgb(120, 120, 120)"],
                [0.7, "rgb(120, 120, 120)"],

                [0.7, "rgb(140, 140, 140)"],
                [0.8, "rgb(140, 140, 140)"],

                [0.8, "rgb(160, 160, 160)"],
                [0.9, "rgb(160, 160, 160)"],

                [0.9, "rgb(180, 180, 180)"],
                [1.0, "rgb(180, 180, 180)"]
            ],
            autocolorscale=False,
            reversescale=True,
            marker=dict(
                line=dict(
                    color='rgb(180,180,180)',
                    width=0.5
                )),
            colorbar=dict(
                autotick=False,
                titleside="right",
                title='Number of ' + virus_name.title() + ' Virus'),
        )]

        layout = dict(
            title=virus_name.title() + ' Virus cases in the world <br>Between ' + str(min_date) + " and " + str(
                max_date),
            margin=Margin(
                l=0,
                r=0,
                b=0,
                t=35,
                pad=0
            ),
            geo=dict(
                showframe=False,
                showcoastlines=False,
                projection=dict(
                    type='Mercator'
                )
            ),
            autosize=True
        )

        fig = dict(data=data, layout=layout)
        return fig
