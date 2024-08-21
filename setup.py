from setuptools import find_packages, setup

setup(
    name="mini_framework",
    version="0.1.0",
    description="A minimalistic Python web framework",
    packages=find_packages(where="src/mini_framework"),
    package_dir={"": "src/mini_framework"},
    install_requires=["jinja2"],
)
