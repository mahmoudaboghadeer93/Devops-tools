import http.client
import boto3
import os
import json

# Boto Connection
aws_region = "eu-west-1"
asg = boto3.client('autoscaling', region_name=aws_region)

def send_slack_notification(webhook_url, message):
    payload = json.dumps({"text": message})
    headers = {"Content-type": "application/json"}
    # Extract hostname and path from the webhook URL
    url_parts = http.client.urlsplit(webhook_url)
    conn = http.client.HTTPSConnection(url_parts.hostname)
    # Make a POST request
    conn.request("POST", url_parts.path, payload, headers)
    response = conn.getresponse()
    if response.status == 200:
        print("Slack notification sent successfully!")
    else:
        print(f"Failed to send Slack notification. Status code: {response.status}, Response: {response.read().decode()}")

def lambda_handler(event, context):
    auto_scaling_groups = [
        {'name': 'eks-node-group-name-1', 'min_size': 0, 'desired_capacity': 0, 'max_size': 0},
        {'name': 'eks-node-group-name-2', 'min_size': 0, 'desired_capacity': 0, 'max_size': 0}
        # Add more Auto Scaling Groups as needed
    ]

    for group in auto_scaling_groups:
        try:
            # Update Auto Scaling Group
            asg_response = asg.update_auto_scaling_group(
                AutoScalingGroupName=group['name'],
                MinSize=group['min_size'],
                DesiredCapacity=group['desired_capacity'],
                MaxSize=group['max_size']
            )
            print(f"Auto Scaling Group '{group['name']}' updated successfully: {asg_response}")
              
        except Exception as e:
            print(f"Error updating Auto Scaling Group '{group['name']}': {e}")
            # Raise an exception if you want to halt the execution in case of an error
            raise e

    # Sending a Slack notification
    slack_webhook_url = os.environ['SLACK_WEBHOOK']
    message_to_send = ':k8s: *Staging Scaled Down* :white_check_mark:'
    send_slack_notification(slack_webhook_url, message_to_send)

    # Return a success response
    return {"statusCode": 200, "body": json.dumps("Auto Scaling Groups updated successfully")}
