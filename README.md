# OST : Optimal Spectral Transportation
Optimal Spectral Transportation : audio musical unmixing using optimal transport.


This repository contains a Python implementation of Optimal Spectral Transportation, a method proposed in the following NIPS 2016 paper:

R. Flamary, C. Févotte, N. Courty, V. Emyia, "Optimal spectral transportation with application to music transcription", Neural Information Processing Systems (NIPS), 2016.

It also contains a real time demonstration of the proposed method illustrated below.

![screenshotost](https://cloud.githubusercontent.com/assets/1386873/19514575/4e47232a-95f4-11e6-9cd2-3e426d645433.png)


## Installation and dependencies

This repository contains only the ost.py Python module and a demo script.

The ost.py module require only numpy. The real time demonstration that unmix the sound of your microphone requires thoss dependencies.

```
numpy
pyaudio
pygame
```

The dependencies can be installed opn a debian-like linux with the following command

```bash
sudo apt-get install python-numpy python-pyaudio python-pygame
```

The python dependencies can also be installed via pip

```bash
pip install PyAudio Pygame numpy
```

Under MacOSX, if there is a problem when installing pyaudio with pip, you need to install the portausio library with Homebrew.
```bash
brew install portaudio
```


## Real time demonstration

## Contact and contributors

* [Rémi Flamary](http://remi.flamary.com/)
* [Nicolas Courty](http://people.irisa.fr/Nicolas.Courty/)
* [Antony Schutz](http://www.antonyschutz.com/) (audio samples)

## Acknowledgements

We want to thank [Antony Schutz](http://www.antonyschutz.com/) (@DeVerMyst) for composing and providing us the sample files in the data folder.
