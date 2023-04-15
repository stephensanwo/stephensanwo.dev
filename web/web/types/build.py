from pydantic import BaseModel


class DomainObject(BaseModel):
    name: str
    domain: str
    redirects_object: dict[str, str]
    static_dir: str
    output_dir: str


class BuildConfig(BaseModel):
    domains: dict[str, DomainObject]
