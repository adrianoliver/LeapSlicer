import os
import unittest
import vtk, qt, ctk, slicer
from slicer.ScriptedLoadableModule import *
import logging
import threading
import time

import sys
# tried many other ways of importing this, to no avail: change to the absolute path of where the leapSDK is on your computer
sys.path.insert(0, "/Program Files (x86)/Leap Motion/LeapDeveloperKit_2.3.1+31549_win/LeapSDK/lib/x64")
sys.path.insert(0, "/Program Files (x86)/Leap Motion/LeapDeveloperKit_2.3.1+31549_win/LeapSDK/lib")

import Leap

from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture

def hello():
    print "hello"


#
# leap_test
#
class leap_test(ScriptedLoadableModule):
    """Uses ScriptedLoadableModule base class, available at:
    https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
    """
    def __init__(self, parent):
        ScriptedLoadableModule.__init__(self, parent)
        self.parent.title = "leap_test" 
        self.parent.categories = ["Examples"]
        self.parent.dependencies = []
        self.parent.contributors = ["HIOA / IVS"] 
        self.parent.helpText = """Testing usin leap in Slicer"""
        self.parent.acknowledgementText = """acknowledgement""" 

#
# leap_testWidget
#
class leap_testWidget(ScriptedLoadableModuleWidget):
    """Uses ScriptedLoadableModuleWidget base class, available at:
    https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
    """
    def setup(self):
        ScriptedLoadableModuleWidget.setup(self)
        # Instantiate and connect widgets ...

        #
        # Parameters Area
        #
        controllerCollapsibleButton = ctk.ctkCollapsibleButton()
        controllerCollapsibleButton.text = "Controller"
        self.layout.addWidget(controllerCollapsibleButton)

        # Layout within the dummy collapsible button
        controllerFormLayout = qt.QFormLayout(controllerCollapsibleButton)

        # Start Button
        self.startButton = qt.QPushButton("Start")
        self.startButton.toolTip = "Start running the Leap"
        self.startButton.connect('clicked()',self.onStartButton)
        controllerFormLayout.addWidget(self.startButton)

        # Stop Button
        self.stopButton = qt.QPushButton("Stop")
        self.stopButton.toolTip = "Stop running the Leap"
        self.stopButton.connect('clicked()',self.onStopButton)
        controllerFormLayout.addWidget(self.stopButton)

    def cleanup(self):
        pass

    def onStartButton(self):
        # instantiate (calls init) the logic
        # TODO: should check if its already initilized... otherwise could create many of them and be confusing
        self.logic = leap_testLogic()

    def onStopButton(self):
        self.logic.stop()


#
# leap_testLogic
#
class leap_testLogic(ScriptedLoadableModuleLogic):
    """This class should implement all the actual
    computation done by your module.    The interface
    should be such that other python code can import
    this class and make use of the functionality without
    requiring an instance of the Widget.
    Uses ScriptedLoadableModuleLogic base class, available at:
    https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
    """
    def __init__(self):
        print "Initiating Leap Controller Reads (adding listener)"
        # get the controller
        self.controller = Leap.Controller()
        # instantiate a listener 
        self.listener = SampleListener()
        # add the listener to the controller
        self.controller.add_listener(self.listener)
        # instantiate the stuff to do with slicer
        self.slicer = Slicer()
        t = threading.Timer(3.0, hello)
        t.start()

    def stop(self):
        print "Stopping Leap Controller Reads"
        self.controller.remove_listener(self.listener)

#
# Class for listener
#
class SampleListener(Leap.Listener):
    def on_connect(self, controller):
        print "Motion Sensor Connected"
        controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE);
        controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);

    def on_disconnect(self, controller):
        print "Motion Sensor Disconnected"

    def on_frame(self, controller):
        # If the listener is working correctly this should get called everytime there is a frame
        frame = controller.frame()
        print "on frame"

        print "Frame id: %d, timestamp: %d, hands: %d, fingers: %d, tools: %d, gestures: %d" % (
        frame.id, frame.timestamp, len(frame.hands), len(frame.fingers), len(frame.tools), len(frame.gestures()))

        # loop through the gestures in the frame and see if any are of the type we are looking for
        for gesture in frame.gestures():
            if gesture.type == Leap.Gesture.TYPE_CIRCLE:
                print "Circle gesture detected"
                self.slicer.onCircleGesture(gesture)
                # call function that you want to happen when a circle gesture is detected

#
# Class for slicer controls
#
class Slicer():
    def __init__(self):
        transformable = slicer.util.getNode('MRHead')
        transform = slicer.vtkMRMLLinearTransformNode()
        slicer.mrmlScene.AddNode(transform)
        newTransform = vtk.vtkTransform()
        transformable.SetAndObserveTransformNodeID(transform.GetID()) 

    def onCircleGesture(self, gesture):
        newTransform.RotateZ(10)
        transform.SetMatrixTransformToParent(newTransform.GetMatrix())
        # TODO: get the information out of the gesture, to figure out if should move clockwise or counterclockwise
        




# ------ DO NOT BOTHER READING THE CODE BELOW THIS POINT ---------------------------------------------------------

# this will get called if you click the 'reload and test' button
class leap_testTest(ScriptedLoadableModuleTest):
    """
    This is the test case for your scripted module.
    Uses ScriptedLoadableModuleTest base class, available at:
    https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
    """

    def setUp(self):
        """ Do whatever is needed to reset the state - typically a scene clear will be enough.
        """
        slicer.mrmlScene.Clear(0)

    def runTest(self):
        """Run as few or as many tests as needed here.
        """
        self.setUp()
        self.test_leap_test1()

    def test_leap_test1(self):
        print "Doing nothing in this test"
