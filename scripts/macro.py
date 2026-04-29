# trace generated using paraview version 5.6.2
#
# To ensure correct image size when batch processing, please search 
# for and uncomment the line `# renderView*.ViewSize = [*,*]`

#### import the simple module from the paraview
from paraview.simple import *
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

import os
import re
import subprocess

run = r"D:/Programa/blueCFD-Core-2020/ofuser-of8/run"
carpetas=os.listdir(run)

# Initialize a counter
contador = 0

for i in carpetas:
    # Increment the counter
    contador += 1

    # Check if the iteration number is 11
    if contador > 10:
        break
    
    # create a new 'Legacy VTK Reader'
    carpeta = LegacyVTKReader(FileNames=['D:\\Programa\\blueCFD-Core-2020\\ofuser-of8\\run\\'+i+'\\VTK\\'+i+'_0.vtk', 'D:\\Programa\\blueCFD-Core-2020\\ofuser-of8\\run\\'+i+'\\VTK\\'+i+'_100.vtk', 'D:\\Programa\\blueCFD-Core-2020\\ofuser-of8\\run\\'+i+'\\VTK\\'+i+'_200.vtk', 'D:\\Programa\\blueCFD-Core-2020\\ofuser-of8\\run\\'+i+'\\VTK\\'+i+'_300.vtk', 'D:\\Programa\\blueCFD-Core-2020\\ofuser-of8\\run\\'+i+'\\VTK\\'+i+'_400.vtk', 'D:\\Programa\\blueCFD-Core-2020\\ofuser-of8\\run\\'+i+'\\VTK\\'+i+'_500.vtk'])
    print(i)
    # get animation scene
    animationScene1 = GetAnimationScene()

    # update animation scene based on data timesteps
    animationScene1.UpdateAnimationUsingDataTimeSteps()
    animationScene1.GoToLast()

    # get active view
    renderView1 = GetActiveViewOrCreate('RenderView')
    # uncomment following to set a specific view size
    # renderView1.ViewSize = [1490, 776]

    # show data in view
    carpeta_Display = Show(carpeta, renderView1)

    # trace defaults for the display properties.
    carpeta_Display.Representation = 'Surface'
    carpeta_Display.ColorArrayName = [None, '']
    carpeta_Display.OSPRayScaleArray = 'U'
    carpeta_Display.OSPRayScaleFunction = 'PiecewiseFunction'
    carpeta_Display.SelectOrientationVectors = 'None'
    carpeta_Display.ScaleFactor = 2.0
    carpeta_Display.SelectScaleArray = 'None'
    carpeta_Display.GlyphType = 'Arrow'
    carpeta_Display.GlyphTableIndexArray = 'None'
    carpeta_Display.GaussianRadius = 0.1
    carpeta_Display.SetScaleArray = ['POINTS', 'U']
    carpeta_Display.ScaleTransferFunction = 'PiecewiseFunction'
    carpeta_Display.OpacityArray = ['POINTS', 'U']
    carpeta_Display.OpacityTransferFunction = 'PiecewiseFunction'
    carpeta_Display.DataAxesGrid = 'GridAxesRepresentation'
    carpeta_Display.SelectionCellLabelFontFile = ''
    carpeta_Display.SelectionPointLabelFontFile = ''
    carpeta_Display.PolarAxes = 'PolarAxesRepresentation'
    carpeta_Display.ScalarOpacityUnitDistance = 0.48958818097867945

    # init the 'GridAxesRepresentation' selected for 'DataAxesGrid'
    carpeta_Display.DataAxesGrid.XTitleFontFile = ''
    carpeta_Display.DataAxesGrid.YTitleFontFile = ''
    carpeta_Display.DataAxesGrid.ZTitleFontFile = ''
    carpeta_Display.DataAxesGrid.XLabelFontFile = ''
    carpeta_Display.DataAxesGrid.YLabelFontFile = ''
    carpeta_Display.DataAxesGrid.ZLabelFontFile = ''

    # init the 'PolarAxesRepresentation' selected for 'PolarAxes'
    carpeta_Display.PolarAxes.PolarAxisTitleFontFile = ''
    carpeta_Display.PolarAxes.PolarAxisLabelFontFile = ''
    carpeta_Display.PolarAxes.LastRadialAxisTextFontFile = ''
    carpeta_Display.PolarAxes.SecondaryRadialAxesTextFontFile = ''

    # reset view to fit data
    renderView1.ResetCamera()

    # get the material library
    materialLibrary1 = GetMaterialLibrary()

    # update the view to ensure updated data information
    renderView1.Update()

    # create a new 'Slice'
    slice1 = Slice(Input=carpeta)
    slice1.SliceType = 'Plane'
    slice1.SliceOffsetValues = [0.0]

    # init the 'Plane' selected for 'SliceType'
    slice1.SliceType.Origin = [5.0, 0.0, 0.25]

    # Properties modified on slice1.SliceType
    slice1.SliceType.Normal = [0.0, 0.0, 1.0]

    # Properties modified on slice1.SliceType
    slice1.SliceType.Normal = [0.0, 0.0, 1.0]

    # show data in view
    slice1Display = Show(slice1, renderView1)

    # trace defaults for the display properties.
    slice1Display.Representation = 'Surface'
    slice1Display.ColorArrayName = [None, '']
    slice1Display.OSPRayScaleArray = 'U'
    slice1Display.OSPRayScaleFunction = 'PiecewiseFunction'
    slice1Display.SelectOrientationVectors = 'None'
    slice1Display.ScaleFactor = 2.0
    slice1Display.SelectScaleArray = 'None'
    slice1Display.GlyphType = 'Arrow'
    slice1Display.GlyphTableIndexArray = 'None'
    slice1Display.GaussianRadius = 0.1
    slice1Display.SetScaleArray = ['POINTS', 'U']
    slice1Display.ScaleTransferFunction = 'PiecewiseFunction'
    slice1Display.OpacityArray = ['POINTS', 'U']
    slice1Display.OpacityTransferFunction = 'PiecewiseFunction'
    slice1Display.DataAxesGrid = 'GridAxesRepresentation'
    slice1Display.SelectionCellLabelFontFile = ''
    slice1Display.SelectionPointLabelFontFile = ''
    slice1Display.PolarAxes = 'PolarAxesRepresentation'

    # init the 'GridAxesRepresentation' selected for 'DataAxesGrid'
    slice1Display.DataAxesGrid.XTitleFontFile = ''
    slice1Display.DataAxesGrid.YTitleFontFile = ''
    slice1Display.DataAxesGrid.ZTitleFontFile = ''
    slice1Display.DataAxesGrid.XLabelFontFile = ''
    slice1Display.DataAxesGrid.YLabelFontFile = ''
    slice1Display.DataAxesGrid.ZLabelFontFile = ''

    # init the 'PolarAxesRepresentation' selected for 'PolarAxes'
    slice1Display.PolarAxes.PolarAxisTitleFontFile = ''
    slice1Display.PolarAxes.PolarAxisLabelFontFile = ''
    slice1Display.PolarAxes.LastRadialAxisTextFontFile = ''
    slice1Display.PolarAxes.SecondaryRadialAxesTextFontFile = ''

    # hide data in view
    Hide(carpeta, renderView1)

    # update the view to ensure updated data information
    renderView1.Update()

    # get layout
    layout1 = GetLayout()

    # split cell
    layout1.SplitHorizontal(0, 0.5)

    # set active view
    SetActiveView(None)

    # Create a new 'SpreadSheet View'
    spreadSheetView1 = CreateView('SpreadSheetView')
    spreadSheetView1.ColumnToSort = ''
    spreadSheetView1.BlockSize = 1024L
    # uncomment following to set a specific view size
    # spreadSheetView1.ViewSize = [400, 400]

    # place view in the layout
    #layout1.AssignView(2, spreadSheetView1)

    # show data in view
    slice1Display_1 = Show(slice1, spreadSheetView1)

    # export view
    ExportView('D:/Programa/blueCFD-Core-2020/ofuser-of8/run/'+i+'/postProcessing/resultados.csv', view=spreadSheetView1)

    #### saving camera placements for all active view
    #### uncomment the following to render all views
    # RenderAllViews()
    # alternatively, if you want to write images, you can use SaveScreenshot(...).

