import pytest
import os
import pathlib
import subprocess

def test_list():
    a = subprocess.run("python src/maps --list", shell=True, capture_output=True)
    assert a.returncode == 0

def test_ambiguous_deploy():
    a = subprocess.run("python src/maps --deploy base/x86_64/debian", shell=True, capture_output=True)
    assert a.returncode == 0

def test_ambiguous_update():
    a = subprocess.run("python src/maps --update base/x86_64/debian", shell=True, capture_output=True)
    assert a.returncode == 0

def test_ambigious_run():
    a = subprocess.run(["python", "src/maps", "--run", "base/x86_64/debian", "--command",
                        "bash -c exit"], shell=False, capture_output=True)
    assert a.returncode == 0

def test_public_passthrough():
    pubdirpath = f"{os.getenv('HOME')}/Public"
    testfilename = 'maps-test-file.txt'
    pathlib.Path(pubdirpath).mkdir(parents=True, exist_ok=True)
    pathlib.Path(f"{pubdirpath}/{testfilename}").touch()
    a = subprocess.run(["python", "src/maps", "--run", "base/x86_64/debian", "--command",
                        f"ls Public/{testfilename}"], shell=False, capture_output=True)
    assert a.returncode == 0
    pathlib.Path(f"{pubdirpath}/{testfilename}").unlink()

def test_ambiguous_reset():
    a = subprocess.run("python src/maps --reset base/x86_64/debian", shell=True, capture_output=True)
    assert a.returncode == 0

def test_ambiguous_uninstall():
    a = subprocess.run("python src/maps --uninstall base/x86_64/debian", shell=True, capture_output=True)
    assert a.returncode == 0

def test_exact_deploy():
    a = subprocess.run("python src/maps --deploy Official:base/x86_64/debian", shell=True, capture_output=True)
    assert a.returncode == 0

def test_exact_update():
    a = subprocess.run("python src/maps --update Official:base/x86_64/debian", shell=True, capture_output=True)
    assert a.returncode == 0

def test_exact_run():
    a = subprocess.run(["python", "src/maps", "--run", "Official:base/x86_64/debian", "--command",
                        "bash -c exit"], shell=False, capture_output=True)
    assert a.returncode == 0

def test_exact_reset():
    a = subprocess.run("python src/maps --reset Official:base/x86_64/debian", shell=True, capture_output=True)
    assert a.returncode == 0

def test_exact_uninstall():
    a = subprocess.run("python src/maps --uninstall Official:base/x86_64/debian", shell=True, capture_output=True)
    assert a.returncode == 0

def test_bad_deploy():
    a = subprocess.run("python src/maps -v --deploy Official:invalid_runtime", shell=True, capture_output=True)
    assert a.returncode != 0

