#!/bin/bash

# Script to install Node.js on macOS
# This script will install Homebrew (if not installed) and then Node.js

echo "Checking for Homebrew..."
if ! command -v brew &> /dev/null; then
    echo "Homebrew not found. Installing Homebrew..."
    echo "You will be prompted for your password."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    
    # Add Homebrew to PATH for Apple Silicon Macs
    if [ -f "/opt/homebrew/bin/brew" ]; then
        echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zshrc
        eval "$(/opt/homebrew/bin/brew shellenv)"
    fi
else
    echo "Homebrew is already installed."
fi

echo "Installing Node.js..."
brew install node

echo ""
echo "Installation complete! Please restart your terminal or run:"
echo "source ~/.zshrc"
echo ""
echo "Then verify with:"
echo "node --version"
echo "npm --version"

