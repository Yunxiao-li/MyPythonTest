#!/usr/bin/env python

# This example creates a tube around a line.
# This is helpful because when you zoom the camera,
# the thickness of a line remains constant,
# while the thickness of a tube varies.


import vtkmodules.all as vtk
# noinspection PyUnresolvedReferences
import vtkmodules.vtkInteractionStyle
# noinspection PyUnresolvedReferences
import vtkmodules.vtkRenderingOpenGL2
from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkFiltersCore import vtkTubeFilter, vtkTriangleFilter
from vtkmodules.vtkFiltersSources import vtkLineSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer
)


def main():
    colors = vtkNamedColors()

    # Create a line
    lineSource = vtkLineSource()
    lineSource.SetPoint1(-1.0, 0.0, 0.0)
    lineSource.SetPoint2(1, 0, 0.0)

    # Setup actor and mapper
    lineMapper = vtkPolyDataMapper()
    lineMapper.SetInputConnection(lineSource.GetOutputPort())

    lineActor = vtkActor()
    lineActor.SetMapper(lineMapper)
    lineActor.GetProperty().SetColor(colors.GetColor3d('Red'))

    # Create tube filter
    tubeFilter = vtkTubeFilter()
    tubeFilter.SetInputConnection(lineSource.GetOutputPort())
    tubeFilter.SetRadius(0.25)
    tubeFilter.SetNumberOfSides(3)
    tubeFilter.Update()

    cutter = vtk.vtkCutter()
    plane = vtk.vtkPlane()
    plane.SetNormal(0,1,0)
    plane.SetOrigin(0,0,0)
    cutter.SetInputConnection(tubeFilter.GetOutputPort())
    cutter.SetCutFunction(plane)

    # Setup actor and mapper
    tubeMapper = vtkPolyDataMapper()
    tubeMapper.SetInputConnection(cutter.GetOutputPort())

    tubeActor = vtkActor()
    tubeActor.SetMapper(tubeMapper)
    # Make the tube have some transparency.
    tubeActor.GetProperty().SetOpacity(0.5)
    tubeActor.GetProperty().SetColor(0,1,0)
    tubeActor.GetProperty().SetLighting(0)

    # Setup render window, renderer, and interactor
    renderer = vtkRenderer()
    renderWindow = vtkRenderWindow()
    renderWindow.SetWindowName('TubeFilter')
    renderWindow.AddRenderer(renderer)

    renderWindowInteractor = vtkRenderWindowInteractor()
    renderWindowInteractor.SetRenderWindow(renderWindow)
    # Visualise the arrow
    renderer.AddActor(lineActor)
    renderer.AddActor(tubeActor)
    renderer.SetBackground(colors.GetColor3d('DarkSlateGray'))
    renderer.ResetCamera()

    renderWindow.SetSize(300, 300)
    renderWindow.Render()
    renderWindowInteractor.Start()


def intersection():
    line1 = vtkLineSource()
    line1.SetPoint1(1,0,0)
    line1.SetPoint2(3,0,0)

    lineMapper1 = vtkPolyDataMapper()
    lineMapper1.SetInputConnection(line1.GetOutputPort())

    lineActor1 = vtkActor()
    lineActor1.SetMapper(lineMapper1)
    lineActor1.GetProperty().SetColor(1,0,0)

    tubefiter1 = vtkTubeFilter()
    tubefiter1.SetInputConnection(line1.GetOutputPort())
    tubefiter1.SetRadius(2.5)
    tubefiter1.SetNumberOfSides(4)

    triangler1 = vtkTriangleFilter()
    triangler1.PassVertsOff()
    triangler1.SetInputConnection(tubefiter1.GetOutputPort())

    mapper1 = vtkPolyDataMapper()
    mapper1.SetInputConnection(triangler1.GetOutputPort())
    actor1 = vtkActor()
    actor1.SetMapper(mapper1)
    actor1.GetProperty().SetColor(0.3,0.3,0.3)
    actor1.GetProperty().SetLighting(0)
    actor1.GetProperty().SetOpacity(0.3)

    line2 = vtkLineSource()
    line2.SetPoint1(2, 0, 0)
    line2.SetPoint2(4, 0, 0)

    lineMapper2 = vtkPolyDataMapper()
    lineMapper2.SetInputConnection(line2.GetOutputPort())

    lineActor2 = vtkActor()
    lineActor2.SetMapper(lineMapper2)
    lineActor2.GetProperty().SetColor(0, 1, 0)

    tubefiter2 = vtkTubeFilter()
    tubefiter2.SetInputConnection(line2.GetOutputPort())
    tubefiter2.SetRadius(2.5)
    tubefiter2.SetNumberOfSides(4)

    triangler2 = vtkTriangleFilter()
    triangler2.PassVertsOff()
    triangler2.SetInputConnection(tubefiter2.GetOutputPort())

    mapper2 = vtkPolyDataMapper()
    mapper2.SetInputConnection(triangler2.GetOutputPort())
    actor2 = vtkActor()
    actor2.SetMapper(mapper2)
    actor2.GetProperty().SetColor(0, 0.3, 0.7)
    actor2.GetProperty().SetLighting(0)
    actor2.GetProperty().SetOpacity(0.5)

    boolop = vtk.vtkBooleanOperationPolyDataFilter()
    boolop.SetInputConnection(0, triangler1.GetOutputPort())
    boolop.SetInputConnection(1, triangler2.GetOutputPort())
    boolop.SetOperationToIntersection()

    insectionmapper = vtkPolyDataMapper()
    insectionmapper.SetInputConnection(boolop.GetOutputPort())
    insectionmapper.ScalarVisibilityOff()
    insecActor = vtkActor()
    insecActor.SetMapper(insectionmapper)
    insecActor.GetProperty().SetOpacity(0.8)
    insecActor.GetProperty().SetColor(1,0.5,0)
    insecActor.GetProperty().SetLighting(0)

    axes = vtk.vtkAxesActor()
    axes.SetTotalLength(1, 1, 1)
    axes.SetShaftType(0)
    axes.SetAxisLabels(0)
    axes.SetCylinderRadius(0.02)

    # Setup render window, renderer, and interactor
    renderer = vtkRenderer()
    renderWindow = vtkRenderWindow()
    renderWindow.SetWindowName('TubeFilter')
    renderWindow.AddRenderer(renderer)

    renderWindowInteractor = vtkRenderWindowInteractor()
    renderWindowInteractor.SetRenderWindow(renderWindow)
    # Visualise the arrow
    renderer.AddActor(insecActor)
    # renderer.AddActor(actor1)
    # renderer.AddActor(actor2)
    renderer.AddActor(lineActor1)
    renderer.AddActor(lineActor2)
    renderer.AddActor(axes)
    renderer.ResetCamera()

    renderWindow.SetSize(300, 300)
    renderWindow.Render()
    renderWindowInteractor.Start()


if __name__ == '__main__':
    # main()
    intersection()
