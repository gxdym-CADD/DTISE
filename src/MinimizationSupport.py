# MinimizationSupport.py

# Import the desired library for supporting minimization of compounds
if USE_GNINA:
    from GninaConverter import GninaConverter as MinimizeConverter
else:
    from SminaConverter import SminaConverter as MinimizeConverter