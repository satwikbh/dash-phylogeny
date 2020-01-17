import sys

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from pandas import read_csv

from Core.Helper import slicer, min_max_date
from Core.Line import create_curve_line
from Core.Map import create_map_bubble_year
from Core.PhyloTree import create_tree
from Core.ReadFiles import create_paths_file

# TODO: Check the recursion limit for big families such as hidelink
sys.setrecursionlimit(10**5)

app = dash.Dash(__name__)
server = app.server

virus_family_name = "scar"
tree_fig = {}
min_date, max_date = 2016, 2019

tree_file, stat_metadata_file, metadata_file = create_paths_file(virus_family_name, level1="", level2="", level3="")
df_stat_metadata = read_csv(metadata_file)

species = ["airinstaller", "browsefox", "downloadadmin", "firseria", "ibryte", "installerex", "mabezat", "parite",
           "refresh", "starter", "wapomi", "allaple", "bundlore", "eggnog", "flystudio", "iframeinject",
           "installmonster", "medfos", "patchload", "sytro", "winwebsec", "alman", "buzus", "expiro", "gamarue",
           "iframeref", "klez", "megasearch", "phish", "renos", "upatre", "xpaj", "autoit", "c99shell", "faceliker",
           "gamevance", "imali", "kykymber", "multiplug", "phishing", "sality", "virlock", "yakes", "beebone",
           "confidence", "fakejquery", "gepys", "inbox", "linkury", "mydoom", "picsys", "scar", "virut", "zbot",
           "bifrose", "cosmu", "fareit", "hidelink", "inor", "lipler", "onlinegames", "ramnit", "scrinject", "vobfus",
           "zehuddlhireroaccess", "blacole", "delf", "fbjack", "hlux", "installbrain", "loadmoney", "outbrowse",
           "redir",
           "soft32downloader", "vtflooder", "zusy", "bladabindi", "domaiq", "fearso", "hotbar", "installcore",
           "lollipop", "palevo", "redirector", "softpulse", "vundo"]


def main():
    m_data = slicer(min_date, max_date)
    mm_date_value = [min_date, max_date]
    fig = create_tree(virus_name=virus_family_name, tree_file=tree_file,
                      metadata_file=metadata_file, ord_by="country",
                      stat_metadata_file=stat_metadata_file)
    tree_fig[tree_file] = fig

    _fig_map_bubble = create_map_bubble_year(virus_family_name, metadata_file, 2, min_date, max_date)
    _fig_curve_line = create_curve_line(df_stat_metadata, virus_family_name, min_date, max_date)

    return _fig_map_bubble, _fig_curve_line, m_data, mm_date_value


fig_map_bubble, fig_curve_line, marks_data, min_max_date_value = main()


def serve_layout():
    return html.Div([
        # Banner display
        html.Div([
            html.H2(
                'Phylogeny trees and global spread of 86 viruses',
                id='title'
            ),
            html.Img(
                src="https://s3-us-west-1.amazonaws.com/plotly-tutorials/logo/new-branding/dash-logo-by-plotly-stripe-inverted.png"
            )
        ],
            className="banner"
        ),

        # Body
        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.Br(),
                                        html.Br(),
                                        html.H6(children='Dataset'),
                                        dcc.Dropdown(
                                            id='d_virus-name',
                                            options=[{'label': species[i], 'value': species[i]} for i in
                                                     range(len(species))],
                                            value='scar',
                                        ),
                                        html.Div(id='output-container'),

                                        html.Br(),
                                        html.Br(),
                                        html.H6(children='Data Range'),
                                        html.Div(id='id-slicer', children=[
                                            dcc.RangeSlider(
                                                id='id-year',
                                                min=min_date,
                                                max=max_date,
                                                step=1,
                                                marks=marks_data,
                                                value=min_max_date_value
                                            ),
                                        ]),
                                        html.Br(),
                                        html.Br(),
                                        html.Div(id='output-container-range-slider'),
                                        html.Br(),
                                        html.Br(),
                                        dcc.Graph(
                                            id='curve-line-graph',
                                            figure=fig_curve_line,
                                            style={'height': 700}
                                        ),
                                    ]),
                            ],
                            className="four columns",
                            style={'margin-top': '10'}
                        ),
                        html.Br(),
                        html.Div(
                            className="eight columns",
                            style={'margin-top': '10'},
                            children=html.Div([
                                html.Div(id='right-top-graph')
                            ])
                        )
                    ], className="row"),

                html.Div(
                    [
                        html.Div(
                            [
                                dcc.Graph(
                                    id='graph_map',
                                    figure=fig_map_bubble
                                )
                            ],
                            className='six columns',
                            style={'margin-top': '10'}
                        ),
                        html.Div(
                            [
                                html.Div(id="id-histo")
                            ],
                            className='six columns',
                            style={'margin-top': '10'}
                        ),
                    ], className="row"
                )
            ],
            className="container"
        )
    ])


app.layout = serve_layout()

"""
CALLBACKS
"""


@app.callback(
    Output('output-container', 'children'),
    [Input('d_virus-name', 'value')])
def _update_legend_gene(virus_name):
    return "You have selected '{}' virus".format(virus_name)


@app.callback(
    Output('right-top-graph', 'children'),
    [Input('d_virus-name', 'value')])
def _update_phylogentic_tree(virus_name):
    virus_name = virus_name.lower()
    ord_by_elt = "country"
    tree_file_filtered, metadata_file_filtered, metadata_file_stat_filtered = create_paths_file(virus_name, level1="",
                                                                                                level2="", level3="")
    if tree_file_filtered in tree_fig:
        fig = tree_fig[tree_file_filtered]
    else:
        fig = create_tree(virus_name=virus_name,
                          tree_file=tree_file_filtered,
                          metadata_file=metadata_file_stat_filtered,
                          ord_by=ord_by_elt,
                          stat_metadata_file=metadata_file_filtered)

        tree_fig[tree_file_filtered] = fig

    return dcc.Graph(
        id='top-graph',
        figure=fig
    )


@app.callback(
    Output('graph_map', 'figure'),
    [Input('d_virus-name', 'value'),
     Input('id-year', 'value')])
def _update_map(virus_name, id_year):
    virus_name = virus_name.lower()
    tree_file_filtered, metadata_file_filtered, metadata_file_stat_filtered = create_paths_file(virus_name, level1="",
                                                                                                level2="", level3="")

    df = read_csv(metadata_file_stat_filtered)

    min_date, max_date = id_year
    # To select only the data between min_date and max_date
    df = df[df["year"] >= min_date]
    df = df[df["year"] <= max_date]
    return create_map_bubble_year(virus_name, metadata_file_stat_filtered, 2, min_date, max_date)


@app.callback(
    Output('id-slicer', 'children'),
    [Input('d_virus-name', 'value')])
def _update_slicer(virus_name):
    virus_name = virus_name.lower()
    tree_file_filtered, metadata_file_filtered, metadata_file_stat_filtered = create_paths_file(virus_name, level1="",
                                                                                                level2="", level3="")

    df = read_csv(metadata_file_stat_filtered)
    min_date, max_date = min_max_date(df)
    # create the dictionary of slider
    marks_data = slicer(min_date, max_date)
    min_max_date_value = [min_date, max_date]

    # To select only the data between min_date and max_date
    df = df[df["year"] >= min_date]
    df = df[df["year"] <= max_date]
    return dcc.RangeSlider(
        id='id-year',
        min=min_date,
        max=max_date,
        step=1,
        marks=marks_data,
        value=min_max_date_value
    )


@app.callback(
    Output('curve-line-graph', 'figure'),
    [Input('d_virus-name', 'value'),
     Input('id-year', 'value')])
def _update_curve(virus_name, id_year):
    virus_name = virus_name.lower()
    tree_file_filtered, metadata_file_filtered, metadata_file_stat_filtered = create_paths_file(virus_name, level1="",
                                                                                                level2="", level3="")
    df = read_csv(metadata_file_stat_filtered)
    min_date, max_date = id_year

    # To select only the data between min_date and max_date
    df = df[df["year"] >= min_date]
    df = df[df["year"] <= max_date]

    return create_curve_line(df, virus_name, min_date, max_date)


@app.callback(
    Output('id-histo', 'children'),
    [Input('d_virus-name', 'value'),
     Input('id-year', 'value')])
def _update_histo(virus_name, id_year):
    virus_name = virus_name.lower()
    tree_file_filtered, metadata_file_filtered, metadata_file_stat_filtered = create_paths_file(virus_name, level1="",
                                                                                                level2="", level3="")
    df = read_csv(metadata_file_stat_filtered)
    min_date, max_date = id_year

    # To select only the data between min_date and max_date
    df = df[df["year"] >= min_date]
    df = df[df["year"] <= max_date]

    # Count the number of viruses by Country
    df_group_by_country = df.groupby(['country']).agg(['count'])['value']
    # Rename the first column in Value
    df_group_by_country.columns = ['value']
    # Move the index values (i.e. Country column) in column and reset index
    df_group_by_country = df_group_by_country.reset_index()

    return dcc.Graph(
        id='right-bottom-histo',
        figure={
            'data': [{
                'x': df_group_by_country['country'],
                'y': df_group_by_country['value'],
                'type': 'bar'
            }],
            'layout': {
                'paper_bgcolor': 'rgba(0,0,0,0)',
                'plot_bgcolor': 'rgba(0,0,0,0)',
                'autosize': True,
                'margin': '0px 0px 0px 0px',
                'title': '<br>Distribution of {} <br>Between {} and {}'.format(virus_name.title(), min_date, max_date)
            }
        }
    )


"""
######################################### CSS #########################################
"""
external_css = [
    "https://cdnjs.cloudflare.com/ajax/libs/normalize/7.0.0/normalize.min.css",  # Normalize the CSS
    "https://fonts.googleapis.com/css?family=Open+Sans|Roboto"  # Fonts
    "https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css",
    "https://cdn.rawgit.com/TahiriNadia/styles/faf8c1c3/stylesheet.css",
    "https://cdn.rawgit.com/TahiriNadia/styles/b1026938/custum-styles_phyloapp.css"
]

for css in external_css:
    app.css.append_css({"external_url": css})

# Running the server
if __name__ == '__main__':
    app.run_server(debug=True, port=8053)
