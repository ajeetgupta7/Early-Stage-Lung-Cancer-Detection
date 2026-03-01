"""
Verify all dependencies are installed correctly
"""

import sys

def verify_packages():
    """Verify all required packages"""
    
    print("\n" + "=" * 70)
    print("VERIFYING PROJECT DEPENDENCIES")
    print("=" * 70 + "\n")
    
    packages = {
        'pandas': 'Data processing',
        'numpy': 'Numerical computing',
        'scipy': 'Scientific computing',
        'sklearn': 'Machine learning',
        'matplotlib': 'Visualization',
        'seaborn': 'Statistical visualization',
    }
    
    failed = []
    for pkg, description in packages.items():
        try:
            __import__(pkg)
            print(f"✓ {pkg:20} - {description}")
        except ImportError:
            print(f"✗ {pkg:20} - {description} [MISSING]")
            failed.append(pkg)
    
    print("\n" + "=" * 70)
    if failed:
        print(f"❌ Missing packages: {', '.join(failed)}")
        print("\nInstall with:")
        print(f"  pip install -r requirements.txt")
        sys.exit(1)
    else:
        print("✅ All dependencies installed successfully!")
        print("=" * 70 + "\n")
        sys.exit(0)

if __name__ == "__main__":
    verify_packages()
