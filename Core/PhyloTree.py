from Core.Helper import get_countries
from Core.ReadFiles import read_treefile, read_metadata
from Core.temp import get_x_coordinates, get_y_coordinates, draw_clade


def create_title(virus):
    graph_title = "Phylogeny of " + virus.title() + " Virus<br>" + "colored according to region and country"
    return graph_title


def create_tree(virus_name, tree_file, metadata_file, ord_by, stat_metadata_file):
    tree = read_treefile(tree_file)
    x_co_ordinates = get_x_coordinates(tree)
    y_co_ordinates = get_y_coordinates(tree)
    line_shapes = []
    draw_clade(tree.root, 0, line_shapes, line_color='rgb(25,25,25)', line_width=1, x_coords=x_co_ordinates,
               y_coords=y_co_ordinates)
    my_tree_clades = x_co_ordinates.keys()
    x_variable = []
    y_variable = []
    text = []

    for cl in my_tree_clades:
        x_variable.append(x_co_ordinates[cl])
        y_variable.append(y_co_ordinates[cl])
        text.append(cl.name)

    metadata_df = read_metadata(stat_metadata_file)
    stat_metadata_df = read_metadata(metadata_file)

    graph_title = create_title(virus_name)
    intermediate_node_color = 'rgb(100,100,100)'

    country_color_code_dict = get_countries(
        non_occurring_countries=["British Virgin Islands", "United States", "France"])

    color = [intermediate_node_color] * len(x_variable)

    for k, vs_name in enumerate(text):
        try:
            if vs_name not in ["None", None]:
                row = metadata_df[metadata_df['name'] == vs_name]
                permalink = row["permalink"].tolist()[0]
                virus_total_link = split_at_n_character(permalink, 50)
                positives = row["positives"].tolist()[0]
                total_detections = row["total"].tolist()[0]
                percentage = str(int((positives / total_detections) * 100))
                md5 = row["md5"].tolist()[0]
                scan_date = row["scan_date"].tolist()[0]
                sha1 = row["sha1"].tolist()[0]
                sha256 = row["sha256"].tolist()[0]
                text[k] = text[k] + '<br>MD5: ' + '{:s}'.format(md5) + '<br>SHA1: ' + '{:s}'.format(
                    sha1) + '<br>SHA256: ' + '{:s}'.format(sha256) + '<br>Seen Date: ' + '{:s}'.format(
                    scan_date) + '<br>Detection Rate: ' + '{:s}'.format(percentage) + '<br>Permalink: ' + '{:s}'.format(
                    virus_total_link)
            else:
                text[k] = '<br>NODE_000: ' + '{:s}'.format(str(k))
        except Exception as e:
            print(e)
            # print(vs_name, vs_name in metadata_df["name"].tolist())

    # for k, vs_name in enumerate(metadata_df['name']):
    #     virus_total_link = split_at_n_character(metadata_df.loc[k, 'permalink'], 50)
    #     positives = metadata_df.loc[k, 'positives']
    #     total_detections = metadata_df.loc[k, 'total']
    #     percentage = str(int((positives / total_detections) * 100))
    #
    #     if vs_name in text:
    #         counter = text.index(vs_name)
    #         text[counter] = text[counter] + '<br>MD5: ' + '{:s}'.format(
    #             metadata_df.loc[k, 'md5']) + '<br>SHA1: ' + '{:s}'.format(
    #             metadata_df.loc[k, 'sha1']) + '<br>SHA256: ' + '{:s}'.format(
    #             metadata_df.loc[k, 'sha256']) + '<br>Seen Date: ' + '{:s}'.format(
    #             metadata_df.loc[k, 'scan_date']) + '<br>Detection Rate: ' + '{:s}'.format(
    #             percentage) + '<br>Permalink: ' + '{:s}'.format(virus_total_link)
    #     else:
    #         counter = text.index(None)
    #         text[counter] = '<br>NODE_000: ' + '{:s}'.format(counter)

    axis = dict(showline=False,
                zeroline=False,
                showgrid=False,
                showticklabels=False,
                title=''  # y title
                )

    label_legend = set(list(stat_metadata_df[ord_by]))
    nodes = []

    for elt in label_legend:
        node = dict(type='scatter',
                    x=x_variable,
                    y=y_variable,
                    mode='markers',
                    marker=dict(color=color,
                                size=5),
                    text=text,  # vignet information of each node
                    hoverinfo='',
                    name=elt
                    )
        nodes.append(node)

    layout = dict(title=graph_title,
                  paper_bgcolor='rgba(0,0,0,0)',
                  dragmode="select",
                  font=dict(family='Balto', size=14),
                  height=1000,
                  autosize=True,
                  showlegend=True,
                  xaxis=dict(showline=True,
                             zeroline=False,
                             showgrid=True,  # To visualize the vertical lines
                             ticklen=4,
                             showticklabels=True,
                             title='branch length'),
                  yaxis=axis,
                  hovermode='closest',
                  shapes=line_shapes,
                  plot_bgcolor='rgb(250,250,250)',
                  legend={'x': 0, 'y': 1},
                  )

    fig = dict(data=nodes, layout=layout)
    return fig


def split_at_n_character(title, n):
    """
    Split Virus Total link if gt 50 characters
    :param title:
    :param n:
    :return:
    """
    sentences = "<br>".join([title[i:i + n] for i in range(0, len(title), n)])
    return sentences
