import vtk


def vtktranslate():
    ren = vtk.vtkRenderer()
    renWin = vtk.vtkRenderWindow()
    renWin.AddRenderer(ren)

    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)

    plane = vtk.vtkPlaneSource()
    plane.SetXResolution(1)
    plane.SetYResolution(1)
    plane.SetCenter(0, 0, 0)
    plane.SetNormal(0, 0, 1)

    # mapper
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(plane.GetOutputPort())
    # actor
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetRepresentationToWireframe()

    ren.AddActor(actor)

    # coordinate
    axes = vtk.vtkAxesActor()
    axes.SetTotalLength(1, 1, 1)
    axes.SetShaftType(0)
    axes.SetAxisLabels(0)
    axes.SetCylinderRadius(0.02)
    ren.AddActor(axes)

    # style
    style = vtk.vtkInteractorStyleTrackballCamera()
    style.SetDefaultRenderer(ren)
    iren.SetInteractorStyle(style)

    # actor.SetOrigin(-2, 0, 0)
    # actor.SetPosition(1, 0, 0)
    actor.SetPosition(3, 0, 0)
    actor.RotateZ(45)

    origin = actor.GetOrigin()
    position = actor.GetPosition()
    print("origin: ", origin)
    print('position: ', position)
    print('actor pos: ')
    print(actor.GetMatrix())
    trans = vtk.vtkTransform()
    trans.PostMultiply()

    trans.RotateZ(45)
    print(trans)
    trans.Translate(2, 0, 0)
    print(trans)

    # trans.Translate(-origin[0], -origin[1],-origin[2])
    # trans.RotateZ(45)
    # trans.Translate(origin[0], origin[1], origin[2])
    # trans.Translate(origin[0] + position[0], origin[1]+ position[1], origin[2]+ position[2])
    actor.SetUserTransform(trans)
    print(actor.GetMatrix())

    camera = vtk.vtkCamera()
    camera.ParallelProjectionOn()
    ren.SetActiveCamera(camera)
    ren.ResetCamera()

    # enable user interface interactor
    iren.Initialize()
    renWin.Render()
    iren.Start()


if __name__ == '__main__':
    vtktranslate()