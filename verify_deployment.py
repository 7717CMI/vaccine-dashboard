#!/usr/bin/env python3
"""
Pre-Deployment Verification Script
Checks all files and configurations before pushing to GitHub/Render
"""

import os
import sys

def check_file_exists(filename, required=True):
    """Check if a file exists"""
    exists = os.path.exists(filename)
    status = "[OK]" if exists else ("[REQUIRED]" if required else "[OPTIONAL]")
    print(f"{status} {filename}")
    if required and not exists:
        return False
    return True

def check_file_content(filename, required_strings):
    """Check if file contains required strings"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        
        all_found = True
        for req_string in required_strings:
            if req_string in content:
                print(f"  [OK] Contains: '{req_string[:50]}...'")
            else:
                print(f"  [MISSING] '{req_string[:50]}...'")
                all_found = False
        return all_found
    except Exception as e:
        print(f"  [ERROR] Error reading file: {e}")
        return False

def main():
    print("=" * 70)
    print("DEPLOYMENT VERIFICATION SCRIPT")
    print("=" * 70)
    print()
    
    # Check required files
    print("Checking Required Files:")
    print("-" * 70)
    
    required_files = [
        'app.py',
        'pages.py',
        'callbacks.py',
        'requirements.txt',
        'Procfile',
        'runtime.txt',
        'README.md',
        '.gitignore'
    ]
    
    optional_files = [
        'Dockerfile',
        'docker-compose.yml',
        'render.yaml',
        'DEPLOYMENT.md'
    ]
    
    all_required_exist = True
    for file in required_files:
        if not check_file_exists(file, required=True):
            all_required_exist = False
    
    print()
    print("Optional Files:")
    print("-" * 70)
    for file in optional_files:
        check_file_exists(file, required=False)
    
    print()
    
    if not all_required_exist:
        print("[FAILED] Some required files are missing!")
        return False
    
    # Check app.py for server variable
    print("Checking app.py Configuration:")
    print("-" * 70)
    app_checks = check_file_content('app.py', [
        'server = app.server',
        'import dash',
        'from pages import',
        'from callbacks import register_all_callbacks'
    ])
    print()
    
    # Check requirements.txt
    print("Checking requirements.txt:")
    print("-" * 70)
    req_checks = check_file_content('requirements.txt', [
        'dash==',
        'dash-bootstrap-components==',
        'plotly==',
        'pandas==',
        'gunicorn==',
        'numpy=='
    ])
    print()
    
    # Check Procfile
    print("Checking Procfile:")
    print("-" * 70)
    proc_checks = check_file_content('Procfile', [
        'web: gunicorn app:server',
        '$PORT'
    ])
    print()
    
    # Check runtime.txt
    print("Checking runtime.txt:")
    print("-" * 70)
    runtime_checks = check_file_content('runtime.txt', ['python-3.11'])
    print()
    
    # Check .gitignore
    print("Checking .gitignore:")
    print("-" * 70)
    gitignore_checks = check_file_content('.gitignore', [
        '__pycache__',
        'venv/',
        '.env'
    ])
    print()
    
    # Check assets folder
    print("Checking assets folder:")
    print("-" * 70)
    assets_exist = check_file_exists('assets/custom.css', required=True)
    print()
    
    # Final verdict
    print("=" * 70)
    if all([app_checks, req_checks, proc_checks, runtime_checks, gitignore_checks, assets_exist]):
        print("[SUCCESS] ALL CHECKS PASSED - READY FOR DEPLOYMENT!")
        print()
        print("Next steps:")
        print("1. git add .")
        print("2. git commit -m 'Deploy: Ready for production'")
        print("3. git push origin main")
        print("4. Deploy on Render Dashboard")
        print()
        return True
    else:
        print("[FAILED] SOME CHECKS FAILED - PLEASE FIX BEFORE DEPLOYMENT")
        print()
        return False
    print("=" * 70)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
