# NIAGADS Open Access Scavenger Hunt Application

A Streamlit app for a 20–30 minute genomics workshop where teams review open NIAGADS resources for one Alzheimer’s disease gene and build a gene evidence summary.

## What participants do

Teams receive or choose one gene from a curated list pulled from intersection of GVC Genes and ADVP curated genes to ensure all questions will give a positive result.

They complete guided activities using NIAGADS and related open resources:

- [ADVP](https://advp.niagads.org/)
- [GenomicsDB](https://www.niagads.org/genomics)
- [FILER](https://tf.lisanwanglab.org/FILER/)
- [VariXam](https://varixam.niagads.org/)
- [TopGenes](https://topgenes.niagads.org/)
- [xQTL Browser](https://xqtl.niagads.org/)
- [NIAGADS API](https://api.niagads.org/)

## Features

- Streamlit workshop app with an in-app leaderboard view
- No application database; uses `st.session_state` plus Google Sheets-backed leaderboard storage
- Team name and random team label generator
- Optional team leader contact email
- Random assigned gene button plus manual gene override
- Visible 20-minute countdown timer
- Workshop Progress sidebar with timer, gene, score, progress, and completed skills
- Activity sections with resource buttons, required answer fields, and inline hints
- Directed GenomicsDB activity that moves from a gene record to summary statistics, dataset record, variant record, genome browser, and follow-up region
- Functional annotation activity that uses the region carried forward from GenomicsDB
- Required activity progress plus inline bonus prompts
- Final Gene Evidence Summary preview
- Leaderboard view backed by Google Sheets

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Deploy on Streamlit Community Cloud

1. Push this repository to GitHub.
2. In Streamlit Community Cloud, create a new app from the repository.
3. Set the main file path to `app.py`.
4. Add Google Sheets credentials in Streamlit secrets if using the leaderboard.
5. Deploy. Streamlit will install dependencies from `requirements.txt`.

## Google Sheets leaderboard setup

The leaderboard is optional. If Google Sheets secrets are not configured, the app still runs and shows a warning in the Submit Results area.

### 1. Create the Google Sheet

1. Go to <https://sheets.google.com>.
2. Create a new blank spreadsheet.
3. Rename it something recognizable, such as `NIAGADS Workshop Leaderboard`.
4. Copy the spreadsheet ID from the browser URL.

For example, if the URL is:

```text
https://docs.google.com/spreadsheets/d/1abcDEFghiJKLmnoPQRstuVWxyz/edit
```

the spreadsheet ID is:

```text
1abcDEFghiJKLmnoPQRstuVWxyz
```

### 2. Create a Google Cloud project

1. Go to <https://console.cloud.google.com/>.
2. In the top project menu, select **New Project**.
3. Name it something like `NIAGADS Workshop Leaderboard`.
4. Click **Create**.
5. Make sure this new project is selected in the top project menu before continuing.

### 3. Enable Google Sheets API

1. In Google Cloud Console, go to **APIs & Services** > **Library**.
2. Search for `Google Sheets API`.
3. Open **Google Sheets API**.
4. Click **Enable**.

### 4. Create the service account

1. Go to **IAM & Admin** > **Service Accounts**.
2. Click **Create service account**.
3. Enter a name, for example `streamlit-leaderboard`.
4. Click **Create and continue**.
5. For this app, you do not need to grant project-wide roles. Click **Continue**.
6. Click **Done**.

### 5. Create and download the JSON key

1. On the **Service Accounts** page, click the service account you just created.
2. Open the **Keys** tab.
3. Click **Add key** > **Create new key**.
4. Choose **JSON**.
5. Click **Create**.
6. Google downloads a `.json` file. Keep it private.

### 6. Share the Sheet with the service account

1. Open the downloaded `.json` file.
2. Copy the `client_email` value. It will look like:

```text
streamlit-leaderboard@your-project.iam.gserviceaccount.com
```

1. Go back to the Google Sheet.
2. Click **Share**.
3. Paste the service account email.
4. Give it **Editor** access.
5. Click **Send** or **Share**.

### 7. Add Streamlit secrets

The downloaded Google key is JSON, but Streamlit secrets are written as TOML. Use the helper script to convert the JSON key into `.streamlit/secrets.toml`:

```bash
python3 scripts/create_streamlit_secrets.py --json-key path/to/google-key.json --spreadsheet-id your-google-sheet-id
```

To use a worksheet/tab name other than `Leaderboard`:

```bash
python3 scripts/create_streamlit_secrets.py --json-key path/to/google-key.json --spreadsheet-id your-google-sheet-id --worksheet-name "Workshop Scores"
```

The script refuses to overwrite an existing secrets file unless you add `--force`.

For Streamlit Community Cloud, open the generated `.streamlit/secrets.toml`, copy its contents, and paste them into the app's **Secrets** settings.

Manual format, if needed:

```toml
[leaderboard]
spreadsheet_id = "your-google-sheet-id"
worksheet_name = "Leaderboard"

[gcp_service_account]
type = "service_account"
project_id = "..."
private_key_id = "..."
private_key = "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"
client_email = "service-account@project.iam.gserviceaccount.com"
client_id = "..."
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "..."
```

Notes:

- `worksheet_name` can be any tab name. If it does not exist, the app creates it.
- Keep the private key on one TOML line with `\n` line breaks, as shown above.
- Do not commit `.streamlit/secrets.toml` to Git.

## Workshop facilitation notes

- Suggested duration: 20 minutes of activity time plus 5–10 minutes for discussion.
- The GenomicsDB activity is designed as the main within-site navigation exercise.
- Optional bonus prompts add points and are not required for completion.
- Hints guide participants without changing the score.
- An activity is complete when all required fields for that activity are filled.
- Leaderboard submissions are written to Google Sheets.
- Participant-facing download buttons are intentionally omitted.
