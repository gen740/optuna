from dataclasses import asdict
from dataclasses import dataclass
import json
import mimetypes
import os
import uuid

from optuna.artifacts._protocol import ArtifactStore
from optuna.artifacts.exceptions import ArtifactNotFound
from optuna.logging import get_logger
from optuna.storages import BaseStorage
from optuna.trial._frozen import FrozenTrial
from optuna.trial._trial import Trial


ARTIFACTS_ATTR_PREFIX = "artifacts:"
DEFAULT_MIME_TYPE = "application/octet-stream"


@dataclass
class ArtifactMeta:
    artifact_id: str
    filename: str
    mimetype: str
    encoding: str | None


def upload_artifact(
    trial: Trial | FrozenTrial | int,
    file_path: str,
    *,
    artifact_store: ArtifactStore,  # prefer with warning
    storage: BaseStorage,
    mimetype=None,
    encoding=None,
) -> str:
    # if trial.study.artifact is None:
    #     raise ArtifactNotFound()
    # filename = os.path.basename(file_path)
    # trial_id = trial._trial_id
    # artifact_id = str(uuid.uuid4())
    # guess_mimetype, guess_encoding = mimetypes.guess_type(filename)
    #
    # artifact = ArtifactMeta(
    #     artifact_id=artifact_id,
    #     filename=filename,
    #     mimetype=mimetype or guess_mimetype or DEFAULT_MIME_TYPE,
    #     encoding=encoding or guess_encoding,
    # )
    # attr_key = ARTIFACTS_ATTR_PREFIX + f"{trial_id}:" + artifact_id
    # trial.study.set_system_attr(attr_key, json.dumps(asdict(artifact)))
    #
    # with open(file_path, "rb") as f:
    #     trial.study.artifact.write(artifact_id, f)
    # return artifact_id
    return ""
