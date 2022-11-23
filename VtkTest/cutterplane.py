import vtkmodules.all as vtk


def trans_camera():
    trans = vtk.vtkTransform()
    trans.PostMultiply()
    trans.RotateY(90)
    print(trans)
    trans.RotateZ(45)
    trans.Translate(1,1,0)
    print(trans)
    trans.PreMultiply()
    trans.RotateY(90)
    trans.Update()
    print(trans)


def create_line_actor():
    sphereSource = vtk.vtkSphereSource()
    sphereSource.SetRadius(1)
    sphereSource.SetPhiResolution(24)
    sphereSource.SetThetaResolution(24)

    transform = vtk.vtkTransform()
    transformfilter = vtk.vtkTransformFilter()
    transformfilter.SetInputConnection(sphereSource.GetOutputPort())
    transformfilter.SetTransform(transform)

    plane = vtk.vtkPlane()
    plane.SetNormal(0,0,1)
    plane.SetOrigin(0,0,0)
    cutter = vtk.vtkCutter()
    cutter.SetInputConnection(transformfilter.GetOutputPort())
    cutter.SetCutFunction(plane)

    mapper = vtk.vtkPolyDataMapper()
    # mapper.SetInputConnection(transformfilter.GetOutputPort())
    mapper.SetInputConnection(cutter.GetOutputPort())
    mapper.ScalarVisibilityOff()

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetColor(1, 0.5, 0)
    actor.GetProperty().SetLineWidth(1.0)
    actor.GetProperty().SetLineStipplePattern(0xFFF9)
    actor.GetProperty().SetLighting(0)
    return actor


def pipline():
    actor = create_line_actor()

    ren = vtk.vtkRenderer()
    ren.AddActor(actor)

    renWin = vtk.vtkRenderWindow()
    renWin.AddRenderer(ren)

    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)

    style = vtk.vtkInteractorStyleTrackballCamera()
    iren.SetInteractorStyle(style)

    iren.Initialize()
    renWin.Render()
    iren.Start()


if '__main__' == __name__:
    pipline()