# AppSec Monitor

The AppSec Monitor is an automated solution for managing and monitoring Static Application Security Testing (SAST) and Dynamic Application Security Testing (DAST) scans. It integrates with Checkmarx for SAST and WebInspect for DAST, providing real-time failure detection, severity-based issue tracking, and notification dispatch via Slack. The system is designed to handle concurrent processing and supports an automated workflow for large-scale and robust AppSec scan management.

## Features

### SAST Monitoring

- **Scan Analysis & Classification:** Parses Checkmarx SAST reports to identify findings flagged 'To Verify' and categorizes them based on severity levels.
- **Real-Time Notifications:** Dispatches alerts with actionable insights to Slack, including direct links to the scans.
- **Scan Data Management:** Creates XML reports and maintains a structured storage of findings, categorized by severity, and tracks verification-required items.
- **Concurrent Scans Handling:** Employs concurrent processing for efficient monitoring of multiple projects.
- **Automated Scan Retrieval:** Retrieves new SAST scan reports by project IDs and collates findings for review.

### DAST Monitoring

- **Scan Health Evaluation:** Determines the health status of DAST scans via WebInspect, capturing complete scan data and metadata.
- **Failed Scans Identification:** Records the count of failed DAST scans and provides file paths for detailed reports.
- **Scan Data Synchronization & Update:** Detects discrepancies between current and temporary scan data, updating records with new project details.
- **Failed Scans Notifications:** Alerts for failed DAST scans are communicated through Slack, with failed scan data written to specified files.
- **Multi-threaded Scan Execution:** Utilizes a ThreadPoolExecutor for concurrent scan result processing.
- **Post-Processing Cleanup:** Automates the cleanup of scan-related files to maintain system efficiency.

### Integration and Notifications

- **Slack Integration:** Real-time notification via Slack channels for immediate attention and response.
- **API Usage:** Harnesses the APIs of Checkmarx and WebInspect for scan data retrieval and parsing.
- **Automated Workflow:** Orchestrates the entire monitoring to notification dispatch workflow, reducing manual effort.

### Error Handling & Logging

- Implements comprehensive error capture and logging to address any anomalies during scan monitoring.

### Scalability

- Engineered to accommodate scaling for additional projects and increased scan volumes as required.

## Getting Started

Instructions for setting up the AppSec Monitor in your environment will be added here.

## Usage

Example commands and usage of the AppSec Monitor will be provided here.

## Contributing

Guidelines for contributing to this project will be described here.

## License

Details about the licensing of the AppSec Monitor will be stated here.

## Authors & Acknowledgment

Credits to the team and contributors will be mentioned here.

## Project Status

Current status and ongoing updates of the AppSec Monitor will be tracked here.
