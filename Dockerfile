# Dockerfile für einen Container, der die kommParl-Spezifikation baut.
# Grundlage ist das Dockerfile aus OParl/spec; für kommParl angepasst
# (siehe HERKUNFT.md).
#
# MIT License
#
# Copyright (c) 2016, Stefan Graupner
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

FROM debian:13-slim

# pandoc, Werkzeuge für die Abbildungen und LaTeX für die PDF-Ausgabe
RUN apt-get update -y && apt-get install --no-install-recommends -y \
  ghostscript \
  lmodern \
  graphviz \
  pandoc \
  texlive-fonts-recommended \
  texlive-plain-generic \
  texlive-humanities \
  texlive-lang-german \
  texlive-lang-greek \
  texlive-latex-recommended \
  texlive-latex-extra \
  texlive-luatex \
  texlive-xetex \
  librsvg2-bin \
  python3 \
  python3-yaml \
  python3-jsonschema \
  imagemagick \
  zip \
  tar \
  git \
  bzip2 && \
  rm -rf /var/lib/apt/lists/* && \
  git config --system --add safe.directory '*'

ENTRYPOINT [ "python3", "build.py" ]

