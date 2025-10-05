"""
Logging utilities for tracking user activity
"""
from datetime import datetime
from flask import request
from flask_login import current_user

# Import database models (with fallback if not available)
try:
    from db import db, UserLog, update_session_activity
    DB_AVAILABLE = True
except ImportError:
    DB_AVAILABLE = False
    print("⚠️  Database not available - logging disabled")

def get_client_ip():
    """Get client IP address"""
    if request.environ.get('HTTP_X_FORWARDED_FOR'):
        return request.environ['HTTP_X_FORWARDED_FOR'].split(',')[0]
    return request.environ.get('REMOTE_ADDR', 'unknown')

def log_event(event_type, event_data=None, user_id=None):
    """
    Log user activity to database

    Args:
        event_type: Type of event (login, logout, navigate, filter, etc.)
        event_data: Additional data (dict)
        user_id: User ID (defaults to current_user.id)
    """
    if not DB_AVAILABLE:
        return None

    try:
        if user_id is None and current_user.is_authenticated:
            user_id = current_user.id

        log = UserLog(
            user_id=user_id,
            event_type=event_type,
            event_data=event_data,
            ip_address=get_client_ip()
        )
        db.session.add(log)
        db.session.commit()
        return log
    except Exception as e:
        print(f"❌ Error logging event: {e}")
        db.session.rollback()
        return None

def log_login(username, success=True):
    """Log login attempt"""
    return log_event(
        event_type='login_success' if success else 'login_failed',
        event_data={'username': username}
    )

def log_logout():
    """Log logout"""
    return log_event(event_type='logout')

def log_navigate(destination_name, latitude, longitude):
    """Log navigate button click"""
    return log_event(
        event_type='navigate',
        event_data={
            'destination': destination_name,
            'latitude': latitude,
            'longitude': longitude
        }
    )

def log_filter_change(filter_type, filter_value):
    """Log filter selection"""
    return log_event(
        event_type='filter_change',
        event_data={
            'filter_type': filter_type,
            'filter_value': filter_value
        }
    )

def log_quick_filter(filter_name):
    """Log quick filter button click"""
    return log_event(
        event_type='quick_filter',
        event_data={'filter_name': filter_name}
    )

def log_page_view(page):
    """Log page view"""
    return log_event(
        event_type='page_view',
        event_data={'page': page}
    )

def log_error(error_message, error_type='general'):
    """Log error"""
    return log_event(
        event_type='error',
        event_data={
            'error_type': error_type,
            'error_message': str(error_message)
        }
    )

def update_user_activity(user_id, session_id):
    """Update user's last activity (for online counter)"""
    if not DB_AVAILABLE:
        return

    try:
        update_session_activity(user_id, session_id)
    except Exception as e:
        print(f"❌ Error updating session: {e}")

def get_user_stats(days=30):
    """
    Get user activity statistics

    Args:
        days: Number of days to look back

    Returns:
        dict with statistics
    """
    if not DB_AVAILABLE:
        return {}

    try:
        from datetime import timedelta
        from sqlalchemy import func

        since = datetime.utcnow() - timedelta(days=days)

        # Total events
        total_events = UserLog.query.filter(UserLog.timestamp >= since).count()

        # Events by type
        events_by_type = db.session.query(
            UserLog.event_type,
            func.count(UserLog.id).label('count')
        ).filter(
            UserLog.timestamp >= since
        ).group_by(UserLog.event_type).all()

        # Most active users
        most_active_users = db.session.query(
            UserLog.user_id,
            func.count(UserLog.id).label('count')
        ).filter(
            UserLog.timestamp >= since,
            UserLog.user_id.isnot(None)
        ).group_by(UserLog.user_id).order_by(
            func.count(UserLog.id).desc()
        ).limit(10).all()

        # Most navigated locations
        navigate_logs = UserLog.query.filter(
            UserLog.event_type == 'navigate',
            UserLog.timestamp >= since
        ).all()

        location_counts = {}
        for log in navigate_logs:
            if log.event_data and 'destination' in log.event_data:
                dest = log.event_data['destination']
                location_counts[dest] = location_counts.get(dest, 0) + 1

        top_locations = sorted(
            location_counts.items(),
            key=lambda x: x[1],
            reverse=True
        )[:10]

        return {
            'total_events': total_events,
            'events_by_type': {et: count for et, count in events_by_type},
            'most_active_users': [
                {'user_id': uid, 'count': count}
                for uid, count in most_active_users
            ],
            'top_locations': [
                {'location': loc, 'count': count}
                for loc, count in top_locations
            ]
        }
    except Exception as e:
        print(f"❌ Error getting stats: {e}")
        return {}

def get_recent_activity(limit=50):
    """Get recent activity logs"""
    if not DB_AVAILABLE:
        return []

    try:
        logs = UserLog.query.order_by(
            UserLog.timestamp.desc()
        ).limit(limit).all()

        return [log.to_dict() for log in logs]
    except Exception as e:
        print(f"❌ Error getting recent activity: {e}")
        return []
