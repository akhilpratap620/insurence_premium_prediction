from collections import namedtuple



InitialisedModelDetail = namedtuple(
    "InitialisedModelDetail",
    ["model_serial_number", "model", "param_grid_search", "model_name"],
)

GridSearchedBestModel = namedtuple(
    "GridSearchedBestModel",
    [
        "model_serial_number",
        "model",
        "best_model",
        "best_parameters",
        "best_score",
    ],
)

BestModel = namedtuple(
    "BestModel",
    [
        "model_serial_number",
        "model",
        "best_model",
        "best_parameters",
        "best_score",
    ],
)

MetricInfoArtifact = namedtuple(
    "MetricInfoArtifact",
    [
        "model_name",
        "model_object",
        "train_rmse",
        "test_rmse",
        "train_accuracy",
        "test_accuracy",
        "model_accuracy",
        "index_number",
    ],
)

ModelTrainerArtifact = namedtuple("ModelTrainerArtifact", ["is_trained", "message", "trained_model_file_path",
                                                           "train_rmse", "test_rmse", "train_accuracy", "test_accuracy",
                                                           "model_accuracy"])


ModelEvaluationArtifact=namedtuple("ModelEvaluationArtifact",['evaluated_model_path', 'is_model_accepted'])