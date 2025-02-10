import pytest
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

def test_exact_reset():
    a = subprocess.run("python src/maps --reset Official:base/x86_64/debian", shell=True, capture_output=True)
    assert a.returncode == 0

def test_exact_uninstall():
    a = subprocess.run("python src/maps --uninstall Official:base/x86_64/debian", shell=True, capture_output=True)
    assert a.returncode == 0

def test_bad_deploy():
    a = subprocess.run("python src/maps -v --deploy Official:invalid_runtime", shell=True, capture_output=True)
    assert a.returncode != 0

