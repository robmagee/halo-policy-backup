# Build Python 3.5 with Custom OpenSSL with VirtualEnv for OSX
*Note: this was also tested with Python 2.7.  Substitute commands accordingly.*

## Update OpenSSL with Homebrew
Homebrew is a package manager for OSX.  If you are unfamiliar with it, you
will need to visit <http://brew.sh/> for instructions on its installation and
usage.  To update OpenSSL on your system, execute the follwing homebrew commands:

```
brew update
brew install openssl
brew link --force openssl
```

Verifiy you have the latest version:

```
which openssl
```

Note that Homebrew will create a symlink in /opt/local/bin to the openssl
located in your Homebrew Cellar- typically located at /usr/local/Cellar/

## Create The Virtual Environment

**Note**: These instructions are for users using python2.x on OSX along
with virutalenv and virutalenvwrapper.  If you are running python 3.x as your
default python you can use the pyvenv tool to manage your virtual environments.
For more, see [the docs](https://docs.python.org/3/library/venv.html).

Execute the following command to create a new virtual environment (you should have
the [virtualenvwrapper](https://virtualenvwrapper.readthedocs.org/en/latest/)
package installed).  Otherwise, use your standard *virtualenv* commands to create
a new environment.

```
mkvirtualenv cphalo --always-copy
```

This will create a new python virtual environment in your default location and
activate it.
Chose a name for the virutal environment that makes sense for you.  *cphalo*
is only an example.

For more on virtualenv and default locations, etc.  See <https://virtualenv.pypa.io/en/latest/>

## Download Python Source Code and Build

Go to <https://www.python.org/downloads/source/> to download the latest 3.5
release.  *Download in tarball format to follow along.*

Expand the tarball and cd in

```
tar jvzf Python-3.5.1.tar.bz2

cd Python-3.5.1
```

### Optional- enable zlib
*(this is used by pip and other usefull tools)*

Open the **Modules/Setup** file and uncomment the following line
(this may be called *Setup.dist* in Python 2.7):
```
uncomment line zlib zlibmodule.c -I$(prefix)/include -L$(exec_prefix)/lib -lz
```

### Build Instructions

If you are getting *Operation not permitted* errors on the `make install`
command then you probably have a python environment that is symlinked to your
system global python executable and associated libraries.  You will need to
create a virtualenv using the `--always-copy` flag to ensure that the virtualenv
is truly stand-alone.

```
#optional, make sure xcode command line tools are installed
xcode-select --install

# let the linker know where the open ssl lib files are- homebrew default
export LDFLAGS="-L/usr/local/Cellar/openssl/1.0.2g/lib/"

# let the compiler know where the openssl include directory is- homebrew default
export CFLAGS="-I/usr/local/Cellar/openssl/1.0.2g/include/"

# MAKE SURE to supply the root directory location of your virtualenv
./configure --enable-shared --prefix=[/your/virtualenv/root/goes/here/]

make
make install

#now point the default python for the env to your new build
cd [/your/virtualenv/root/goes/here]
mv python python_OLD
ln -s python3.5 python

```

## Verify Your install
Make sure your virutal environment is activated.  With the virtual environment
you created active, start python ane check the OpenSSL version:

```
python

Python 3.5.1 (default, Mar 21 2016, 11:00:17)
[GCC 4.2.1 Compatible Apple LLVM 7.0.0 (clang-700.1.76)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> import ssl
>>> print(ssl.OPENSSL_VERSION)
OpenSSL 1.0.2g  1 Mar 2016
exit()
```

## Optional: Install pip

Execute the following to install the python package manager pip:

```
wget https://bootstrap.pypa.io/get-pip.py --no-check-certificate
python get-pip.py
```
