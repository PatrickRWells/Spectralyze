import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="spectralyze",
    version="0.0.1",
    author="Patrick Wells",
    author_email="patrick.wells.95@gmail.com",
    description="Tools for analyzing galaxy spectra",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/PatrickRWells/Spectralyze",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    scripts=['bin/spectralyze_gui']
)
