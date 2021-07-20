#le but du script est de couper l'image en morceau affin de ne récuperer que la plante A ou D
#par contre je ne couperais qu'en fonction de la ou j'ai parametre
#corentin MASLARD maslard.corentin@gmail.com
#cree le 2021/07/14

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

import numpy as np
import os
import math
from PIL import Image,ImageDraw
import time
import pandas as pd
import sys
from skimage import io, img_as_float32, color, img_as_ubyte

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

#add in input user (may be)
plant_D_position=[1750,7500]#des position aproximative
hauteur_rhyzo=[0,11500]

#hauteur_rhyzo=[1000,1500]

#begin of the script
num_cut_folder=["cut_img_",str(num_cut)]
num_cut_folder="".join(num_cut_folder)

fusion_dir = ['fusion_', assembly_type,'_',str(num_cut)] #normalement lui il doit deja etre cree
fusion_dir="".join(fusion_dir) ; #print(fusion_dir)
taskids = os.listdir(path_to_target) #touts les dossiers chiffre

#juste pour rajouter l'enderscor
if assembly_type=="Simple Segmentation":
    assembly_type2="Simple_Segmentation"
verif=["_",assembly_type2,"_compil_",str(num_cut),".png"]
verif="".join(verif)
#print(verif)


for taskid in taskids:
    print("taskid : ",taskid)
    taskid_dir = os.path.join(path_to_target, taskid)
    #print(taskid_dir)
    root = []
    if taskid.isnumeric() and os.path.isdir(taskid_dir):
        fusion_dir2=os.path.join(taskid_dir,fusion_dir)
        if os.path.isdir(fusion_dir2):
            #cree les dossiers A et D si il n'existe pas
            output_folderA=os.path.join(fusion_dir2,'A')
            output_folderD = os.path.join(fusion_dir2, 'D')
            if not os.path.exists(output_folderA):
                os.makedirs(output_folderA)
            if not os.path.exists(output_folderD):
                os.makedirs(output_folderD)

            files = os.listdir(fusion_dir2)
            files.sort()  # ascending order

            compile_name = []
            background = []
            root = []
            nod = []

            for file in files:
                if file.endswith(verif):
                    #creation du nom de fichier a sauvegarder, permet aussi de ne pas cree l'image si elle existe deja
                    name_img = [file[:-4], "_D.png"]
                    name_img = "".join(name_img)
                    if not os.path.exists(os.path.join(fusion_dir2,"D", name_img)):#permet de passer a une autre image si il y en a deja une
                        print(file)
                        file_path = os.path.join(fusion_dir2, file)
                        n_img = Image.open(file_path)
                        largeur, hauteur = n_img.size

                        imageBrutD = Image.new("RGB", (largeur, hauteur),(212,230,241))
                        imageBrutA=Image.new("RGB", (largeur, hauteur),(212,230,241))
                        #print(imageBrut.size)
                        interval = time.time() - start_time
                        print('Total time in seconds:', interval)
                        print("for plant D")

                        background_n = 0
                        root_n = 0
                        nod_n = 0

                        for x in range(plant_D_position[0],plant_D_position[1]):
                            #if x in range(plant_D_position[0],plant_D_position[1]) or x in range(plant_A_position[0],plant_A_position[1]):
                            #print(plant_D_position[0])
                            #print("coucou")
                            # pour chaque colonne :
                            for y in range(hauteur_rhyzo[0],hauteur_rhyzo[1]):
                                p = n_img.getpixel((x, y))
                                #print(p)
                                # transformation des 1 en blanc:
                                if p == (255,255,255):
                                    p=(255, 255, 255)
                                    background_n = background_n + 1
                                    #print("coucou")
                                if p == (0,0,0):
                                    p=(0,0,0)
                                    root_n = root_n + 1
                                if p == (255, 0, 0):
                                    p = (255, 0, 0)
                                    nod_n = nod_n + 1
                                    #print("coucou")
                                # creation du pixel correspondant dans la nv image:
                                imageBrutD.putpixel((x, y), p)

                        #sauvegarde de l'image

                        imageBrutD.save(os.path.join(fusion_dir2,"D",name_img), "PNG")

                        #pour le fichier csv
                        compile_name.append(name_img[:-4])
                        background.append(str(background_n))
                        root.append(str(root_n))
                        nod.append(str(nod_n))
                        #print(nod, root, background)

                        #time
                        interval = time.time() - start_time
                        print('Total time in seconds:', interval)

                        #remise a zero des comptages de pixel
                        background_n = 0
                        root_n = 0
                        nod_n = 0

                        print("for plantA")
                        for x in range(plant_D_position[1],largeur):
                            #if x in range(plant_D_position[0],plant_D_position[1]) or x in range(plant_A_position[0],plant_A_position[1]):
                            #print(plant_D_position[0])
                            #print("coucou")
                            # pour chaque colonne :
                            for y in range(hauteur_rhyzo[0],hauteur_rhyzo[1]):
                                p = n_img.getpixel((x, y))
                                # print(p)
                                # transformation des 1 en blanc:
                                if p == (255, 255, 255):
                                    p = (255, 255, 255)
                                    background_n = background_n + 1
                                    # print("coucou")
                                if p == (0, 0, 0):
                                    p = (0, 0, 0)
                                    root_n = root_n + 1
                                if p == (255, 0, 0):
                                    p = (255, 0, 0)
                                    nod_n = nod_n + 1
                                # creation du pixel correspondant dans la nv image:
                                imageBrutA.putpixel((x-plant_D_position[1], y), p)
                        #coller le bout de gauche a droite
                        interval = time.time() - start_time
                        print('Total time in seconds:', interval)

                        print("for small part of the plant A")
                        for x in range(0,plant_D_position[0]):
                            #if x in range(plant_D_position[0],plant_D_position[1]) or x in range(plant_A_position[0],plant_A_position[1]):
                            #print(plant_D_position[0])
                            #print("coucou")
                            # pour chaque colonne :
                            for y in range(hauteur_rhyzo[0],hauteur_rhyzo[1]):
                                p = n_img.getpixel((x, y))
                                # print(p)
                                # transformation des 1 en blanc:
                                if p == (255, 255, 255):
                                    p = (255, 255, 255)
                                    background_n = background_n + 1
                                    # print("coucou")
                                if p == (0, 0, 0):
                                    p = (0, 0, 0)
                                    root_n = root_n + 1
                                if p == (255, 0, 0):
                                    p = (255, 0, 0)
                                    nod_n = nod_n + 1
                                # creation du pixel correspondant dans la nv image:
                                imageBrutA.putpixel((x+largeur-plant_D_position[1], y), p)

                        # sauvegarde de l'image
                        name_img = [file[:-4], "_A.png"]
                        name_img = "".join(name_img)
                        imageBrutA.save(os.path.join(fusion_dir2, "A", name_img), "PNG")

                        # pour le fichier csv
                        compile_name.append(name_img[:-4])
                        background.append(str(background_n))
                        root.append(str(root_n))
                        nod.append(str(nod_n))
                        # print(nod, root, background)

                        #imageBrutA.show()
                        interval = time.time() - start_time
                        print('Total time in seconds:', interval)

    if not len(root)==0:
        df = pd.DataFrame({"Label":compile_name,"root": root, "background": background, "nod": nod})
        #print(df)

        chemin=[fusion_dir2,"/result_nb_pixel_by_plant.csv"]
        chemin="".join(chemin)
        df.to_csv(chemin, decimal=",", index=False)

