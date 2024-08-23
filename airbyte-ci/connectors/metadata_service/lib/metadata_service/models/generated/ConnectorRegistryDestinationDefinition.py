# generated by datamodel-codegen:
#   filename:  ConnectorRegistryDestinationDefinition.yaml

from __future__ import annotations

from datetime import date, datetime
from typing import Any, Dict, List, Optional, Union
from uuid import UUID

from pydantic import AnyUrl, BaseModel, Extra, Field, conint, constr
from typing_extensions import Literal


class ReleaseStage(BaseModel):
    __root__: Literal["alpha", "beta", "generally_available", "custom"] = Field(
        ..., description="enum that describes a connector's release stage", title="ReleaseStage"
    )


class SupportLevel(BaseModel):
    __root__: Literal["community", "certified", "archived"] = Field(
        ..., description="enum that describes a connector's release stage", title="SupportLevel"
    )


class ResourceRequirements(BaseModel):
    class Config:
        extra = Extra.forbid

    cpu_request: Optional[str] = None
    cpu_limit: Optional[str] = None
    memory_request: Optional[str] = None
    memory_limit: Optional[str] = None


class JobType(BaseModel):
    __root__: Literal["get_spec", "check_connection", "discover_schema", "sync", "reset_connection", "connection_updater", "replicate"] = (
        Field(..., description="enum that describes the different types of jobs that the platform runs.", title="JobType")
    )


class NormalizationDestinationDefinitionConfig(BaseModel):
    class Config:
        extra = Extra.allow

    normalizationRepository: str = Field(
        ...,
        description="a field indicating the name of the repository to be used for normalization. If the value of the flag is NULL - normalization is not used.",
    )
    normalizationTag: str = Field(..., description="a field indicating the tag of the docker repository to be used for normalization.")
    normalizationIntegrationType: str = Field(
        ..., description="a field indicating the type of integration dialect to use for normalization."
    )


class AllowedHosts(BaseModel):
    class Config:
        extra = Extra.allow

    hosts: Optional[List[str]] = Field(
        None,
        description="An array of hosts that this connector can connect to.  AllowedHosts not being present for the source or destination means that access to all hosts is allowed.  An empty list here means that no network access is granted.",
    )


class RolloutConfiguration(BaseModel):
    class Config:
        extra = Extra.forbid

    initialPercentage: Optional[conint(ge=0, le=100)] = Field(
        0, description="The percentage of users that should receive the new version initially."
    )
    maxPercentage: Optional[conint(ge=0, le=100)] = Field(
        50, description="The percentage of users who should receive the release candidate during the test phase before full rollout."
    )
    advanceDelayMinutes: Optional[conint(ge=10)] = Field(
        10, description="The number of minutes to wait before advancing the rollout percentage."
    )


class SuggestedStreams(BaseModel):
    class Config:
        extra = Extra.allow

    streams: Optional[List[str]] = Field(
        None,
        description="An array of streams that this connector suggests the average user will want.  SuggestedStreams not being present for the source means that all streams are suggested.  An empty list here means that no streams are suggested.",
    )


class AirbyteInternal(BaseModel):
    class Config:
        extra = Extra.allow

    sl: Optional[Literal[100, 200, 300]] = None
    ql: Optional[Literal[100, 200, 300, 400, 500, 600]] = None


class GitInfo(BaseModel):
    class Config:
        extra = Extra.forbid

    commit_sha: Optional[str] = Field(None, description="The git commit sha of the last commit that modified this file.")
    commit_timestamp: Optional[datetime] = Field(None, description="The git commit timestamp of the last commit that modified this file.")
    commit_author: Optional[str] = Field(None, description="The git commit author of the last commit that modified this file.")
    commit_author_email: Optional[str] = Field(None, description="The git commit author email of the last commit that modified this file.")


class SourceFileInfo(BaseModel):
    metadata_etag: Optional[str] = None
    metadata_file_path: Optional[str] = None
    metadata_bucket_name: Optional[str] = None
    metadata_last_modified: Optional[str] = None
    registry_entry_generated_at: Optional[str] = None


class ConnectorMetrics(BaseModel):
    all: Optional[Any] = None
    cloud: Optional[Any] = None
    oss: Optional[Any] = None


class ConnectorMetric(BaseModel):
    class Config:
        extra = Extra.allow

    usage: Optional[Union[str, Literal["low", "medium", "high"]]] = None
    sync_success_rate: Optional[Union[str, Literal["low", "medium", "high"]]] = None
    connector_version: Optional[str] = None


class ConnectorPackageInfo(BaseModel):
    cdk_version: Optional[str] = None


class StreamBreakingChangeScope(BaseModel):
    class Config:
        extra = Extra.forbid

    scopeType: Any = Field("stream", const=True)
    impactedScopes: List[str] = Field(..., description="List of streams that are impacted by the breaking change.", min_items=1)


class JobTypeResourceLimit(BaseModel):
    class Config:
        extra = Extra.forbid

    jobType: JobType
    resourceRequirements: ResourceRequirements


class GeneratedFields(BaseModel):
    git: Optional[GitInfo] = None
    source_file_info: Optional[SourceFileInfo] = None
    metrics: Optional[ConnectorMetrics] = None
    sbomUrl: Optional[str] = Field(None, description="URL to the SBOM file")


class BreakingChangeScope(BaseModel):
    __root__: StreamBreakingChangeScope = Field(..., description="A scope that can be used to limit the impact of a breaking change.")


class ActorDefinitionResourceRequirements(BaseModel):
    class Config:
        extra = Extra.forbid

    default: Optional[ResourceRequirements] = Field(
        None, description="if set, these are the requirements that should be set for ALL jobs run for this actor definition."
    )
    jobSpecific: Optional[List[JobTypeResourceLimit]] = None


class VersionBreakingChange(BaseModel):
    class Config:
        extra = Extra.forbid

    upgradeDeadline: date = Field(..., description="The deadline by which to upgrade before the breaking change takes effect.")
    message: str = Field(..., description="Descriptive message detailing the breaking change.")
    migrationDocumentationUrl: Optional[AnyUrl] = Field(
        None,
        description="URL to documentation on how to migrate to the current version. Defaults to ${documentationUrl}-migrations#${version}",
    )
    scopedImpact: Optional[List[BreakingChangeScope]] = Field(
        None,
        description="List of scopes that are impacted by the breaking change. If not specified, the breaking change cannot be scoped to reduce impact via the supported scope types.",
        min_items=1,
    )


class ConnectorBreakingChanges(BaseModel):
    class Config:
        extra = Extra.forbid

    __root__: Dict[constr(regex=r"^\d+\.\d+\.\d+$"), VersionBreakingChange] = Field(
        ..., description="Each entry denotes a breaking change in a specific version of a connector that requires user action to upgrade."
    )


class ConnectorRegistryDestinationDefinition(BaseModel):
    class Config:
        extra = Extra.allow

    destinationDefinitionId: UUID
    name: str
    dockerRepository: str
    dockerImageTag: str
    documentationUrl: str
    icon: Optional[str] = None
    iconUrl: Optional[str] = None
    spec: Dict[str, Any]
    tombstone: Optional[bool] = Field(
        False, description="if false, the configuration is active. if true, then this configuration is permanently off."
    )
    public: Optional[bool] = Field(False, description="true if this connector definition is available to all workspaces")
    custom: Optional[bool] = Field(False, description="whether this is a custom connector definition")
    releaseStage: Optional[ReleaseStage] = None
    supportLevel: Optional[SupportLevel] = None
    releaseDate: Optional[date] = Field(None, description="The date when this connector was first released, in yyyy-mm-dd format.")
    tags: Optional[List[str]] = Field(
        None, description="An array of tags that describe the connector. E.g: language:python, keyword:rds, etc."
    )
    resourceRequirements: Optional[ActorDefinitionResourceRequirements] = None
    protocolVersion: Optional[str] = Field(None, description="the Airbyte Protocol version supported by the connector")
    normalizationConfig: Optional[NormalizationDestinationDefinitionConfig] = None
    supportsDbt: Optional[bool] = Field(
        None,
        description="an optional flag indicating whether DBT is used in the normalization. If the flag value is NULL - DBT is not used.",
    )
    allowedHosts: Optional[AllowedHosts] = None
    releases: Optional[ConnectorReleases] = None
    ab_internal: Optional[AirbyteInternal] = None
    supportsRefreshes: Optional[bool] = False
    generated: Optional[GeneratedFields] = None
    packageInfo: Optional[ConnectorPackageInfo] = None
    language: Optional[str] = Field(None, description="The language the connector is written in")


class ConnectorReleases(BaseModel):
    class Config:
        extra = Extra.forbid

    releaseCandidates: Optional[ConnectorReleaseCandidates] = None
    breakingChanges: Optional[ConnectorBreakingChanges] = None
    migrationDocumentationUrl: Optional[AnyUrl] = Field(
        None,
        description="URL to documentation on how to migrate from the previous version to the current version. Defaults to ${documentationUrl}-migrations",
    )


class ConnectorReleaseCandidates(BaseModel):
    class Config:
        extra = Extra.forbid

    __root__: Dict[constr(regex=r"^\d+\.\d+\.\d+$"), VersionReleaseCandidate] = Field(
        ..., description="Each entry denotes a release candidate version of a connector."
    )


class VersionReleaseCandidate(BaseModel):
    class Config:
        extra = Extra.forbid

    rolloutConfiguration: RolloutConfiguration
    registryEntry: Optional[Union[ConnectorRegistrySourceDefinition, ConnectorRegistryDestinationDefinition]] = None


class ConnectorRegistrySourceDefinition(BaseModel):
    class Config:
        extra = Extra.allow

    sourceDefinitionId: UUID
    name: str
    dockerRepository: str
    dockerImageTag: str
    documentationUrl: str
    icon: Optional[str] = None
    iconUrl: Optional[str] = None
    sourceType: Optional[Literal["api", "file", "database", "custom"]] = None
    spec: Dict[str, Any]
    tombstone: Optional[bool] = Field(
        False, description="if false, the configuration is active. if true, then this configuration is permanently off."
    )
    public: Optional[bool] = Field(False, description="true if this connector definition is available to all workspaces")
    custom: Optional[bool] = Field(False, description="whether this is a custom connector definition")
    releaseStage: Optional[ReleaseStage] = None
    supportLevel: Optional[SupportLevel] = None
    releaseDate: Optional[date] = Field(None, description="The date when this connector was first released, in yyyy-mm-dd format.")
    resourceRequirements: Optional[ActorDefinitionResourceRequirements] = None
    protocolVersion: Optional[str] = Field(None, description="the Airbyte Protocol version supported by the connector")
    allowedHosts: Optional[AllowedHosts] = None
    suggestedStreams: Optional[SuggestedStreams] = None
    maxSecondsBetweenMessages: Optional[int] = Field(
        None, description="Number of seconds allowed between 2 airbyte protocol messages. The source will timeout if this delay is reach"
    )
    erdUrl: Optional[str] = Field(None, description="The URL where you can visualize the ERD")
    releases: Optional[ConnectorReleases] = None
    ab_internal: Optional[AirbyteInternal] = None
    generated: Optional[GeneratedFields] = None
    packageInfo: Optional[ConnectorPackageInfo] = None
    language: Optional[str] = Field(None, description="The language the connector is written in")


ConnectorRegistryDestinationDefinition.update_forward_refs()
ConnectorReleases.update_forward_refs()
ConnectorReleaseCandidates.update_forward_refs()
VersionReleaseCandidate.update_forward_refs()
