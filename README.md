# LNBits-python-tutorial

This python scripts simply shows how to use LNbits in python to create or pay invoices.

The scripts make use of the python library pylnbits, which is a python wrapper for the LNbits API.

[pylnbits on GitHub](https://github.com/lightningames/pylnbits)

[lnbits on GitHub](https://github.com/lnbits/lnbits/)

[lnbits Website](https://lnbits.com/)


## How to use

### Prerequisites
Setup a .env file with the content from form .env_example and replace the necessary information.
You will need an LNBits instance. It's possible to self host LNBits or you can use a provider like.

[https://lnbits.de/](https://lnbits.de/)


### Setup and install the requirements:
The version of python needs to be 3.9 or 3.10.

```
git clone https://github.com/f418me/LNbits-python-tutorial.git
cd LNbits-python-tutorial
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```


### Run the scripts

```python createInvoice.py```
```python payInvoice.py```