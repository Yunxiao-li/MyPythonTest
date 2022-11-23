import vtk
from ErrorObserver import *
from NiiObject import *
from config import *
from NiiLabel import *

error_observer = ErrorObserver()

'''
VTK Pipeline:   reader ->
                extractor -> 
                decimate -> 
                smoother -> 
                normalizer -> 
                mapper
'''


def read_volume(file_name):
    """
    :param file_name: The filename of type 'nii.gz'
    :return: vtkNIFTIImageReader (https://www.vtk.org/doc/nightly/html/classvtkNIFTIImageReader.html)
    """
    reader = vtk.vtkNIFTIImageReader()
    reader.SetFileNameSliceOffset(1)
    reader.SetDataByteOrderToBigEndian()
    reader.SetFileName(file_name)
    reader.Update()
    return reader


def create_vertebra_extractor(vertebra):
    """
    Given the output from vertebra (vtkNIFTIImageReader) extract it into 3D using
    vtkFlyingEdges3D algorithm (https://www.vtk.org/doc/nightly/html/classvtkFlyingEdges3D.html)
    :param vertebra: a vtkNIFTIImageReader volume containing the vertebra
    :return: the extracted volume from vtkFlyingEdges3D
    """
    vertebra_extractor = vtk.vtkFlyingEdges3D()
    vertebra_extractor.SetInputConnection(vertebra.reader.GetOutputPort())
    # vertebra_extractor.SetValue(0, sum(vertebra.scalar_range)/2)
    return vertebra_extractor


def create_mask_extractor(mask):
    """
    Given the output from mask (vtkNIFTIImageReader) extract it into 3D using
    vtkDiscreteMarchingCubes algorithm (https://www.vtk.org/doc/release/5.0/html/a01331.html).
    This algorithm is specialized for reading segmented volume labels.
    :param mask: a vtkNIFTIImageReader volume containing the mask
    :return: the extracted volume from vtkDiscreteMarchingCubes
    """
    mask_extractor = vtk.vtkDiscreteMarchingCubes()
    mask_extractor.SetInputConnection(mask.reader.GetOutputPort())
    return mask_extractor


def create_polygon_reducer(extractor):
    """
    Reduces the number of polygons (triangles) in the volume. This is used to speed up rendering.
    (https://www.vtk.org/doc/nightly/html/classvtkDecimatePro.html)
    :param extractor: an extractor (vtkPolyDataAlgorithm), will be either vtkFlyingEdges3D or vtkDiscreteMarchingCubes
    :return: the decimated volume
    """
    reducer = vtk.vtkDecimatePro()
    reducer.AddObserver('ErrorEvent', error_observer)  # throws an error event if there is no data to decimate
    reducer.SetInputConnection(extractor.GetOutputPort())
    reducer.SetTargetReduction(0.5)  # magic number
    reducer.PreserveTopologyOn()
    return reducer


def create_smoother(reducer, smoothness):
    """
    Reorients some points in the volume to smooth the render edges.
    (https://www.vtk.org/doc/nightly/html/classvtkSmoothPolyDataFilter.html)
    :param reducer:
    :param smoothness:
    :return:
    """
    smoother = vtk.vtkSmoothPolyDataFilter()
    smoother.SetInputConnection(reducer.GetOutputPort())
    smoother.SetNumberOfIterations(smoothness)
    return smoother


def create_normals(smoother):
    """
    The filter can reorder polygons to insure consistent orientation across polygon neighbors. Sharp edges can be split
    and points duplicated with separate normals to give crisp (rendered) surface definition.
    (https://www.vtk.org/doc/nightly/html/classvtkPolyDataNormals.html)
    :param smoother:
    :return:
    """
    vertebra_normals = vtk.vtkPolyDataNormals()
    vertebra_normals.SetInputConnection(smoother.GetOutputPort())
    vertebra_normals.SetFeatureAngle(60.0)  #
    return vertebra_normals


def create_mapper(stripper):
    vertebra_mapper = vtk.vtkPolyDataMapper()
    vertebra_mapper.SetInputConnection(stripper.GetOutputPort())
    vertebra_mapper.ScalarVisibilityOff()
    vertebra_mapper.Update()
    return vertebra_mapper


def create_property(opacity, color):
    prop = vtk.vtkProperty()
    prop.SetColor(color[0], color[1], color[2])
    prop.SetOpacity(opacity)
    return prop


def create_actor(mapper, prop):
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.SetProperty(prop)
    return actor


def create_mask_table():
    m_mask_opacity = 1
    vertebra_lut = vtk.vtkLookupTable()
    vertebra_lut.SetRange(0, 4)
    vertebra_lut.SetRampToLinear()
    vertebra_lut.SetValueRange(0, 1)
    vertebra_lut.SetHueRange(0, 0)
    vertebra_lut.SetSaturationRange(0, 0)

    #vertebra_lut.SetNumberOfTableValues(28)
    vertebra_lut.SetTableRange(0, 27)
    vertebra_lut.SetTableValue(0, 0, 0, 0, 0)
    vertebra_lut.SetTableValue(1, 1, 0, 0, m_mask_opacity)  # RED
    vertebra_lut.SetTableValue(2, 0, 1, 0, m_mask_opacity)  # GREEN
    vertebra_lut.SetTableValue(3, 1, 1, 0, m_mask_opacity)  # YELLOW
    vertebra_lut.SetTableValue(4, 0, 0, 1, m_mask_opacity)  # BLUE
    vertebra_lut.SetTableValue(5, 1, 0, 1, m_mask_opacity)  # MAGENTA
    vertebra_lut.SetTableValue(6, 0, 1, 1, m_mask_opacity)  # CYAN
    vertebra_lut.SetTableValue(7, 1, 0.5, 0.5, m_mask_opacity)  # RED_2
    vertebra_lut.SetTableValue(8, 0.5, 1, 0.5, m_mask_opacity)  # GREEN_2
    vertebra_lut.SetTableValue(9, 0.5, 0.5, 1, m_mask_opacity)  # BLUE_2
    
    vertebra_lut.SetTableValue(10, 1, 0, 0, m_mask_opacity)  # RED
    vertebra_lut.SetTableValue(11, 0, 1, 0, m_mask_opacity)  # GREEN
    vertebra_lut.SetTableValue(12, 1, 1, 0, m_mask_opacity)  # YELLOW
    vertebra_lut.SetTableValue(13, 0, 0, 1, m_mask_opacity)  # BLUE
    vertebra_lut.SetTableValue(14,1, 0, 1, m_mask_opacity)  # MAGENTA
    vertebra_lut.SetTableValue(15, 0, 1, 1, m_mask_opacity)  # CYAN
    vertebra_lut.SetTableValue(16, 1, 0.5, 0.5, m_mask_opacity)  # RED_2
    vertebra_lut.SetTableValue(17, 0.5, 1, 0.5, m_mask_opacity)  # GREEN_2
    vertebra_lut.SetTableValue(18, 0.5, 0.5, 1, m_mask_opacity)  # BLUE_2

    vertebra_lut.SetTableValue(19, 1, 0, 0, m_mask_opacity)  # RED
    vertebra_lut.SetTableValue(20, 0, 1, 0, m_mask_opacity)  # GREEN
    vertebra_lut.SetTableValue(21, 1, 1, 0, m_mask_opacity)  # YELLOW
    vertebra_lut.SetTableValue(22, 0, 0, 1, m_mask_opacity)  # BLUE
    vertebra_lut.SetTableValue(23, 1, 0, 1, m_mask_opacity)  # MAGENTA
    vertebra_lut.SetTableValue(24, 0, 1, 1, m_mask_opacity)  # CYAN
    vertebra_lut.SetTableValue(25, 1, 0.5, 0.5, m_mask_opacity)  # RED_2
    vertebra_lut.SetTableValue(26, 0.5, 1, 0.5, m_mask_opacity)  # GREEN_2
    vertebra_lut.SetTableValue(27, 0.5, 0.5, 1, m_mask_opacity)  # BLUE_2
    vertebra_lut.Build()
    return vertebra_lut


def create_table():
    table = vtk.vtkLookupTable()
    table.SetRange(0.0, 1675.0)  # +1
    table.SetRampToLinear()
    table.SetValueRange(0, 1)
    table.SetHueRange(0, 0)
    table.SetSaturationRange(0, 0)


def add_surface_rendering(nii_object, label_idx, label_value):
    nii_object.labels[label_idx].extractor.SetValue(0, label_value)
    nii_object.labels[label_idx].extractor.Update()

    # if the cell size is 0 then there is no label_idx data
    if nii_object.labels[label_idx].extractor.GetOutput().GetMaxCellSize():
        reducer = create_polygon_reducer(nii_object.labels[label_idx].extractor)
        smoother = create_smoother(reducer, nii_object.labels[label_idx].smoothness)
        normals = create_normals(smoother)
        actor_mapper = create_mapper(normals)
        actor_property = create_property(nii_object.labels[label_idx].opacity, nii_object.labels[label_idx].color)
        actor = create_actor(actor_mapper, actor_property)
        nii_object.labels[label_idx].actor = actor
        nii_object.labels[label_idx].smoother = smoother
        nii_object.labels[label_idx].property = actor_property


def setup_slicer(renderer, vertebra):
    x = vertebra.extent[1]
    y = vertebra.extent[3]
    z = vertebra.extent[5]

    axial = vtk.vtkImageActor()
    axial_prop = vtk.vtkImageProperty()
    axial_prop.SetOpacity(0)
    axial.SetProperty(axial_prop)
    axial.GetMapper().SetInputConnection(vertebra.image_mapper.GetOutputPort())
    axial.SetDisplayExtent(0, x, 0, y, int(z/2), int(z/2))
    axial.InterpolateOn()
    axial.ForceOpaqueOn()

    coronal = vtk.vtkImageActor()
    cor_prop = vtk.vtkImageProperty()
    cor_prop.SetOpacity(0)
    coronal.SetProperty(cor_prop)
    coronal.GetMapper().SetInputConnection(vertebra.image_mapper.GetOutputPort())
    coronal.SetDisplayExtent(0, x, int(y/2), int(y/2), 0, z)
    coronal.InterpolateOn()
    coronal.ForceOpaqueOn()

    sagittal = vtk.vtkImageActor()
    sag_prop = vtk.vtkImageProperty()
    sag_prop.SetOpacity(0)
    sagittal.SetProperty(sag_prop)
    sagittal.GetMapper().SetInputConnection(vertebra.image_mapper.GetOutputPort())
    sagittal.SetDisplayExtent(int(x/2), int(x/2), 0, y, 0, z)
    sagittal.InterpolateOn()
    sagittal.ForceOpaqueOn()

    renderer.AddActor(axial)
    renderer.AddActor(coronal)
    renderer.AddActor(sagittal)

    return [axial, coronal, sagittal]


def setup_projection(vertebra, renderer):
    slice_mapper = vtk.vtkImageResliceMapper()
    slice_mapper.SetInputConnection(vertebra.reader.GetOutputPort())
    slice_mapper.SliceFacesCameraOn()
    slice_mapper.SliceAtFocalPointOn()
    slice_mapper.BorderOff()

    vertebra_image_prop = vtk.vtkImageProperty()
    vertebra_image_prop.SetOpacity(0.0)
    vertebra_image_prop.SetInterpolationTypeToLinear()
    image_slice = vtk.vtkImageSlice()
    image_slice.SetMapper(slice_mapper)
    image_slice.SetProperty(vertebra_image_prop)
    image_slice.GetMapper().SetInputConnection(vertebra.image_mapper.GetOutputPort())
    renderer.AddViewProp(image_slice)
    return vertebra_image_prop


def setup_vertebra(renderer, file):
    vertebra = NiiObject()
    vertebra.file = file
    vertebra.reader = read_volume(vertebra.file)
    vertebra.labels.append(NiiLabel(vertebra_COLORS[0], vertebra_OPACITY, vertebra_SMOOTHNESS))
    vertebra.labels[0].extractor = create_vertebra_extractor(vertebra)
    vertebra.extent = vertebra.reader.GetDataExtent()

    scalar_range = vertebra.reader.GetOutput().GetScalarRange()
    bw_lut = vtk.vtkLookupTable()
    bw_lut.SetTableRange(scalar_range)
    bw_lut.SetSaturationRange(0, 0)
    bw_lut.SetHueRange(0, 0)
    bw_lut.SetValueRange(0, 2)
    bw_lut.Build()

    view_colors = vtk.vtkImageMapToColors()
    view_colors.SetInputConnection(vertebra.reader.GetOutputPort())
    view_colors.SetLookupTable(bw_lut)
    view_colors.Update()
    vertebra.image_mapper = view_colors
    vertebra.scalar_range = scalar_range

    add_surface_rendering(vertebra, 0, sum(scalar_range)/2)  # render index, default extractor value
    renderer.AddActor(vertebra.labels[0].actor)
    return vertebra


def setup_mask(renderer, file):
    mask = NiiObject()
    mask.file = file
    mask.reader = read_volume(mask.file)
    mask.extent = mask.reader.GetDataExtent()
    
    n_labels = int(mask.reader.GetOutput().GetScalarRange()[1])
    n_labels = n_labels #if n_labels <= 10 else 10
    #print(n_labels)
    #print(MASK_COLORS)
    for label_idx in range(n_labels):
        print(label_idx)
        mask.labels.append(NiiLabel(MASK_COLORS[label_idx], MASK_OPACITY, MASK_SMOOTHNESS))
        mask.labels[label_idx].extractor = create_mask_extractor(mask)
        add_surface_rendering(mask, label_idx, label_idx + 1)
        renderer.AddActor(mask.labels[label_idx].actor)
    
    return mask
