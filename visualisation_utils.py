"""Set of functions for visualisations."""
import numpy as np
import torch
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

COLOR_LIST = ['white', 'red', 'green', 'yellow', 'orange', 'pink',
              'blue', 'cyan', 'black', 'grey']
CMAP = ListedColormap(COLOR_LIST)
CLASS_NAMES = ['No Data', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']


def _image_show(raster, title='Natural color composite'):
    """Show a figure based on a hyperspectral raster."""
    plt.imshow(raster/3000)
    plt.title(title)
    plt.axis('off')


def _class_show(raster, title):
    """Show a figure based on a classification."""
    plt.imshow(raster, cmap=CMAP)
    # plt.colorbar(ticks=(np.linspace(0.5, 8.5, 10)))
    plt.title(title)
    plt.axis('off')


def show_img_ref(hs_img, gt_img):
    """Show the hyperspectral image and a training reference."""
    plt.figure(figsize=[16, 8])
    plt.subplot(1, 2, 1)
    _image_show(hs_img)
    plt.subplot(1, 2, 2)
    _class_show(gt_img, 'Reference data')

    for label, color in zip(CLASS_NAMES, COLOR_LIST):
        plt.plot(0, 0, 's', label=label,
                 color=color, markeredgecolor='black')
    plt.legend()


def show_spectral_curve(tile_dict, tile_num,
                        title='Spectral curve for pixel #'):
    """Show a figure of the spectal curve."""
    x = np.linspace(404, 997, num=54)
    if len(tile_dict["imagery"].shape) == 4:
        y = tile_dict["imagery"][tile_num, 0, 0, :]
        lbl = tile_dict["reference"][tile_num, 0, 0, :][0] + 1
    elif len(tile_dict["imagery"].shape) == 3:
        y = tile_dict["imagery"][tile_num, 0, :]
        lbl = tile_dict["reference"][tile_num] + 1
    else:
        print('The input data is in an incompatible shape.')

    plt.plot(x, y, label=f'class #{lbl}')
    plt.title(f'{title} {tile_num}')
    plt.xlabel('Wavelength [nm]')
    plt.legend()


def show_augment_spectral(tile_dict, tile_num, aug_funct):
    """Show a figure of the original spectal curve and the augmented curve."""
    plt.figure(figsize=[8, 4])
    plt.subplot(1, 2, 1)
    show_spectral_curve(tile_dict, tile_num,
                        title='Original spectral curve for pixel #')
    plt.subplot(1, 2, 2)
    tensor_obs = torch.from_numpy(tile_dict["imagery"])
    tensor_gt = torch.from_numpy(tile_dict["reference"])
    aug_obs, aug_gt = aug_funct(tensor_obs, tensor_gt)
    aug_dict = {'imagery': aug_obs, 'reference': aug_gt}
    show_spectral_curve(aug_dict, tile_num,
                        title='Augmented spectral curve for pixel #')


def show_classified(hs_img, gt_img, class_img):
    """Compare the classification result to the reference data."""
    plt.figure(figsize=[15, 5])
    plt.subplot(1, 3, 1)
    _image_show(hs_img)

    plt.subplot(1, 3, 2)
    _class_show(gt_img, 'Reference data')

    for label, color in zip(CLASS_NAMES, COLOR_LIST):
        plt.plot(0, 0, 's', label=label,
                 color=color, markeredgecolor='black')
    plt.legend()

    plt.subplot(1, 3, 3)
    _class_show(class_img, 'Classified data')
