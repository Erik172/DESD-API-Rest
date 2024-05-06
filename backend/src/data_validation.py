def data_file_validation(request):
    """
    Validate the data in the request object and provide default values if necessary.

    Args:
        request (object): The request object containing the data.

    Returns:
        dict: A dictionary containing the validated data.

    """
    if request.method == "POST":
        if "work_id" not in request.form:
            request.form["work_id"] = "rode_test"

        if "archivo" not in request.form:
            request.form["archivo"] = "no_name"

        if "tipo" not in request.form:
            request.form["tipo"] = "image"

        return request.form