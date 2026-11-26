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

# Accessing the iOrchid Web Frontend

Once iOrchid has successfully started, its web frontend can be accessed through a web browser.

There are two ways to access the frontend, depending on whether your server has a domain name.

## Scenario 1: Server with a domain name

If your server has a registered domain name (for example, `iorchid.example.com`), you can access the frontend using that domain.

**Step 1.** Ensure your domain's DNS records point to your server's public IP address.

**Step 2.** Ensure port 5002 is permitted through your server firewall and any external firewall.

**Step 3.** Open your browser and enter:

```text
http://iorchid.example.com:5002
```

Replace `iorchid.example.com` with your actual domain name.

**Recommended:** For production deployments, configure a reverse proxy such as Nginx or Apache with HTTPS. This allows users to access iOrchid through:

```text
https://iorchid.example.com
```

This requires additional server configuration and a valid TLS certificate.

## Scenario 2: Server without a domain name

If your server does not have a domain name, you can access the frontend using its public IP address.

**Step 1.** Find your server's public IP address.

**Step 2.** Ensure port 5002 is permitted through your server firewall and any external firewall.

**Step 3.** Open your browser and enter:

```text
http://YOUR-SERVER-IP:5002
```

For example:

```text
http://203.0.113.10:5002
```

Replace the example IP address with your server's actual public IP address.

## Important troubleshooting information

If the frontend does not load, check the following:

1. Confirm that iOrchid is running on the server.
2. Confirm that the web server is listening on port 5002.
3. Check that your firewall permits the required traffic.
4. If using a domain, verify that its DNS records point to the correct server.
5. Check the server terminal for error messages.

**Security notice:** Do not expose the iOrchid frontend directly to the public internet without appropriate security measures. For internet-facing installations, use HTTPS and consider restricting access through a firewall or VPN.

**Remember:** The server must remain running, and the iOrchid application process must stay active for the frontend to remain available.
