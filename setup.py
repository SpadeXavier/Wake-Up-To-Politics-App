from cx_Freeze import setup, Executable 

setup(name='wutp',
      version='0.1',
      description='Wake Up to Politics',
      executables = [Executable("wutp_app.py")])


































