import subprocess
import json

print("Welcome to the iOrchid Installer!")
print("Running this script will install iOrchid Horticulture Management.")
print("This requires 40mb of free space on your device.")
print("Do you want to continue? (y/n)")
reply = input("Y/n: ")
if reply.lower() == 'y':
    print("Installing iOrchid...")
    result = subprocess.run(['sh', './executables/install.sh'], capture_output=True, text=True)
    if result.returncode == 0:
        print("Installation complete!")
    else:
        print("Installation failed!")
        print("Error:", result.stderr)