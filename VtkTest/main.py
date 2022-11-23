# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import vtk


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


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

    # actor.RotateZ(45)
    # actor.SetPosition(3, 0, 0)
    print('actor pos: ')
    print(actor.GetMatrix())
    trans = vtk.vtkTransform()
    trans.PostMultiply()
    z = trans.RotateZ(45)
    # trans.RotateY(45)
    # trans.Translate(-2, 0, 0)
    # trans.PostMultiply()
    # trans.RotateZ(45)
    # trans.RotateY(45)
    trans.Translate(2, 0, 0)
    actor.SetUserTransform(trans)
    trans2 = vtk.vtkTransform()
    trans2.Identity()
    # actor.SetUserTransform(trans2)
    trans2.PostMultiply()
    trans2.RotateZ(45)
    trans2.Translate(0, 2, 0)
    actor.SetUserTransform(trans2)
    print(trans)
    print('----------Actor Matrix------------')
    print(actor.GetMatrix())
    # c = vtk.vtkMatrix4x4()
    # c.Multiply4x4(actor.GetUserMatrix(), trans.GetMatrix(), c)
    # print('\nresult:')
    # print(c)
    # ply show
    plyfilename = "C:\\Navigation\\1059942-15cm.ply"
    reader = vtk.vtkPLYReader()
    reader.SetFileName(plyfilename)
    reader.Update()
    polymapper = vtk.vtkPolyDataMapper()
    polymapper.SetInputConnection(reader.GetOutputPort())
    polyActor = vtk.vtkActor()
    polyActor.SetMapper(polymapper)
    ren.AddActor(polyActor)

    camera = vtk.vtkCamera()
    camera.ParallelProjectionOn()
    ren.SetActiveCamera(camera)
    ren.ResetCamera()

    # enable user interface interactor
    iren.Initialize()
    renWin.Render()
    iren.Start()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('')
    vtktranslate()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
