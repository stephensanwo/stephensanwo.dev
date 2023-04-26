# flake8:noqa
"""
Two constructs to host static sites in aws using S3, cloudfront and Route53.
StaticSitePublicS3 creates a public S3 bucket with website enabled and
uses Origin Custom Header (referer) to limit the access of s3 objects to the
CloudFront only.
"""
from aws_cdk import (
    aws_s3 as s3,
    aws_s3_deployment as s3_deployment,
    aws_cloudfront as cloudfront,
    aws_cloudfront_origins as origins,
    aws_certificatemanager as acm,
    aws_route53 as route53,
    aws_route53_patterns as patterns,
    aws_route53_targets as targets,
    aws_iam as iam,
    aws_ssm as ssm,
    RemovalPolicy,
    Duration
)
from constructs import Construct
from cdk.types import DomainObject
import os


class StaticSitePublicS3(Construct):
    """The base class for StaticSite constructs"""

    def __init__(
        self,
        scope,
        construct_id,
        hosted_zone_id: str,
        hosted_zone_name: str,
        origin_custom_header_parameter_name: str,
        domain_object: DomainObject,
        domain_certificate_arn=None,
        **kwargs,
    ):
        super().__init__(scope, construct_id, **kwargs)

        # Public variables
        self.bucket = None
        self.certificate = None
        self.distribution = None

        # Internal variables
        self._domain_object = domain_object
        self._origin_custom_header_parameter_name = origin_custom_header_parameter_name

        # Instance Variables
        self.__domain_certificate_arn = domain_certificate_arn
        self.__hosted_zone_id = hosted_zone_id
        self.__hosted_zone_name = hosted_zone_name

        # Get the origin referer header value
        self.__origin_referer_header = self._get_referer_header(
            self._origin_custom_header_parameter_name,
        )

        self._build_site()

    def _build_site(self):
        """The Template Method for building the site.
        It uses hook functions which are implemented in the sub classes
        """
        # Create the S3 bucket for the site contents
        self._create_site_bucket()

        # Get the hosted zone based on the provided domain name
        hosted_zone = self._get_hosted_zone()

        # Get an existing or create a new certificate for the site domain
        self._create_certificate(hosted_zone)

        # create the cloud front distribution
        self._create_cloudfront_distribution()

        # Create a Route53 record
        self._create_route53_record(hosted_zone)

        # Configure subdomain redirects
        self._create_https_redirects()

        # Create the S3 deployment
        self._create_bucket_deployment()

        # Create the static files deployment
        self._create_static_files_deployment()

    def _get_hosted_zone(self):
        return route53.HostedZone.from_hosted_zone_attributes(
            self,
            f"{self._domain_object.name}-hosted-zone",
            zone_name=self.__hosted_zone_name,
            hosted_zone_id=self.__hosted_zone_id,
        )

    def _create_route53_record(self, hosted_zone):
        route53.ARecord(
            self,
            f"{self._domain_object.name}-site-alias-record",
            record_name=self._domain_object.name,
            zone=hosted_zone,
            target=route53.RecordTarget.from_alias(
                targets.CloudFrontTarget(self.distribution)
            ),
        )

    def _create_certificate(self, hosted_zone):
        if self.__domain_certificate_arn:
            # If certificate arn is provided, import the certificate
            self.certificate = acm.Certificate.from_certificate_arn(
                self,
                f"{self._domain_object.name}-site-certificate",
                certificate_arn=self.__domain_certificate_arn,
            )
        else:
            # If certificate arn is not provided, create a new one.
            # ACM certificates that are used with CloudFront must be in
            # the us-east-1 region.
            self.certificate = acm.DnsValidatedCertificate(
                self,
                f"{self._domain_object.name}-site-certificate",
                domain_name=self._domain_object.name,
                hosted_zone=hosted_zone,
                region="us-east-1",
            )

    def _create_https_redirects(self):
        if self._domain_object.redirects_object:
            for source, target in self._domain_object.redirects_object.items():
                patterns.HttpsRedirect(
                    self, f"{source}-redirect",
                    record_names=[f"{source}"],
                    target_domain=target,
                    zone=route53.HostedZone.from_hosted_zone_attributes(
                        self, f"{source}-hosted-zone",
                        hosted_zone_id=self.__hosted_zone_id,
                        zone_name=self.__hosted_zone_name,
                    )
                )

    def _get_referer_header(self, parameter_name):
        return ssm.StringParameter.from_string_parameter_attributes(
            self, "custom_header", parameter_name=parameter_name
        ).string_value

    def _create_site_bucket(self):
        """Creates a public S3 bucket for the static site construct"""
        self.bucket = s3.Bucket(
            self,
            f"{self._domain_object.name}-site-bucket",
            bucket_name=self._domain_object.name,
            website_index_document="index.html",
            website_error_document="404.html",
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True,
        )
        bucket_policy = iam.PolicyStatement(
            actions=["s3:GetObject"],
            resources=[self.bucket.arn_for_objects("*")],
            principals=[iam.AnyPrincipal()],
        )
        bucket_policy.add_condition(
            "StringEquals",
            {"aws:Referer": self.__origin_referer_header},
        )

        self.bucket.add_to_resource_policy(bucket_policy)

    def _create_cloudfront_distribution(self):
        """Create a cloudfront distribution with a public bucket as the origin"""
        origin_source = cloudfront.CustomOriginConfig(
            domain_name=self.bucket.bucket_website_domain_name,
            origin_protocol_policy=cloudfront.OriginProtocolPolicy.HTTP_ONLY,
            origin_headers={"Referer": self.__origin_referer_header},
        )

        self.distribution = cloudfront.CloudFrontWebDistribution(
            self,
            f"{self._domain_object.name}-cloudfront-distribution",
            viewer_certificate=cloudfront.ViewerCertificate.from_acm_certificate(
                self.certificate,
                aliases=[
                    self._domain_object.name],
                security_policy=cloudfront.SecurityPolicyProtocol.TLS_V1_2_2019,
                ssl_method=cloudfront.SSLMethod.SNI
            ),
            origin_configs=[
                cloudfront.SourceConfiguration(
                    custom_origin_source=origin_source,
                    behaviors=[
                        cloudfront.Behavior(
                            is_default_behavior=True,
                        )
                    ],
                )
            ],
            viewer_protocol_policy=cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
            price_class=cloudfront.PriceClass.PRICE_CLASS_ALL,
        )

    def _create_bucket_deployment(self):
        ROOT = os.path.dirname(os.path.abspath("./web"))

        s3_deployment.BucketDeployment(self, f"{self._domain_object.name}-site-html-files",
                                       sources=[s3_deployment.Source.asset(
                                           os.path.join(ROOT, self._domain_object.output_dir))],
                                       destination_bucket=self.bucket,
                                       cache_control=[
                                           s3_deployment.CacheControl.set_public(),
                                           s3_deployment.CacheControl.max_age(
                                               Duration.hours(1))
                                       ],
                                       prune=False,
                                       distribution=self.distribution,
                                       content_type="text/html",
                                       exclude=["*.xml"]
                                       )

    def _create_static_files_deployment(self):
        ROOT = os.path.dirname(os.path.abspath("./web"))

        # Transfer assets for sites, bud exclude shared domain
        s3_deployment.BucketDeployment(self, f"{self._domain_object.name}-site-static-files",
                                       sources=[s3_deployment.Source.asset(
                                           os.path.join(ROOT, "dist/static"))],
                                       destination_bucket=self.bucket,
                                       cache_control=[
                                           s3_deployment.CacheControl.set_public(),
                                           s3_deployment.CacheControl.max_age(
                                               Duration.hours(1))
                                       ],
                                       prune=False,
                                       distribution=self.distribution)
