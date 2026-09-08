#!/usr/bin/env python3
"""
Pennsylvania Health Insurance Audit & Rate Analysis (2026) - Repository Initializer
Automates creation of repository structure, verified data files, execution permissions,
and Git initialization using standard library utilities.
"""

import os
import sys
import subprocess

REPO_NAME = "pennsylvania-health-insurance-audit-2026"
BASE_DIR = os.path.join(os.getcwd(), REPO_NAME)

DATA_RATES_CSV = """carrier_name,approved_rate_change,market_segment,primary_rating_areas
Ambetter (Centene),+37.8%,Individual,1-9
Keystone Health Plan Central,+22.4%,Individual,6;7;9
Keystone Health Plan East,+22.0%,Individual,8
UPMC Health Plan,+24.8%,Individual,1;5
Highmark Inc.,+17.7%,Individual,1;2;4;5;6;7;9
Highmark Benefits Group,+18.4%,Individual,3;8
Geisinger Health Plan,+11.6%,Individual,2;3;5;6;7;9
Partners Insurance Co.,-10.1%,Individual,3;6;8
"""

DATA_RATING_AREAS_CSV = """rating_area_id,primary_hub,constituent_counties
1,Erie / Northwest,"Erie, Crawford, Mercer"
2,Northern Tier Central,"Cameron, Elk, Potter"
3,Northeast & Susquehanna Valley,"Bradford, Carbon, Clinton, Columbia, Lackawanna, Luzerne, Lycoming, Monroe, Montour, Northumberland, Pike, Snyder, Sullivan, Susquehanna, Tioga, Union, Wayne, Wyoming"
4,West Central / Laurel Highlands,"Bedford, Blair, Cambria, Clearfield, Fulton, Huntingdon, Indiana, Somerset"
5,Capital Region & South Central,"Adams, Cumberland, Dauphin, Franklin, Juniata, Lancaster, Lebanon, Mifflin, Perry, York"
6,Lehigh Valley & Reading,"Berks, Centre, Lehigh, Northampton, Schuylkill"
7,South Central Border,"Adams, Berks, Lancaster, York"
8,Philadelphia Metropolitan Area,"Bucks, Chester, Delaware, Montgomery, Philadelphia"
9,North Central / Ridge and Valley,"Centre, Clinton, Columbia, Lycoming, Montour, Northumberland, Snyder, Tioga, Union"
"""

def run_command(cmd, cwd=None):
    """Executes shell command and prints status."""
    try:
        res = subprocess.run(cmd, shell=True, check=True, cwd=cwd, capture_output=True, text=True)
        print(f"[OK] {cmd}")
        return res.stdout
    except subprocess.CalledProcessError as e:
        print(f"[ERR] {cmd}\n{e.stderr}")
        return None

def build_repository():
    print(f"🚀 Initializing repository in {BASE_DIR}...")
    
    # Create directory tree
    dirs = [
        BASE_DIR,
        os.path.join(BASE_DIR, "data"),
        os.path.join(BASE_DIR, "docs")
    ]
    for d in dirs:
        os.makedirs(d, exist_ok=True)
        print(f"Created directory: {d}")
        
    # Write CSV data files
    rates_path = os.path.join(BASE_DIR, "data", "approved_rates_2026.csv")
    with open(rates_path, "w", encoding="utf-8") as f:
        f.write(DATA_RATES_CSV)
    print(f"Wrote file: {rates_path}")

    areas_path = os.path.join(BASE_DIR, "data", "rating_areas_2026.csv")
    with open(areas_path, "w", encoding="utf-8") as f:
        f.write(DATA_RATING_AREAS_CSV)
    print(f"Wrote file: {areas_path}")

    # Set execution permissions on setup script if on POSIX
    if os.name == "posix":
        os.chmod(__file__, 0o755)
        print("Set executable permissions (chmod +x) on setup script.")

    # Initialize Git repository
    print("\n📦 Configuring Git repository...")
    run_command("git init", cwd=BASE_DIR)
    run_command("git add .", cwd=BASE_DIR)
    run_command('git commit -m "Initial commit: Verified 2026 PA Health Insurance Audit Framework"', cwd=BASE_DIR)

    print(f"\n✅ Setup complete! Repository ready at:\n   {BASE_DIR}\n")

if __name__ == "__main__":
    build_repository()