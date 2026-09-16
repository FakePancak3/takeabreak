<div align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="tdark.png">
    <img src="tlight.png" alt="TakeABreak" width="600">
  </picture>
</div>

<p align="center">
  <img src="https://img.shields.io/badge/platform-windows-blue?style=for-the-badge" alt="windows">
  <img src="https://img.shields.io/badge/license-mit-yellow?style=for-the-badge" alt="license">
</p>

# TakeABreak

A simple Python app that reminds you to take a break from your screen

TakeABreak is a small hobby project I made to remind people to step away from their computer every now and then

Its meant to be simple and lightweight and its not really meant to be some big professional application

## Features

* Simple break reminders
* Lightweight
* Simple interface
* Open source
* Easy to change and mess around with

## Windows SmartScreen Warning

If you download the prebuilt version of TakeABreak on Windows you might get a Microsoft Defender SmartScreen warning

This is because the executable is not signed

TakeABreak is just a hobby project and I do not have a code signing certificate for it so Windows cannot verify the publisher

Windows can sometimes warn about unsigned programs especially when they are not well known yet

The warning does not automatically mean that the program is malicious

If you are not comfortable running the prebuilt executable you can always look through the source code and build it yourself

## Building From Source

You can build and run TakeABreak yourself using Git and Python

### Requirements

* Python
* Git

### Clone the repository

```bash
git clone https://github.com/FakePancak3/takeabreak.git
```

### Go into the project folder

```bash
cd takeabreak
```

### Run the app

```bash
python takeabreak.py
```

If python does not work on your system you can also try

```bash
python3 takeabreak.py
```

## Building an Executable

If you want to make your own Windows executable you can use PyInstaller

First install it with

```bash
pip install pyinstaller
```

Then run

```bash
pyinstaller --onefile --windowed takeabreak.py
```

Your executable should then be inside the dist folder

Building it yourself does not sign the executable so Windows SmartScreen may still show a warning

## Why

This started as a small personal project and something I wanted to make for myself

I also wanted to experiment with Python and make something that could actually be useful

## Contributing

This is mainly just a hobby project but if you find a bug or want to improve something feel free to contribute

If you want to contribute

1. Fork the repository
2. Create a new branch
3. Make your changes
4. Test everything
5. Open a pull request

## License

TakeABreak is released under the MIT License

See the LICENSE file for more information

## Repository

The source code can be found on GitHub

https://github.com/FakePancak3/takeabreak
