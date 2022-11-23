import vtkmodules.all as vtk

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

# axes 1
axes1 = vtk.vtkAxesActor()
axes1.SetTotalLength(30, 30, 30)
axes1.SetShaftType(0)
axes1.SetAxisLabels(0)
axes1.SetCylinderRadius(0.01)


# axes 2
axes2 = vtk.vtkAxesActor()
axes2.SetTotalLength(20, 20, 20)
axes2.SetShaftType(0)
axes2.SetAxisLabels(0)
axes2.SetCylinderRadius(0.02)
# rotate
angle_y = 45
angle_z = 45
trans = vtk.vtkTransform()
trans.PostMultiply()
trans.RotateY(angle_y)
print(trans)
trans.RotateZ(angle_z)
# trans.Translate(5, 5, 0)
axes1.SetUserTransform(trans)

trans2 = vtk.vtkTransform()
trans2.PostMultiply()
trans2.RotateY(angle_y)
trans2.RotateZ(angle_z)
# trans2.Translate(10,10,10)
trans2.PreMultiply()
trans2.RotateY(90)
trans2.Update()
axes2.SetUserTransform(trans2)

# add axes
ren.AddActor(axes1)
ren.AddActor(axes2)

camera = vtk.vtkCamera()
camera.ParallelProjectionOn()
ren.SetActiveCamera(camera)
ren.ResetCamera()

# enable user interface interactor
iren.Initialize()
renWin.Render()
iren.Start()