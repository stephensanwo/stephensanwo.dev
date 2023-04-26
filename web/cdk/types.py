from pydantic import BaseModel, validator
from enum import Enum
from web.types.build import BuildConfig
from typing import Optional


class DeploymentEnv(str, Enum):
    staging = "staging",
    production = "production"


class CDKConfig(BaseModel):
    account: str = None
    region: str = "eu-west-1"
    description: str = None
    deployment_environment: str = None  # staging | production

    @validator('deployment_environment')
    def validate_deployment_environment(cls, value):
        # flake8: noqa
        if value != DeploymentEnv.staging and value != DeploymentEnv.production:
            raise ValueError("Invalid aws deployment environment")
        return value


class DomainObject(BaseModel):
    name: str
    domain: str
    redirects_object: dict[str, str]
    static_dir: str
    output_dir: str
    xml_dir: Optional[str] = None

class CDKProps(BaseModel):
    namespace: str
    domain_name: str
    domain_certificate_arn: str
    enable_s3_website_endpoint: str
    origin_custom_header_parameter_name: str
    hosted_zone_id: str
    hosted_zone_name: str
    build_config: BuildConfig
