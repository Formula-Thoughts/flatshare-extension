import boto3

from src.core import IBlobRepo, Group, IGroupRepo
from src.data import S3ClientWrapper
from src.data.repositories import S3BlobRepo, S3GroupRepo
from formula_thoughts_web.ioc import Container

s3 = boto3.client('s3')


def register_data_dependencies(container: Container):
    (container.register_factory(service=S3ClientWrapper, factory=lambda: S3ClientWrapper(client=s3))
     .register(service=IBlobRepo[Group], implementation=S3BlobRepo[Group])
     .register(service=IGroupRepo, implementation=S3GroupRepo))
