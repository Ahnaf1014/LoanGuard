"""Dashboard feature: read-only portfolio totals shown on the home page."""

from flask import Blueprint, render_template

from services.dashboard_service import DashboardService

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/")
def dashboard():
    """Load summary metrics and render the dashboard landing page."""
    metrics = DashboardService.get_summary_metrics()
    return render_template("dashboard/index.html", **metrics)
