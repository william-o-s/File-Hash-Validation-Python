### Summary
File-Hash Validation is a Python script for validating the hashes of downloaded files. It can be used to ensure that your downloaded files have not been tampered with.
I primarily struggled with using CertUtil to first calculate the hash of a file, then comparing each character to the expected hash-string. Also, as I am a little paranoid, I also try to check multiple hash types. This program primarily takes care of both calculating the hash of a file and validating it in an automated manner.

### Installation
You only need Python installed to run this program. All dependencies are part of the Python standard library. I would note that I used Python 3.10 in developing this application.

### Supported Hashes
- The following hashes are supported:
    1. MD5
    2. SHA1
    3. SHA256
- The following input methods are supported:
    1. Manual input

### GUI
- The program is running on tkinter.

### Upcoming Features
- Multithreading to prevent suspension of application.

### Epilogue
I hope this program serves you well.
-William / PlanetAstro