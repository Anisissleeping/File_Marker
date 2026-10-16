
echo Updating pip..
python -m pip install --upgrade pip

echo Installing required Python packages...
python -m pip install psutil
python3 -m pip install show-in-file-manager


@echo off
"C:\Users\Anis\AppData\Local\Python\pythoncore-3.14-64\python.exe" "D:\File_Marker\file_prober.py"
pause
