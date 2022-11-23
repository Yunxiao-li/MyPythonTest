import matplotlib.pyplot as plt
import SimpleITK as sitk


def read_nii_file2(img_path):
    """
    根据nii文件路径读取nii图像
    """
    nii_image = sitk.ReadImage(img_path)
    return nii_image

def Resampling(img,lable = False):
    original_size = img.GetSaacing()
    original_spacing = img.GetSpacing() #获取图像原始分辨率
    new_spacing = [1, 1, 1] #设置图像新的分辨率为1*1*1

    new_size = [int(round(original_size[0] * (original_spacing[0] /1))),
                int(round(original_size[1] * (original_spacing[1] / 1))),
                int(round(original_size[2] * (original_spacing[2] / 1)))] #计算图像在新的分辨率下尺寸大小
    resampleSliceFilter = sitk.ResampleImageFilter() #初始化
    if lable == False:
        Resampleimage = resampleSliceFilter.Execute(img, new_size, sitk.Transform(), sitk.sitkBSpline,
                                                img.GetOrigin(), new_spacing, img.GetDirection(), 0,
                                                img.GetPixelIDValue())
        ResampleimageArray = sitk.GetArrayFromImage(Resampleimage)
        ResampleimageArray[ResampleimageArray < 0] = 0 #将图中小于0的元素置为0
    else:# for label, should use sitk.sitkLinear to make sure the original and resampled label are the same!!!
        Resampleimage = resampleSliceFilter.Execute(img, new_size, sitk.Transform(), sitk.sitkLinear,
                                                    img.GetOrigin(), new_spacing, img.GetDirection(), 0,
                                                    img.GetPixelIDValue())
        ResampleimageArray = sitk.GetArrayFromImage(Resampleimage)
        return ResampleimageArray


def nii_one_slice2(image):
    """
    显示nii image中的其中1张slice
    """
    # C,H,W
    # SimpleITK读出的image的data的数组顺序为：Channel,Height，Width
    image_arr = sitk.GetArrayFromImage(image)
    print(type(image_arr))
    print(image_arr.shape)
    image_2d = image_arr[:, 585, :]
    spimg = Resampling(image_2d)
    plt.imshow(spimg, cmap='gray')
    plt.show()

niipath = r"C:\\Users\\liw66\\Downloads\\StandardPatientData_XK_Thorax_C-_Thorax_20150513192915_3.nii.gz"
nii_image2 = read_nii_file2(niipath)
nii_one_slice2(nii_image2)


# def resample(image, scan, new_spacing=[1, 1, 1]):
#     image = imgs_to_process
#     scan = patient
#     # Determine current pixel spacing
#     spacing = map(float, ([scan[0].SliceThickness] + list(scan[0].PixelSpacing)))
#     spacing = np.array(list(spacing))
#
#     resize_factor = spacing / new_spacing
#
#     new_real_shape = image.shape * resize_factor
#
#     new_shape = np.round(new_real_shape)
#
#     real_resize_factor = new_shape / image.shape
#
#     new_spacing = spacing / real_resize_factor
#
#     image = scipy.ndimage.interpolation.zoom(image, real_resize_factor)
#
#     return image, new_spacing
#
#
# print("Shape before resampling\t", tosmlimage.shape)  # Shape before resampling  (129, 512, 512)
# imgs_after_resamp, spacing = resample(tosmlimage, patient, [1, 1, 1])
# print("Shape after resampling\t", imgs_after_resamp.shape)  # Shape after resampling   (206, 292, 292)
# plt.imshow(imgs_after_resamp, cmap='gray')
# plt.show()

