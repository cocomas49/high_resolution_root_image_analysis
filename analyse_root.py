#Corentin Maslard maslard.corentin@gmail.com
#Le but est de faire des mesures sur les racines segmenté
    # creation convex_hull (air, perimetre,centroïde)
    # largeur, profondeur,
        #dans un future gespère proche, mesure de la longueur total des racines

#Package

#specifique pour le convexhull
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from skimage import data, filters, color, morphology,io,util, img_as_float, img_as_ubyte, img_as_float32
from skimage.color import rgb2gray, convert_colorspace, label2rgb
from skimage.draw import circle
from skimage.filters import threshold_otsu
from skimage.io import imread, imsave
from skimage.measure import label, perimeter,regionprops, find_contours
from skimage.morphology import convex_hull_object, closing,square
from skimage.transform import rescale, resize, downscale_local_mean
from skimage.util import invert

import time
import numpy as np
import os
import math
from PIL import Image,ImageDraw
import time
import pandas as pd
import sys

start_time = time.time()

##### imput user
path_to_target=input('Name of the folder to analyze : ')
num_cut=int(input('The rac number of cut of one image (4 or 8) : '))

assembly_type=input("'Simple Segmentation' or 'Probabilities' :" )
if assembly_type == 'Simple Segmentation' or assembly_type == 'Probabilities':
    print("Cool, bon choix")
else:
    print('assembly_type error, tap Simple_Segmentation or Probabilities')
    sys.exit()

# a enlever une fois le script finit
#path_to_target='C:/Users/masla/OneDrive/Document/2.Cours, apprentissage/Dijon travail/annalyse/py/img_analyse/test'
#assembly_type='Simple Segmentation'
#num_cut=4

#begin of the script
num_cut_folder=["cut_img_",str(num_cut)]
num_cut_folder="".join(num_cut_folder)

name_folder=["A","D"]

fusion_dir = ['fusion_', assembly_type,'_',str(num_cut)] #normalement lui il doit deja etre cree
fusion_dir="".join(fusion_dir) ; #print(fusion_dir)
taskids = os.listdir(path_to_target) #touts les dossiers chiffre

#juste pour rajouter l'enderscor
if assembly_type=="Simple Segmentation":
    assembly_type2="Simple_Segmentation"
#650_GEAP218_U4_5184_SOY9_WW_S_#3_650_20201019-171705_Simple_Segmentation_compil_4_A.png

#nom du dossier a cree

#print(verif)

start_time = time.time()

#dans un premiers temps je convertie toute les images en gris (car avex skimage ça ne fonctionne pas, teste avec PIL)


for taskid in taskids:
    print("taskid : ",taskid)
    taskid_dir = os.path.join(path_to_target, taskid)

    if taskid.isnumeric() and os.path.isdir(taskid_dir):
        fusion_dir2=os.path.join(taskid_dir,fusion_dir)
        output_folder = os.path.join(taskid_dir,fusion_dir,"convex_hull")
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        if os.path.isdir(fusion_dir2):
            Label=[]
            compile_name = []
            num_label=[]
            perimeter=[]
            area=[]
            profondeur=[]
            largeur=[]
            for folder in name_folder: #si A ou D
                folder_path = os.path.join(fusion_dir2,folder)
                print(folder_path)
                files = os.listdir(folder_path)
                files.sort()  # ascending order

                for file in files:
                    start_time_file = time.time()
                    #si un dossier nomer convex_hull n'est pas crée le crée

                    verif = ["_", assembly_type2, "_compil_", str(num_cut), "_", folder, ".png"]
                    verif = "".join(verif)
                    print(file)
                    print(verif)
                    if file.endswith(verif):
                        file_path=os.path.join(folder_path, file)
                        # debut de la lecture de l'image
                        print("lecture_img")
                        read_img=io.imread(file_path)
                        # ajouter le 2/2/2021
                        read_img=img_as_float32(read_img) # float32 = [0:1] precision 32 bits
                        ndims = read_img.shape  # original dimensions
                        if ndims[2] == 4:  # alpha present
                            read_img = color.rgba2rgb(read_img)
                        read_img = np.uint8(read_img * 255)

                        print("transformation_gris") # Lecture et creation d'un tableau numpy

                        img_gray = rgb2gray(read_img)
                        image_rescaled = rescale(img_gray, 0.25,
                                                 anti_aliasing=False)  # ne pas oublier la conversion a la fin. avec 0,25 je passe de 12000 à 3000 (et c'est vachement plus rapide !!!)
                        print("resize")
                        thresh = threshold_otsu(image_rescaled)
                        bin = image_rescaled > thresh ;print("treshold") #image binomial

                        bin = invert(bin) #inversion des couleurs

                        print('morphology_closing')

                        image_rescaled2 = morphology.binary_closing(bin, morphology.disk(18)).astype(
                            np.int)  # plus cette valeur est élever plus la conexion entre les racines est fortes mais plus le convexul est grossier et plus ça mets de temps.

                        print("convex_hull")
                        chull = convex_hull_object(image_rescaled2)

                        name_file1=[file[:-4],"_convex_hull.png"]
                        name_file1="".join(name_file1)
                        print(output_folder)
                        print(os.path.join(output_folder,name_file1))

                        imsave(os.path.join(output_folder,name_file1), invert(img_as_ubyte(chull)))

                        print("analyser convex_hull")
                        label_image=label(chull)
                        image_label_overlay = label2rgb(label_image, image=chull, bg_label=0)

                        #surement a enlever
                        fig, axes = plt.subplots(1, 2, figsize=(8, 4))
                        ax = axes.ravel()
                        ax[1].imshow(image_label_overlay)

                        for region in regionprops(label_image):
                            # take regions with large enough areas
                            if region.area >= 100000:
                                # draw rectangle around segmented coins
                                minr, minc, maxr, maxc = region.bbox
                                rect = mpatches.Rectangle((minc, minr), maxc - minc, maxr - minr, fill=False,
                                                          edgecolor='red', linewidth=2)
                                circle = mpatches.Circle((region.centroid), 25)
                                ax[1].add_patch(circle)
                                ax[1].add_patch(rect)
                                print(region.label)
                                print(region.perimeter)
                                print(region.area)
                                print(maxr - minr)
                                print(maxc - minc)
                                print(region.centroid)

                                # creation des donnees
                                Label.append(file[:-4])
                                num_label.append(str(region.label))
                                perimeter.append(str(region.perimeter))
                                area.append(region.area)
                                profondeur.append(maxr - minr)
                                largeur.append(maxc - minc)

                        # a enlever, juste pour l'observation ----
                        ax[1].set_title('Convex_hull')
                        ax[1].set_axis_off()

                        ax[0].set_title('Original picture')
                        ax[0].imshow(bin, cmap=plt.cm.gray)
                        ax[0].set_axis_off()

                        name_file2 = ["resume_",file[:-4], "_convex_hull2.png"]
                        name_file2 = "".join(name_file2)

                        plt.tight_layout()
                        plt.savefig(os.path.join(output_folder,name_file2), dpi=None, facecolor='w',
                                    edgecolor='w',
                                    orientation='portrait', papertype=None, format=None,
                                    transparent=False, bbox_inches=None, pad_inches=0.1,
                                    frameon=None, metadata=None)

                        # exportation des donnees
                        df = pd.DataFrame({"Label": Label, "num_label": num_label, "perimeter": perimeter, "area": area,
                                           "profondeur": profondeur, "largeur": largeur})
                        print(df)

                        chemin = [fusion_dir2, "/result_convex_hull.csv"]
                        chemin = "".join(chemin)
                        df.to_csv(chemin, decimal=",", index=False)

                        #timing
                        interval = time.time() - start_time_file
                        print('Time in seconds of this fill:', interval)

                        interval = time.time() - start_time
                        print('Total time in seconds :', interval)

                        #interval = time.time() - start_time

                        #conversion, mesure

                        #compilation des données
                        #on passe a la suivante


                        #print('Total time in seconds:', interval)
'''
    if not len(root)==0:
        #creation du tableau csv
        df = pd.DataFrame({"Label":compile_name,"root": root, "background": background, "nod": nod})

        chemin=[fusion_dir2,"/result_nb_pixel_by_plant.csv"]
        chemin="".join(chemin)
        df.to_csv(chemin, decimal=",", index=False)
'''
print("finit")
