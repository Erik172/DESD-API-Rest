def data_file_validation(request):
    """
    Validate the data in the request object and provide default values if necessary.

    Args:
        request (object): The request object containing the data.

    Returns:
        dict: A dictionary containing the validated data.

    """
    if request.method == "POST":
        form_data = request.form.to_dict()  # Create a mutable copy of request.form
        if "work_id" not in form_data:
            form_data["work_id"] = "rode_test"

        if "archivo" not in form_data:
            form_data["archivo"] = "no_name"

        if "tipo" not in form_data:
            form_data["tipo"] = "image"

        return form_data
