import math
import time
import os
import sys
import argparse

import PyQt5.QtWidgets as QtWidgets
import PyQt5.QtCore as Qt
from PyQt5.QtWidgets import QAction
from PyQt5.Qt import QFileDialog
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from vtkUtils import *
from config import *


class MainWindow(QtWidgets.QMainWindow, QtWidgets.QApplication):
    def __init__(self, app):
        self.app = app
        QtWidgets.QMainWindow.__init__(self, None)

        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("File")
        openImageAction = QAction('Load Image',self)
        openImageAction.triggered.connect(self.openfile)
        file_menu.addAction(openImageAction)

        openSegAction = QAction('Load Segmentation',self)
        openSegAction.triggered.connect(self.open_seg)
        file_menu.addAction(openSegAction)

        reinitAction = QAction('Refresh',self)
        reinitAction.triggered.connect(self.reinit)
        file_menu.addAction(reinitAction)
        
        # base setup
        self.renderer, self.frame, self.vtk_widget, self.interactor, self.render_window = self.setup()
        self.vertebra, self.mask = setup_vertebra(self.renderer, self.app.vertebra_FILE), setup_mask(self.renderer,
                                                                                            self.app.MASK_FILE)

        # setup vertebra projection and slicer
        self.vertebra_image_prop = setup_projection(self.vertebra, self.renderer)
        self.vertebra_slicer_props = setup_slicer(self.renderer, self.vertebra)  # causing issues with rotation
        self.slicer_widgets = []

        # vertebra pickers
        self.vertebra_threshold_sp = self.create_new_picker(self.vertebra.scalar_range[1], self.vertebra.scalar_range[0], 5.0,
                                                         sum(self.vertebra.scalar_range) / 2, self.vertebra_threshold_vc)
        self.vertebra_opacity_sp = self.create_new_picker(1.0, 0.0, 0.1, vertebra_OPACITY, self.vertebra_opacity_vc)
        self.vertebra_smoothness_sp = self.create_new_picker(1000, 100, 100, vertebra_SMOOTHNESS, self.vertebra_smoothness_vc)
        self.vertebra_lut_sp = self.create_new_picker(3.0, 0.0, 0.1, 2.0, self.lut_value_changed)
        self.vertebra_projection_cb = self.add_vertebra_projection()
        self.vertebra_slicer_cb = self.add_vertebra_slicer()

        # mask pickers
        self.mask_opacity_sp = self.create_new_picker(1.0, 0.0, 0.1, MASK_OPACITY, self.mask_opacity_vc)
        self.mask_smoothness_sp = self.create_new_picker(1000, 100, 100, MASK_SMOOTHNESS, self.mask_smoothness_vc)
        self.mask_label_cbs = []

        # create grid for all widgets
        self.grid = QtWidgets.QGridLayout()

        # add each widget
        self.add_vtk_window_widget()
        self.add_vertebra_settings_widget()
        #self.add_mask_settings_widget()
        self.add_views_widget()

        #  set layout and show
        self.render_window.Render()
        self.setWindowTitle(APPLICATION_TITLE)
        self.frame.setLayout(self.grid)
        self.setCentralWidget(self.frame)
        self.set_axial_view()
        self.interactor.Initialize()
        self.show()

    def openfile(self):
        openfile_name = QFileDialog.getOpenFileName(self,'Select File','','NIfTI File(*.nii , *.nii.gz)')
        self.image_name = openfile_name[0]

    def open_seg(self):
        open_seg_name = QFileDialog.getOpenFileName(self,'Select File','','NIfTI File(*.nii , *.nii.gz)')
        self.seg_name = open_seg_name[0]

    def reinit(self):
        # base setup
        self.renderer, self.frame, self.vtk_widget, self.interactor, self.render_window = self.setup()
        self.vertebra, self.mask = setup_vertebra(self.renderer, self.image_name), setup_mask(self.renderer,
                                                                                            self.seg_name)

        # setup vertebra projection and slicer
        self.vertebra_image_prop = setup_projection(self.vertebra, self.renderer)
        self.vertebra_slicer_props = setup_slicer(self.renderer, self.vertebra)  # causing issues with rotation
        self.slicer_widgets = []

        # vertebra pickers
        self.vertebra_threshold_sp = self.create_new_picker(self.vertebra.scalar_range[1], self.vertebra.scalar_range[0], 5.0,
                                                         sum(self.vertebra.scalar_range) / 2, self.vertebra_threshold_vc)
        self.vertebra_opacity_sp = self.create_new_picker(1.0, 0.0, 0.1, vertebra_OPACITY, self.vertebra_opacity_vc)
        self.vertebra_smoothness_sp = self.create_new_picker(1000, 100, 100, vertebra_SMOOTHNESS, self.vertebra_smoothness_vc)
        self.vertebra_lut_sp = self.create_new_picker(3.0, 0.0, 0.1, 2.0, self.lut_value_changed)
        self.vertebra_projection_cb = self.add_vertebra_projection()
        self.vertebra_slicer_cb = self.add_vertebra_slicer()

        # mask pickers
        self.mask_opacity_sp = self.create_new_picker(1.0, 0.0, 0.1, MASK_OPACITY, self.mask_opacity_vc)
        self.mask_smoothness_sp = self.create_new_picker(1000, 100, 100, MASK_SMOOTHNESS, self.mask_smoothness_vc)
        self.mask_label_cbs = []

        # create grid for all widgets
        self.grid = QtWidgets.QGridLayout()

        # add each widget
        self.add_vtk_window_widget()
        self.add_vertebra_settings_widget()
        #self.add_mask_settings_widget()
        self.add_views_widget()

        #  set layout and show
        self.render_window.Render()
        self.setWindowTitle(APPLICATION_TITLE)
        self.frame.setLayout(self.grid)
        self.setCentralWidget(self.frame)
        self.set_axial_view()
        self.interactor.Initialize()
        self.show()

    def reorient(self):
        output_folder ="reoriented"
        reorient_command = r"python D:\VertebraeSeg\GUI\inference_scripts\reorient.py --image " + self.image_name + r" --output_folder " + output_folder
        print(reorient_command)
        os.system(reorient_command)
    
    def spine_localization(self):
        script_path = r"D:\VertebraeSeg\GUI\inference_scripts\main_spine_localization.py"
        image_folder_path = r"D:\VertebraeSeg\GUI\3d-nii-visualizer-master\visualizer\reoriented"
        setup_folder_path = r"D:\VertebraeSeg\GUI\3d-nii-visualizer-master\visualizer\setup"
        model_files_path = r"D:\VertebraeSeg\GUI\gui_test\pre_trained_model\spine_localization\model"
        output_folder_path = r"D:\VertebraeSeg\GUI\3d-nii-visualizer-master\visualizer\output"
        spine_localization_commmand = "python " + script_path + " --image_folder " + image_folder_path + " --setup_folder " + setup_folder_path\
                                      + " --model_files " + model_files_path + " --output_folder " + output_folder_path
        print(spine_localization_commmand)
        os.system(spine_localization_commmand)
    
    def ver_localization(self):
        script_path = r"D:\VertebraeSeg\GUI\inference_scripts\main_vertebrae_localization.py"
        image_folder_path = r"D:\VertebraeSeg\GUI\3d-nii-visualizer-master\visualizer\reoriented"
        setup_folder_path = r"D:\VertebraeSeg\GUI\3d-nii-visualizer-master\visualizer\setup"
        model_files_path = r"D:\VertebraeSeg\GUI\gui_test\pre_trained_model\vertebrae_localization\model"
        output_folder_path = r"D:\VertebraeSeg\GUI\3d-nii-visualizer-master\visualizer\output"
        ver_localization_commmand = "python " + script_path + " --image_folder " + image_folder_path + " --setup_folder " + setup_folder_path\
                                      + " --model_files " + model_files_path + " --output_folder " + output_folder_path
        print(ver_localization_commmand)
        os.system(ver_localization_commmand)
    
    def ver_segmentation(self):
        script_path = r"D:\VertebraeSeg\GUI\inference_scripts\main_vertebrae_segmentation.py"
        image_folder_path = r"D:\VertebraeSeg\GUI\3d-nii-visualizer-master\visualizer\reoriented"
        setup_folder_path = r"D:\VertebraeSeg\GUI\3d-nii-visualizer-master\visualizer\setup"
        model_files_path = r"D:\VertebraeSeg\GUI\gui_test\pre_trained_model\vertebrae_segmentation\model"
        output_folder_path = r"D:\VertebraeSeg\GUI\3d-nii-visualizer-master\visualizer\output"
        ver_segmentation_commmand = "python " + script_path + " --image_folder " + image_folder_path + " --setup_folder " + setup_folder_path\
                                      + " --model_files " + model_files_path + " --output_folder " + output_folder_path
        print(ver_segmentation_commmand)
        os.system(ver_segmentation_commmand)

    @staticmethod
    def setup():
        """
        Create and setup the base vtk and Qt objects for the application
        """
        renderer = vtk.vtkRenderer()
        frame = QtWidgets.QFrame()
        vtk_widget = QVTKRenderWindowInteractor()
        interactor = vtk_widget.GetRenderWindow().GetInteractor()
        render_window = vtk_widget.GetRenderWindow()

        frame.setAutoFillBackground(True)
        vtk_widget.GetRenderWindow().AddRenderer(renderer)
        render_window.AddRenderer(renderer)
        interactor.SetRenderWindow(render_window)
        interactor.SetInteractorStyle(vtk.vtkInteractorStyleTrackballCamera())

        # required to enable overlapping actors with opacity < 1.0
        # this is causing some issues with flashing objects
        # render_window.SetAlphaBitPlanes(1)
        # render_window.SetMultiSamples(0)
        # renderer.UseDepthPeelingOn()
        # renderer.SetMaximumNumberOfPeels(2)

        return renderer, frame, vtk_widget, interactor, render_window

    def lut_value_changed(self):
        lut = self.vertebra.image_mapper.GetLookupTable()
        new_lut_value = self.vertebra_lut_sp.value()
        lut.SetValueRange(0.0, new_lut_value)
        lut.Build()
        self.vertebra.image_mapper.SetLookupTable(lut)
        self.vertebra.image_mapper.Update()
        self.render_window.Render()

    def add_vertebra_slicer(self):
        slicer_cb = QtWidgets.QCheckBox("Slicer")
        slicer_cb.clicked.connect(self.vertebra_slicer_vc)
        return slicer_cb

    def add_vtk_window_widget(self):
        base_vertebra_file = os.path.basename(self.app.vertebra_FILE)
        base_mask_file = os.path.basename(self.app.MASK_FILE)

        '''object_title = "Vertebrae: {0} (min: {1:.2f}, max: {2:.2f})        Mask: {3}".format(base_vertebra_file,
                                                                                         self.vertebra.scalar_range[0],
                                                                                         self.vertebra.scalar_range[1],
                                                                                         base_mask_file)'''

        object_title = "Vertebrae: {0}         Mask: {3}".format(base_vertebra_file,
                                                                                         self.vertebra.scalar_range[0],
                                                                                         self.vertebra.scalar_range[1],
                                                                                         base_mask_file)
                                                                                                                                                             
        object_group_box = QtWidgets.QGroupBox(object_title)
        object_layout = QtWidgets.QVBoxLayout()
        object_layout.addWidget(self.vtk_widget)
        object_group_box.setLayout(object_layout)
        self.grid.addWidget(object_group_box, 0, 2, 5, 5)
        # must manually set column width for vtk_widget to maintain height:width ratio
        self.grid.setColumnMinimumWidth(2, 700)

    def add_vertebra_settings_widget(self):
        vertebra_group_box = QtWidgets.QGroupBox("")
        vertebra_group_layout = QtWidgets.QGridLayout()
        #vertebra_group_layout.addWidget(QtWidgets.QLabel("Vertebrae Threshold"), 0, 0)
        #vertebra_group_layout.addWidget(QtWidgets.QLabel("Vertebrae Opacity"), 1, 0)
        #vertebra_group_layout.addWidget(QtWidgets.QLabel("Vertebrae Smoothness"), 2, 0)
        #vertebra_group_layout.addWidget(QtWidgets.QLabel("Image Intensity"), 3, 0)
        #vertebra_group_layout.addWidget(self.vertebra_threshold_sp, 0, 1, 1, 2)
        #vertebra_group_layout.addWidget(self.vertebra_opacity_sp, 1, 1, 1, 2)
        #vertebra_group_layout.addWidget(self.vertebra_smoothness_sp, 2, 1, 1, 2)
        #vertebra_group_layout.addWidget(self.vertebra_lut_sp, 3, 1, 1, 2)
        

        self.reorient_button = QtWidgets.QPushButton(self)
        vertebra_group_layout.addWidget(self.reorient_button,1,0)
        self.reorient_button.setObjectName("reorient")
        self.reorient_button.setText("reorient")
        self.reorient_button.clicked.connect(self.reorient)
        self.image_name = ""
        
        self.spine_loc_button = QtWidgets.QPushButton(self)
        vertebra_group_layout.addWidget(self.spine_loc_button,1,1)
        self.spine_loc_button.setObjectName("spine_localization")
        self.spine_loc_button.setText("spine_localization")
        self.spine_loc_button.clicked.connect(self.spine_localization)

        self.ver_loc_button = QtWidgets.QPushButton(self)
        vertebra_group_layout.addWidget(self.ver_loc_button)
        self.ver_loc_button.setObjectName("vertebrae_localization")
        self.ver_loc_button.setText("vertebrae_localization")
        self.ver_loc_button.clicked.connect(self.ver_localization)

        self.ver_seg_button = QtWidgets.QPushButton(self)
        vertebra_group_layout.addWidget(self.ver_seg_button)
        self.ver_seg_button.setObjectName("vertebrae_segmentation")
        self.ver_seg_button.setText("vertebrae_segmentation")
        self.ver_seg_button.clicked.connect(self.ver_segmentation)
        
        vertebra_group_layout.addWidget(self.create_new_separator(), 3, 0, 1, 3)

        vertebra_group_layout.addWidget(self.vertebra_projection_cb, 4, 0)
        vertebra_group_layout.addWidget(self.vertebra_slicer_cb, 4, 1)

        vertebra_group_layout.addWidget(self.create_new_separator(), 5, 0, 1, 3)
        vertebra_group_layout.addWidget(QtWidgets.QLabel("Axial Slice"), 6, 0)
        vertebra_group_layout.addWidget(QtWidgets.QLabel("Coronal Slice"), 7, 0)
        vertebra_group_layout.addWidget(QtWidgets.QLabel("Sagittal Slice"), 8, 0)

        # order is important
        slicer_funcs = [self.axial_slice_changed, self.coronal_slice_changed, self.sagittal_slice_changed]
        current_label_row = 6
        # data extent is array [xmin, xmax, ymin, ymax, zmin, zmax)
        # we want all the max values for the range
        extent_index = 5
        for func in slicer_funcs:
            slice_widget = QtWidgets.QSlider(Qt.Qt.Horizontal)
            slice_widget.setDisabled(True)
            self.slicer_widgets.append(slice_widget)
            vertebra_group_layout.addWidget(slice_widget, current_label_row, 1, 1, 2)
            slice_widget.valueChanged.connect(func)
            slice_widget.setRange(self.vertebra.extent[extent_index - 1], self.vertebra.extent[extent_index])
            slice_widget.setValue(self.vertebra.extent[extent_index] / 2)
            current_label_row += 1
            extent_index -= 2

        vertebra_group_box.setLayout(vertebra_group_layout)
        self.grid.addWidget(vertebra_group_box, 0, 0, 1, 2)

    def axial_slice_changed(self):
        pos = self.slicer_widgets[0].value()
        self.vertebra_slicer_props[0].SetDisplayExtent(self.vertebra.extent[0], self.vertebra.extent[1], self.vertebra.extent[2],
                                                    self.vertebra.extent[3], pos, pos)
        self.render_window.Render()

    def coronal_slice_changed(self):
        pos = self.slicer_widgets[1].value()
        self.vertebra_slicer_props[1].SetDisplayExtent(self.vertebra.extent[0], self.vertebra.extent[1], pos, pos,
                                                    self.vertebra.extent[4], self.vertebra.extent[5])
        self.render_window.Render()

    def sagittal_slice_changed(self):
        pos = self.slicer_widgets[2].value()
        self.vertebra_slicer_props[2].SetDisplayExtent(pos, pos, self.vertebra.extent[2], self.vertebra.extent[3],
                                                    self.vertebra.extent[4], self.vertebra.extent[5])
        self.render_window.Render()

    def add_mask_settings_widget(self):
        mask_settings_group_box = QtWidgets.QGroupBox("Mask Settings")
        mask_settings_layout = QtWidgets.QGridLayout()
        mask_settings_layout.addWidget(QtWidgets.QLabel("Mask Opacity"), 0, 0)
        mask_settings_layout.addWidget(QtWidgets.QLabel("Mask Smoothness"), 1, 0)
        mask_settings_layout.addWidget(self.mask_opacity_sp, 0, 1)
        mask_settings_layout.addWidget(self.mask_smoothness_sp, 1, 1)
        mask_multi_color_radio = QtWidgets.QRadioButton("Multi Color")
        mask_multi_color_radio.setChecked(True)
        mask_multi_color_radio.clicked.connect(self.mask_multi_color_radio_checked)
        mask_single_color_radio = QtWidgets.QRadioButton("Single Color")
        mask_single_color_radio.clicked.connect(self.mask_single_color_radio_checked)
        mask_settings_layout.addWidget(mask_multi_color_radio, 2, 0)
        mask_settings_layout.addWidget(mask_single_color_radio, 2, 1)
        mask_settings_layout.addWidget(self.create_new_separator(), 3, 0, 1, 2)

        self.mask_label_cbs = []
        c_col, c_row = 0, 4  # c_row must always be (+1) of last row
        for i in range(1, 11):
            self.mask_label_cbs.append(QtWidgets.QCheckBox("Label {}".format(i)))
            mask_settings_layout.addWidget(self.mask_label_cbs[i - 1], c_row, c_col)
            c_row = c_row + 1 if c_col == 1 else c_row
            c_col = 0 if c_col == 1 else 1

        mask_settings_group_box.setLayout(mask_settings_layout)
        self.grid.addWidget(mask_settings_group_box, 1, 0, 2, 2)

        for i, cb in enumerate(self.mask_label_cbs):
            if i < len(self.mask.labels) and self.mask.labels[i].actor:
                cb.setChecked(True)
                cb.clicked.connect(self.mask_label_checked)
            else:
                cb.setDisabled(True)

    def add_views_widget(self):
        axial_view = QtWidgets.QPushButton("Axial")
        coronal_view = QtWidgets.QPushButton("Coronal")
        sagittal_view = QtWidgets.QPushButton("Sagittal")
        views_box = QtWidgets.QGroupBox("Views")
        views_box_layout = QtWidgets.QVBoxLayout()
        views_box_layout.addWidget(axial_view)
        views_box_layout.addWidget(coronal_view)
        views_box_layout.addWidget(sagittal_view)
        views_box.setLayout(views_box_layout)
        self.grid.addWidget(views_box, 2, 0, 2, 2)
        axial_view.clicked.connect(self.set_axial_view)
        coronal_view.clicked.connect(self.set_coronal_view)
        sagittal_view.clicked.connect(self.set_sagittal_view)

    @staticmethod
    def create_new_picker(max_value, min_value, step, picker_value, value_changed_func):
        if isinstance(max_value, int):
            picker = QtWidgets.QSpinBox()
        else:
            picker = QtWidgets.QDoubleSpinBox()

        picker.setMaximum(max_value)
        picker.setMinimum(min_value)
        picker.setSingleStep(step)
        picker.setValue(picker_value)
        picker.valueChanged.connect(value_changed_func)
        return picker

    def add_vertebra_projection(self):
        projection_cb = QtWidgets.QCheckBox("Projection")
        projection_cb.clicked.connect(self.vertebra_projection_vc)
        return projection_cb

    def mask_label_checked(self):
        for i, cb in enumerate(self.mask_label_cbs):
            if cb.isChecked():
                self.mask.labels[i].property.SetOpacity(self.mask_opacity_sp.value())
            elif cb.isEnabled():  # labels without data are disabled
                self.mask.labels[i].property.SetOpacity(0)
        self.render_window.Render()

    def mask_single_color_radio_checked(self):
        for label in self.mask.labels:
            if label.property:
                label.property.SetColor(MASK_COLORS[0])
        self.render_window.Render()

    def mask_multi_color_radio_checked(self):
        for label in self.mask.labels:
            if label.property:
                label.property.SetColor(label.color)
        self.render_window.Render()

    def vertebra_projection_vc(self):
        projection_checked = self.vertebra_projection_cb.isChecked()
        self.vertebra_slicer_cb.setDisabled(projection_checked)  # disable slicer checkbox, cant use both at same time
        self.vertebra_image_prop.SetOpacity(projection_checked)
        self.render_window.Render()

    def vertebra_slicer_vc(self):
        slicer_checked = self.vertebra_slicer_cb.isChecked()

        for widget in self.slicer_widgets:
            widget.setEnabled(slicer_checked)

        self.vertebra_projection_cb.setDisabled(slicer_checked)  # disable projection checkbox, cant use both at same time
        for prop in self.vertebra_slicer_props:
            prop.GetProperty().SetOpacity(slicer_checked)
        self.render_window.Render()

    def vertebra_opacity_vc(self):
        opacity = round(self.vertebra_opacity_sp.value(), 2)
        self.vertebra.labels[0].property.SetOpacity(opacity)
        self.render_window.Render()

    def vertebra_threshold_vc(self):
        self.process_changes()
        threshold = self.vertebra_threshold_sp.value()
        self.vertebra.labels[0].extractor.SetValue(0, threshold)
        self.render_window.Render()

    def vertebra_smoothness_vc(self):
        self.process_changes()
        smoothness = self.vertebra_smoothness_sp.value()
        self.vertebra.labels[0].smoother.SetNumberOfIterations(smoothness)
        self.render_window.Render()

    def mask_opacity_vc(self):
        opacity = round(self.mask_opacity_sp.value(), 2)
        for i, label in enumerate(self.mask.labels):
            if label.property and self.mask_label_cbs[i].isChecked():
                label.property.SetOpacity(opacity)
        self.render_window.Render()

    def mask_smoothness_vc(self):
        self.process_changes()
        smoothness = self.mask_smoothness_sp.value()
        for label in self.mask.labels:
            if label.smoother:
                label.smoother.SetNumberOfIterations(smoothness)
        self.render_window.Render()

    def set_axial_view(self):
        self.renderer.ResetCamera()
        fp = self.renderer.GetActiveCamera().GetFocalPoint()
        p = self.renderer.GetActiveCamera().GetPosition()
        dist = math.sqrt((p[0] - fp[0]) ** 2 + (p[1] - fp[1]) ** 2 + (p[2] - fp[2]) ** 2)
        self.renderer.GetActiveCamera().SetPosition(fp[0], fp[1], fp[2] + dist)
        self.renderer.GetActiveCamera().SetViewUp(0.0, 1.0, 0.0)
        self.renderer.GetActiveCamera().Zoom(1.8)
        self.render_window.Render()

    def set_coronal_view(self):
        self.renderer.ResetCamera()
        fp = self.renderer.GetActiveCamera().GetFocalPoint()
        p = self.renderer.GetActiveCamera().GetPosition()
        dist = math.sqrt((p[0] - fp[0]) ** 2 + (p[1] - fp[1]) ** 2 + (p[2] - fp[2]) ** 2)
        self.renderer.GetActiveCamera().SetPosition(fp[0], fp[2] - dist, fp[1])
        self.renderer.GetActiveCamera().SetViewUp(0.0, 0.5, 0.5)
        self.renderer.GetActiveCamera().Zoom(1.8)
        self.render_window.Render()

    def set_sagittal_view(self):
        self.renderer.ResetCamera()
        fp = self.renderer.GetActiveCamera().GetFocalPoint()
        p = self.renderer.GetActiveCamera().GetPosition()
        dist = math.sqrt((p[0] - fp[0]) ** 2 + (p[1] - fp[1]) ** 2 + (p[2] - fp[2]) ** 2)
        self.renderer.GetActiveCamera().SetPosition(fp[2] + dist, fp[0], fp[1])
        self.renderer.GetActiveCamera().SetViewUp(0.0, 0.0, 1.0)
        self.renderer.GetActiveCamera().Zoom(1.6)
        self.render_window.Render()

    @staticmethod
    def create_new_separator():
        horizontal_line = QtWidgets.QWidget()
        horizontal_line.setFixedHeight(1)
        horizontal_line.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        horizontal_line.setStyleSheet("background-color: #c8c8c8;")
        return horizontal_line

    def process_changes(self):
        for _ in range(10):
            self.app.processEvents()
            time.sleep(0.1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Reads Nii.gz Files and renders them in 3D.')
    parser.add_argument('-i')
    parser.add_argument('-m')

    args = parser.parse_args()
    print(args)
    app = QtWidgets.QApplication(sys.argv)

    app.vertebra_FILE = args.i
    app.MASK_FILE = args.m
    window = MainWindow(app)
    sys.exit(app.exec_())