## Totpy

### Description
Totpy is CLI TOTP generator and management tool for Linux and MacOS. Can generate a TOTP token from a given secret key or from one stored in the configuration file. The secrets can be added to the configuration file using a secret key or the QR code image of a secret key. The default configuration file is stored in ```~/.local/config/totpy```, but can be overriden with a given one.

<div style="text-align:center"><img src="https://raw.githubusercontent.com/jorgegarciadev/totpy/master/img/Screenshot.png" /></div>

### Instalation
Totpy requires the follow packages:

- Click 7.0 ([https://click.palletsprojects.com/en/7.x/](https://click.palletsprojects.com/en/7.x/))
- Pillow 7.0.0 ([https://pillow.readthedocs.io/en/stable/](https://pillow.readthedocs.io/en/stable/))
- pypng 0.0.20 ([https://pypng.readthedocs.io/en/latest/](https://pypng.readthedocs.io/en/latest/))
- PyQRCode 1.2.1 ([https://pythonhosted.org/PyQRCode/](https://pythonhosted.org/PyQRCode/) )
- pyzbar 0.1.8 ([https://github.com/NaturalHistoryMuseum/pyzbar/](https://github.com/NaturalHistoryMuseum/pyzbar/) )

Totpy can be installed from this repository using pip:

```$ pip install git+https://github.com/jorgegarciadev/totpy.git```

From the Python Package Index using pip:

```$ pip install totpy```

Or cloning this repository and running setup.py:

```
$ git clone https://github.com/jorgegarciadev/totpy.git
$ python setup.py install --user
```

in all cases It installs the module and the CLI tool.

### Usage

### ```-c --conf PATH```

Overrides the configuration stored in ```~/.local/config/totpy/config.json``` and uses the new file from now on. Check ```config.example``` for more info.

```$ totpy -c conf.json foo```


### ```-a --add NAME```

Adds a new secret to the config file. The new secret can be added using a QR code image:

```$ totpy -a foo -q foo.png```

Or passing directly the secret using the ```-s``` option:

```$ totpy -a foo -s JBSWY3DPEHPK3PXP```

If the entry already exists it will be overwriten.


### ```-qr NAME```

Generates a QR code for the given name and prints it in the terminal.

```$ totpy -qr foo```

<div style="text-align:center"><img src="https://raw.githubusercontent.com/jorgegarciadev/totpy/master/img/Screenshot2.png" /></div>


### ```-l --list```

Shows all the entries' names in the configuration file.

```$ totpy -l```


### ```-s --secret```

Generates a TOTP token for the given secret key.

```
$ totpy -s JBSWY3DPEHPK3PXP
235467
```


### ```NAME```

Generates a TOTP token using the secret stored in the configuration file for the given name.

```
$ totpy granada
099299
```


## Totpy module

Totpy includes three classes:

- Base: A helper class for managing the configuration file.
- Totpy: The class that defines the ```totpy``` CLI tool behaviour.
- Totp: The class that generates the token.

### Totp class

This can be imported in your project and used. This is the source code:

```python
class Totp(object):
  """docstring for Totpy"""
  def __init__(self, secret):
    self.secret = secret

  def getHotpToken(self, interval):
    key = base64.b32decode(self.secret, True)
    msg = struct.pack(">Q", int(time.time()) // interval)
    h = hmac.new(key, msg, hashlib.sha1).digest()
    o = h[19] & 15
    h = (struct.unpack(">I", h[o:o+4])[0] & 0x7fffffff) % 1000000
    return h

  def getTotpToken(self):
    return self.getHotpToken(interval=30)
```
## License

This is free and open source software. You can use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of it, under the terms of the MIT License. See LICENSE.txt for details.

This software is provided "AS IS", WITHOUT WARRANTY OF ANY KIND, express or implied. See LICENSE.txt for details.


## Support

To report bugs, suggest improvements, or ask questions, please create a new issue at [https://github.com/jorgegarciadev/totpy/issues](https://github.com/jorgegarciadev/totpy/issues) .