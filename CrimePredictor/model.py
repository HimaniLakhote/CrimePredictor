import pandas as pd
from pgmpy.models import DiscreteBayesianNetwork
from pgmpy.estimators import BayesianEstimator
from pgmpy.inference import VariableElimination


def load_and_preprocess_data(filepath: str) -> pd.DataFrame:
    data = pd.read_csv(filepath)
    data = data.dropna()
    data = data.drop_duplicates()
    data = data.apply(lambda x: x.str.lower() if x.dtype == "object" else x)
    return data


def build_bayesian_network(data: pd.DataFrame) -> DiscreteBayesianNetwork:
    target_cols = {'crime', 'suspect'}
    feature_cols = [col for col in data.columns if col not in target_cols]

    edges = []

    # All features → crime
    edges.extend([(feature, 'crime') for feature in feature_cols])

    # All features → suspect
    edges.extend([(feature, 'suspect') for feature in feature_cols])

    # crime → suspect
    edges.append(('crime', 'suspect'))

    return DiscreteBayesianNetwork(edges)


def train_model(model, data):
    model.fit(data, estimator=BayesianEstimator, prior_type="BDeu")
    return model


def predict_all(evidence_dict: dict):
    # Filter valid columns
    valid_evidence = {k: v for k, v in evidence_dict.items() if k in data.columns}

    crime_result = infer.query(variables=['crime'], evidence=valid_evidence)
    suspect_result = infer.query(variables=['suspect'], evidence=valid_evidence)

    # Convert to dictionary
    crime_dict = dict(zip(crime_result.state_names['crime'], crime_result.values))
    suspect_dict = dict(zip(suspect_result.state_names['suspect'], suspect_result.values))

    return crime_dict, suspect_dict


# Initialize everything
data = load_and_preprocess_data("crime_dataset.csv")
model = build_bayesian_network(data)
model = train_model(model, data)
infer = VariableElimination(model)


# Export
__all__ = ['data', 'predict_all']