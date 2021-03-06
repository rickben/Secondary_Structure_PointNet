# -*- coding: utf-8 -*-
"""
Created on Fri Sep 18 17:37:08 2020

@author: Ofek Mula
"""
import argparse
import numpy as np
import matplotlib.pyplot as plt
import os


"""
this file is for plotting the histogram of secondary structure inside the protein database.
depends on your choose of the model in the the command line arguments, 
it plots the histogram of secondary structure in division of 8 or 3 classes 
"""
new_label_dictionary = {
    0: 0, 1: 0, 2: 0,  # helix
    3: 1, 4: 1,  # sheet
    5: 2, 6: 2, 7: 2  # coil
}

parser = argparse.ArgumentParser()
parser.add_argument('--pointNet_model', type=int, default=0,
                    help='choose model for visu log[0= LocalPointnet,1= PointNet3 ,2=Pointnet8, deafult=0]')
FLAGS = parser.parse_args()

MODEL = FLAGS.pointNet_model
model_dic = {0: 'LocalPointNet3',
             1: 'PointNet3',
             2: 'PointNet8'}

if MODEL < 0 or MODEL > 2:
    MODEL = 0
if MODEL == 2:
    NUM_CLASSES = 8
else:
    NUM_CLASSES = 3


def residues_histogram(proteins_array):
    if NUM_CLASSES == 3:
        histogram = [0, 0, 0]
    else:
        histogram = [0, 0, 0, 0, 0, 0, 0, 0]
    for protein in proteins_array:
        for residue_label in protein:
            histogram[int(residue_label)] += 1
    return histogram


def plot_histogram(histogram):
    fig = plt.figure()
    ax = fig.add_axes([0, 0, 1, 1])
    if NUM_CLASSES == 3:
        langs = ['helix', 'sheet', 'coil']  # for 3 classes
    else:
        langs = ['H', 'I', 'G', 'B', 'E', 'S', 'T', '-']  # for 8 classes
    students = histogram
    ax.bar(langs, students)
    ax.set_ylabel('quantity')
    ax.set_xlabel('secondary structure')
    plt.show()
    return


def traverse_db():
    data_batch_list = []
    label_batch_list = []
    protein_info_dir = "./" + model_dic[MODEL] + "/Proteins_Info"
    print(protein_info_dir)
    for subdir_info, dirs_info, files_info in os.walk(protein_info_dir):
        for protein_dir in dirs_info:
            dir_name = os.path.join(subdir_info, protein_dir)
            for subdir, dirs, files in os.walk(dir_name):
                for protein_files in files:
                    protein_name_npy = os.path.join(subdir, protein_files)
                    if ("label" in protein_name_npy):
                        label_batch = np.load(protein_name_npy)
                        for i, label in enumerate(label_batch):
                            if NUM_CLASSES == 3:
                                label_batch[i] = new_label_dictionary[label]  # for 3 classes
                            else:
                                label_batch[i] = label_batch[i]  # for 8 classes
                if (label_batch.shape[0] > 0):
                    label_batch_list.append(label_batch)

    label_batches = np.array(label_batch_list)
    plot_histogram((residues_histogram(label_batches)))


if __name__ == "__main__":
    traverse_db()