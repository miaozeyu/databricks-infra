# Databricks Terraform Configuration

This repository contains Terraform configurations for managing Databricks resources. It includes GitHub Actions workflows for automated deployment and management of Databricks resources.

## Prerequisites

- [Terraform](https://www.terraform.io/downloads.html) >= 1.0.0
- [GitHub Account](https://github.com)
- [Databricks Workspace](https://www.databricks.com/)

## Setup

1. Clone this repository
   ```bash
   git clone https://github.com/miaozeyu/databricks-assignment.git
   cd databricks-assignment
   ```

2. Initialize Terraform
   ```bash
   terraform init
   ```

## GitHub Secrets

Set the following secrets in your GitHub repository settings (Settings > Secrets > Actions):

- `DATABRICKS_HOST`: Your Databricks workspace URL
- `DATABRICKS_TOKEN`: Your Databricks personal access token
- `TF_API_TOKEN`: Your Terraform Cloud API token (if using Terraform Cloud)

## Usage

### Plan Changes

```bash
terraform plan -var="databricks_host=$DATABRICKS_HOST" -var="databricks_token=$DATABRICKS_TOKEN"
```

### Apply Changes

```bash
terraform apply -var="databricks_host=$DATABRICKS_HOST" -var="databricks_token=$DATABRICKS_TOKEN"
```

## Scripts

### disable_job_weekends.py

This script checks if today is a weekend and disables the specified Databricks job if it is. It's designed to be run as a daily scheduled job.

#### Prerequisites
- Python 3.8+
- Databricks CLI configured with your workspace credentials
- Required Python packages (install with `pip install -r requirements.txt`)

#### Testing the Databricks Job Disabling Script

1. Activate the virtual environment (if using one):
   ```bash
   # Navigate to the project root directory
   cd /path/to/databricks-infra
   
   # Activate the virtual environment
   source databricks/bin/activate
   ```

2. Run the script:
   ```bash
   python scripts/disable_job_weekends.py
   ```

3. The script will:
   - Check if today is a weekend
   - If it is a weekend, it will disable the scheduled job
   - If it's a weekday, it will enable the job if it was previously disabled

## GitHub Actions

This repository includes GitHub Actions workflows for:

- **Terraform Plan**: Runs `terraform plan` on pull requests
- **Terraform Apply**: Runs `terraform apply` on push to the `main` branch

## License

MIT
# Test GitHub Actions
