# encoding=utf8
"""
查看和显示nii文件
"""

import matplotlib

matplotlib.use('TkAgg')

from matplotlib import pylab as plt
import nibabel as nib
from nibabel import nifti1
from nibabel.viewers import OrthoSlicer3D

# example_filename = \
#     r"C:\\Datum\\LocalData\\AI\\pic\\test\\test_1.1_Crane_Helice_Sans_Inj_et_avec_Injectin-----Sans_DMPR_20060101000000_201a.nii.gz"
example_filename = \
    r"C:\\Users\\liw66\\Downloads\\StandardPatientData_XK_Thorax_C-_Thorax_20150513192915_3.nii.gz"

img = nib.load(example_filename)
# print(img)
print(img.header['pixdim'])
pixdim = img.header['pixdim']
print('pixdim[2]: ', format(pixdim[1]))
print(img.header['db_name'])  # 输出头信息

width, height, queue = img.dataobj.shape

OrthoSlicer3D(img.dataobj).show()

num = 1
# for i in range(0, queue, 10):
#     img_arr = img.dataobj[:, :, i]
#     plt.subplot(5, 4, num)
#     plt.imshow(img_arr, cmap='gray')
#     num += 1
#
# plt.show()
