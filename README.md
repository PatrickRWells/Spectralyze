# Spectralyze GUI
A GUI utility for viewing and processing spectral data. Currently, works with
1D spectra from Keck Deimos, but has been written to easily be extended to
other types of spectra.

## Installing

Since this projcet is very early in its development, it is recommended you
install with pip in development mode:

'''
git pull https://github.com/PatrickRWells/Spectralyze.git
cd spectralyze
pip install -e .
'''

This way updating the code will be as easy as pulling the new version from
GitHub

### Requirements

This requirements need to be installed before installing Spectralyze

keckode: https://github.com/cdfassnacht/keckcode
specim: https://github.com/cdfassnacht/specim
cdfutils: https://github.com/cdfassnacht/cdfutils


##

### Running

Run the following command in your terminal:

'''spectralyze_gui'''
