from pydantic import BaseModel
from typing import Optional


class DomainObject(BaseModel):
    name: str
    domain: str
    redirects_object: dict[str, str]
    static_dir: str
    output_dir: str
    xml_dir: Optional[str] = None


class BuildConfig(BaseModel):
    domains: dict[str, DomainObject]
