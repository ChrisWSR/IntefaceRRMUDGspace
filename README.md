# IntefaceRRMUDGspace
# IntefaceRRMUDGspace

This repository contains tools for detecting rocks, bottles, and hammers adapted to ROS. Follow the steps below to set up and run the project.

## Branches

The repository has the following branches:

- `rocks-ros`: Detects rocks and their types.
- `hammer-bottles-ros`: Detects bottles and hammers using ROS.
- `hammer-bottles`: Detects bottles and hammers without ROS.

## Setup Instructions

### 1. Clone the Repository

First, clone the repository to your local machine:

```bash
git clone https://github.com/ChrisWSR/IntefaceRRMUDGspace.git
cd IntefaceRRMUDGspace
```

### 2. Switch Branches

Switch to one of the available branches based on your requirements:

#### For `rocks-ros` branch:

```bash
git checkout rocks-ros
```

#### For `hammer-bottles-ros` branch:

```bash
git checkout hammer-bottles-ros
```

#### For `hammer-bottles` branch:

```bash
git checkout hammer-bottles
```

### 3. Set Up Virtual Environment

Set up the virtual environment using the provided `setup_venv.sh` script:

```bash
source setup_venv.sh
```

### 4. Run the Program

Finally, run the main program using:

```bash
python main.py
```

## Additional Information

- Ensure you have the necessary permissions to execute the `setup_venv.sh` script.
- Make sure ROS is installed and properly configured on your system if you are using the ROS-related branches.

For any issues or further information, please refer to the repository's issues section or contact the repository maintainer.
