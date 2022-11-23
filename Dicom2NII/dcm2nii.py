import dicom2nifti
import dicom2nifti.settings as settings
# infile = r"C:\\Datum\\LocalData\\AI\\pic\\test\\test_1.1_Crane_Helice_Sans_Inj_et_avec_Injectin-----Sans_DMPR_20060101000000_201a.nii.gz"
dicom_directory = r"C:\Datum\LocalData\AI\pic\test\Series201"
output_folder = r"C:\\Datum\\LocalData\\AI\\pic\\result"

# dicom2nifti.dicom_series_to_nifti(infile, outpath)
# settings.disable_validate_orthogonal()
settings.disable_validate_slice_increment()
settings.enable_resampling()
settings.set_resample_spline_interpolation_order(1)
settings.set_resample_padding(-1000)

dicom2nifti.convert_directory(dicom_directory, output_folder)
