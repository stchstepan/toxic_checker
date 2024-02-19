# toxic-checker

Toxic Checker is a Python script designed to identify potentially toxic libraries in a project's dependencies. It uses a pre-defined database of toxic repositories and generates a Software Benchmarking Report (SBOM) for the project. By comparing the extracted library names from the SBOM with the toxic repository database, it identifies potential matches and provides information on the degree of similarity.

## Usage.

1. Run the Toxic Checker script:

``bash
sudo python3 toxic_checker.py
```

2. Follow the prompts to provide information about your project, including languages used and SBOM file path/names.

3. Toxic Checker will generate SBOM files and compare the extracted library names against the toxic repository database.

4. The script will output any matches found, including project language, library names, toxic repository names, and similarity factor.

## Note

- Adjust the similarity threshold (the script defaults to 60%) as needed to customize the matching criteria.
- Internet connection is required to obtain the database of toxic repositories and necessary packages.