### Formal Language Theory

[![Build Status](https://travis-ci.com/Duletov/formal_languages.svg?branch=master)](https://travis-ci.com/Duletov/formal_languages)
[![Build Status](https://travis-ci.com/Duletov/formal_languages.svg?branch=Task01)](https://travis-ci.com/Duletov/formal_languages)
[![Build Status](https://travis-ci.com/Duletov/formal_languages.svg?branch=Task02)](https://travis-ci.com/Duletov/formal_languages)

#### Installation & Running

 - The only requirement for running is Docker:
   - `docker build ./ -t formal_languages --build-arg graph=<path to graph file> --build-arg regex=<path to file with names of regex files> [--build-arg start=<path to the file with start vertices>] [--build-arg end=<path to the file with end vertices>]`
   - `docker run formal_languages`