# flake8:noqa
from aws_cdk import CfnOutput, Stack
from cdk.static_site import StaticSitePublicS3
from cdk.types import CDKProps


class StaticSiteStack(Stack):
    def __init__(self, scope, construct_id, props: CDKProps, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        # Create site, certificate, redirects and cloudfront
        for name, domain in props.build_config.domains.items():
            site = StaticSitePublicS3(
                self,
                f"{domain.name}-construct",
                domain_certificate_arn=props.domain_certificate_arn,
                hosted_zone_id=props.hosted_zone_id,
                hosted_zone_name=props.hosted_zone_name,
                origin_custom_header_parameter_name=props.origin_custom_header_parameter_name,
                domain_object=domain,
            )

            # Add stack outputs for s3 bucket
            CfnOutput(
                self,
                f"{domain.name}-site-bucket-name",
                value=site.bucket.bucket_name,
            )

            # Add stack output for cloudfront
            CfnOutput(
                self,
                f"{domain.name}-DistributionId",
                value=site.distribution.distribution_id,
            )
