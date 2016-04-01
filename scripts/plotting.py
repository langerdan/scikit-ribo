#!/usr/bin/env python

## ----------------------------------------
## scikit-ribo
## ----------------------------------------
## a module for preprocessing bam files
## ----------------------------------------
## author: Han Fang
## contact: hanfang.cshl@gmail.com
## website: hanfang.github.io
## date: 1/28/2016
## ----------------------------------------

from __future__ import print_function, division
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import sys
import pandas as pd
import seaborn as sns
import numpy as np
import pybedtools as pbt
import argparse


class Figures:
    ''' define a class for plotting figures
    '''
    def __init__(self, df_fn, gene_name):
        self.df_fn = df_fn
        self.gene_name = gene_name

    def plot_coverage_on_transcript(self):
        ## YLR110C
        self.ribo_df = pd.read_table(self.df_fn,  header=0)
        ribo_array = np.array(self.ribo_df[self.ribo_df["gene_name"] == self.gene_name]["ribosome_count"])
        pair_prob_array = np.array(self.ribo_df[self.ribo_df["gene_name"] == self.gene_name]["pair_prob"])
        if self.ribo_df[self.ribo_df["gene_name"] == self.gene_name]["gene_strand"].values[0] == "-":
            ribo_array = ribo_array[::-1]
            pair_prob_array = pair_prob_array[::-1]

        ## plot the ribosome count along a transcript
        plt.figure()
        plt.subplot(2, 1, 1)
        plt.title( self.gene_name )
        plt.plot( ribo_array, sns.xkcd_rgb["denim blue"], lw = 2)
        plt.axvline(0, color="#999999",dashes=[3,2],zorder=-1)
        plt.axvline(ribo_array.size ,color="#999999",dashes=[3,2],zorder=-1)
        plt.ylabel("Ribosome counts")
        plt.subplot(2, 1, 2)
        plt.plot( pair_prob_array, sns.xkcd_rgb["medium green"])        
        plt.ylabel("Pairing probability")
        plt.xlabel("Position in transcript (5' to 3')")
        plt.axvline(0, color="#999999",dashes=[3,2],zorder=-1)
        plt.axvline(ribo_array.size ,color="#999999",dashes=[3,2],zorder=-1)
        plt.gcf()
        plt.savefig( self.gene_name + "_ribosome_count.pdf")


## ----------------------------------------
## the main work
## ----------------------------------------
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", help="input data frame, required")
    parser.add_argument("-g", help="gene name of interest, required")

    ## check if there is any argument
    if len(sys.argv) <= 1:
        parser.print_usage()
        sys.exit(1)
    else:
        args = parser.parse_args()

    ## process the file if the input files exist
    if (args.i != None and args.g != None):
        print("[status]\tprocessing the input file: " + args.i, flush=True)
        df_fn = args.i
        gene_name = args.g

        print("[execute]\tplotting ribosome coverage along transcript" + str(gene_name), flush=True)
        figures_hdl = Figures(df_fn, gene_name)
        figures_hdl.plot_coverage_on_transcript()

        ## end
        print("[status]\tPlotting module finished.", flush=True)

    else:
        print("[error]\tmissing argument", flush=True)
        parser.print_usage()
