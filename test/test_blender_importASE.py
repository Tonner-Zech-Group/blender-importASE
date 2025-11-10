import unittest
import os
import json
import shutil
import sys

# Test functions that are independent of blender/bpy

class TestFunctions(unittest.TestCase):

        def test_is_inside_cell(self):
                pass

# Fully integrated test with blender

class TestBlender(unittest.TestCase):

        def setUp(self) -> None:
                self.testpath = os.path.join(os.path.dirname(__file__))
                # ensure a clean blender enviroment
                if sys.platform == "win32":
                        self.blender_cfg = os.path.expandvars(r"%USERPROFILE%\AppData\Roaming\Blender Foundation\Blender\Version")
                elif sys.platform == "darwin":
                        self.blender_cfg = os.path.expanduser("~/Library/Application Support/Blender/")
                else:
                        self.blender_cfg = os.path.expanduser("~/.config/blender/")
                if os.path.exists(self.blender_cfg):
                        shutil.rmtree(self.blender_cfg)
                return super().setUp()
                
        def tearDown(self) -> None:
                # clean up files created during test
                for f in ["blender_out.log", "blender_err.log", "blender_img.png", "blender_out.json", "current_test.py", "ase_addon.zip"]:
                        if os.path.exists(os.path.join(os.path.dirname(__file__), f)):
                                os.remove(os.path.join(os.path.dirname(__file__), f))
                if os.path.exists(self.blender_cfg):
                        shutil.rmtree(self.blender_cfg)
                return super().tearDown()

        def _run_test(self, executeable="blender", input="testcase.py", output="blender_out.log", error="blender_err.log", render="blender_img.png"):
                import subprocess
                import os
                output = os.path.join(os.path.dirname(__file__), output)
                error = os.path.join(os.path.dirname(__file__), error)
                render = os.path.join(os.path.dirname(__file__), render)
                if os.path.exists(output):
                        os.remove(output)
                if os.path.exists(render):
                        os.remove(render)
                if os.path.exists("blender_out.json"):
                        os.remove("blender_out.json")
                ret = subprocess.run([executeable, "--background", "--python", input], capture_output=True)
                print("Return code:", ret.returncode)
                with open(output, "w") as f:
                        f.write(ret.stdout.decode())
                with open(error, "w") as f:
                        f.write(ret.stderr.decode())
                self.assertEqual(ret.returncode, 0)
                self.assertTrue(os.path.exists(output))

        def _prepare_runfile(self, filename):
                path = os.path.join(os.path.dirname(__file__), "test_templates", filename)
                if os.path.exists(os.path.join(os.path.dirname(__file__), "current_test.py")):
                        os.remove(os.path.join(os.path.dirname(__file__), "current_test.py"))
                shutil.copyfile(path, os.path.join(os.path.dirname(__file__), "current_test.py"))
                return os.path.join(os.path.dirname(__file__), "current_test.py")

        def _modify_runfile(self, placeholder, new, filename="current_test.py"):
                path = os.path.join(os.path.dirname(__file__), filename)
                with open(path, "r") as f:
                        content = f.read()
                content = content.replace(placeholder, new)
                with open(path, "w") as f:
                        f.write(content)

        def test_blender(self):
                print("Testing Blender execution... ", end="")
                testfile = self._prepare_runfile("test_blender.py")
                self._run_test(input=testfile)
                with open(os.path.join(self.testpath, "blender_out.json"), "r") as f:
                        data = json.load(f)
                self.assertIn("blender_version", data)
                self.assertIn("python_version", data)
                self.assertIn("objects", data)
                self.assertIsInstance(data["objects"], list)
                version = data["blender_version"]
                print("Blender version:", version)
                self.assertTrue(version[0] >= 4, "Unsupported Blender version") # major version
                self.assertTrue(version[1] >= 4, "Unsupported Blender version") # minor version
                print("OK")

        def test_install_addon(self):
                print("Testing Addon installation... ", end="")
                testfile = self._prepare_runfile("test_install_addon.py")
                # pack the addon into a zip file
                root_dir = os.path.join(os.path.dirname(__file__), "..")
                base_dir = "blender_importASE"
                shutil.make_archive("ase_addon", "zip", root_dir=root_dir, base_dir=base_dir)
                zip_path = os.path.abspath("ase_addon.zip")
                self._modify_runfile("###ADDON_PATH###", zip_path)
                self._run_test(input=testfile, output="install_addon_out.log", error="install_addon_err.log")
                with open(os.path.join(self.testpath, "install_addon_out.log"), "r") as f:
                        log = f.read()
                self.assertIn("Modules Installed", log)
                with open(os.path.join(self.testpath, "blender_out.json"), "r") as f:
                        data = json.load(f)
                self.assertIn("modules", data)
                self.assertIn("addon_enabled", data)
                self.assertTrue(data["addon_enabled"], "Addon was not enabled")
                self.assertIsInstance(data["modules"], list)
                self.assertIn("ase", data["modules"])
                print("Done")


class TestAddon(unittest.TestCase):
        
        def setUp(self) -> None:
                self.testpath = os.path.join(os.path.dirname(__file__))
                if sys.platform == "win32":
                        self.blender_cfg = os.path.expandvars(r"%USERPROFILE%\AppData\Roaming\Blender Foundation\Blender\Version")
                elif sys.platform == "darwin":
                        self.blender_cfg = os.path.expanduser("~/Library/Application Support/Blender/")
                else:
                        self.blender_cfg = os.path.expanduser("~/.config/blender/")
                if os.path.exists(self.blender_cfg):
                        shutil.rmtree(self.blender_cfg)
                # install the addon before running tests
                testfile = self._prepare_runfile("test_install_addon.py")
                # pack the addon into a zip file
                root_dir = os.path.join(os.path.dirname(__file__), "..")
                base_dir = "blender_importASE"
                shutil.make_archive("ase_addon", "zip", root_dir=root_dir, base_dir=base_dir)
                zip_path = os.path.abspath("ase_addon.zip")
                self._modify_runfile("###ADDON_PATH###", zip_path)
                self._run_test(input=testfile, output="install_addon_out.log", error="install_addon_err.log")
                return super().setUp()
                
        def tearDown(self) -> None:
                # clean up files created during test
                for f in ["blender_out.log", "blender_err.log", "blender_img.png", "blender_out.json", "current_test.py", "ase_addon.zip"]:
                        if os.path.exists(os.path.join(os.path.dirname(__file__), f)):
                                os.remove(os.path.join(os.path.dirname(__file__), f))
                return super().tearDown()

        def _run_test(self, executeable="blender", input="testcase.py", output="blender_out.log", error="blender_err.log", render="blender_img.png"):
                import subprocess
                import os
                output = os.path.join(os.path.dirname(__file__), output)
                error = os.path.join(os.path.dirname(__file__), error)
                render = os.path.join(os.path.dirname(__file__), render)
                if os.path.exists(output):
                        os.remove(output)
                if os.path.exists(render):
                        os.remove(render)
                if os.path.exists("blender_out.json"):
                        os.remove("blender_out.json")
                ret = subprocess.run([executeable, "--background", "--python", input], capture_output=True)
                print("Return code:", ret.returncode)
                with open(output, "w") as f:
                        f.write(ret.stdout.decode())
                with open(error, "w") as f:
                        f.write(ret.stderr.decode())
                self.assertEqual(ret.returncode, 0)
                self.assertTrue(os.path.exists(output))

        def _prepare_runfile(self, filename):
                path = os.path.join(os.path.dirname(__file__), "test_templates", filename)
                if os.path.exists(os.path.join(os.path.dirname(__file__), "current_test.py")):
                        os.remove(os.path.join(os.path.dirname(__file__), "current_test.py"))
                shutil.copyfile(path, os.path.join(os.path.dirname(__file__), "current_test.py"))
                return os.path.join(os.path.dirname(__file__), "current_test.py")

        def _modify_runfile(self, placeholder, new, filename="current_test.py"):
                path = os.path.join(os.path.dirname(__file__), filename)
                with open(path, "r") as f:
                        content = f.read()
                content = content.replace(placeholder, new)
                with open(path, "w") as f:
                        f.write(content)

        def test_import_mol(self):
                print("Testing Molecule import... ", end="")
                pass
                print("OK")

        def test_import_mol_double(self):
                print("Testing Molecule import (double)... ", end="")
                pass
                print("OK")

        def test_import_crystal(self):
                print("Testing Crystal import... ", end="")
                pass
                print("OK")

        def test_import_crystal_double(self):
                print("Testing Crystal import (double)... ", end="")
                pass
                print("OK")

        def test_import_density(self):
                print("Testing Density import... ", end="")
                pass
                print("OK")

        def test_materials(self):
                print("Testing Materials import... ", end="")
                pass
                print("OK")