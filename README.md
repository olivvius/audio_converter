# Audio Converter

This is an audio converter application built using PyQt5 and Python. The application allows you to convert audio files into different formats and sample rates. it also allows you to convert a entire folder of audio files. Finally, you can edit metadatas of all audio files of a folder. The app is available in englis, spanish, french and hindi.

![](screen.png?raw=true "screen")


## Prerequisites

- Python 3.11.11
- PyEnv (for managing Python versions)
- PyQt5
- Other dependencies listed in `requirements.txt`

## Setup

Follow the steps below to set up and run the application on your local machine.

### 1. Clone the repository

Clone the repository using Git:

```bash
git clone https://github.com/olivvius/audio_converter.git
cd audio_converter
```

### 2. Create virtual environnment
If you don’t have PyEnv installed, install it first. Follow the instructions here: https://github.com/pyenv/pyenv

Then: 

```bash
pyenv install 3.11.11
pyenv global 3.11.11
venv virtualenv 3.11.11 audio_converter_venv
```

Activate it :

Mac/linux:
    
```bash
source venv/bin/activate
```

Windows :

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application


```bash
python3 converter.py
```

### 5. Build executables (optionnal)

```bash
pip install pyinstaller
pyinstaller --onefile --windowed converter.py
```
