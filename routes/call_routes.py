from flask import Blueprint, render_template, request, jsonify
from services.call_service import CallService
from utils.decorators import login_required, admin_required
from datetime import datetime

call_bp = Blueprint("call", __name__, url_prefix="/call")


@call_bp.route("/", methods=["POST"])
@admin_required
def create_call():
    try:
        data = request.get_json()

        title = data.get("title", "").strip() if data else ""
        description = data.get("description", "").strip() if data else ""
        opening_date = data.get("opening_date") if data else None
        closing_date = data.get("closing_date") if data else None

        errors = {}

        if not title:
            errors["title"] = "El título es obligatorio."
        elif len(title) > 80:
            errors["title"] = "El título no puede exceder 80 caracteres."

        if not opening_date:
            errors["opening_date"] = "La fecha de inicio es obligatoria."

        if not closing_date:
            errors["closing_date"] = "La fecha de cierre es obligatoria."

        if opening_date and closing_date:
            try:
                opening_dt = datetime.strptime(opening_date, "%Y-%m-%d")
                closing_dt = datetime.strptime(closing_date, "%Y-%m-%d")

                if closing_dt < opening_dt:
                    errors["closing_date"] = (
                        "La fecha de cierre debe ser posterior a la fecha de inicio."
                    )
            except ValueError:
                errors["opening_date"] = "Formato de fecha inválido."

        if errors:
            return jsonify({"errors": errors}), 422

        call, error, status_code = CallService.create(
            title=title,
            description=description,
            opening_date=opening_date,
            closing_date=closing_date,
        )

        if error:
            return jsonify({"error": error}), status_code

        return (
            jsonify(
                {"message": "Convocatoria creada exitosamente.", "call_id": call.id}
            ),
            201,
        )

    except Exception as e:
        return jsonify({"error": "Error interno del servidor."}), 500


@call_bp.route("/", methods=["GET"])
@login_required
def view_all():
    calls = CallService.get_all()
    return render_template("call/manage_call.html", calls=calls)


@call_bp.route("/<int:call_id>", methods=["GET"])
@login_required
def view_call(call_id):
    call = CallService.get_by_id(call_id)
    if not call:
        return render_template("404.html"), 404
    return render_template("call/view_call.html", call=call)


@call_bp.route("/<int:call_id>", methods=["PUT"])
@admin_required
def update_call(call_id):
    try:
        data = request.get_json()

        title = data.get("title", "").strip() if data else ""
        description = data.get("description", "").strip() if data else ""
        opening_date = data.get("opening_date") if data else None
        closing_date = data.get("closing_date") if data else None

        errors = {}

        if not title:
            errors["title"] = "El título es obligatorio."
        elif len(title) > 80:
            errors["title"] = "El título no puede exceder 80 caracteres."

        if not opening_date:
            errors["opening_date"] = "La fecha de inicio es obligatoria."

        if not closing_date:
            errors["closing_date"] = "La fecha de cierre es obligatoria."

        if opening_date and closing_date:
            try:
                opening_dt = datetime.strptime(opening_date, "%Y-%m-%d")
                closing_dt = datetime.strptime(closing_date, "%Y-%m-%d")

                if closing_dt < opening_dt:
                    errors["closing_date"] = (
                        "La fecha de cierre debe ser posterior a la fecha de inicio."
                    )
            except ValueError:
                errors["opening_date"] = "Formato de fecha inválido."

        if errors:
            return jsonify({"errors": errors}), 422

        call, error, status_code = CallService.update(
            call_id,
            title=title,
            description=description,
            opening_date=opening_date,
            closing_date=closing_date,
        )

        if error:
            return jsonify({"error": error}), status_code

        return jsonify({"message": "Convocatoria actualizada exitosamente."})

    except Exception as e:
        return jsonify({"error": "Error interno del servidor."}), 500


@call_bp.route("/<int:call_id>", methods=["DELETE"])
@admin_required
def delete_call(call_id):
    try:
        call, error, status_code = CallService.delete(call_id)

        if error:
            return jsonify({"error": error}), status_code

        return jsonify({"message": "Convocatoria eliminada exitosamente."})

    except Exception as e:
        return jsonify({"error": "Error interno del servidor."}), 500
