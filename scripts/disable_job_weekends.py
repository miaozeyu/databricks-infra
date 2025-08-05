"""
This script checks if today is a weekend and disables the specified Databricks job if it is.
It's designed to be run as a daily scheduled job.
"""
import os
import datetime
from databricks.sdk import WorkspaceClient
from databricks.sdk.service import jobs
import traceback

def is_weekend():
    """Check if today is a weekend (Saturday or Sunday)."""
    return datetime.datetime.today().weekday() >= 5  # 5 = Saturday, 6 = Sunday

def update_job_schedule(workspace_client, job_id, enable):
    """Update the job's schedule status."""
    try:
        print(f"Fetching job details for job ID: {job_id}")
        job = workspace_client.jobs.get(job_id)
        
        if not hasattr(job.settings, 'schedule') or job.settings.schedule is None:
            print("This job doesn't have a schedule. Creating a new schedule...")
            # If job doesn't have a schedule, create one
            schedule = jobs.CronSchedule(
                quartz_cron_expression="0 0 5 * * ?",  # Every day at 5 AM
                timezone_id="America/New_York",
                pause_status=jobs.PauseStatus.PAUSED if not enable else jobs.PauseStatus.UNPAUSED
            )
        else:
            print(f"Current schedule: {job.settings.schedule}")
            # Use existing schedule but update the pause status
            schedule = jobs.CronSchedule(
                quartz_cron_expression=job.settings.schedule.quartz_cron_expression,
                timezone_id=job.settings.schedule.timezone_id,
                pause_status=jobs.PauseStatus.PAUSED if not enable else jobs.PauseStatus.UNPAUSED
            )
        
        print(f"Updating job with schedule: {schedule}")
        # Update the job with the new schedule
        workspace_client.jobs.update(
            job_id=job_id,
            new_settings=jobs.JobSettings(
                schedule=schedule
            )
        )
        
        status = "enabled" if enable else "disabled"
        print(f"Successfully {status} job {job_id}")
        return True
    except Exception as e:
        print(f"Error updating job {job_id}: {str(e)}")
        print("Full traceback:")
        traceback.print_exc()
        return False

def main():
    # Initialize the Databricks workspace client
    workspace_client = WorkspaceClient()
    
    # Get job ID from environment variable or use the one from the Terraform output
    job_id = os.getenv("DATABRICKS_JOB_ID", "304500324654231")  # Default to the job ID from your Terraform output
    
    if is_weekend():
        print("Today is a weekend. Disabling the job...")
        update_job_schedule(workspace_client, job_id, enable=False)
    else:
        print("Today is a weekday. Ensuring the job is enabled...")
        update_job_schedule(workspace_client, job_id, enable=True)

if __name__ == "__main__":
    main()
