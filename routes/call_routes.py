from flask import Blueprint, render_template, request, jsonify
from services.call_service import CallService
from utils.decorators import login_required, admin_required

call_bp = Blueprint("call", __name__, url_prefix="/call")


@call_bp.route("/", methods=["POST"])
@admin_required
def create_call():
    data = request.get_json()
    title = data.get("title", "").strip() if data else ""
    description = data.get("description", "").strip() if data else ""
    opening_date = data.get("opening_date") if data else None
    closing_date = data.get("closing_date") if data else None

    if not title:
        return jsonify({"error": "El título es obligatorio."}), 422

    call, error, status_code = CallService.create(
        title=title,
        description=description,
        opening_date=opening_date,
        closing_date=closing_date,
    )
    if error:
        return jsonify({"error": error}), status_code

    return jsonify({"message": "Convocatoria creada.", "call_id": call.id}), 201


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
    data = request.get_json()
    title = data.get("title", "").strip() if data else ""
    description = data.get("description", "").strip() if data else ""
    opening_date = data.get("opening_date") if data else None
    closing_date = data.get("closing_date") if data else None

    if not title:
        return jsonify({"error": "El título es obligatorio."}), 422

    call, error, status_code = CallService.update(
        call_id,
        title=title,
        description=description,
        opening_date=opening_date,
        closing_date=closing_date,
    )
    if error:
        return jsonify({"error": error}), status_code

    return jsonify({"message": "Convocatoria actualizada."})


@call_bp.route("/<int:call_id>", methods=["DELETE"])
@admin_required
def delete_call(call_id):
    call, error, status_code = CallService.delete(call_id)
    if error:
        return jsonify({"error": error}), status_code

    return jsonify({"message": "Convocatoria eliminada."})
