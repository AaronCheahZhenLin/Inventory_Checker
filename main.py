import boto3
import csv
from datetime import datetime

ec2 = boto3.client('ec2', region_name='us-east-1')
s3 = boto3.client('s3', region_name='us-east-1')
lambd = boto3.client('lambda', region_name='us-east-1')

#List all EC2 instances with their state, type, and tags
def list_ec2_instance():
    response = ec2.describe_instances()
    ec2_data = []

    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instance_id = instance['InstanceId']
            instance_state = instance['State']['Name']
            instance_type = instance['InstanceType']

            tags={}
            instance_name = "No Name" 
            for tag in instance.get('Tags', []): 
                tags[tag['Key']] = tag['Value'] 
                if tag['Key'] == 'Name':
                    instance_name = tag['Value']

            ec2_data.append({
                'id': instance_id,
                'state': instance_state,
                'type': instance_type,
                'name': instance_name
            })
                
    return ec2_data


#Enumerate S3 buckets with size estimates

def estimated_bucket_size():
    
    totalbucket = s3.list_buckets()
    bucketsize = 0
    totalsize = 0
    s3_data = []

    for bucket in totalbucket['Buckets']:
        response = s3.list_objects_v2(Bucket=bucket['Name'])
        if 'Contents' in response:
            for size in response['Contents']:
                objectsize = size['Size']
                bucketsize += objectsize
                totalsize += objectsize
            
            bucketsize = 0
        else:
            print("This bucket is empty")

        s3_data.append({
        'BucketName': bucket['Name'],
        'BucketSize': bucketsize,
        'TotalSize': totalsize
    })

    return s3_data

    

#Count Lambda functions and their runtimes
def lambda_runtime():
    #runtime = lambd.get_function(FunctionName=)
    functions = lambd.list_functions()
    count = 0
    lambda_data = []

    if functions['Functions']:
        for numberoffunctions in functions['Functions']:
            count += 1

        lambda_data.append({
        'numberoffunctions': numberoffunctions['FunctionName'],
        'count': count,
        'Runtime': numberoffunctions['Runtime']
    })

    else:
        print("There are no functions")
        

    return lambda_data

# Check for elastic IPs
def list_elastic_ips():

    eips = ec2.describe_addresses()
    eips_data = []

    if eips['Addresses']:
        for eip in eips['Addresses']:
            eips_data.append({
                'AllocatedID': eip['AllocationId'],
                'AssociationID': eip.get('AssociationId', 'N/A'),
                'Domain': eip['Domain'],
                'PrivateIPAddress': eip.get('PrivateIpAddress', 'N/A'),
                'InstanceID': eip.get('InstanceId', 'N/A'),
                'PublicIP': eip['PublicIp']
            })
    else:
        print("There are no elastic IP addresses")

    return eips_data



# EBS Volumes

def list_ebs_volumes():
    ebs = ec2.describe_volumes()
    ebs_data = []

    if ebs['Volumes']:
        for volumes in ebs['Volumes']:

            CreationTime = volumes['CreateTime']
            readable_time = CreationTime.strftime('%Y-%m-%d %H:%M:%S')

            ebs_data.append({
                'VolumeId': volumes['VolumeId'],
                'Size': volumes['Size'],
                'State': volumes['State'],
                'CreationTime': readable_time,
                'Attachments': volumes.get('Attachments', 'N/A')
            })
    else:
        print('There are no EBS volumes')
    return ebs_data



#Export to CSV/JSON with timestamp

def export_to_csv(ec2_data, s3_data, lambda_data, eips_data, ebs_data):

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"Inventory_{timestamp}.csv"


    with open (f'D:\PythonProjects\Boto3\InventoryChecker\{filename}', 'w', newline = '') as file:
        ec2_columns = ['Instance Id', 'Instance State', 'Instance Type', 'Instance Name']
        s3_columns = ['Bucket Name', 'Bucket Size', 'Total Size']
        lambda_columns = ['Function Name', 'Count', 'Runtime']
        eips_columns = ['AllocatedID', 'AssociationID', 'Domain', 'PrivateIPAddress', 'InstanceID', 'PublicIP']
        ebs_columns = ['VolumeId', 'Size', 'State', 'CreationTime', 'Attachments']

        writer = csv.DictWriter(file, fieldnames=ec2_columns)
        writer.writeheader()

        for ec2 in ec2_data:
            writer.writerow({'Instance ID': ec2['id'], 
                             'Instance State': ec2['state'],
                              'Instance Type': ec2['type'] , 
                              'Instance Name': ec2['name']})
            
        writer.writerow({})

        writer = csv.DictWriter(file, fieldnames=s3_columns)
        writer.writeheader()

        for s3 in s3_data:
            writer.writerow({'Bucket Name': s3['BucketName'], 
                             'Bucket Size': s3['BucketSize'],
                              'Total Size': s3['TotalSize'] })
            
        writer.writerow({})

        writer = csv.DictWriter(file, fieldnames=lambda_columns)
        writer.writeheader()

        for lamda in lambda_data:       
            writer.writerow({'Function Name': lamda['numberoffunctions'], 
                             'Count': lamda['count'],
                             'Runtime': lamda['Runtime']
                               })
            
        writer.writerow({})

        writer = csv.DictWriter(file, fieldnames=eips_columns)
        writer.writeheader()

        for eip in eips_data:
            writer.writerow({                
                'AllocatedID': eip['AllocationId'],
                'AssociationID': eip('AssociationId'),
                'Domain': eip['Domain'],
                'PrivateIPAddress': eip('PrivateIpAddress'),
                'InstanceID': eip('InstanceId'),
                'PublicIP': eip['PublicIp']})
            
        writer.writerow({})

        writer = csv.DictWriter(file, fieldnames=ebs_columns)
        writer.writeheader()

        for ebs in ebs_data:
            writer.writerow({
                'VolumeId': ebs['VolumeId'],
                'Size': ebs['Size'],
                'State': ebs['State'],
                'CreationTime': ebs['CreationTime'],
                'Attachments': ebs.get('Attachments', 'N/A')     
            })

def main():
    ec2_results = list_ec2_instance()
    s3_results = estimated_bucket_size()
    lambda_results = lambda_runtime()
    eips_results = list_elastic_ips()
    ebs_results = list_ebs_volumes()
    export_to_csv(ec2_results, s3_results, lambda_results, eips_results, ebs_results)

if __name__ == "__main__":
    main()