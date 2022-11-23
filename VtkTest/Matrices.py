import numpy
import vtk


TBA = numpy.array([[-1,0,0,3],
                    [0,1,0,2],
                    [0,0,-1,0],
                    [0,0,0,1]])
T = numpy.array([[0,-1,0,0],
                    [1,0,0,2],
                    [0,0,1,0],
                    [0,0,0,1]])

pos = numpy.array([[0.707107,-0.707107,0,3],
                    [0.707107,0.707107,0,2],
                    [0,0,1,0],
                    [0,0,0,1]])

PreR90TX2 = numpy.array([[0,-1,0,0],
                    [1,0,0,2],
                    [0,0,1,0],
                    [0,0,0,1]])

PosR90TX2 = numpy.array([[0,-1,0,2],
                    [1,0,0,0],
                    [0,0,1,0],
                    [0,0,0,1]])

preM = numpy.array([[0,0,1,0],
                    [0,1,0,0],
                    [-1,0,0,0],
                    [0,0,0,1]])

# postM = numpy.array([[0,-0.707107,0.707107,-3.47937],
#                     [0,0.707107,0.707107,204.54062],
#                     [-1,0,0,-211.839996],
#                     [0,0,0,1]])
postM = numpy.array([[0,-0.707107,0.707107,9.88],
                    [0,0.707107,0.707107,170.4],
                    [-1,0,0,-211.839996],
                    [0,0,0,1]])
pos = numpy.array([0,0,500,1])
m1 = numpy.dot(postM, preM)
print(m1)
pos1 = numpy.dot(m1, numpy.transpose(pos))
print(pos1)


# print(numpy.dot(pos, PreR90TX2))
# print('\n')
# print(numpy.dot(PreR90TX2, pos))

# trans = vtk.vtkTransform()
# trans.RotateZ(60)
# print(trans)
# mat = vtk.vtkMatrix4x4()
# trans.GetTranspose(mat)
# print(mat)
