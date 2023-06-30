import json
import mimetypes
import os
from typing import TYPE_CHECKING
from typing import TypedDict
import uuid

from optuna.artifacts.exceptions import ArtifactNotFound
from optuna.trial._trial import Trial


ARTIFACTS_ATTR_PREFIX = "artifacts:"

if TYPE_CHECKING:
    ArtifactMeta = TypedDict(
        "ArtifactMeta",
        {
            "artifact_id": str,
            "filename": str,
            "mimetype": str | None,
            "encoding": str | None,
        },
    )


def upload_artifact(trial: Trial, file_path: str, mimetype=None, encoding=None):
    filename = os.path.basename(file_path)
    trial_id = trial._trial_id
    artifact_id = str(uuid.uuid4())
    guess_mimetype, guess_encoding = mimetypes.guess_type(filename)
    artifact: ArtifactMeta = {
        "artifact_id": artifact_id,
        "mimetype": mimetype or guess_mimetype,
        "encoding": encoding or guess_encoding,
        "filename": filename,
    }
    attr_key = _artifact_prefix(trial_id=trial_id) + artifact_id
    trial.storage.get_trial(trial_id).set_system_attr(attr_key, json.dumps(artifact))

    with open(file_path, "rb") as f:
        if trial.study.artifact is None:
            raise ArtifactNotFound
        trial.study.artifact.write(artifact_id, f)
    return artifact_id


def _artifact_prefix(trial_id: int) -> str:
    return ARTIFACTS_ATTR_PREFIX + f"{trial_id}:"
