from utils.logger import logger
from models.host import HostModel


def export_html(output: str, hosts: list[HostModel], duration, generated_at):
    """Export audit results to a HTML file."""
    logger.verbose = True
    if not output.endswith(".html"):
        output += ".html"

    hosts_count = len(hosts)
    users_count = sum(len(host.users) for host in hosts)

    safe_count = 0
    warning_count = 0
    expired_count = 0
    never_count = 0

    html = f"""<!DOCTYPE html>
    <html lang="en">
    <head>
    <meta charset="UTF-8">
    <title>PEXA Password Expiration Audit Report</title>

    <style>

    body {{
        font-family: monospace;
        color: #000;
        background: #fff;
        margin: 20px;
    }}

    .container {{
        max-width: 1200px;
        margin: auto;
    }}

    h1 {{
        font-size: 18px;
        font-weight: bold;
        margin: 0 0 5px 0;
    }}

    h2 {{
        font-size: 16px;
        font-weight: bold;
        margin: 20px 0 10px 0;
    }}

    .subtitle {{
        color: #444;
        margin-bottom: 20px;
        font-size: 14px;
    }}

    .summary {{
        margin: 20px 0;
        border: 1px solid #000;
        padding: 10px;
        display: inline-block;
    }}

    .summary-item {{
        display: inline-block;
        margin-right: 30px;
    }}

    .summary-item strong {{
        font-weight: bold;
    }}

    .host {{
        margin-top: 25px;
        border-top: 1px solid #ccc;
        padding-top: 15px;
    }}

    table {{
        width: 100%;
        border-collapse: collapse;
        margin-top: 10px;
        font-size: 13px;
    }}

    th {{
        background: #000;
        color: #fff;
        padding: 6px 8px;
        text-align: left;
        font-weight: bold;
    }}

    td {{
        padding: 5px 8px;
        border-bottom: 1px solid #ddd;
    }}

    tr:hover {{
        background: #f0f0f0;
    }}

    .safe {{
        background: #fff;
    }}

    .warning {{
        background: #ffffcc;
    }}

    .expired {{
        background: #ffcccc;
    }}

    .never {{
        background: #e8e8e8;
    }}

    .footer {{
        margin-top: 40px;
        border-top: 1px solid #000;
        padding-top: 15px;
        font-size: 13px;
    }}

    .overall {{
        font-size: 16px;
        font-weight: bold;
        margin-top: 10px;
    }}

    .critical {{
        color: #cc0000;
    }}

    .attention {{
        color: #cc6600;
    }}

    .healthy {{
        color: #006600;
    }}

    </style>

    </head>

    <body>

    <div class="container">

    <h1>PEXA Password Expiration Audit Report</h1>
    <p class="subtitle">Generated: {generated_at} | Duration: {duration}</p>

    <div class="summary">
        <span class="summary-item"><strong>Hosts:</strong> {hosts_count}</span>
        <span class="summary-item"><strong>Users:</strong> {users_count}</span>
    </div>
    """

    for host in hosts:
        html += f"""
        <div class="host">
        <h2>{host.hostname} ({len(host.users)} users)</h2>

        <table>
        <tr>
            <th>Username</th>
            <th>UID</th>
            <th>Status</th>
            <th>Password Expires</th>
        </tr>
        """

        for user in host.users:
            if user.status.lower() == "safe":
                row_class = "safe"
            elif user.status.lower() == "warning":
                row_class = "warning"
            elif user.status.lower() == "expired":
                row_class = "expired"
            else:
                row_class = "never"

            if user.expires_in_days is None:
                expires = "Never"
                never_count += 1
                safe_count += 1
            elif user.expires_in_days < 0:
                expires = f"Expired ({abs(user.expires_in_days)} days ago)"
                expired_count += 1
            elif user.expires_in_days <= 7:
                if user.expires_in_days == 0:
                    expires = "Expires Today"
                else:
                    expires = f"{user.expires_in_days} days"
                warning_count += 1
            else:
                expires = f"{user.expires_in_days} days"
                safe_count += 1

            html += f"""
            <tr class="{row_class}">
                <td>{user.username}</td>
                <td>{user.uid}</td>
                <td>{user.status}</td>
                <td>{expires}</td>
            </tr>
            """

        html += "</table></div>"

    if expired_count > 0:
        overall_result = "CRITICAL"
        overall_class = "critical"
    elif warning_count > 0:
        overall_result = "ATTENTION REQUIRED"
        overall_class = "attention"
    else:
        overall_result = "HEALTHY"
        overall_class = "healthy"

    html += f"""
    <div class="footer">
        <h2>Account Summary</h2>
        <div class="summary">
            <span class="summary-item"><strong>Safe:</strong> {safe_count}</span>
            <span class="summary-item"><strong>Warning:</strong> {warning_count}</span>
            <span class="summary-item"><strong>Expired:</strong> {expired_count}</span>
            <span class="summary-item"><strong>Never Expires:</strong> {never_count}</span>
        </div>
        <p class="overall {overall_class}">Overall Status: {overall_result}</p>
        <p>Generated by PEXA - Password Expiration Auditor</p>
    </div>

    </div>

    </body>
    </html>
    """

    with open(output, "w") as f:
        f.write(html)
    logger.success(f"HTML report written to '{output}'")
