[![Author](https://img.shields.io/badge/author-Pulsar7-lightgrey.svg?colorB=9900cc&style=flat-square)](https://github.com/Pulsar7)
[![Release](https://img.shields.io/github/release/dmhendricks/file-icon-vectors.svg?style=flat-square)](https://github.com/Pulsar7/A.M.M.E/releases)
[![Twitter](https://img.shields.io/twitter/url/https/github.com/dmhendricks/file-icon-vectors.svg?style=social)](https://twitter.com/SevenPulsar)

# A.M.M.E

## :pushpin: Table of contents

* :point_right: [Explanation](#explanation)
* :point_right: [Installation](#installation)
* :point_right: [Example](#example)
* :point_right: [ToDo](#todo)
* :point_right: [Suggestions & Reports](#suggestions--reports)

## Explanation

This encryption uses analytic geometry in two-dimensional space. 

### Encryption

It (pseudo-)randomly generates 4 vectors for each character. Two straight line equations are created from these vectors, which are then checked for collinearity. If the direction vectors of the straight line equation are multiples of each other, new vectors are generated and checked until this case no longer occurs. Furthermore, an intersection of both straight lines is calculated in order to then calculate the intersection angle. Finally, the intersection angles are assigned to the characters and the previously typed message is replaced with the previously used vectors.

### Decryption

When it comes to decryption, the above part is pretty much the same. Only that at the beginning the key and the encrypted message for the calculation "must be prepared". Additional character strings and information were appended to the encryption for "further protection". Finally, the vectors read out from the message are used to calculate the intersection angles and finally form a decrypted message thanks to the key.

## Installation

:small_orange_diamond: **Download Repository & Requirements**
    
    sudo apt install git
    git clone https://github.com/Pulsar7/A.M.M.E.git
    pip3 install sympy rich
    cd A.M.M.E/
    
:small_orange_diamond: **Asking for help**

    python3 amme.py --help

## Example

    python3 amme.py --encrypt --message "SECRET MESSAGE"
    cat msg.txt
**Output: (Illustration 1)**
![Example 1](https://github.com/Pulsar7/A.M.M.E/blob/main/example1.png)
    
    python3 amme.py --decrypt --message "[INSERTED MESSAGE FROM Illustration 1]"
    
    Please insert key> [INSERTED KEY FROM Illustration 1]
    
**Output: (Illustration 2)**

![Example 2](https://github.com/Pulsar7/A.M.M.E/blob/main/example2.png)

## ToDo

- [ ] Add 3-Dimensional vectors
- [ ] Add hashlib

## Suggestions & Reports

Suggestions or errors are welcome to be [:link: reported](https://github.com/Pulsar7/A.M.M.E/issues)!
