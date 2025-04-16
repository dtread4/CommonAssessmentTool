from app.clients.service.constants import COLUMNS_FIELDS, INTERVENTION_FIELDS


def get_feature_columns():
    """Get all feature columns"""
    return COLUMNS_FIELDS


def get_intervention_columns():
    """Get all intervention columns"""
    return INTERVENTION_FIELDS


def get_all_feature_columns():
    """Get all feature columns"""
    return get_feature_columns() + get_intervention_columns()


def get_true_file_name(model_type, filename):
    """Format pickle file name"""
    return filename.format(model_type).replace(" ", "_")



