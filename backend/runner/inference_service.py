from OpenDCAN.models import ResNetInferenceModel


def inference_sample(model_path, sample_path, classes):

    idx_to_classes = {i : cls_name for i, cls_name in enumerate(classes)}

    model = ResNetInferenceModel(len(classes) + 1)
    model.load_parameter(model_path)

    with open(sample_path, 'rb') as f:
        pred, likelihood = model.predict(f)
    
    predict_class = idx_to_classes[pred]
    likelihood = round((100-likelihood*100),3)

    return predict_class, likelihood