# Installing Node.js and npm on macOS

You need to install Node.js (which includes npm) to work with the frontend React application.

## Option 1: Install via Homebrew (Recommended)

### Step 1: Install Homebrew (if not already installed)
Open Terminal and run:
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```
Follow the on-screen instructions. You may be prompted for your password.

### Step 2: Install Node.js
After Homebrew is installed, run:
```bash
brew install node
```

### Step 3: Verify Installation
```bash
node --version
npm --version
```

## Option 2: Direct Download (Easier, but less flexible)

1. Visit https://nodejs.org/
2. Download the LTS (Long Term Support) version for macOS
3. Run the installer package (.pkg file)
4. Follow the installation wizard
5. Restart your terminal after installation

### Verify Installation
```bash
node --version
npm --version
```

## Option 3: Install using nvm (Node Version Manager)

If you want to manage multiple Node.js versions:

1. Install nvm:
```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
```

2. Restart your terminal or run:
```bash
source ~/.zshrc
```

3. Install Node.js:
```bash
nvm install --lts
nvm use --lts
```

## After Installation

Once npm is installed, navigate to the frontend directory and install dependencies:

```bash
cd hr-video-analyzer/frontend
npm install
```

Then you can start the development server:
```bash
npm start
```

## Troubleshooting

If npm is still not found after installation:
1. Close and reopen your terminal
2. Check your PATH: `echo $PATH`
3. Verify Node.js location: `which node` (should show `/usr/local/bin/node` or `/opt/homebrew/bin/node` for Apple Silicon Macs)

### If npm is installed but not found in PATH (Homebrew on Apple Silicon)

If you installed via Homebrew on an Apple Silicon Mac (M1/M2/M3), you may need to add Homebrew to your PATH:

```bash
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zshrc
source ~/.zshrc
```

Then verify:
```bash
npm --version
```

### If you get "Could not read package.json" error

Make sure you're in the correct directory. The `package.json` is located in `hr-video-analyzer/frontend/`:

```bash
cd hr-video-analyzer/frontend
npm install
```

