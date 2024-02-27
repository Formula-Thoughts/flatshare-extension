import boto3
from formula_thoughts_web.ioc import Container

from backend.src.core import IBlobRepo, Group, IGroupRepo
from backend.src.data import S3ClientWrapper
from backend.src.data.repositories import S3BlobRepo, S3GroupRepo

s3 = boto3.client('s3')


def register_data_dependencies(container: Container):
    (container.register_factory(service=S3ClientWrapper, factory=lambda: S3ClientWrapper(client=s3))
     .register(service=IBlobRepo[Group], implementation=S3BlobRepo[Group])
     .register(service=IGroupRepo, implementation=S3GroupRepo))
