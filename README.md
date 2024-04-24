[![source under MIT licence](https://img.shields.io/badge/source%20license-MIT-green)](LICENSE.txt)
[![data under CC BY 4.0 license](https://img.shields.io/badge/data%20license-CC%20BY%204.0-green)](https://creativecommons.org/licenses/by/4.0/)
[![Open in Code Ocean](https://codeocean.com/codeocean-assets/badge/open-in-code-ocean.svg)](https://codeocean.com/capsule/4010023/tree/v1)

# VulnMiner: A Comprehensive Framework for Vulnerability Collection from C/C++ Source Code

In this study, we have presented an vulnerability data extraction tool to detect vulnerabilities in the C\C++ source code of several operating systems(OS) and software. The source code of major software was used to create a binary and multi-class labeled dataset including both vulnerable and benign samples. The vulnerability types presented in the extracted dataset are linked to the Common Weakness Enumeration (CWE) records.

# Software Dependencies

- Python (3.7)
- pip 23.3.1
- FlawFinder 2.0.19
- Cppcheck 2.10.3
- RATS v2.4 - Rough Auditing Tool for Security
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

# Instruction to run data extractor

Once required packages were installed, run the command to extract the vulnerability data from the given input projects as listed in `config.yaml`:

```
python3 -m source.extract
```

If you want to extract the vulnerability data from any source-code project and collect the data to the given SQLite3 database (overriding the `config.yaml` parameters). You can execute the command as follows-

```
python3 -m source.extract --project [project-dir] --database [db-name.db]
```

Once the execution of the script completes, it will save all the collected vulnerability data (statements and functions) to a database file as specified in `database` parameter in `config.yaml` file, i.e., `data/VulnMiner.db`.

# Initial Release of VulnMiner Dataset

The `VulnMiner.db` dataset is a collection of vulnerable codes from various projects. The current VulnMiner dataset has 2,263,907 statements (2,165,850 benign and 98,057 vulnerable) and 1,026,111 functions (922,473 benign and 103,638 vulnerable). Among all the projects analyzed, `linux` has the highest number of entries, totaling 1,193,381 statements and 451,021 functions, followed by `chromium` with 216,724 statements and 257,917 functions. While the size of vulnerability and weakness samples (statements and functions) reflects the severity of the projects, it's worth noting that larger projects like \emph{linux} may naturally harbor more vulnerable samples.

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

## Dataset Link

The initial release of the extracted dataset can be accessible at [zenodo](https://doi.org/10.5281/zenodo.11050380) and earlier IoT-Specific version of the dataset is available at [zenodo](https://doi.org/10.5281/zenodo.10203899).

## Acknowledgements

The research presented in this paper has benefited from the [Kristiania-HPC](https://kristiania-hpc.github.io/build/index.html) which is financially supported by the Kristiania University College.
