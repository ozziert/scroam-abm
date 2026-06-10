# SCROAM v0.1

SCROAM is a minimal, mechanism-based agent simulation for a master's thesis on
supply chain resilience under non-damage business interruption (NDBI).

The prototype studies German manufacturing exposure to low-wind electricity
price shocks. It compares whether parametric NDBI insurance and a shared
peer-to-peer (P2P) liquidity pool can reduce unfunded Additional Increased Cost
of Working (AICOW), production disruption, stock-outs, and supply chain ripple
effects.

SCROAM v0.1 uses plain Python classes rather than Mesa. The priority is a
transparent mechanism that can be explained, tested, and extended in the
thesis.

## Conceptual Model

The daily mechanism is:

1. A synthetic wind index is generated.
2. Low wind increases the synthetic electricity spot price.
3. A price above the normal level creates operational AICOW.
4. Insurance may pay when both the wind and price triggers are met.
5. In the combined scenario, the P2P pool funds part of the remaining loss.
6. Unfunded AICOW reduces effective production capacity.
7. Lower production depletes inventory and can create stock-outs.

This is not a trading-level electricity price forecasting model or an
electricity derivative model. It is an operational resilience prototype using
plausible synthetic shocks.

## Scenarios

| Scenario | Mechanism |
| --- | --- |
| `safety_stock_only` | Inventory buffer plus a fixed disrupted-capacity factor |
| `traditional_bi` | Traditional BI comparator with no NDBI payout for the synthetic price shock |
| `parametric_ndbi` | Wind-and-price trigger with an AICOW-linked payout |
| `parametric_ndbi_p2p` | Parametric NDBI plus shared P2P liquidity for residual loss |

The P2P pool is shared by all manufacturers and has finite capital. Payouts stop
when the pool is depleted.

## Key Performance Indicators

- Stock-out rate
- Average service level
- Total AICOW
- Total parametric insurance payout
- Total P2P payout
- Residual loss
- Total system cost proxy
- P2P pool depletion and remaining capital

For v0.1, total system cost is defined as residual loss plus insurance and P2P
payouts. This is deliberately simplified. Later versions can model premiums,
pool contributions, financing costs, and transfer costs separately.

## Run in Google Colab

First publish the repository to GitHub as described in the next section. Then
open a new Google Colab notebook and run these cells in order.

Cell 1 - clone and install:

```python
GITHUB_USERNAME = "YOUR_GITHUB_USERNAME"
REPOSITORY = "scroam-abm"

%cd /content
!git clone https://github.com/{GITHUB_USERNAME}/{REPOSITORY}.git
%cd {REPOSITORY}
!python -m pip install -r requirements.txt
```

Cell 2 - run the complete 100-seed experiment:

```python
!python scripts/run_colab_demo.py
```

Cell 3 - inspect the generated tables:

```python
import pandas as pd

results = pd.read_csv("outputs/results/scroam_v01_results.csv")
summary = pd.read_csv("outputs/results/scroam_v01_summary.csv")

display(results.head())
display(summary)
```

Cell 4 - display one generated figure:

```python
from IPython.display import Image, display

display(Image(filename="outputs/figures/average_service_level.png"))
```

The included
[`notebooks/SCROAM_v01_Colab_Run.ipynb`](notebooks/SCROAM_v01_Colab_Run.ipynb)
also provides cells for installation, execution, result display, and plotting.
Replace `YOUR_GITHUB_USERNAME` after publishing the repository.

## Publish to GitHub

1. Sign in to GitHub and open <https://github.com/new>.
2. Create a public repository named `scroam-abm`.
3. Do not add a README, `.gitignore`, or license on GitHub because these files
   already exist locally.
4. Run the following commands from the local `scroam-abm` directory, replacing
   `YOUR_GITHUB_USERNAME` once:

```bash
git init
git add .
git commit -m "Initial SCROAM v0.1"
git branch -M main
git remote add origin https://github.com/YOUR_GITHUB_USERNAME/scroam-abm.git
git push -u origin main
```

If GitHub CLI is installed and authenticated, it can create and push the
repository directly instead:

```bash
git init
git add .
git commit -m "Initial SCROAM v0.1"
git branch -M main
gh repo create scroam-abm --public --source=. --remote=origin --push
```

Before committing, `git status --short` should not list `.venv/`, `build/`,
Python cache files, generated CSV files, or generated PNG files.

## Local Setup

Python 3.10 or newer is required.

### macOS/Linux

```bash
git clone https://github.com/YOUR_GITHUB_USERNAME/scroam-abm.git
cd scroam-abm
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pytest
python scripts/run_colab_demo.py
```

### Windows PowerShell

```powershell
git clone https://github.com/YOUR_GITHUB_USERNAME/scroam-abm.git
cd scroam-abm
py -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install -r requirements.txt
py -m pytest
py scripts\run_colab_demo.py
```

### Git Bash on Windows

```bash
git clone https://github.com/YOUR_GITHUB_USERNAME/scroam-abm.git
cd scroam-abm
python -m venv .venv
source .venv/Scripts/activate
python -m pip install -r requirements.txt
python -m pytest
python scripts/run_colab_demo.py
```

Results are saved to:

```text
outputs/results/scroam_v01_results.csv
outputs/results/scroam_v01_summary.csv
outputs/figures/
```

## Use from Python

```python
from scroam.config import SimulationConfig
from scroam.experiments import run_monte_carlo
from scroam.model import SUPPORTED_SCENARIOS

config = SimulationConfig()
results = run_monte_carlo(config, SUPPORTED_SCENARIOS, n_runs=100)
```

All random values are generated from explicit simulation seeds. The same seed
is reused across scenarios in the Monte Carlo runner, supporting like-for-like
scenario comparison.

## Project Status

Version 0.1 uses synthetic wind and electricity price data. Future versions are
intended to integrate empirical ERA5 wind data and EPEX SPOT electricity price
data, calibrate manufacturing exposure, and introduce explicit supply network
links for richer ripple-effect analysis.
