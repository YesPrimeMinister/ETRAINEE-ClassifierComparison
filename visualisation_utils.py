"""Set of functions for visualisations."""
import numpy as np
import torch
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from time import gmtime, strftime

COLOR_LIST = ['white', 'red', 'green', 'yellow', 'orange', 'pink',
              'blue', 'cyan', 'black', 'grey']
COLOR_LIST = ('white', 'blue', 'green', 'olive', 'red',
              'yellow', 'grey', 'cyan', 'orange', 'black')
CMAP = ListedColormap(COLOR_LIST)
CLASS_NAMES = ['No Data', 'af', 'afs', 'bor', 'desch', 'klec', 'nard', 'sut',
               'vres', 'vyfuk']
CLASS_NAMES = ['No Data', 'metlička křivolaká',
               'metlička, tomka a ostřice',
               'brusnice borůvková', 'metlice trsnatá',
               'borovice kleč', 'smilka tuhá', 'kamenná moře bez vegetace',
               'vřes obecný', 'kameny, půda, mechy a vegetace']
CLASS_NAMES = ('No Data', 'Water', 'Trees', 'Meadows', 'Self-Blocking Bricks',
               'Bare Soil', 'Asphalt', 'Bitumen', 'Tiles', 'Shadows')


def _image_show(raster, title='Natural color composite'):
    """Show a figure based on a hyperspectral raster."""
    plt.imshow(raster/3000)
    plt.title(title)
    plt.axis('off')


def _class_show(raster, title):
    """Show a figure based on a classification."""
    C_MAP = ListedColormap(COLOR_LIST, N = max(np.unique(raster)))
    plt.imshow(raster, cmap=C_MAP, interpolation='nearest')
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
    plt.legend(ncol=3)


def show_spectral_curve(tile_dict, tile_num,
                        title='Spectral curve for pixel #'):
    """Show a figure of the spectral curve."""
    x = np.linspace(404, 997, tile_dict["imagery"].shape[-1])
    if len(tile_dict["imagery"].shape) == 4:
        y = tile_dict["imagery"][tile_num, 0, 0, :]
        lbl = tile_dict["reference"][tile_num, 0, 0, :][0] + 1
    elif len(tile_dict["imagery"].shape) == 3:
        y = tile_dict["imagery"][tile_num, 0, :]
        lbl = tile_dict["reference"][tile_num] + 1
    else:
        print('The input data is in an incompatible shape.')

    plt.plot(x, y, label=f'{CLASS_NAMES[lbl]}')
    plt.title(f'{title} {tile_num}')
    plt.xlabel('Wavelength [nm]')
    plt.legend(bbox_to_anchor=(0.5, 0.89), loc='lower center')


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


def show_augment_spatial(tile_dict, tile_num, aug_funct):
    """Show a figure of the original and the augmented RGB composite."""
    img_rgb = tile_dict['imagery'][tile_num, [25, 15, 5], :, :]
    img_rgb_transposed = img_rgb.transpose((1, 2, 0))
    tile_gt = tile_dict['reference'][tile_num, :, :]
    plt.figure(figsize=[20, 5])

    plt.subplot(1, 4, 1)
    _image_show(img_rgb_transposed*20000, title='Original RGB composite')

    plt.subplot(1, 4, 2)
    img_hs = tile_dict['imagery'][tile_num, :, :, :]
    img_augmented, gt_augmented = aug_funct(torch.from_numpy(img_hs),
                                 torch.from_numpy(tile_gt[None, :, :]))
    print(img_augmented.shape)
    img_augmented_np = np.array(img_augmented)
    img_aug_trans = img_augmented_np[0, [25, 15, 5], :, :].transpose(1, 2, 0)

    _image_show(np.array(img_aug_trans)*20000, title='Augmented RGB composite')

    plt.subplot(1, 4, 3)
    _class_show(tile_gt, 'Original reference data')

    for label, color in zip(CLASS_NAMES, COLOR_LIST):
        plt.plot(0, 0, 's', label=label,
                 color=color, markeredgecolor='black')
    plt.subplot(1, 4, 4)
    _class_show(np.array(gt_augmented[0,:,:]), 'Augmented reference data')
    #plt.legend()

def show_augment_spectro_spatial(tile_dict, tile_num, aug_funct):
    """Show a figure of the original and the augmented RGB composite."""
    img_rgb = tile_dict['imagery'][tile_num, 0, [25, 15, 5], :, :]
    img_rgb_transposed = img_rgb.transpose((1, 2, 0))
    tile_gt = tile_dict['reference'][tile_num, :, :]
    plt.figure(figsize=[20, 5])

    plt.subplot(1, 4, 1)
    _image_show(img_rgb_transposed*20000, title='Original RGB composite')

    plt.subplot(1, 4, 2)
    img_hs = tile_dict['imagery'][tile_num, 0, :, :, :]
    img_augmented, gt_augmented = aug_funct(torch.from_numpy(img_hs),
                                 torch.from_numpy(tile_gt[None, :, :]))
    print(img_augmented.shape)
    img_augmented_np = np.array(img_augmented)
    img_aug_trans = img_augmented_np[0, 0, [25, 15, 5], :, :].transpose(1, 2, 0)

    _image_show(np.array(img_aug_trans)*20000, title='Augmented RGB composite')

    plt.subplot(1, 4, 3)
    _class_show(tile_gt, 'Original reference data')

    for label, color in zip(CLASS_NAMES, COLOR_LIST):
        plt.plot(0, 0, 's', label=label,
                 color=color, markeredgecolor='black')

    plt.subplot(1, 4, 4)
    _class_show(np.array(gt_augmented[0,:,:]), 'Augmented reference data')
    #plt.legend()


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


def sec_to_hms(sec):
    """Convert seconds to hours, minutes, seconds."""
    ty_res = gmtime(sec)
    res = strftime("%Hh, %Mm, %Ss", ty_res)
    return str(res)
