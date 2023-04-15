# flake8:noqa
from aws_cdk import App, Environment
from cdk.stack import StaticSiteStack
from config import cdk_config, settings
from cdk.types import CDKProps, DeploymentEnv


app = App()
config = cdk_config()
context = app.node.try_get_context("stackProps")
settings = settings()
props = CDKProps(
    namespace=context[f"{config.deployment_environment}"].get("namespace"),
    domain_name=context[f"{config.deployment_environment}"].get(
        "domain_name"),
    domain_certificate_arn=context[f"{config.deployment_environment}"].get(
        "domain_certificate_arn"
    ),
    enable_s3_website_endpoint=context[f"{config.deployment_environment}"].get(
        "enable_s3_website_endpoint"
    ),
    origin_custom_header_parameter_name=context[f"{config.deployment_environment}"].get(
        "origin_custom_header_parameter_name"
    ),
    hosted_zone_id=context[f"{config.deployment_environment}"].get(
        "hosted_zone_id"),
    hosted_zone_name=context[f"{config.deployment_environment}"].get(
        "hosted_zone_name"),
    build_config=settings.build_config
)

env = Environment(
    account=config.account,
    region=config.region,
)


StaticSite = StaticSiteStack(
    scope=app,
    construct_id=f"{props.namespace}-stack",
    props=props,
    env=env,
    description=config.description,
)

app.synth()
