# coding:utf-8
# !/usr/bin/env python

__author__ = 'XingHua'

"""

"""

import sys

sys.path.insert(0, '..')
import PythonOgreConfig
import ogre.renderer.OGRE as ogre
import SampleFramework as sf


class Tutorial(sf.Application):
    def _createScene(self):
        camera = self.camera
        sceneManager = self.sceneManager

        entity = sceneManager.createEntity("robot", "robot.mesh")
        sceneManager.getRootSceneNode().createChildSceneNode(ogre.Vector3(0, 0, 0)).attachObject(entity)
        light = sceneManager.createLight('BlueLight')
        light.setPosition(-200, -80, -100)
        light.setDiffuseColour(ogre.ColourValue(0.5, 0.5, 1.0))
        light = sceneManager.createLight('GreenLight')
        light.setPosition(0, 0, -100)
        light.setDiffuseColour(0.5, 1.0, 0.5)
        camera.setPosition(100, 50, 100)
        camera.lookAt(-50, 50, 0)


if __name__ == '__main__':
    ta = Tutorial()
    ta.go()
