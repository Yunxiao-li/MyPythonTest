from nilearn.image import resample_img
import numpy as np
import nibabel as nib
import time

# imgpath = r'C:\Datum\LocalData\AI\pic\test\test_1.1_Crane_Helice_Sans_Inj_et_avec_Injectin-----Sans_DMPR_20060101000000_201.nii'
imgpath = r"C:\\Users\\liw66\\Downloads\\StandardPatientData_XK_Thorax_C-_Thorax_20150513192915_3.nii.gz"
timebegin = time.time()
img = nib.load(imgpath)
# print(img)
pixspace = img.header['pixdim']
print('pixel space: ', pixspace)

target_affine = np.diag((pixspace[1], pixspace[1], pixspace[1]))
new_img = resample_img(img, target_affine)
new_img.to_filename(r"C:\\Users\\liw66\\Downloads\\out9.nii.gz")
timeend = time.time()
print('run time: ', timeend-timebegin, 's')
print(new_img)
print('complete')
# gz_path = r"C:\\Users\\liw66\\Downloads\\StandardPatientData_XK_Thorax_C-_Thorax_20150513192915_3.nii.gz"
# # gz_path = r'C:\Datum\LocalData\AI\pic\test\test_1.1_Crane_Helice_Sans_Inj_et_avec_Injectin-----Sans_DMPR_20060101000000_201.nii'
