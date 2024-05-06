def data_file_validation(request):
    if request.method == "POST":
        if "work_id" not in request.form:
            request.form["work_id"] = "rode_test"

        if "archivo" not in request.form:
            request.form["archivo"] = "no_name"

        if "tipo" not in request.form:
            request.form["tipo"] = "image"

        return request.form