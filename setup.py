import cx_Freeze

# run python setup.py build in the directory with this file, and the resulting
# build directory will have the wutp executable 
# Note: might have to manually move images folder to build exe directory

base = None

executables = [cx_Freeze.Executable("wutp_app.py", base=base)] 

cx_Freeze.setup(name='wutp',
      options={"build_exe": {"packages":["tkinter"],
      "include_files":["images/previous.png", "images/next.png"]}},
      version='0.1',
      description='Wake Up to Politics',
      executables=executables
      )


































