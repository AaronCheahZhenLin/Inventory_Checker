# Inventory_Checker
This is a script used to check AWS Resources.
This script does the following:

1. List all EC2 instances with their state, type, and tags
2. Enumerate S3 buckets with size estimates
3. Count Lambda functions and their runtimes
4. Checks for any allocated or unused Elastic IPs
5. Finds all EBS attached/unattached volumes with their sizes, creation time and current state
6. Export to CSV/JSON with timestamp