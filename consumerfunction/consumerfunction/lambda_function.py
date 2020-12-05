
"""
SQS to S3
"""

import json
import boto3
import botocore
#import pandas as pd
import pandas as pd
import boto3
from io import StringIO


#SETUP LOGGING
import logging
from pythonjsonlogger import jsonlogger

LOG = logging.getLogger()
LOG.setLevel(logging.DEBUG)
logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter()
logHandler.setFormatter(formatter)
LOG.addHandler(logHandler)

#S3 BUCKET
REGION = "us-east-1"

#google trend
from pytrends.request import TrendReq

pytrends = TrendReq(hl='en-US', tz=360)

### SQS Utils###
def sqs_connection():
    """Creates an SQS Connection which defaults to global var REGION"""

    sqs_client = boto3.client("sqs", region_name=REGION)
    log_sqs_client_msg = "Creating SQS connection in Region: [%s]" % REGION
    LOG.info(log_sqs_client_msg)
    return sqs_client


def delete_sqs_msg(queue_name, receipt_handle):

    sqs_client = sqs_connection()
    try:
        queue_url = sqs_client.get_queue_url(QueueName=queue_name)["QueueUrl"]
        delete_log_msg = "Deleting msg with ReceiptHandle %s" % receipt_handle
        LOG.info(delete_log_msg)
        response = sqs_client.delete_message(QueueUrl=queue_url, ReceiptHandle=receipt_handle)
    except botocore.exceptions.ClientError as error:
        exception_msg = "FAILURE TO DELETE SQS MSG: Queue Name [%s] with error: [%s]" %\
            (queue_name, error)
        LOG.exception(exception_msg)
        return None

    delete_log_msg_resp = "Response from delete from queue: %s" % response
    LOG.info(delete_log_msg_resp)
    return response


def trend_lookup(name, time_window, posttime):
    keywords = [name]
    pytrends.build_payload(kw_list=keywords, cat=0, timeframe=time_window, geo='US')
    trend = pytrends.interest_over_time()
    trend = trend[posttime]
    # drop unused column
    trend = trend.drop('isPartial', axis = 1)
    return trend


def write_s3(df, bucket, name):
    """Write S3 Bucket"""

    csv_buffer = StringIO()
    df.to_csv(csv_buffer)
    s3_resource = boto3.resource('s3')
    filename = f"{name}.csv"
    res = s3_resource.Object(bucket, filename).put(Body=csv_buffer.getvalue())
    LOG.info(f"result of write to bucket: {bucket} with:\n {res}")


def lambda_handler(event, context):
    """Entry Point for Lambda"""

    LOG.info(f"SURVEYJOB LAMBDA, event {event}, context {context}")
    receipt_handle  = event['Records'][0]['receiptHandle'] #sqs message
    event_source_arn = event['Records'][0]['eventSourceARN']

    names = [] #Captured from Queue

    # Process Queue
    for record in event['Records']:
        body = json.loads(record['body'])
        brand_name = body['brandname']
        post_time = body['posttime']

        #Capture for processing
        names.append(brand_name)

        extra_logging = {"body": body, "brand_name":brand_name}
        LOG.info(f"SQS CONSUMER LAMBDA, splitting sqs arn with value: {event_source_arn}",extra=extra_logging)
        qname = event_source_arn.split(":")[-1]
        extra_logging["queue"] = qname
        LOG.info(f"Attemping Deleting SQS receiptHandle {receipt_handle} with queue_name {qname}", extra=extra_logging)
        res = delete_sqs_msg(queue_name=qname, receipt_handle=receipt_handle)
        LOG.info(f"Deleted SQS receipt_handle {receipt_handle} with res {res}", extra=extra_logging)

    LOG.info(f"Looking up trend with values: {names}")
    df = trend_lookup(brand_name, 'now 1-d', post_time)
    
    file_name = post_time + '_' + brand_name

    # Write result to S3
    write_s3(df=df, bucket="brandtrend", name = file_name)