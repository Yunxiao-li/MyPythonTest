python reorient_reference_to_rai.py --image_folder D:\VertebraeSeg\GUI\gui_test\images --output_folder D:\VertebraeSeg\GUI\gui_test\images_rai

python main_spine_localization.py --image_folder D:\VertebraeSeg\GUI\gui_test\images_rai --setup_folder D:\VertebraeSeg\GUI\gui_test\setup --model_files D:\VertebraeSeg\GUI\gui_test\pre_trained_model\spine_localization\model --output_folder D:\VertebraeSeg\GUI\gui_test\output

python main_vertebrae_localization.py --image_folder D:\VertebraeSeg\GUI\gui_test\images_rai --setup_folder D:\VertebraeSeg\GUI\gui_test\setup --model_files D:\VertebraeSeg\GUI\gui_test\pre_trained_model\vertebrae_localization\model --output_folder D:\VertebraeSeg\GUI\gui_test\output

python main_vertebrae_segmentation.py --image_folder D:\VertebraeSeg\GUI\gui_test\images_rai --setup_folder D:\VertebraeSeg\GUI\gui_test\setup --model_files D:\VertebraeSeg\GUI\gui_test\pre_trained_model\vertebrae_segmentation\model --output_folder D:\VertebraeSeg\GUI\gui_test\output


python reorient_prediction_to_reference.py --image_folder /tmp/vertebrae_segmentation --reference_folder /data --output_folder /data/results
