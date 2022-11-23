"""
Resample nii file
convert pixel spacing to normal

-- usage --
python resample.py input output_dir[optional]
input: directory or file
output: directory, if set output_dir, file will be saved in input directory
note: saved filename will be appended a flag : 'resampled'
"""

import SimpleITK as sitk
import numpy as np
import time
import sys
import glob
import os
from pathlib import Path


def para_input():
    print('--------------- task begin ------------')
    input_file = ''
    output_dir = ''
    files = []
    para_len = len(sys.argv)
    if 1 == para_len:
        print('usage: resample.py "input directory or file" "output directory"')
    elif 2 == para_len:
        input_file = sys.argv[1]
        print('Input file:', input_file)
        output_dir, basename = os.path.split(input_file)
    elif 3 == para_len:
        input_file = sys.argv[1]
        output_dir = sys.argv[2]
        if not (os.path.isdir(output_dir)):
            sys.exit('output is not directory')
        print("Input file:", input_file)
        print("Output dir:", output_dir)
    else:
        sys.exit('input error')

    if os.path.isdir(input_file):
        input_file += "//*.nii*"
        for fname in glob.glob(input_file, recursive=False):
            print("loading: {}".format(fname))
            files.append(fname)
        print('input file count: ', len(files))
    else:
        files.append(input_file)

    # resample and save
    for fname in files:
        dirname, filename = os.path.split(fname)
        print('-------- begin resample: ', filename)
        output_file = output_dir + '//' + filename.split('.nii')[0] + '_resampled.nii.gz'
        print('outfile: ', output_file)
        begin_time = time.time()
        resample_nii(fname, output_file)
        end_time = time.time()
        print('-------- finish resample, time-consuming: ', end_time - begin_time, 's')

    print('--------------- task finish ------------')


# resample image using new spacing
def resample_image(itk_image, out_spacing):
    original_spacing = itk_image.GetSpacing()
    original_size = itk_image.GetSize()

    # image size according to new spacing
    out_size = [
        int(np.round(original_size[0] * original_spacing[0] / out_spacing[0])),
        int(np.round(original_size[1] * original_spacing[1] / out_spacing[1])),
        int(np.round(original_size[2] * original_spacing[2] / out_spacing[2]))
    ]

    resample = sitk.ResampleImageFilter()
    resample.SetOutputSpacing(out_spacing)
    resample.SetSize(out_size)
    resample.SetOutputDirection(itk_image.GetDirection())
    resample.SetOutputOrigin(itk_image.GetOrigin())
    resample.SetTransform(sitk.Transform())
    resample.SetDefaultPixelValue(itk_image.GetPixelIDValue())

    resample.SetInterpolator(sitk.sitkBSpline)
    # print(resample)
    return resample.Execute(itk_image)


def resample_nii(input_path, out_file):
    original_img = sitk.ReadImage(input_path)
    resample_nii_image(original_img, out_file)


def resample_nii_image(nii_img, out_file):
    pix_spacing = nii_img.GetSpacing()
    print('Original image Spacing：', pix_spacing)
    print('Original image Size：', nii_img.GetSize())

    new_pix_spacing = [pix_spacing[0], pix_spacing[0], pix_spacing[0]]
    resample_img = resample_image(nii_img, new_pix_spacing)
    print('Resampled image Spacing：', resample_img.GetSpacing())
    print('Resampled image Size：', resample_img.GetSize())

    sitk.WriteImage(resample_img, out_file)


def convert_dcm2nii_resample(directory_path):
    reader = sitk.ImageSeriesReader()
    reader.MetaDataDictionaryArrayUpdateOn()
    reader.LoadPrivateTagsOn()
    series_IDs = sitk.ImageSeriesReader.GetGDCMSeriesIDs(directory_path)
    series_ID = series_IDs[1]
    dicom_names = reader.GetGDCMSeriesFileNames(directory_path, series_ID)
    reader.SetFileNames(dicom_names)
    image3D = reader.Execute()
    # determine if it is scout
    slice_number = 0
    # slice_keys = reader.GetMetaDataKeys(slice_number)
    # reader.HasMetaDataKey(slice_number, '0008|0008')
    meta_data = reader.GetMetaData(slice_number, '0008|0008')
    scout_flag = "LOCALIZER"
    if scout_flag in meta_data:
        return

    # resample
    path = Path(directory_path).parent
    resample_nii_image(image3D, r"C:\Datum\LocalData\AI\pic\result\001.nii.gz")


# dir_path = r"C:\Datum\LocalData\AI\pic\dcm\Series201"
dir_path = r"C:\Users\liw66\Downloads\Cadaver_H13099-CT_Full body_2019-05-17\DICOM 1 phase"
convert_dcm2nii_resample(dir_path)
