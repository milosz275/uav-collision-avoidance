# Compiles the project into a single executable file using PyInstaller.
# The compiled executable is placed in the dist folder.
$version = Get-Content "uav_collision_avoidance\version.py" | ForEach-Object { if ($_ -match '__version__ = "(.+)"') { $Matches[1] } }
pyinstaller --onefile --distpath .\dist --name "uav-collision-avoidance-$version" main.py
