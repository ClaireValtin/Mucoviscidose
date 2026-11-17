# Mucoviscidose · CFTR desk

A cystic fibrosis and *CFTR* reference desk: variant lookup plus the clinical essentials on one page.

**Open it:** https://clairevaltin.github.io/Mucoviscidose/

## What it does

- **Variant lookup** – type one CFTR variant, or two for a genotype, and get the CFTR2 interpretation (CF-causing, varying clinical consequence, non CF-causing) together with live ClinVar data. Legacy names (e.g. `F508del`), c., p. and genomic coordinates (GRCh38 or GRCh37) all work.
- **Browse** the full CFTR2 variant list
- **Gene and variant classes** – locus, protein, the six functional classes and the targeted therapies for each
- **Clinical sections** – how CF presents, sweat chloride interpretation, the path from suspicion to diagnosis, genetic testing and counselling, CFTR modulators and supportive care
- Every section links to its sources

## How to use

Open the link above. Nothing to install.

## Repository contents

- `index.html` – the whole app, with the CFTR2 list embedded
- `data/CFTR2_*.xlsx` – the CFTR2 variant list it was built from
- `tools/build_cftr2.py` – script that embeds a new CFTR2 release into the page

## Disclaimer

**This tool is NOT validated for clinical or diagnostic use.** It is provided for research and educational purposes only, without any warranty.

## License & citation

© 2026 Soufiyan Rehioui. All rights reserved.

You're welcome to explore this code. If you'd like to use, adapt, or share it, please get in touch first: rehiouisoufiyan@gmail.com

If this work helps you, please cite it or link back to this repository.
