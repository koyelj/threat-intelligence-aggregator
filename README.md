\# Threat Intelligence Aggregator



A Python-based cybersecurity project for collecting, processing, normalizing, and correlating threat intelligence indicators.



\## Features



\* Threat intelligence feed processing

\* Indicator of Compromise (IOC) parsing

\* Indicator normalization

\* Correlation of repeated indicators across sources

\* Rule-based risk scoring and severity classification

\* PostgreSQL database integration

\* Blocklist generation and export



\## Technologies Used



\* Python

\* PostgreSQL

\* SQL

\* Git and GitHub



\## Project Structure



\* `database/` — Database-related components

\* `feeds/` — Threat intelligence feeds

\* `parser/` — IOC parsing

\* `processing/` — Data processing

\* `normalization/` — Indicator normalization

\* `correlation/` — Indicator correlation and blocklist generation

\* `enrichment/` — Enrichment components

\* `exports/` — Generated outputs

\* `dashboard/` — Dashboard components

\* `logs/` — Log files



\## Running the Project



Activate the virtual environment and run the relevant Python modules from the project directory.



Example commands, if applicable to your current implementation:



```powershell

python -m correlation.correlate

python -m correlation.blocklist\_generator

```



\## Purpose



The project demonstrates how threat intelligence indicators can be organized, correlated, risk-scored, and exported to support defensive cybersecurity analysis.



\## Author



Koyel Jana



\## Disclaimer



For educational purposes and defensive cybersecurity use.



