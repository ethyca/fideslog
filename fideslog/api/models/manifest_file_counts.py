from pydantic import BaseModel, Field


class ManifestFileCounts(BaseModel):
    """
    A JSON object structure containing the counts of dataset, policy,
    and system manifests currently in use.
    """

    datasets: int = Field(
        0,
        description="The number of dataset manifests currently in use",
    )
    policies: int = Field(
        0,
        description="The number of policy manifests currently in use",
    )
    systems: int = Field(
        0,
        description="The number of system manifests currently in use",
    )
