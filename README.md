[![Active](https://img.shields.io/badge/status-actively_maintained-darkgreen)](#)  [![Python](https://img.shields.io/badge/python-3.x-blue?logo=python)](#)  [![Platform](https://img.shields.io/badge/platform-cross--platform-lightgrey)](#) [![Privacy](https://img.shields.io/badge/privacy-100%25_local-darkgreen)](#)

[![Stars](https://img.shields.io/github/stars/gokeeper/tesla-order-status?style=social)](https://github.com/gokeeper/tesla-order-status/stargazers) [![Forks](https://img.shields.io/github/forks/gokeeper/tesla-order-status?style=social)](https://github.com/gokeeper/tesla-order-status/network/members) [![Issues](https://img.shields.io/github/issues/gokeeper/tesla-order-status?style=social)](https://github.com/gokeeper/tesla-order-status/issues)

[![Referral](https://img.shields.io/badge/support-via_Tesla_referral-cc0000?logo=tesla&logoColor=white)](https://ts.la/nan462780)

# TOSTL — Tesla Order Status Tracker Lite 🚗📦
Stay in control of your Tesla order from the moment you place it until delivery. This open-source Python tool gives you direct access to the Tesla API so you always know what is happening with your vehicle.

> 🍴 **Fork notice:** This is a stripped-down fork of [chrisi51/tesla-order-status](https://github.com/chrisi51/tesla-order-status) — all telemetry, third-party data collection, auto-updaters, multi-language UI, and clipboard/share helpers have been removed. The only network connections made by this script are to Tesla's own API endpoints; nothing is sent anywhere else.
>
> 🔑 **OAuth fix credit:** The `tesla://auth/callback` redirect URI fix that restores login in June 2026 was adapted from [adriankumpf/tesla_auth#99](https://github.com/adriankumpf/tesla_auth/issues/99). See the [Authentication](#authentication) section for the new flow.

## Table of Contents
1. [Why You'll Love It](#why-youll-love-it)
2. [Get Started](#get-started)
3. [Installation](#installation)
4. [Authentication](#authentication)
5. [Usage](#usage)
6. [Configuration](#configuration)
7. [History & Preview](#history--preview)
8. [Disclaimer](#disclaimer)
9. [Support & Contact](#support--contact)

## Why You'll Love It
- 🔍 **Direct Tesla API connection**: Get the latest order information without any detours.
- 🧾 **Display of important details**: Vehicle options, production and delivery progress.
- 🕒 **History at a glance**: Every change (e.g. VIN allocation) is documented locally.
- 🔁 **Multi-order ready**: Handles multiple Tesla orders at once, with `--order <reference>` to focus on a single one.
- 🪶 **Lite**: No telemetry, no auto-updater, no clipboard helpers, no third-party services — just orders.
- 🔐 **Privacy-focused**: Tokens and settings remain on your device. Nothing is sent anywhere except Tesla's own API.

The goal is to give users more transparency and control over the ordering process – without depending on external services.

## Get Started
Download the complete project to your machine. If you are unsure how, you can grab the ZIP archive directly from GitHub: https://github.com/gokeeper/tesla-order-status/archive/refs/heads/main.zip
> ⚠️ Do not run single scripts without the rest of the repository. Everything is meant to work together.

## Installation

1. Install [Python 3](https://www.python.org/downloads/) for your operating system.
2. Install the required dependency:
```sh
pip install requests
```

### macOS Tip
For a clean setup, create a virtual environment before installing dependencies:
```sh
# create the environment
python3 -m venv .venv
# activate it
source .venv/bin/activate
# install dependencies just for this project
python3 -m pip install requests
```

## Authentication
On first run the script opens Tesla's login page in your browser. After you complete login (and 2FA), Tesla redirects to the custom URL scheme `tesla://auth/callback?code=...`. Because this is not a regular `https://` URL, the browser will not display it as a page — it may prompt to open the Tesla app, show "can't open link", or just stay on a blank/previous page. **That is expected.**

To capture the URL with the authorization code:

1. Before submitting the login form, open your browser's Developer Tools (**F12**) and switch to the **Network** tab. Enable **Preserve log** so entries survive the redirect.
2. Complete the Tesla login (email → password → 2FA).
3. In the Network tab, find the last request to `auth.tesla.com/...` that responds with **302**. Open its **Headers** and copy the value of the **Location** response header — it will look like `tesla://auth/callback?code=...&state=...`.
4. Paste that URL into the script when prompted.

Tokens are exchanged directly with Tesla; nothing leaves your machine. With your permission the resulting `tesla_tokens.json` is saved locally for future runs.

> ℹ️ Tesla disabled the previous `https://auth.tesla.com/void/callback` redirect URI in 2026, which is why the flow now uses the custom `tesla://` scheme. If you used an older version of this script and hit `The 'redirect_uri' supplied is not registered for this 'client_id'`, update to the latest version.

## Usage
Run the main script to fetch and display your order details:
```sh
python3 tostl.py
```
### Optional flags:
Get an overview of all command-line options:
```sh
python3 tostl.py --help
```
#### Output Modes
Only one of the options can be used at a time.
- `--all` display every available key in your history (verbose output)
- `--details` show additional information such as financing details.
- `--status` only report whether the order information has changed since the last run. no login happens, so tesla_tokens.json have to be present already. token will get refreshed if necessary.
  - 0 => no changes
  - 1 => changes detected
  - 2 => pending updates
  - -1 => error ... you better run the script once without any params to make sure, it is working. Possibly the api token is invalid or there is no tesla_orders.json already

#### Work Modes
Work modes can be combined with any output mode:
- `--cached` – reuse locally cached order data without calling the API
- Automatic caching activates when you run the script again within one minute of a successful API request, keeping Tesla happy with fewer calls.

#### Order Filters
- `--order <referenceNumber>` – refresh every order in the background but only print the selected one (e.g. `--order RN123456`).

## Configuration
### General Settings
The script stores the configuration in `data/private/settings.json`. Feel free to tweak it—if something breaks, the script falls back to default values.

### Option Codes
Known Tesla option codes are bundled with the repository in `data/public/option-codes/codes.json` (snapshot taken from the upstream codebase). You can drop additional JSON files into `data/public/option-codes/` to extend or override entries; later files win if the same code is defined more than once.

## History & Preview
The script stores the latest order information in `tesla_orders.json` and keeps a change log in `tesla_order_history.json`. Every detected difference—like a VIN assignment—is appended to the history file and displayed after the current status. The "Order Information" section always shows live data first, followed by historical changes.

### Order Information
```
---------------------------------------------
              ORDER INFORMATION
---------------------------------------------
Order Details:
- Order ID: RN100000000
- Status: BOOKED
- Model: my
- VIN: N/A

Configuration Options:
- APBS: Autopilot base features
- APPB: Enhanced Autopilot
- CPF0: Standard Connectivity
- IPW8: Interior: Black and White
- MDLY: Model Y
- MTY47: Model Y Long Range Dual Motor
- PPSB: Paint: Deep Blue Metallic
- SC04: Pay-per-use Supercharging
- STY5S: Seating: 5 Seat Interior
- WY19P: 19" Crossflow wheels (Model Y Juniper)

Delivery Information:
- Routing Location: None (N/A)
- Delivery Center: Tesla Delivery & Used Car Center Hanau Holzpark
- Delivery Window: 6 September - 30 September
- ETA to Delivery Center: None
- Delivery Appointment: None

Financing Information:
- Finance Product: OPERATIONAL_LEASE
- Finance Partner: Santander Consumer Leasing GmbH
- Monthly Payment: 683.35
- Term (months): 48
- Interest Rate: 6.95 %
- Range per Year: 10000
- Financed Amount: 60270
- Approved Amount: 60270
---------------------------------------------
```

### Timeline
```
Order Timeline:
- 2025-08-07: Reservation
- 2025-08-07: Order Booked
- 2025-08-07: Delivery Window: 6 September - 30 September
- 2025-08-23: new Delivery Window: 10 September - 30 September
```

### Change History
```
Change History:
2025-08-19: ≠ 0.details.tasks.deliveryDetails.regData.regDetails.company.address.careOf: Maximilian Mustermann -> Max Mustermann
2025-08-19: ≠ 0.details.tasks.deliveryDetails.regData.orderDetails.vin: None -> 131232
2025-08-19: + 0.details.tasks.deliveryDetails.regData.orderDetails.userId: 10000000
2025-08-19: - 0.details.tasks.deliveryDetails.regData.orderDetails.ritzbitz
```

## Issues
If you have any issues, running the script or getting error messages, please feel free to ask for help in the [issues](https://github.com/gokeeper/tesla-order-status/issues) section.


## Disclaimer
- The script runs locally on your machine.
- The only network connections are to Tesla's own API endpoints for authentication and order data.
- You need to log in via browser and return the resulting URL to the script to extract the login token used for the API.
- The script only uses the token to work with for the current session.
- With your permission the script stores the token on your hard disk.

## Support & Contact
If you want to support the project, you can use my link on your next Tesla order: https://ts.la/nan462780
