#!/usr/bin/env python3

import hmac, base64, struct, hashlib, time
import os, json, re
import pyqrcode
from pyzbar import pyzbar
from PIL import Image
import click

BASE = "/.config/totpy/"

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

class Base(object):
  """docstring for Totpy"""
  def __init__(self, config_file=None):
    self.config_file = config_file
    if self.config_file:
      self.config = self.loadConfigurationFile()
    else:
      self.config_file = os.path.expanduser("~") + BASE + "config.json"
      if not self.configurationFileExists():
        self.createConfigurationFile()
      else:
        self.loadConfiguration()

  def configurationFileExists(self):
    return os.path.exists(self.config_file)

  def createConfigurationFile(self):
    base = os.path.expanduser("~") + BASE
    print(base)
    if not os.path.exists(base):
      os.mkdir(base)

    with open(self.config_file, "w") as f:
      f.write("{}")
    self.loadConfiguration()

  def loadConfiguration(self):
    with open(self.config_file) as f:
      c = f.read()
    self.config = json.loads(c)

  def saveConfiguration(self):
    with open(self.config_file, 'w') as f:
      c = json.dumps(self.config, indent=2)
      f.write(c)

  def itemList(self):
    items = []
    for item in self.config:
      items.append(item)

    return items

  def colorines(self, color):
    colors = {"red": "\033[0;31;40m",
              "green": "\033[0;32;40m",
              "yellow": "\033[0;33;40m",
              "blue": "\033[0;34;40m",
              "magenta": "\033[0;35;40m",
              "cyan": "\033[0;36;40m",
              "white": "\033[0;37;40m" }

    if color in colors:
      return colors[color]
    else:
      return colors["white"]

  def colorize(self, msg, color):
    color = self.colorines(color)
    ending = "\033[0;37;40m"
    return color + msg + ending

class Totpy(Base):
  def __init__(self, config_file=None):
    Base.__init__(self, config_file=config_file)

  def getTotpTokenByName(self, name):
    for item in self.config:
      if name == item:
        t = Totp(self.config[name]["secret"])
        return t.getTotpToken()

  def addSecret(self, name, secret):
    self.config[name] = {'secret': secret, 'date': time.time()}
    self.saveConfiguration()

  def addSecretQr(self, name, image):
    # otpauth://totp/test?secret=JBSWY3DPEHPK3PXP&issuer=jorgegarciadev
    qr = pyzbar.decode(Image.open(image))
    otpauth = qr[0][0].decode("utf-8")
    pattern = "\?(secret=.+)&"
    secret = re.findall(pattern, otpauth)[0].split('=')[1]
    self.addSecret(name, secret)

  def removeSecret(self, name):
    for item in self.config:
      if name == item:
        self.config.pop(name)
        self.saveConfiguration()
        return 1

  def getQr(self, name):
    for item in self.config:
      if name == item:
        otpauth = "otpauth://totp/%s?secret=%s" % (name, self.config[name]["secret"])
        qr = pyqrcode.create(otpauth)
        return qr.terminal()



def main():

  def copyToken(token):
    import pyperclip
    pyperclip.copy(token)

  CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

  @click.command(context_settings=CONTEXT_SETTINGS)
  @click.option('-s', '--secret', type=str, metavar='SECRET',  help="Returns the TOTP token for the given secret. Used with -add, provides the secret for the new entry")
  @click.option('-qr', type=str, metavar="NAME", help="Prints secret's QR code for the given entry.")
  @click.option('-a', '--add', metavar='NAME', type=str, help="Adds new TOTP to config file using a secret or a QR code. Use with -s or -q")
  @click.option('-r', '--remove', metavar='NAME', type=str, help="Removes the given entry from the configutarion file.")
  @click.option('-q', type=str, metavar='PATH', help="Used with --add. Path to the QR code png image.")
  @click.option('-l', '--list', 'listing', is_flag=True, help="Displays all entries' names in the config file.")
  @click.option('-c', '--conf', metavar='PATH', type=str, help="Overrides the configuration with the one given.")
  @click.option('--copy', is_flag=True, help='Copies the TOTP token to the clipboard.')
  @click.argument("name", required=False)

  def cli(name, secret, qr, q, add, listing, conf, remove, copy):
    """Totpy - CLI TOTP generator and management tool"""

    if listing:
      t = Totpy(conf)
      click.echo(t.itemList())
    elif add: 
      if secret:
        t = Totpy(conf)
        t.addSecret(add, secret)
        click.echo("New item %s added suscessfully!" % (add))
      elif q:
        t = Totpy(conf)
        t.addSecretQr(add, q)
        click.echo("New item '%s' added suscessfully!" % (add))
      else:
        if not secret or not qr:
          click.echo("Missing argument: secret or qr")
    elif remove:
      t = Totpy(conf)
      t.removeSecret(remove)
      click.echo("%s removed suscessfully" % (remove))
    elif secret:
      t = Totp(secret)
      token = t.getTotpToken()
      click.echo(token)
      if copy:
        copyToken(token)
    elif qr:
      t = Totpy(conf)
      qr = t.getQr(qr)
      if qr:
        click.echo(qr)
      else:
        click.echo("No entry with name %s in configuration file" % (qr))
    elif name:
      t = Totpy(conf)
      token = t.getTotpTokenByName(name)
      if token:
        click.echo(token)
        if copy:
          copyToken(token)
      else:
        click.echo("No entry with name %s in configuration file" % (qr))
    else:
      ctx=click.get_current_context(silent=True)
      click.echo(ctx.get_help())

  cli()

if __name__ == '__main__':
  main()
