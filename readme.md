# Docker Image File System Extractor (DIFSE)

**Version:** 1.0.0

DIFSE is a utility tool designed to pull Docker images, save them into tar archives, and extract their file systems for analysis.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [License](#license)

## Prerequisites

- Python 3.x
- Docker

Ensure Docker is running and you have the necessary permissions to pull and manipulate images.

## Installation

1. Clone this repository:
    ```bash
    git clone https://github.com/n3tw4rl0k/difse.git
    ```

2. Navigate to the directory:
    ```bash
    cd difse
    ```

## Usage

Run the script using the following command:

```bash
python3 difse.py gcr.io/distroless/cc-debian11:latest
```
