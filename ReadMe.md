# WaterlooWorks Auto Submission Tool

This tool is intended to help students automatically submit their applications on WaterlooWorks and save time.

## Install Dependencies
This tool requires [Python 3](https://www.python.org/downloads/). After installing python and cloning the repository, run the following command to install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Before running the script, create a `.env` file in the root directory with the following contents:

```.env
USERNAME=<your username>
PASSWORD=<your password>
```

Then you can run the script with the following command:

```bash
python AutoSubmission.py
```

Since DUO 2FA is enabled, you will need to enter the verification code from your phone.