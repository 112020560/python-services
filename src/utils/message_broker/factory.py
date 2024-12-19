import boto3

from src.utils.message_broker.adapters.sns import SNSAdapter


def get_message_broker(klass):
    """Factory to get the right analytics adapter.

    Args:
        klass : str
            String that represents the class to be instantiated
        *args : args
            List of args to be forwarded to the created adapter

    Returns:
        SegmentAdapter
    """
    if klass == "SNS":
        return SNSAdapter(client=boto3.client("sns", region_name="us-east-1"))

    return None
