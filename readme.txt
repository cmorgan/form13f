
Environment dependencies
------------------------

pip  # (sudo easy_install pip)
Python 2.7+  # tested up to Python 3.3.2

Ubuntu
""""""

pip  # (sudo easy_install pip)
gcc  # (sudo apt-get install gcc)

OSX 10.8.2
""""""""""

XCode 4.6.2  # (maybe lower version OK, but i tested with this)
Command Line Tools (OS X Mountain Lion) for Xcode - April 15, 2013
pip  # ("sudo easy_install pip" should work)


Install
-------

Once environment dependencies are met::

    pip install -r requirements.txt
    python setup.py develop


Execute
-------

Once installed::

    solo-filing-answer

Tests
-----

from project root::

    nosetests
