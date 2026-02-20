# Inventory_Checker
This is a script used to check AWS Resources.
This script does the following:
A)List all EC2 instances with their state, type, and tags
B)Enumerate S3 buckets with size estimates
C)Count Lambda functions and their runtimes
D)Checks for any allocated or unused Elastic IPs
E)Finds all EBS attached/unattached volumes with their sizes, creation time and current state
F)Export to CSV/JSON with timestamp