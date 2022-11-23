import vtk


tran = vtk.vtkTransform()
tran.PostMultiply()
# tran.RotateZ(90)
# tran.Translate(0,0,1)
# print(tran)
# outpoints = [0,0,0]
# points = [2,1,0]
# tran.TransformPoint(points, outpoints)
# print(outpoints)
# PosM = tran.Get
# tran.PreMultiply()
# tran.RotateY(45)
# tran.Translate(0,1,0)
# print(tran)
tran.RotateY(45)
tran.RotateZ(0)
tran.PreMultiply()
tran.RotateY(90)
tran.Update()
print(tran)
tran2 = vtk.vtkTransform()
tran2.PreMultiply()
tran2.RotateZ(60)
tran2.RotateY(30)
tran2.RotateY(90)
tran2.Update()
print(tran2)