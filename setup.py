from cx_Freeze import setup, Executable 

# run python setup.py build in the directory with this file, and the resulting
# build directory will have the wutp executable 
# Note: may have to manually move images directory into builds folder 
setup(name='wutp',
      version='0.1',
      description='Wake Up to Politics',
      executables = [Executable("wutp_app.py")])


































