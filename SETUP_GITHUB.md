# GitHub Repository Setup Instructions

## Step 1: Create GitHub Repository

1. Go to [GitHub](https://github.com)
2. Click the "+" button in the top right corner
3. Select "New repository"
4. Fill in repository details:
   - **Repository name**: `magicavoxel-mcp-gen`
   - **Description**: `A comprehensive toolkit for working with MagicaVoxel files and palettes`
   - **Visibility**: Public or Private (your choice)
   - **Don't initialize** with README, .gitignore, or license (we already have these)

5. Click "Create repository"

## Step 2: Connect Local Repository to GitHub

After creating the repository, GitHub will show you commands. Run these in your terminal:

```bash
# Add remote repository (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/magicavoxel-mcp-gen.git

# Push to GitHub
git push -u origin main
```

## Step 3: Alternative - Using SSH (Recommended)

If you have SSH keys set up:

```bash
git remote add origin git@github.com:YOUR_USERNAME/magicavoxel-mcp-gen.git
git push -u origin main
```

## What's Included in Your Repository

✅ **Complete toolkit** for MagicaVoxel palette work  
✅ **255-color palette** extracted from your image  
✅ **Utility functions** for color matching  
✅ **Example scripts** for creating voxel models  
✅ **Documentation** and usage guides  
✅ **Requirements** file for easy setup  
✅ **Proper .gitignore** for Python projects  

## Repository Structure After Push

```
magicavoxel-mcp-gen/
├── .gitignore              # Python gitignore
├── README.md               # Main project documentation
├── README_PALETTE.md       # Palette-specific documentation
├── requirements.txt        # Python dependencies
├── palette_utils.py        # Core palette utilities
├── extract_palette.py      # Palette extraction script
├── create_red_cube.py      # Example usage
├── magica_palette.json     # Your extracted palette (255 colors)
├── SETUP_GITHUB.md         # This file
├── Pallet/                 # Directory with your palette image
│   └── pallet.png         # Your MagicaVoxel palette
└── red_cube.vox           # Example output (ignored by git)
```

## Next Steps After Setup

1. **Clone on other machines**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/magicavoxel-mcp-gen.git
   cd magicavoxel-mcp-gen
   pip install -r requirements.txt
   ```

2. **Share your work**: Send the GitHub link to others

3. **Contribute**: Make changes and push updates:
   ```bash
   git add .
   git commit -m "Your changes"
   git push
   ```

## Troubleshooting

### If push fails with "error: src refspec main does not match any"
```bash
git branch -M main
git push -u origin main
```

### If you need to set up GitHub authentication
- **HTTPS**: Use GitHub Personal Access Token
- **SSH**: Set up SSH keys (recommended for frequent use)

### If repository already exists remotely
```bash
git remote set-url origin https://github.com/YOUR_USERNAME/magicavoxel-mcp-gen.git
git push -u origin main
```

## Repository Features

- 🎨 **255 custom colors** from your MagicaVoxel palette
- 🔧 **Easy integration** with any voxel project
- 📚 **Complete documentation** and examples
- 🚀 **Ready to use** - just install and run
- 🔄 **Updatable** - easily change your palette

Your repository is ready for sharing and collaboration!
