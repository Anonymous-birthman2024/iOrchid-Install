# iOrchid Horticulture Management — Installation Instructions

## 1. Access your server

**1a.** Gain access to your Linux server through SSH, a terminal, or a directly connected console.

**1b. Prerequisites**

Your server must have:

- Python 3.9 or higher.
- Git installed.
- A Linux-based operating system.
- An active internet connection.
- At least 500 MB of available disk space.
- Permission to write to your home directory.

**Windows is not supported. Please do not attempt to install iOrchid on Windows.**

## 2. Obtain the installer

Execute the following command to download the installer:

```bash
git clone https://github.com/Anonymous-birthman2024/iOrchid-Install.git
```

*Note: You must have permission to access the private installer repository.*

## 3. Navigate to the installer

Navigate into the directory that was just downloaded:

```bash
cd iOrchid-Install
```

## 4. Run the installation wizard

Execute the installer:

```bash
python3 installScript.py
```

Follow the instructions displayed in the terminal and confirm that you wish to proceed.

The installer will check your system, download the main iOrchid program, create a Python virtual environment and install the required dependencies.

## 5. Start iOrchid

Once installation has completed, the main program will be located at:

```bash
~/iOrchid-Horticulture-Management
```

To start iOrchid, execute:

```bash
cd ~/iOrchid-Horticulture-Management
```

Then:

```bash
./venv/bin/python run.py
```

**Important:** Keep the terminal session and server running while iOrchid is operating. Closing the terminal or stopping the process may stop the software.

## 6. Access the web interface

Once the web server has started, open a browser and navigate to:

```text
http://SERVER-IP:5002
```

Replace `SERVER-IP` with your server's actual IP address.

Ensure that port 5002 is permitted through your firewall if you intend to access the interface remotely. Do not expose the interface publicly without appropriate network security.

## 7. Installation logs

The installer records its activity in:

```bash
~/.iorchid-installer.log
```

If installation fails, please include this log when reporting the problem.

---

**Thank you for installing iOrchid Horticulture Management!**
