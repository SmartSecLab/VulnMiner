[![source under MIT licence](https://img.shields.io/badge/source%20license-MIT-green)](LICENSE.txt)
[![data under CC BY 4.0 license](https://img.shields.io/badge/data%20license-CC%20BY%204.0-green)](https://creativecommons.org/licenses/by/4.0/)
[![Open in Code Ocean](https://codeocean.com/codeocean-assets/badge/open-in-code-ocean.svg)](https://codeocean.com/capsule/0170549/tree)

# VulnMiner: A Comprehensive Framework for Vulnerability Detection in C/C++ Source Code

In this study, we have presented an vulnerability data extraction tool to detect vulnerabilities in the C\C++ source code of several operating systems(OS) and software. The source code of major software was used to create a binary and multi-class labeled dataset including both vulnerable and benign samples.
The vulnerability types presented in the extracted dataset are linked to the Common Weakness Enumeration (CWE) records.

## Dataset extraction approach for vulnerability analysis

The proposed method for vulnerability data collection is as follows:

![framework](figure/framework.png?raw=true "The proposed framework for vulnerability data collection")

Follow the vulnerability dataset extraction instruction as follows:

# Software Dependencies

- Python (3.7)
- pip 23.3.1
- FlawFinder 2.0.19
- Cppcheck 2.10.3
- Clang Static Analyzer 15.0.0

## Python Dependencies

The code is written in python 3.7. The program requires the following python packages:

Follow `requirements.txt` to see the python APIs used in the repository to reproduce the result. Run the following command to create a virtual environment, activate it and install all thre required python dependencies.

```
conda create -n vulnminer python==3.8
conda activate vulnminer
pip install pip==23.3.1
pip install -r requirements.txt
```

# Initial Release of VulnMiner Dataset

The `VulnMiner` dataset is a collection of vulnerable codes from various projects. In the current version of the extracted dataset, there are 1,014,548 statements (948,996 benign and 65,052 vulnerable samples) and 548,089 functions (481,390 benign and 66,699 vulnerable samples). We have collected the vulnerable data from the following projects.

## Generic Projects

| Project      | version | URL                                                                                       |
| ------------ | ------- | ----------------------------------------------------------------------------------------- |
| linux-kernel | 6.0     | https://cdn.kernel.org/pub/linux/kernel/v6.x/linux-6.0.tar.gz                             |
| VLC          | 3.0.15  | https://download.videolan.org/pub/videolan/vlc/3.0.15/vlc-3.0.15.tar.xz                   |
| OpenCV       | 4.9.0   | https://github.com/opencv/opencv/releases/download/4.9.0/opencv-4.9.0-android-sdk.zip     |
| FFmpeg       | 6.1.1   | https://ffmpeg.org/releases/ffmpeg-6.1.1.tar.xz                                           |
| httpd        | 2.4.58  | https://dlcdn.apache.org/httpd/httpd-2.4.58.tar.gz                                        |
| ImageMagick  | 7.1.1   | https://imagemagick.org/archive/ImageMagick.tar.gz                                        |
| WireShark    | 4.2.4   | https://2.na.dl.wireshark.org/src/wireshark-4.2.4.tar.xz                                  |
| OpenSSL      | 3.0.13  | https://www.openssl.org/source/openssl-3.0.13.tar.gz                                      |
| SystemD      | 255     | https://github.com/systemd/systemd/archive/refs/tags/v255.tar.gz                          |
| tcpdump      | 4.99.4  | https://www.tcpdump.org/release/tcpdump-4.99.4.tar.xz                                     |
| tensorflow   | 2.16.1  | https://github.com/tensorflow/tensorflow/archive/refs/tags/v2.16.1.tar.gz                 |
| CycloneTCP   | 2.4.0   | https://www.oryx-embedded.com/download/CycloneTCP_SSL_SSH_IPSEC_EAP_CRYPTO_Open_2_4_0.zip |
| Chromium     | 495913c | https://github.com/chromium/chromium/archive/refs/heads/main.zip                          |

## IoT Specific Projects

| Project    | version   | URL                                   |
| ---------- | --------- | ------------------------------------- |
| linux-rpi  | 6.1.y     | www.raspberrypi.com/software/         |
| ARMmbed    | 6.17.0    | https://os.mbed.com/mbed-os/          |
| FreeRTOS   | 202212.01 | www.freertos.org/a00104.html          |
| RIOT       | 2023.07   | https://github.com/RIOT-OS/RIOT       |
| contiki    | 2.4       | https://github.com/contiki-os/contiki |
| gnucobol   | 3.2       | https://gnucobol.sourceforge.io/      |
| mbed-os    | 6.17.0    | https://github.com/ARMmbed/mbed-os    |
| miropython | 1.12.0    | https://micropython.org/              |
| mosquito   | 2.0.18    | https://github.com/eclipse/mosquitto  |
| openwrt    | 23.05.2   | https://github.com/openwrt/openwrt    |

Among all extracted projects, `linux-rpi` has the most recorded entries with 816,672 total statements and 456,380 functions, which is followed by `ARMmbed` with 43,782 statements and 26,095 functions. Of course, the severity of the project can be seen in the size of the vulnerability and weakness samples present in the project. However, `linux-rpi` being the biggest project in size in the list can tend to hold a higher number of vulnerable samples. The SQLite database file has three tables, namely `project` for project-level information, `statement` for statement-level information, and
`function` for function-level information.

## Dataset Link

The initial release of the extracted dataset can be accessible at [zenodo](https://zenodo.org/uploads/10203899) (with DOI:10.5281/zenodo.10203899).

## Acknowledgements

The research presented in this paper has benefited from the [Kristiania-HPC](https://kristiania-hpc.github.io/build/index.html) which is financially supported by the Kristiania University College.
