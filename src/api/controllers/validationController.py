def validateForCreate(req, validator, model):
    inputValidator = validator(req)
    try:
        if not inputValidator.validate():
            return None, inputValidator.errors, 400
    except TypeError:
        return None, "Not correct json format", 400

    for key in req.get_json():
        if hasattr(model, key):
            col = getattr(model, key)
            if col.prop.expression.const:
                return None, "forbidden attribute", 400
        else:
            return None, "More json parameters where given than expected", 400
    return True


def validateForUpdate(req, validator, model):
    inputValidator = validator(req)
    try:
        if not inputValidator.validate():
            return None, inputValidator.errors, 400
    except TypeError:
        return None, "Not correct json format", 400

    for key in req.get_json():
        if key != "id":
            if hasattr(model, key):
                col = getattr(model, key)
                if col.prop.expression.readonly or col.prop.expression.const:
                    return None, "forbidden attribute", 400
            else:
                return None, "More json parameters where given than expected", 400
    return True
