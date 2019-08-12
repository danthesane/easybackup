import unittest
from os import getcwd, mkdir, rmdir
from easyBackup import validateArgs, doBackup

# if these tests pass, loadConfig and editConfig also pass.
# The only thing not tested is validateArgs -b. But test_backup covers that almost completely.
# However if something unfindable happens... Check there.

class test_add_origin(unittest.TestCase):
    def test_add_that_origin(self):
        self.assertTrue(validateArgs(["easyBackup.py","-a", getcwd()])) # these also test editConfig

class test_add_destination(unittest.TestCase):
    def test_add_dest(self):
        self.assertTrue(validateArgs(["easyBackup.py","-d", getcwd()]))

class test_remove_origin(unittest.TestCase):
    def test_remove_origin(self):
        self.assertTrue(validateArgs(["easyBackup.py","-r", getcwd()]))

class test_remove_destination(unittest.TestCase):
    def test_remove_dest(self):
        self.assertTrue(validateArgs(["easyBackup.py","-R", getcwd()]))

class test_view_config(unittest.TestCase):
    def test_view_conf(self):
        self.assertTrue(validateArgs(["easyBackup.py","-v"]))

class test_perform_backup(unittest.TestCase):
    def test_backup(self):
        testorigin = getcwd() + "\\test1"
        testdest = testorigin + "\\dest1"
        mkdir(testorigin)
        mkdir(testdest)

        self.assertTrue(doBackup([testorigin], [testdest]))

        rmdir(testdest + "\\dest1")
        rmdir(testdest)
        rmdir(testorigin)
