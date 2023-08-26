import numpy as np
import argparse
import os
import tifffile as tiff
import time
import datetime
import random
from skimage import io
import logging
import math
import pdb

def shuffle_datasets(train_raw, train_GT, name_list):
    index_list = list(range(0, len(name_list)))
    # print('index_list -----> ',index_list)
    random.shuffle(index_list)
    random_index_list = index_list
    # print('index_list -----> ',index_list)
    new_name_list = list(range(0, len(name_list)))
    train_raw = np.array(train_raw)
    # print('train_raw shape -----> ',train_raw.shape)
    train_GT = np.array(train_GT)
    # print('train_GT shape -----> ',train_GT.shape)
    new_train_raw = train_raw
    new_train_GT = train_GT
    for i in range(0,len(random_index_list)):
        # print('i -----> ',i)
        new_train_raw[i,:,:,:] = train_raw[random_index_list[i],:,:,:]
        new_train_GT[i,:,:,:] = train_GT[random_index_list[i],:,:,:]
        new_name_list[i] = name_list[random_index_list[i]]
    # new_train_raw = np.expand_dims(new_train_raw, 4)
    # new_train_GT = np.expand_dims(new_train_GT, 4)
    return new_train_raw, new_train_GT, new_name_list

def train_preprocess(args):
    img_h = args.img_h
    img_w = args.img_w
    img_s2 = args.img_s*2
    gap_h = args.gap_h
    gap_w = args.gap_w
    gap_s2 = args.gap_s*2
    im_folder = 'datasets//'+args.datasets_folder

    name_list = []
    train_raw = []
    train_GT = []
    for im_name in list(os.walk(im_folder, topdown=False))[-1][-1]:
        print('im_name -----> ',im_name)
        im_dir = im_folder+'//'+im_name
        noise_im = tiff.imread(im_dir)
        print('noise_im shape -----> ',noise_im.shape)
        # print('noise_im max -----> ',noise_im.max())
        # print('noise_im min -----> ',noise_im.min())
        noise_im = (noise_im-noise_im.min()).astype(np.float32)/args.normalize_factor

        whole_w = noise_im.shape[2]
        whole_h = noise_im.shape[1]
        whole_s = noise_im.shape[0]
        print('int((whole_h-img_h+gap_h)/gap_h) -----> ',int((whole_h-img_h+gap_h)/gap_h))
        print('int((whole_w-img_w+gap_w)/gap_w) -----> ',int((whole_w-img_w+gap_w)/gap_w))
        print('int((whole_s-img_s2+gap_s2)/gap_s2) -----> ',int((whole_s-img_s2+gap_s2)/gap_s2))
        for x in range(0,int((whole_h-img_h+gap_h)/gap_h)):
            for y in range(0,int((whole_w-img_w+gap_w)/gap_w)):
                for z in range(0,int((whole_s-img_s2+gap_s2)/gap_s2)):
                    init_h = gap_h*x
                    end_h = gap_h*x + img_h
                    init_w = gap_w*y
                    end_w = gap_w*y + img_w
                    init_s = gap_s2*z
                    end_s = gap_s2*z + img_s2
                    noise_patch1 = noise_im[init_s:end_s:2,init_h:end_h,init_w:end_w]
                    noise_patch2 = noise_im[init_s+1:end_s:2,init_h:end_h,init_w:end_w]
                    patch_name = args.datasets_folder+'_x'+str(x)+'_y'+str(y)+'_z'+str(z)
                    train_raw.append(noise_patch1.transpose(1,2,0))
                    train_GT.append(noise_patch2.transpose(1,2,0))
                    name_list.append(patch_name)
    return train_raw, train_GT, name_list, noise_im

def test_preprocess(args):
    img_h = args.img_h
    img_w = args.img_w
    img_s2 = args.img_s
    gap_h = args.gap_h
    gap_w = args.gap_w
    gap_s2 = args.gap_s
    im_folder = 'datasets//'+args.datasets_folder

    name_list = []
    train_raw = []
    for im_name in list(os.walk(im_folder, topdown=False))[-1][-1]:
        # print('im_name -----> ',im_name)
        im_dir = im_folder+'//'+im_name
        noise_im = tiff.imread(im_dir)
        # print('noise_im shape -----> ',noise_im.shape)
        # print('noise_im max -----> ',noise_im.max())
        # print('noise_im min -----> ',noise_im.min())
        noise_im = (noise_im-noise_im.min()).astype(np.float32)/args.normalize_factor

        whole_w = noise_im.shape[2]
        whole_h = noise_im.shape[1]
        whole_s = noise_im.shape[0]
        # print('int((whole_h-img_h+gap_h)/gap_h) -----> ',int((whole_h-img_h+gap_h)/gap_h))
        # print('int((whole_w-img_w+gap_w)/gap_w) -----> ',int((whole_w-img_w+gap_w)/gap_w))
        # print('int((whole_s-img_s2+gap_s2)/gap_s2) -----> ',int((whole_s-img_s2+gap_s2)/gap_s2))
        for x in range(0,int((whole_h-img_h+gap_h)/gap_h)):
            for y in range(0,int((whole_w-img_w+gap_w)/gap_w)):
                for z in range(0,int((whole_s-img_s2+gap_s2)/gap_s2)):
                    init_h = gap_h*x
                    end_h = gap_h*x + img_h
                    init_w = gap_w*y
                    end_w = gap_w*y + img_w
                    init_s = gap_s2*z
                    end_s = gap_s2*z + img_s2
                    noise_patch1 = noise_im[init_s:end_s,init_h:end_h,init_w:end_w]
                    patch_name = args.datasets_folder+'_x'+str(x)+'_y'+str(y)+'_z'+str(z)
                    train_raw.append(noise_patch1.transpose(1,2,0))
                    name_list.append(patch_name)
    return train_raw, name_list, noise_im

def test_preprocess_lessMemory (args):
    img_h = args.img_h
    img_w = args.img_w
    img_s2 = args.img_s
    gap_h = args.gap_h
    gap_w = args.gap_w
    gap_s2 = args.gap_s
    im_folder = 'datasets//'+args.datasets_folder

    name_list = []
    # train_raw = []
    coordinate_list={}
    for im_name in list(os.walk(im_folder, topdown=False))[-1][-1]:
        # print('im_name -----> ',im_name)
        im_dir = im_folder+'//'+im_name
        noise_im = tiff.imread(im_dir)
        # print('noise_im shape -----> ',noise_im.shape)
        # print('noise_im max -----> ',noise_im.max())
        # print('noise_im min -----> ',noise_im.min())
        if noise_im.shape[0]>args.test_datasize:
            noise_im = noise_im[0:args.test_datasize,:,:]
        noise_im = (noise_im-noise_im.min()).astype(np.float32)/args.normalize_factor

        whole_w = noise_im.shape[2]
        whole_h = noise_im.shape[1]
        whole_s = noise_im.shape[0]
        # print('int((whole_h-img_h+gap_h)/gap_h) -----> ',int((whole_h-img_h+gap_h)/gap_h))
        # print('int((whole_w-img_w+gap_w)/gap_w) -----> ',int((whole_w-img_w+gap_w)/gap_w))
        # print('int((whole_s-img_s2+gap_s2)/gap_s2) -----> ',int((whole_s-img_s2+gap_s2)/gap_s2))
        for x in range(0,int((whole_h-img_h+gap_h)/gap_h)):
            for y in range(0,int((whole_w-img_w+gap_w)/gap_w)):
                for z in range(0,int((whole_s-img_s2+gap_s2)/gap_s2)):
                    single_coordinate={'init_h':0, 'end_h':0, 'init_w':0, 'end_w':0, 'init_s':0, 'end_s':0}
                    init_h = gap_h*x
                    end_h = gap_h*x + img_h
                    init_w = gap_w*y
                    end_w = gap_w*y + img_w
                    init_s = gap_s2*z
                    end_s = gap_s2*z + img_s2
                    single_coordinate['init_h'] = init_h
                    single_coordinate['end_h'] = end_h
                    single_coordinate['init_w'] = init_w
                    single_coordinate['end_w'] = end_w
                    single_coordinate['init_s'] = init_s
                    single_coordinate['end_s'] = end_s
                    # noise_patch1 = noise_im[init_s:end_s,init_h:end_h,init_w:end_w]
                    patch_name = args.datasets_folder+'_x'+str(x)+'_y'+str(y)+'_z'+str(z)
                    # train_raw.append(noise_patch1.transpose(1,2,0))
                    name_list.append(patch_name)
                    # print(' single_coordinate -----> ',single_coordinate)
                    coordinate_list[patch_name] = single_coordinate
    return  name_list, noise_im, coordinate_list

def get_gap_s(args, img, stack_num):
    whole_w = img.shape[2]
    whole_h = img.shape[1]
    whole_s = img.shape[0]
    print('whole_w -----> ',whole_w)
    print('whole_h -----> ',whole_h)
    print('whole_s -----> ',whole_s)
    w_num = math.floor((whole_w-args.img_w)/args.gap_w)+1
    h_num = math.floor((whole_h-args.img_h)/args.gap_h)+1
    s_num = math.ceil(args.train_datasets_size/w_num/h_num/stack_num)
    print('w_num -----> ',w_num)
    print('h_num -----> ',h_num)
    print('s_num -----> ',s_num)
    gap_s = math.floor((whole_s-args.img_s*2)/(s_num-1))
    print('gap_s -----> ',gap_s)
    return gap_s

def train_preprocess_lessMemory(args):
    img_h = args.img_h
    img_w = args.img_w
    img_s2 = args.img_s*2
    gap_h = args.gap_h
    gap_w = args.gap_w
    gap_s2 = args.gap_s*2
    im_folder = args.datasets_path+'//'+args.datasets_folder

    name_list = []
    # train_raw = []
    coordinate_list={}
    for im_name in list(os.walk(im_folder, topdown=False))[-1][-1]:
        # print('im_name -----> ',im_name)
        im_dir = im_folder+'//'+im_name
        noise_im = tiff.imread(im_dir)
        if noise_im.shape[0]>args.select_img_num:
            noise_im = noise_im[0:args.select_img_num,:,:]
        gap_s2 = get_gap_s(args, noise_im)
        # print('noise_im shape -----> ',noise_im.shape)
        # print('noise_im max -----> ',noise_im.max())
        # print('noise_im min -----> ',noise_im.min())
        noise_im = (noise_im-noise_im.min()).astype(np.float32)/args.normalize_factor

        whole_w = noise_im.shape[2]
        whole_h = noise_im.shape[1]
        whole_s = noise_im.shape[0]
        # print('int((whole_h-img_h+gap_h)/gap_h) -----> ',int((whole_h-img_h+gap_h)/gap_h))
        # print('int((whole_w-img_w+gap_w)/gap_w) -----> ',int((whole_w-img_w+gap_w)/gap_w))
        # print('int((whole_s-img_s2+gap_s2)/gap_s2) -----> ',int((whole_s-img_s2+gap_s2)/gap_s2))
        for x in range(0,int((whole_h-img_h+gap_h)/gap_h)):
            for y in range(0,int((whole_w-img_w+gap_w)/gap_w)):
                for z in range(0,int((whole_s-img_s2+gap_s2)/gap_s2)):
                    single_coordinate={'init_h':0, 'end_h':0, 'init_w':0, 'end_w':0, 'init_s':0, 'end_s':0}
                    init_h = gap_h*x
                    end_h = gap_h*x + img_h
                    init_w = gap_w*y
                    end_w = gap_w*y + img_w
                    init_s = gap_s2*z
                    end_s = gap_s2*z + img_s2
                    single_coordinate['init_h'] = init_h
                    single_coordinate['end_h'] = end_h
                    single_coordinate['init_w'] = init_w
                    single_coordinate['end_w'] = end_w
                    single_coordinate['init_s'] = init_s
                    single_coordinate['end_s'] = end_s
                    # noise_patch1 = noise_im[init_s:end_s,init_h:end_h,init_w:end_w]
                    patch_name = args.datasets_folder+'_x'+str(x)+'_y'+str(y)+'_z'+str(z)
                    # train_raw.append(noise_patch1.transpose(1,2,0))
                    name_list.append(patch_name)
                    # print(' single_coordinate -----> ',single_coordinate)
                    coordinate_list[patch_name] = single_coordinate
    return  name_list, noise_im, coordinate_list

def train_preprocess_lessMemoryMulStacks(args):
    img_h = args.img_h
    img_w = args.img_w
    img_s2 = args.img_s*2
    gap_h = args.gap_h
    gap_w = args.gap_w
    gap_s2 = args.gap_s*2
    im_folder = args.datasets_path+'//'+args.datasets_folder

    name_list = []
    # train_raw = []
    coordinate_list={}

    print('list(os.walk(im_folder, topdown=False)) -----> ',list(os.walk(im_folder, topdown=False)))
    stack_num = len(list(os.walk(im_folder, topdown=False))[-1][-1])
    print('stack_num -----> ',stack_num)
    for im_name in list(os.walk(im_folder, topdown=False))[-1][-1]:
        # print('im_name -----> ',im_name)
        im_dir = im_folder+'//'+im_name
        noise_im = tiff.imread(im_dir)
        if noise_im.shape[0]>args.select_img_num:
            noise_im = noise_im[0:args.select_img_num,:,:]
        gap_s2 = get_gap_s(args, noise_im, stack_num)
        # print('noise_im shape -----> ',noise_im.shape)
        # print('noise_im max -----> ',noise_im.max())
        # print('noise_im min -----> ',noise_im.min())
        noise_im = (noise_im-noise_im.min()).astype(np.float32)/args.normalize_factor

        whole_w = noise_im.shape[2]
        whole_h = noise_im.shape[1]
        whole_s = noise_im.shape[0]
        # print('int((whole_h-img_h+gap_h)/gap_h) -----> ',int((whole_h-img_h+gap_h)/gap_h))
        # print('int((whole_w-img_w+gap_w)/gap_w) -----> ',int((whole_w-img_w+gap_w)/gap_w))
        # print('int((whole_s-img_s2+gap_s2)/gap_s2) -----> ',int((whole_s-img_s2+gap_s2)/gap_s2))
        for x in range(0,int((whole_h-img_h+gap_h)/gap_h)):
            for y in range(0,int((whole_w-img_w+gap_w)/gap_w)):
                for z in range(0,int((whole_s-img_s2+gap_s2)/gap_s2)):
                    single_coordinate={'init_h':0, 'end_h':0, 'init_w':0, 'end_w':0, 'init_s':0, 'end_s':0}
                    init_h = gap_h*x
                    end_h = gap_h*x + img_h
                    init_w = gap_w*y
                    end_w = gap_w*y + img_w
                    init_s = gap_s2*z
                    end_s = gap_s2*z + img_s2
                    single_coordinate['init_h'] = init_h
                    single_coordinate['end_h'] = end_h
                    single_coordinate['init_w'] = init_w
                    single_coordinate['end_w'] = end_w
                    single_coordinate['init_s'] = init_s
                    single_coordinate['end_s'] = end_s
                    # noise_patch1 = noise_im[init_s:end_s,init_h:end_h,init_w:end_w]
                    patch_name = args.datasets_folder+'_'+im_name.replace('.tif','')+'_x'+str(x)+'_y'+str(y)+'_z'+str(z)
                    # train_raw.append(noise_patch1.transpose(1,2,0))
                    name_list.append(patch_name)
                    # print(' single_coordinate -----> ',single_coordinate)
                    coordinate_list[patch_name] = single_coordinate
    return  name_list, noise_im, coordinate_list

def shuffle_datasets_lessMemory(name_list):
    index_list = list(range(0, len(name_list)))
    # print('index_list -----> ',index_list)
    random.shuffle(index_list)
    random_index_list = index_list
    # print('index_list -----> ',index_list)
    new_name_list = list(range(0, len(name_list)))
    for i in range(0,len(random_index_list)):
        new_name_list[i] = name_list[random_index_list[i]]
    return new_name_list

def test_preprocess_lessMemoryPadding (args):
    img_h = args.img_h
    img_w = args.img_w
    img_s2 = args.img_s
    gap_h = args.gap_h
    gap_w = args.gap_w
    gap_s2 = args.gap_s
    im_folder = 'datasets//'+args.datasets_folder

    name_list = []
    # train_raw = []
    coordinate_list={}
    for im_name in list(os.walk(im_folder, topdown=False))[-1][-1]:
        # print('im_name -----> ',im_name)
        im_dir = im_folder+'//'+im_name
        raw_noise_im = tiff.imread(im_dir)
        if raw_noise_im.shape[0]>args.test_datasize:
            raw_noise_im = raw_noise_im[0:args.test_datasize,:,:]
        raw_noise_im = (raw_noise_im-raw_noise_im.min()).astype(np.float32)/args.normalize_factor

        print('raw_noise_im shape -----> ',raw_noise_im.shape)
        noise_im_w = math.ceil((raw_noise_im.shape[2]-img_w)/gap_w)*gap_w+img_w
        noise_im_h = math.ceil((raw_noise_im.shape[1]-img_h)/gap_h)*gap_h+img_h
        noise_im_s = math.ceil((raw_noise_im.shape[0]-img_s2)/gap_s2)*gap_s2+img_s2
        noise_im = np.zeros([noise_im_s,noise_im_h,noise_im_w])
        noise_im[0:raw_noise_im.shape[0], 0:raw_noise_im.shape[1], 0:raw_noise_im.shape[2]]=raw_noise_im
        noise_im = noise_im.astype(np.float32)
        print('noise_im shape -----> ',noise_im.shape)
        # print('noise_im max -----> ',noise_im.max())
        # print('noise_im min -----> ',noise_im.min())

        whole_w = noise_im.shape[2]
        whole_h = noise_im.shape[1]
        whole_s = noise_im.shape[0]
        # print('int((whole_h-img_h+gap_h)/gap_h) -----> ',int((whole_h-img_h+gap_h)/gap_h))
        # print('int((whole_w-img_w+gap_w)/gap_w) -----> ',int((whole_w-img_w+gap_w)/gap_w))
        # print('int((whole_s-img_s2+gap_s2)/gap_s2) -----> ',int((whole_s-img_s2+gap_s2)/gap_s2))
        for x in range(0,int((whole_h-img_h+gap_h)/gap_h)):
            for y in range(0,int((whole_w-img_w+gap_w)/gap_w)):
                for z in range(0,int((whole_s-img_s2+gap_s2)/gap_s2)):
                    single_coordinate={'init_h':0, 'end_h':0, 'init_w':0, 'end_w':0, 'init_s':0, 'end_s':0}
                    init_h = gap_h*x
                    end_h = gap_h*x + img_h
                    init_w = gap_w*y
                    end_w = gap_w*y + img_w
                    init_s = gap_s2*z
                    end_s = gap_s2*z + img_s2
                    single_coordinate['init_h'] = init_h
                    single_coordinate['end_h'] = end_h
                    single_coordinate['init_w'] = init_w
                    single_coordinate['end_w'] = end_w
                    single_coordinate['init_s'] = init_s
                    single_coordinate['end_s'] = end_s
                    # noise_patch1 = noise_im[init_s:end_s,init_h:end_h,init_w:end_w]
                    patch_name = args.datasets_folder+'_x'+str(x)+'_y'+str(y)+'_z'+str(z)
                    # train_raw.append(noise_patch1.transpose(1,2,0))
                    name_list.append(patch_name)
                    # print(' single_coordinate -----> ',single_coordinate)
                    coordinate_list[patch_name] = single_coordinate
    return  name_list, noise_im, coordinate_list, raw_noise_im

def test_preprocess_lessMemoryNoTail (args):
    img_h = args.img_h
    img_w = args.img_w
    img_s2 = args.img_s
    gap_h = args.gap_h
    gap_w = args.gap_w
    gap_s2 = args.gap_s
    cut_w = (img_w - gap_w)/2
    cut_h = (img_h - gap_h)/2
    cut_s = (img_s2 - gap_s2)/2
    im_folder = args.datasets_path+'//'+args.datasets_folder

    name_list = []
    # train_raw = []
    coordinate_list={}
    for im_name in list(os.walk(im_folder, topdown=False))[-1][-1]:
        # print('im_name -----> ',im_name)
        im_dir = im_folder+'//'+im_name
        noise_im = tiff.imread(im_dir)
        # print('noise_im shape -----> ',noise_im.shape)
        # print('noise_im max -----> ',noise_im.max())
        # print('noise_im min -----> ',noise_im.min())
        if noise_im.shape[0]>args.test_datasize:
            noise_im = noise_im[0:args.test_datasize,:,:]
        noise_im = (noise_im-noise_im.min()).astype(np.float32)/args.normalize_factor

        whole_w = noise_im.shape[2]
        whole_h = noise_im.shape[1]
        whole_s = noise_im.shape[0]

        num_w = math.ceil((whole_w-img_w+gap_w)/gap_w)
        num_h = math.ceil((whole_h-img_h+gap_h)/gap_h)
        num_s = math.ceil((whole_s-img_s2+gap_s2)/gap_s2)
        # print('int((whole_h-img_h+gap_h)/gap_h) -----> ',int((whole_h-img_h+gap_h)/gap_h))
        # print('int((whole_w-img_w+gap_w)/gap_w) -----> ',int((whole_w-img_w+gap_w)/gap_w))
        # print('int((whole_s-img_s2+gap_s2)/gap_s2) -----> ',int((whole_s-img_s2+gap_s2)/gap_s2))
        for x in range(0,num_h):
            for y in range(0,num_w):
                for z in range(0,num_s):
                    single_coordinate={'init_h':0, 'end_h':0, 'init_w':0, 'end_w':0, 'init_s':0, 'end_s':0}
                    if x != (num_h-1):
                        init_h = gap_h*x
                        end_h = gap_h*x + img_h
                    elif x == (num_h-1):
                        init_h = whole_h - img_h
                        end_h = whole_h

                    if y != (num_w-1):
                        init_w = gap_w*y
                        end_w = gap_w*y + img_w
                    elif y == (num_w-1):
                        init_w = whole_w - img_w
                        end_w = whole_w

                    if z != (num_s-1):
                        init_s = gap_s2*z
                        end_s = gap_s2*z + img_s2
                    elif z == (num_s-1):
                        init_s = whole_s - img_s2
                        end_s = whole_s
                    single_coordinate['init_h'] = init_h
                    single_coordinate['end_h'] = end_h
                    single_coordinate['init_w'] = init_w
                    single_coordinate['end_w'] = end_w
                    single_coordinate['init_s'] = init_s
                    single_coordinate['end_s'] = end_s

                    if y == 0:
                        single_coordinate['stack_start_w'] = y*gap_w
                        single_coordinate['stack_end_w'] = y*gap_w+img_w-cut_w
                        single_coordinate['patch_start_w'] = 0
                        single_coordinate['patch_end_w'] = img_w-cut_w
                    elif y == num_w-1:
                        single_coordinate['stack_start_w'] = whole_w-img_w+cut_w
                        single_coordinate['stack_end_w'] = whole_w
                        single_coordinate['patch_start_w'] = cut_w
                        single_coordinate['patch_end_w'] = img_w
                    else:
                        single_coordinate['stack_start_w'] = y*gap_w+cut_w
                        single_coordinate['stack_end_w'] = y*gap_w+img_w-cut_w
                        single_coordinate['patch_start_w'] = cut_w
                        single_coordinate['patch_end_w'] = img_w-cut_w

                    if x == 0:
                        single_coordinate['stack_start_h'] = x*gap_h
                        single_coordinate['stack_end_h'] = x*gap_h+img_h-cut_h
                        single_coordinate['patch_start_h'] = 0
                        single_coordinate['patch_end_h'] = img_h-cut_h
                    elif x == num_h-1:
                        single_coordinate['stack_start_h'] = whole_h-img_h+cut_h
                        single_coordinate['stack_end_h'] = whole_h
                        single_coordinate['patch_start_h'] = cut_h
                        single_coordinate['patch_end_h'] = img_h
                    else:
                        single_coordinate['stack_start_h'] = x*gap_h+cut_h
                        single_coordinate['stack_end_h'] = x*gap_h+img_h-cut_h
                        single_coordinate['patch_start_h'] = cut_h
                        single_coordinate['patch_end_h'] = img_h-cut_h

                    if z == 0:
                        single_coordinate['stack_start_s'] = z*gap_s2
                        single_coordinate['stack_end_s'] = z*gap_s2+img_s2-cut_s
                        single_coordinate['patch_start_s'] = 0
                        single_coordinate['patch_end_s'] = img_s2-cut_s
                    elif z == num_s-1:
                        single_coordinate['stack_start_s'] = whole_s-img_s2+cut_s
                        single_coordinate['stack_end_s'] = whole_s
                        single_coordinate['patch_start_s'] = cut_s
                        single_coordinate['patch_end_s'] = img_s2
                    else:
                        single_coordinate['stack_start_s'] = z*gap_s2+cut_s
                        single_coordinate['stack_end_s'] = z*gap_s2+img_s2-cut_s
                        single_coordinate['patch_start_s'] = cut_s
                        single_coordinate['patch_end_s'] = img_s2-cut_s

                    # noise_patch1 = noise_im[init_s:end_s,init_h:end_h,init_w:end_w]
                    patch_name = args.datasets_folder+'_x'+str(x)+'_y'+str(y)+'_z'+str(z)
                    # train_raw.append(noise_patch1.transpose(1,2,0))
                    name_list.append(patch_name)
                    # print(' single_coordinate -----> ',single_coordinate)
                    coordinate_list[patch_name] = single_coordinate
    return  name_list, noise_im, coordinate_list


    # stack_start_w ,stack_end_w ,patch_start_w ,patch_end_w ,
    # stack_start_h ,stack_end_h ,patch_start_h ,patch_end_h ,
    # stack_start_s ,stack_end_s ,patch_start_s ,patch_end_s

