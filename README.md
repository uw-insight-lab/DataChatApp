# DataChatApp

Example template application for building an LLM-power chart bot that is meant to analyze data.

*Note: this repository is still under construction*

## Getting started 

### Prerequisites

1. Install Miniconda or Anaconda
   - Download Miniconda from [here](https://docs.conda.io/en/latest/miniconda.html)
   - Or download Anaconda from [here](https://www.anaconda.com/download)
   - Follow the installation instructions for your operating system


2. Install Git (if not already installed)
   - For Windows: Download and install from [Git for Windows](https://gitforwindows.org/)
   - For macOS: Install via [Homebrew](https://brew.sh/) `brew install git` or download from [git-scm.com](https://git-scm.com/download/mac)

### Installation Steps

1. Clone this repository
   ```bash
   git clone https://github.com/yourusername/DataChatApp.git
   cd DataChatApp
   ```

2. Create and activate the conda environment
   ```bash
   # Create environment from environment.yml
   conda env create -f environment.yml

   # Activate the environment
   conda activate DataChatApp
   ```

3. Verify Installation
   ```bash
   # Check if environment is properly set up
   python -c "import pandas; print('Setup successful!')"
   ```


