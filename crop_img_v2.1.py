# instalation de numpy avec la commande dans le terminal pip install opencv-python
# python -m pip install -U pip
# python -m pip install -U matplotlib

import numpy as np
import os
from skimage import io, img_as_float32, color, img_as_ubyte


#path_to_target= "C:/Users/masla/OneDrive/Document/2.Cours, apprentissage/Dijon travail/annalyse/py/img_analyse/img"
#path_to_target = '/Volumes/KINGSTON32/coco/img'
path_to_target='H:/img'
path_to_target=input("Name of the folder to analyze : ")
num_cut=input("cut the image into x² sections. (ex: x=4 so 16 image portion), Entered x : ")
#num_cut=4
num_cut=int(num_cut)
cropped_dir = ["cut_img","_",str(num_cut)]
cropped_dir="".join(cropped_dir)


taskids = os.listdir(path_to_target)
#print(taskids)
for taskid in taskids:
    taskid_dir = os.path.join(path_to_target, taskid)
    if taskid.isnumeric() and os.path.isdir(taskid_dir):
        files = os.listdir(taskid_dir)
        files.sort()
        for file in files:
            if file.endswith('.png'):
                print(file)
                filepath = os.path.join(taskid_dir, file)
                #print(filepath)

                rgb_img = io.imread(filepath, as_gray=False)
                # corrige la lecture et force ainsi les bonnes couleurs
                rgb_img = img_as_float32(rgb_img) # float32 = [0:1] precision 32 bits
                ndims = rgb_img.shape # original dimensions
                if ndims[2] == 4: # alpha present
                    rgb_img = color.rgba2rgb(rgb_img)
                rgb_img = np.uint8(rgb_img * 255)
                filename, ext = os.path.splitext(file)

                r_img=rgb_img.shape[0] #A changer
                tail=r_img/num_cut
                a = np.arange(num_cut+1)#creation d'un vecteur
                vec=a[0:(num_cut):1]*tail #ici je ne prend en compte que ce qui est bon
                for i in range(0,num_cut): # pour tout les cut
                    for j in range(0,num_cut):
                        x=int(vec[i])
                        y=int(vec[j])
                        l=a[i]
                        c=a[j]
                        crop_img = rgb_img[y:y + int(tail), x:x + int(tail)]
                        output_folder=os.path.join(path_to_target, taskid, cropped_dir)
                        #print(output_folder)
                        if not os.path.exists(output_folder):
                            os.makedirs(output_folder)

                        outputfile = os.path.join(path_to_target, taskid, cropped_dir, (filename + '_' + str(l + 1) + '_' + str(c + 1) + '.png'))
                        if not os.path.isfile(outputfile):
                            print(outputfile)
                            tmp = os.path.dirname(outputfile)
                            #print(tmp)
                            if not os.path.isdir(tmp):
                                os.makedirs(tmp)
                            io.imsave(outputfile, img_as_ubyte(crop_img)) #ubyte = int [0:255] precision 8 bits
