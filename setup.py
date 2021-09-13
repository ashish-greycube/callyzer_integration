from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in callyzer_integration/__init__.py
from callyzer_integration import __version__ as version

setup(
	name="callyzer_integration",
	version=version,
	description="Intergration between ERPNext and Callyzer , a call log data analysis tool for CRM domain",
	author="GreyCube Technologies",
	author_email="admin@greycube.in",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
