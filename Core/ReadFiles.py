from Bio import Phylo
from pandas import read_csv


def read_treefile(filename):
    tree = Phylo.read(filename, "newick")
    return tree


def read_metadata(filename):
    df = read_csv(filename)
    return df


def create_paths_file(virus_name, level1="", level2="", level3=""):
    dir = "data/VirusShare/" + virus_name + "/"
    if level1 == "" and level2 == "" and level3 == "":
        tree_file = dir + "nextstrain_" + virus_name + "_tree.new"
        metadata_file = dir + "nextstrain_" + virus_name + "_metadata.csv"
        stat_file = dir + "stat_year_nextstrain_" + virus_name + "_metadata.csv"
        return tree_file, metadata_file, stat_file
    elif level2 == "" and level3 == "":
        dir = dir + "/" + level1 + "/"
        tree_file = dir + "nextstrain_" + virus_name + "_" + level1 + "_tree.new"
        metadata_file = dir + "nextstrain_" + virus_name + "_" + level1 + "_metadata.csv"
        stat_file = dir + "stat_year_nextstrain_" + virus_name + "_" + level1 + "_metadata.csv"
        return tree_file, metadata_file, stat_file
    elif level3 == "":
        dir = dir + "/" + level1 + "/" + level2 + "/"
        tree_file = dir + "nextstrain_" + virus_name + "_" + level1 + "_" + level2 + "_tree.new"
        metadata_file = dir + "nextstrain_" + virus_name + "_" + level1 + "_" + level2 + "_metadata.csv"
        stat_file = dir + "stat_year_nextstrain_" + virus_name + "_" + level1 + "_" + level2 + "_metadata.csv"
        return tree_file, metadata_file, stat_file
    else:
        dir = dir + "/" + level1 + "/" + level2 + "/" + level3 + "/"
        tree_file = dir + "nextstrain_" + virus_name + "_" + level1 + "_" + level2 + "_" + level3 + "_tree.new"
        metadata_file = dir + "nextstrain_" + virus_name + "_" + level1 + "_" + level2 + "_" + level3 + "_metadata.csv"
        stat_file = dir + "stat_year_nextstrain_" + virus_name + "_" + level1 + "_" + level2 + "_" + level3 + "_metadata.csv"
        return tree_file, metadata_file, stat_file
