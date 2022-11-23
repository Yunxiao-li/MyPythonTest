import vtk
import os

def stl2actor(ageometry_path, ageometry_name, ageometry_color):

    render_lib = vtk.vtkPLYReader()
    render_lib.SetFileName(os.path.join(ageometry_path, ageometry_name+".ply"))
    render_lib.Update()
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(render_lib.GetOutputPort())

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    # actor.GetProperty().SetColor(ageometry_color)

    return actor

def showActor():

    ren = vtk.vtkRenderer()
    renWin = vtk.vtkRenderWindow()
    renWin.AddRenderer(ren)

    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)

    # coordinate
    axes = vtk.vtkAxesActor()
    axes.SetTotalLength(50, 50, 50)
    axes.SetShaftType(0)
    axes.SetAxisLabels(0)
    axes.SetCylinderRadius(0.02)
    ren.AddActor(axes)

    # distance
    distancewidget = vtk.vtkDistanceWidget()
    handle = vtk.vtkPointHandleRepresentation3D()
    representation = vtk.vtkDistanceRepresentation2D()
    representation.SetHandleRepresentation(handle)
    distancewidget.SetRepresentation(representation)
    distancewidget.CreateDefaultRepresentation()
    distancewidget.SetInteractor(iren)
    # distancewidget.AddObserver("PlacePointEvent", vtk.vtkDistanceCallback())
    distancewidget.SetEnabled(1)
    # actor
    path = r'C:\WorkFiles\repo\cranefeasibility\Resources\Models'
    name = '1059942-15cm'
    # name = 'ArmTrackerCrane2.0-20220620'
    # name = 'ArmTrackerCrane2.03'
    actor = stl2actor(path,name,"")
    ren.AddActor(actor)

    # style
    style = vtk.vtkInteractorStyleTrackballCamera()
    style.SetDefaultRenderer(ren)
    iren.SetInteractorStyle(style)

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
    showActor()