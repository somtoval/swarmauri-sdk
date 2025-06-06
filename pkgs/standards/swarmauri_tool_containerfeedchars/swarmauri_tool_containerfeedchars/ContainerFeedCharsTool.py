import subprocess
from typing import List, Literal
from pydantic import Field
from swarmauri_base.tools.ToolBase import ToolBase
from swarmauri_standard.tools.Parameter import Parameter
from swarmauri_base.ComponentBase import ComponentBase


@ComponentBase.register_type(ToolBase, "ContainerFeedCharsTool")
class ContainerFeedCharsTool(ToolBase):
    """Execute a command inside a running container."""

    version: str = "1.0.0"
    name: str = "ContainerFeedCharsTool"
    description: str = "Run a shell command inside a Docker or Kubernetes container."
    type: Literal["ContainerFeedCharsTool"] = "ContainerFeedCharsTool"

    driver: Literal["docker", "kubernetes"] = "docker"

    parameters: List[Parameter] = Field(
        default_factory=lambda: [
            Parameter(
                name="container_name",
                input_type="string",
                description="Target container or pod name",
                required=True,
            ),
            Parameter(
                name="command",
                input_type="string",
                description="Shell command to execute",
                required=True,
            ),
        ]
    )

    def __call__(self, container_name: str, command: str) -> dict:
        if self.driver == "docker":
            cmd = ["docker", "exec", container_name, "sh", "-c", command]
        else:
            cmd = ["kubectl", "exec", container_name, "--", "sh", "-c", command]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(result.stderr.strip())
        return {"stdout": result.stdout.strip()}
