"""Dataset adapters: turn a permitted dataset into SeriesVolume objects.

Each adapter owns ordering (slice_index), plane assignment, series selection and
corrupt-input detection for its dataset. Labels are loaded separately by
``kneescope_ml.labels`` and never pass through an adapter used for inference.
"""
