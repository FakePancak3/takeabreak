<div align="center">
  <picture>
    <!-- Dark mode image -->
    <source media="(prefers-color-scheme: dark)" srcset="tdark.png">
    <!-- Light mode image (fallback) -->
    <img src="tlight.png" alt="Description of the image" width="600">
  </picture>
</div>

<p align="center">
  <a href="" target="_blank">
    <img src="https://img.shields.io/badge/platform-windows-blue?style=for-the-badge" alt="idk" />
  </a>
  <a href="" target="_blank">
    <img src="https://img.shields.io/badge/license-mit-yellow?style=for-the-badge" alt="license" />
  </a>
</p>

# TakeABreak

A simple Python application that reminds you to take a break from your screen

TakeABreak is a small **hobby project** built to provide a simple reminder to step away from your computer every once in a while. Its intentionally lightweight and isn't intended to be a large commercial application

## ✨ Features

* Simple break reminders
* Lightweight
* Minimal and easy-to-use interface
* Open source and available to modify

## ⚠️ Windows SmartScreen Warning

When downloading or running a pre-built version of TakeABreak on Windows you may see a **Microsoft Defender SmartScreen** warning

This is expected

TakeABreak is a **hobby project and the Windows executable is unsigned**, meaning it does not have a codesigning certificate that Windows can use to verify the publishers identity

Because the executable is unsigned and may not have an established reputation with SmartScreen windows can display a warning even though the warning itself does **not** mean that the application is malicious

If you downloaded the executable from the official repository you can inspect the source code yourself and if you prefer, build the application from source instead of using a prebuilt executable

## 🛠️ Building From Source

You can build and run TakeABreak directly from the source code using Git

### Requirements

* [Python](https://www.python.org/)
* [Git](https://git-scm.com/)
* Any dependencies required by the project

### 1. Clone the repository

```bash
git clone https://github.com/FakePancak3/takeabreak.git
```

### 2. Enter the project directory

```bash
cd takeabreak
```

### 3. Run the application

```bash
python takeabreak.py
```

Depending on your Python installation you may need to use:

```bash
python3 takeabreak.py
```

### Building an Executable

If you want to create your own Windows executable from the source you can use a Python packaging tool such as PyInstaller

Install it with:

```bash
pip install pyinstaller
```

Then build the application with:

```bash
pyinstaller --onefile --windowed takeabreak.py
```

The resulting executable will be placed in the `dist` directory

> Building the application yourself does not automatically make the executable digitally signed a selfbuilt executable can therefore still trigger Windows SmartScreen warnings

## 🎯 Why?

This project was made as a small personal/hobby project to experiment with Python and create something useful for everyday computer use.

## 🤝 Contributing

This is primarily a hobby project, but suggestions, bug reports, and improvements are welcome

If youd like to contribute:

1. Fork the repository
2. Create a new branch
3. Make your changes
4. Test them locally
5. Open a pull request
## 📄 License

TakeABreak is released under the **MIT License**.

See [`LICENSE`](LICENSE) for the full license text.

## 🔗 Repository

Source code:

https://github.com/FakePancak3/takeabreak
