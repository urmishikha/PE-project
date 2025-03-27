def generate_compliance_report():
    report = {
        "total_alerts": total_alerts,
        "anomalies_detected": total_anomalies,
        "blocked_ips": blocked_ips,
        "audit_logs": audit_logs
    }
    return report