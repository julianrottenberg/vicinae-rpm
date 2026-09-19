# vicinae-rpm

RPM builds of [vicinae](https://vicinae.com) for openSUSE Tumbleweed,
built from source in a Tumbleweed container by GitHub Actions.

Checks upstream releases every 6 hours; new releases are built, signed,
and published automatically.

## Use

```
sudo rpm --import https://julianrottenberg.github.io/vicinae-rpm/repodata/repomd.xml.key
sudo zypper ar -cfp 95 https://julianrottenberg.github.io/vicinae-rpm/ vicinae-rpm
sudo zypper ref vicinae-rpm
sudo zypper in vicinae
```

After that, `zypper dup` keeps vicinae current.
