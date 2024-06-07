### Tokybook Downloader

This script downloads audio chapters from Tokybook. It retrieves the chapter links from the provided Tokybook URL, then downloads the corresponding audio files and saves them as MP3 files.

#### Installation

Before running the script, make sure you have Python 3.x installed on your system. Additionally, install the required Python packages using pip:

```bash
pip install requests tqdm json5
```

#### How to Run

1. Clone or download the repository containing this script.
2. Navigate to the directory where the script is located.
3. Open a terminal or command prompt in that directory.

To run the script, use the following command:

```bash
python tokybook_downloader.py
```

You will be prompted to enter the Tokybook URL. Once you enter the URL, the script will start downloading the audio chapters into the 'MP3' directory.

#### Note

- The script uses `requests`, `tqdm`, and `json5` libraries, which are installed in the initial step.
- Ensure you have a stable internet connection for uninterrupted downloads.
- The downloaded MP3 files will be saved in the 'MP3' directory within the script's directory.

Feel free to reach out if you encounter any issues or have questions!
