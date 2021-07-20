#corentin MASLARD maslard.corentin@gmail.com
#cree le 2020.01.17
#Etape:
    #-prendre tout les nom des fichier (issus des finichiers d'origine)
    #-prendre toute les photots qui contienne les nom segmetations simple ou prediction (selon ce que j'ai choisis au debut)
    #verifier que tout les morceaux de photos sont la.
    #-une fonction qui transforme toutes les images sans distinction. Les pixel 1, 2 et 3 sont remplacer en pixcel de couleur et toutes les image sont placé dans un seul dossier.
    #-cree la fonction qui rassemble toutes les images et qui les mets toute dans un dernier dossier (toujours dans le dossier a chiffre)
    #Puis une fonction qui mesure des paramètres physio comme la surface racinaire. La surface en nodule.
    #ultérieurement le convexul.

import numpy as np
import os
from PIL import Image
import pandas as pd
import sys
from skimage import io, img_as_float32, color, img_as_ubyte

#a remetre une fois le script finis

path_to_target=input('Name of the folder to analyze : ')
num_cut=int(input('The rac number of cut of one image (4 or 8) : '))

assembly_type=input("'Simple Segmentation' or 'Probabilities' :" )
if assembly_type == 'Simple Segmentation' or assembly_type == 'Probabilities':
    print("Cool, bon choix")
else:
    print('assembly_type error, tap Simple_Segmentation or Probabilities')
    sys.exit()

#path_to_target='C:/Users/masla/OneDrive/Document/2.Cours, apprentissage/Dijon travail/annalyse/py/img_analyse/test'
#assembly_type='Simple Segmentation'
#num_cut=4
num_cut_folder=["cut_img_",str(num_cut)]
num_cut_folder="".join(num_cut_folder)

fusion_dir = ['fusion_', assembly_type,'_',str(num_cut)]
fusion_dir="".join(fusion_dir) ; print(fusion_dir) #nom du dossier qui devra être creer si il n'existe pas
taskids = os.listdir(path_to_target)
tail_img=12000
img_size=tail_img/num_cut
#print(taskids)
assembly_type=[assembly_type,".png"]
assembly_type="".join(assembly_type)

files_n=[]
for taskid in taskids:
    taskid_dir = os.path.join(path_to_target, taskid)
    #print(taskid_dir)
    if taskid.isnumeric() and os.path.isdir(taskid_dir):
        files = os.listdir(taskid_dir)
        files.sort() #ascending order
        taskid_cut_dir=os.path.join(path_to_target,taskid,num_cut_folder)
        print(taskid_cut_dir)
        files_cut=os.listdir(taskid_cut_dir)
        files_cut.sort()
        #print(files)
        #print(files_cut)
        #files_cut=os.listdir(taskid_dir)
        #creation du dossier
        output_folder = os.path.join(path_to_target, taskid, fusion_dir)
        # print(output_folder)
        compile_name=[]
        background = []
        root = []
        nod = []

        #obtenir les noms des images originales
        for file in files:
            verif = [] #verifie si il y a les fichier de segmentation
            background_n = 0
            root_n = 0
            nod_n = 0
            for file_cut in files_cut:
                if file_cut.startswith(file[:-4]) and file_cut.endswith(assembly_type):
                    verif.append(file_cut)

            #print(len(verif))
            if (len(verif) == 0):
                break
            # creation du dossier
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)
            if file.endswith('.png'):
                print(file[:-4])
                file2 = [file[:-4], '_Simple_Segmentation_compil_', str(num_cut), '.png']
                file2 = "".join(file2)
                if not os.path.exists(os.path.join(output_folder,file2)): #permet de passer a une autre image si il y en a deja une
                    #creation d'une image blanche aux bonnes dimenssions
                    new_img = Image.new('RGB', (tail_img, tail_img), (250, 250, 250))
                    #print(file[:-4])
                    for file_cut in files_cut:

                        #print(assembly_type)
                        if file_cut.startswith(file[:-4]) and file_cut.endswith(assembly_type):
                            file_cut_path=os.path.join(taskid_cut_dir,file_cut)
                            n_img = Image.open(file_cut_path)
                            largeur, hauteur = n_img.size
                            imageBrut = Image.new("RGB", (largeur, hauteur))

                            print(file_cut)
                            coo_img_x=int(file_cut[-25])
                            coo_img_y=int(file_cut[-27])
                            #print(coo_img_x)
                            #print(coo_img_y)
                            #new_img.show()
                            # pour chaque ligne:
                            for y in range(hauteur):
                                # pour chaque colonne :
                                for x in range(largeur):
                                    # code du pixel (niveau de gris)
                                    p = n_img.getpixel((x, y))
                                    # print(p)
                                    # transformation des 1 en blanc:
                                    if p == 1:
                                        p = (255, 255, 255)
                                        background_n=background_n+1
                                    if p==3:
                                        nod_n=nod_n+1
                                        p=(255,0,0)
                                    if p==2:
                                        p = (0, 0, 0)
                                        root_n=root_n+1
                                    # creation du pixel correspondant dans la nv image:
                                    imageBrut.putpixel((x, y), p)
                            #print((coo_img_y) * img_size)
                            #print((coo_img_x - 1) * img_size)
                            #print(new_img.size)
                            #print(((coo_img_y-1) * img_size,(coo_img_x - 1) * img_size))
                            #imageBrut.show() #ca cest ok il s'affiche
                            new_img.paste(imageBrut,(int((coo_img_y-1) * img_size),int((coo_img_x - 1) * img_size)))
                    #print('ici ça doit imprimer')


                    file2=[file[:-4],'_Simple_Segmentation_compil_',str(num_cut),'.png']
                    file2="".join(file2)
                    #print(background_n)
                    #print(root_n)
                    #print(nod_n)
                    compile_name.append(file[:-4])
                    background.append(str(background_n))
                    root.append(str(root_n))
                    nod.append(str(nod_n))
                    #print(background)
                    #print(root)
                    #print(nod)
                    # ici je dois reussire a faire une liste
                    print(os.path.join(output_folder,file2))
                    new_img.save(os.path.join(output_folder, file2), "PNG")
                    print("finit")

                            #imageBrut.show()
    if not len(root)==0:
        df = pd.DataFrame({"Label":compile_name,"root": root, "background": background, "nod": nod})
        print(df)

        chemin=[output_folder,"/result_nb_pixel.csv"]
        chemin="".join(chemin)
        df.to_csv(chemin, decimal=",", index=False)