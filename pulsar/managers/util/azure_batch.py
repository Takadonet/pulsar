"""Interface layer for Azure's batch library shared between Galaxy and Pulsar."""
from typing import (
    Any,
    Dict,
)

AZURE_BATCH_IMPORT_MSG = (
    "The Python 'azure-batch' package is required to use "
    "this feature, please install it or correct the "
    "following error:\nImportError {msg!s}"
)

try:
    from azure.batch import BatchServiceClient, models
    from azure.batch.models import BatchErrorException, TaskAddParameter,TaskContainerSettings, JobAddParameter, PoolInformation
    from azure.batch.batch_auth import SharedKeyCredentials

except ImportError as e:
    azure = None
    AZURE_BATCH_IMPORT_MSG.format(msg=str(e))

def ensure_azure_batch_available() -> None:
    if azure is None:
        raise Exception(AZURE_BATCH_IMPORT_MSG)
    
def get_azure_client(destination_params: Dict[str, Any]) -> BatchServiceClient:
    azure_batch_account_name=destination_params['azure_batch_account_name']
    azure_batch_account_key=destination_params['azure_batch_account_key']
    azure_batch_service_url=destination_params['azure_batch_service_url']

    credentials = SharedKeyCredentials(
        azure_batch_account_name,
        azure_batch_account_key
    )

    batch_client = BatchServiceClient(
        credentials,
        batch_url=azure_batch_service_url)

    return batch_client