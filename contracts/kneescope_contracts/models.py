"""Canonical KneeScope API and artifact contracts.

These Pydantic models are the single source of truth. Generated artifacts:

- ``contracts/schema/*.schema.json`` via ``scripts/export_contracts.py``
- ``contracts/openapi.json`` via the same script (from the FastAPI app)
- ``web/src/api/schema.d.ts`` via ``pnpm --dir web gen:api``

Changing anything here is a contract change: follow ``AGENTS.md`` ("Changing a shared
contract") and bump ``SCHEMA_VERSION``.
"""

from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from typing import Literal, Self

from pydantic import BaseModel, ConfigDict, Field, model_validator

SCHEMA_VERSION = "0.1.0"

EXPLANATION_NOTICE = "Shows what influenced the model score; it does not localise an injury."
FIXTURE_NOTICE = "FIXTURE - hand-written development data, not a model output."


class Contract(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, protected_namespaces=())


# ---------------------------------------------------------------------------
# Enumerations
# ---------------------------------------------------------------------------


class Plane(StrEnum):
    sagittal = "sagittal"
    coronal = "coronal"
    axial = "axial"


class DataOrigin(StrEnum):
    """Where a study or artifact came from."""

    fixture = "fixture"
    dataset = "dataset"


class ResultSource(StrEnum):
    """How a prediction was produced. Never relabel one as another."""

    live = "live"
    cached = "cached"
    fixture = "fixture"


class FindingStatus(StrEnum):
    scored = "scored"
    not_evaluated = "not_evaluated"
    unavailable = "unavailable"
    unsupported = "unsupported"
    failed = "failed"


class ScoreKind(StrEnum):
    uncalibrated_model_score = "uncalibrated_model_score"
    calibrated_probability = "calibrated_probability"


class AnalysisStatus(StrEnum):
    not_run = "not_run"
    cached = "cached"
    failed = "failed"


class LabelState(StrEnum):
    positive = "positive"
    negative = "negative"
    unknown = "unknown"
    not_labeled = "not_labeled"


class LabelProvenance(StrEnum):
    expert_annotation = "expert_annotation"
    dataset_provided = "dataset_provided"
    report_extracted = "report_extracted"
    fixture = "fixture"


class SliceOrder(StrEnum):
    """How slice_index 0..n-1 was ordered for a series."""

    patient_position = "patient_position"
    instance_number = "instance_number"
    dataset_provided = "dataset_provided"
    synthetic = "synthetic"


class ErrorCode(StrEnum):
    STUDY_NOT_FOUND = "STUDY_NOT_FOUND"
    SERIES_NOT_FOUND = "SERIES_NOT_FOUND"
    SLICE_OUT_OF_RANGE = "SLICE_OUT_OF_RANGE"
    FINDING_NOT_IN_PROFILE = "FINDING_NOT_IN_PROFILE"
    EXPLANATION_UNAVAILABLE = "EXPLANATION_UNAVAILABLE"
    LABELS_UNAVAILABLE = "LABELS_UNAVAILABLE"
    MODEL_NOT_LOADED = "MODEL_NOT_LOADED"
    INPUT_INVALID = "INPUT_INVALID"
    PREPROCESSING_FAILED = "PREPROCESSING_FAILED"
    INFERENCE_FAILED = "INFERENCE_FAILED"
    INFERENCE_TIMEOUT = "INFERENCE_TIMEOUT"
    VALIDATION_ERROR = "VALIDATION_ERROR"
    INTERNAL_ERROR = "INTERNAL_ERROR"


class Reason(Contract):
    code: str = Field(description="Machine-readable code, usually an ErrorCode value.")
    message: str = Field(description="Plain-language explanation safe to show to a reviewer.")


# ---------------------------------------------------------------------------
# Findings registry
# ---------------------------------------------------------------------------


class FindingDefinition(Contract):
    finding_id: str
    display_name: str
    description: str


class FindingProfile(Contract):
    profile_id: str
    dataset_id: str | None
    status: Literal["candidate", "selected", "fixture_only"]
    note: str
    findings: list[FindingDefinition]


# ---------------------------------------------------------------------------
# Studies and series
# ---------------------------------------------------------------------------


class SeriesSummary(Contract):
    series_id: str
    plane: Plane | None = Field(description="None when the plane could not be determined.")
    description: str | None = None
    num_slices: int = Field(ge=1)
    slice_order: SliceOrder
    fluid_sensitive: bool | None = None
    fat_suppressed: bool | None = None
    rendered_width: int = Field(ge=1, description="Width in px of PNGs from the slice endpoint.")
    rendered_height: int = Field(ge=1)


class StudySummary(Contract):
    study_id: str
    display_label: str
    origin: DataOrigin
    dataset_id: str | None
    planes_available: list[Plane]
    series_count: int = Field(ge=0)
    analysis_status: AnalysisStatus


class StudyDetail(StudySummary):
    series: list[SeriesSummary]
    missing_planes: list[Plane]
    warnings: list[Reason] = Field(default_factory=list)

    @model_validator(mode="after")
    def _planes_consistent(self) -> Self:
        present = {s.plane for s in self.series if s.plane is not None}
        if set(self.planes_available) != present:
            raise ValueError("planes_available must equal the planes of the listed series")
        if set(self.missing_planes) != set(Plane) - present:
            raise ValueError("missing_planes must list exactly the planes with no series")
        if self.series_count != len(self.series):
            raise ValueError("series_count must equal len(series)")
        return self


class StudyList(Contract):
    studies: list[StudySummary]
    origin_notice: str | None = None


# ---------------------------------------------------------------------------
# Predictions
# ---------------------------------------------------------------------------


class ModelInfo(Contract):
    model_id: str
    model_version: str
    checkpoint_sha256: str | None = Field(
        description="SHA-256 of the checkpoint file. None only for fixtures."
    )
    finding_profile: str
    supported_findings: list[str]
    trained_on: str | None = Field(description="Dataset ID and partition; None for fixtures.")


class PreprocessingInfo(Contract):
    version: str
    config_sha256: str | None = None


class ResultProvenance(Contract):
    source: ResultSource
    computed_at: datetime | None = Field(description="When the scores were originally computed.")
    served_at: datetime
    latency_ms: float | None = Field(
        default=None, ge=0, description="Wall time of this live run; only for source=live."
    )
    cache_key: str | None = None
    notice: str | None = None

    @model_validator(mode="after")
    def _source_rules(self) -> Self:
        if self.source is ResultSource.live:
            if self.latency_ms is None or self.computed_at is None:
                raise ValueError("live results require computed_at and latency_ms")
            if self.cache_key is not None:
                raise ValueError("live results must not carry a cache_key")
        elif self.source is ResultSource.cached:
            if self.computed_at is None or self.cache_key is None:
                raise ValueError("cached results require computed_at and cache_key")
            if self.latency_ms is not None:
                raise ValueError("cached results must not report a live latency")
        elif self.source is ResultSource.fixture:
            if not self.notice or "FIXTURE" not in self.notice:
                raise ValueError("fixture results must carry a notice containing 'FIXTURE'")
            if self.latency_ms is not None:
                raise ValueError("fixture results must not report a latency")
        return self


class FindingResult(Contract):
    finding_id: str
    display_name: str
    status: FindingStatus
    score: float | None = Field(default=None, ge=0.0, le=1.0)
    score_kind: ScoreKind | None = None
    threshold: float | None = Field(
        default=None, ge=0.0, le=1.0, description="Validated operating threshold, if one exists."
    )
    above_threshold: bool | None = None
    reason: Reason | None = None
    explanation_available: bool = False

    @model_validator(mode="after")
    def _status_rules(self) -> Self:
        if self.status is FindingStatus.scored:
            if self.score is None or self.score_kind is None:
                raise ValueError("scored findings require score and score_kind")
            if (self.threshold is None) != (self.above_threshold is None):
                raise ValueError("threshold and above_threshold must be set together")
            if self.threshold is not None and self.above_threshold != (self.score >= self.threshold):
                raise ValueError("above_threshold must equal score >= threshold")
        else:
            if self.score is not None or self.score_kind is not None or self.threshold is not None:
                raise ValueError(f"{self.status} findings must not carry a score or threshold")
            if self.above_threshold is not None or self.explanation_available:
                raise ValueError(f"{self.status} findings have no threshold or explanation")
            if self.status is not FindingStatus.not_evaluated and self.reason is None:
                raise ValueError(f"{self.status} findings require a reason")
        return self


class InputUsage(Contract):
    plane: Plane
    series_id: str
    slices_used: int = Field(ge=0)


class PredictionRequest(Contract):
    study_id: str
    findings: list[str] | None = Field(
        default=None, description="Subset of the active profile; None means all."
    )
    allow_cached: bool = Field(
        default=True, description="Serve a matching cached result instead of running live."
    )


class PredictionResponse(Contract):
    schema_version: str = SCHEMA_VERSION
    prediction_id: str
    study_id: str
    provenance: ResultProvenance
    model: ModelInfo
    preprocessing: PreprocessingInfo
    findings: list[FindingResult]
    inputs: list[InputUsage]
    missing_planes: list[Plane]
    warnings: list[Reason] = Field(default_factory=list)

    @model_validator(mode="after")
    def _consistency(self) -> Self:
        ids = [f.finding_id for f in self.findings]
        if len(ids) != len(set(ids)):
            raise ValueError("finding_id values must be unique")
        if self.provenance.source is ResultSource.fixture:
            if not self.model.model_id.startswith("fixture") or self.model.checkpoint_sha256:
                raise ValueError("fixture results must name a fixture model and no checkpoint")
        elif not self.model.checkpoint_sha256:
            raise ValueError("live and cached results must identify their checkpoint")
        supported = set(self.model.supported_findings)
        for f in self.findings:
            if f.status is FindingStatus.unsupported and f.finding_id in supported:
                raise ValueError(f"{f.finding_id} is supported by the model; cannot be unsupported")
            if f.status is FindingStatus.scored and f.finding_id not in supported:
                raise ValueError(f"{f.finding_id} is not supported by the model; cannot be scored")
        return self


# ---------------------------------------------------------------------------
# Explanations
# ---------------------------------------------------------------------------


class ExplanationSlice(Contract):
    slice_index: int = Field(ge=0, description="0-based index in the series' slice order.")
    weight: float = Field(ge=0.0, le=1.0, description="Relative influence, max-normalised.")


class AttentionMap(Contract):
    slice_index: int = Field(ge=0)
    width: int = Field(ge=1)
    height: int = Field(ge=1)
    encoding: Literal["png_base64_gray8"] = "png_base64_gray8"
    data: str = Field(description="Base64 PNG, gray 0-255 = relative attention 0-1.")


class Explanation(Contract):
    schema_version: str = SCHEMA_VERSION
    study_id: str
    finding_id: str
    prediction_id: str
    model_version: str
    status: Literal["available", "unavailable"]
    kind: Literal["influential_slices", "attention_map"] | None = None
    series_id: str | None = None
    plane: Plane | None = None
    coordinate_space: Literal["rendered_slice_pixels"] = "rendered_slice_pixels"
    rendered_width: int | None = None
    rendered_height: int | None = None
    slices: list[ExplanationSlice] = Field(default_factory=list)
    attention: list[AttentionMap] = Field(default_factory=list)
    source: ResultSource
    reason: Reason | None = None
    notice: str = EXPLANATION_NOTICE

    @model_validator(mode="after")
    def _alignment(self) -> Self:
        if self.status == "unavailable":
            if self.reason is None or self.slices or self.attention:
                raise ValueError("unavailable explanations carry a reason and no content")
            return self
        if self.kind is None or self.series_id is None or self.plane is None:
            raise ValueError("available explanations require kind, series_id and plane")
        if not self.slices:
            raise ValueError("available explanations list at least one slice")
        for m in self.attention:
            if (m.width, m.height) != (self.rendered_width, self.rendered_height):
                raise ValueError("attention maps must match the rendered slice size")
        return self


# ---------------------------------------------------------------------------
# Dataset labels (evaluation only; never an inference input)
# ---------------------------------------------------------------------------


class DatasetLabel(Contract):
    finding_id: str
    state: LabelState
    provenance: LabelProvenance
    source_ref: str | None = Field(
        default=None, description="Where the label came from, e.g. 'train.csv' or 'rules v0.2'."
    )


class StudyLabels(Contract):
    schema_version: str = SCHEMA_VERSION
    study_id: str
    dataset_id: str | None
    origin: DataOrigin
    labels: list[DatasetLabel]
    notice: str = "Dataset labels are for evaluation only. They are never used by the model."


# ---------------------------------------------------------------------------
# Metrics and model card
# ---------------------------------------------------------------------------


class MetricValue(Contract):
    value: float | None = None
    status: Literal["defined", "undefined_single_class", "not_computed"]
    reason: str | None = None

    @model_validator(mode="after")
    def _value_rules(self) -> Self:
        if (self.status == "defined") != (self.value is not None):
            raise ValueError("value is present exactly when status is 'defined'")
        if self.status != "defined" and not self.reason:
            raise ValueError("undefined or uncomputed metrics require a reason")
        return self


class FindingMetrics(Contract):
    finding_id: str
    n_positive: int = Field(ge=0)
    n_negative: int = Field(ge=0)
    n_unknown: int = Field(ge=0, description="Excluded from every metric; never counted as negative.")
    roc_auc: MetricValue
    pr_auc: MetricValue
    prevalence: float | None = Field(default=None, ge=0, le=1)
    threshold: float | None = Field(default=None, ge=0, le=1)
    threshold_selected_on: Literal["validation"] | None = None
    sensitivity: MetricValue
    specificity: MetricValue
    brier: MetricValue

    @model_validator(mode="after")
    def _single_class(self) -> Self:
        single = self.n_positive == 0 or self.n_negative == 0
        if single and self.roc_auc.status == "defined":
            raise ValueError("ROC AUC is undefined when the partition has only one class")
        if (self.threshold is None) != (self.threshold_selected_on is None):
            raise ValueError("a threshold must state where it was selected")
        return self


class MacroAuc(Contract):
    value: float | None
    included: list[str]
    excluded: list[Reason] = Field(description="code = finding_id, message = why excluded.")


class InferenceMeasurement(Contract):
    latency_ms_p50: float = Field(ge=0)
    latency_ms_p95: float = Field(ge=0)
    peak_memory_mb: float = Field(ge=0)
    n_runs: int = Field(ge=1)
    hardware: str


class MetricsSnapshot(Contract):
    schema_version: str = SCHEMA_VERSION
    status: Literal["available", "unavailable"]
    reason: str | None = None
    origin: DataOrigin
    model: ModelInfo | None = None
    preprocessing: PreprocessingInfo | None = None
    dataset_id: str | None = None
    partition: Literal["validation", "test"] | None = None
    split_method: str | None = None
    grouping_unit: Literal["patient", "study"] | None = None
    n_studies: int | None = Field(default=None, ge=0)
    per_finding: list[FindingMetrics] = Field(default_factory=list)
    macro_roc_auc: MacroAuc | None = None
    calibration: Literal["not_assessed", "assessed"] = "not_assessed"
    inference: InferenceMeasurement | None = None
    created_at: datetime | None = None

    @model_validator(mode="after")
    def _availability(self) -> Self:
        if self.status == "unavailable":
            if not self.reason or self.per_finding or self.macro_roc_auc:
                raise ValueError("unavailable snapshots carry a reason and no metrics")
            return self
        required = (
            self.model,
            self.dataset_id,
            self.partition,
            self.split_method,
            self.grouping_unit,
            self.n_studies,
            self.created_at,
        )
        if any(v is None for v in required):
            raise ValueError(
                "available snapshots must state model, dataset, partition, "
                "split method, grouping unit, study count and creation time"
            )
        if self.origin is DataOrigin.fixture:
            raise ValueError("fixture metrics may only be 'unavailable'")
        return self


class ModelCardSection(Contract):
    section_id: str
    title: str
    body: str


class ModelCard(Contract):
    schema_version: str = SCHEMA_VERSION
    status: Literal["draft", "published"]
    origin: DataOrigin
    model: ModelInfo | None
    preprocessing: PreprocessingInfo | None
    sections: list[ModelCardSection]
    limitations: list[str]
    updated_at: datetime | None = None


# ---------------------------------------------------------------------------
# Service
# ---------------------------------------------------------------------------


class Health(Contract):
    status: Literal["ok", "degraded"]
    api_version: str
    schema_version: str = SCHEMA_VERSION
    mode: Literal["fixture", "model"]
    model_loaded: bool
    model_version: str | None
    preprocessing_version: str
    finding_profile: str


class ApiErrorBody(Contract):
    code: str
    message: str
    request_id: str
    retryable: bool
    detail: dict[str, object] | None = None


class ApiError(Contract):
    error: ApiErrorBody


EXPORTED_MODELS: tuple[type[BaseModel], ...] = (
    FindingProfile,
    StudyList,
    StudyDetail,
    PredictionRequest,
    PredictionResponse,
    Explanation,
    StudyLabels,
    MetricsSnapshot,
    ModelCard,
    Health,
    ApiError,
)
