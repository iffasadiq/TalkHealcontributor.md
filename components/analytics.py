import pandas as pd
import plotly.graph_objs as go
from typing import Tuple, List, Dict, Any

# Example: mood_log should be a DataFrame with columns: ['timestamp', 'mood_score']
# timestamp: datetime, mood_score: int or float

def analyze_mood_trends(mood_log: pd.DataFrame) -> Dict[str, Any]:
    """
    Analyze mood trends using rolling averages and day/time patterns.
    Returns insights and recommendations.
    """
    if mood_log.empty:
        return {"insights": [], "recommendations": [], "charts": []}

    mood_log = mood_log.copy()
    mood_log['timestamp'] = pd.to_datetime(mood_log['timestamp'])
    mood_log['day_of_week'] = mood_log['timestamp'].dt.day_name()
    mood_log['hour'] = mood_log['timestamp'].dt.hour

    # Rolling average (7-day window)
    mood_log = mood_log.sort_values('timestamp')
    mood_log['rolling_avg'] = mood_log['mood_score'].rolling(window=7, min_periods=1).mean()

    # Day-of-week analysis
    dow_avg = mood_log.groupby('day_of_week')['mood_score'].mean().sort_values()
    lowest_day = dow_avg.idxmin()
    highest_day = dow_avg.idxmax()

    # Time-of-day analysis
    hod_avg = mood_log.groupby('hour')['mood_score'].mean().sort_values()
    lowest_hour = hod_avg.idxmin()
    highest_hour = hod_avg.idxmax()

    insights = [
        f"Your average mood is lowest on {lowest_day} (score: {dow_avg[lowest_day]:.2f}).",
        f"Your average mood is highest on {highest_day} (score: {dow_avg[highest_day]:.2f}).",
        f"Mood tends to dip at {lowest_hour}:00 (score: {hod_avg[lowest_hour]:.2f}).",
        f"Mood peaks at {highest_hour}:00 (score: {hod_avg[highest_hour]:.2f})."
    ]

    # Simple recommendations
    recommendations = []
    if dow_avg[lowest_day] < dow_avg.mean() - 0.5:
        recommendations.append(f"Consider scheduling a Focus Session or Yoga on {lowest_day}.")
    if hod_avg[lowest_hour] < hod_avg.mean() - 0.5:
        recommendations.append(f"Try a Breathing Exercise around {lowest_hour}:00 when mood dips.")

    # Plotly line chart for rolling average
    chart = go.Figure()
    chart.add_trace(go.Scatter(x=mood_log['timestamp'], y=mood_log['mood_score'], mode='lines+markers', name='Mood Score'))
    chart.add_trace(go.Scatter(x=mood_log['timestamp'], y=mood_log['rolling_avg'], mode='lines', name='7-Day Rolling Avg'))
    chart.update_layout(title='Mood Over Time', xaxis_title='Date', yaxis_title='Mood Score')

    return {
        "insights": insights,
        "recommendations": recommendations,
        "charts": [chart]
    }

def analyze_activity_mood_correlation(mood_data: pd.DataFrame) -> Dict[str, Any]:
    """
    Analyze the correlation between activities and mood levels.
    Returns insights about which activities improve mood and recommendations.
    """
    if mood_data.empty or 'activities' not in mood_data.columns:
        return {
            "top_activities": [],
            "activity_insights": [],
            "activity_recommendations": [],
            "activity_chart": None
        }

    # Convert mood levels to numeric values
    mood_mapping = {
        "very_low": 1,
        "low": 2,
        "okay": 3,
        "good": 4,
        "great": 5
    }

    mood_data = mood_data.copy()
    mood_data['mood_numeric'] = mood_data['mood_level'].map(mood_mapping)

    # Explode activities to separate rows
    activity_mood = mood_data.explode('activities')

    # Remove rows with empty activities
    activity_mood = activity_mood[activity_mood['activities'].notna()]
    activity_mood = activity_mood[activity_mood['activities'] != '']

    if activity_mood.empty:
        return {
            "top_activities": [],
            "activity_insights": ["No activity data available for analysis."],
            "activity_recommendations": [],
            "activity_chart": None
        }

    # Calculate average mood for each activity
    activity_stats = activity_mood.groupby('activities').agg({
        'mood_numeric': ['mean', 'count', 'std']
    }).round(2)

    # Flatten column names
    activity_stats.columns = ['avg_mood', 'count', 'std_dev']
    activity_stats = activity_stats.reset_index()

    # Sort by average mood (descending) and filter activities with at least 2 occurrences
    activity_stats = activity_stats[activity_stats['count'] >= 2].sort_values('avg_mood', ascending=False)

    # Get top 3 activities
    top_activities = activity_stats.head(3).to_dict('records')

    # Generate insights
    insights = []
    recommendations = []

    if len(top_activities) >= 3:
        insights.append(f"🏆 **Top 3 Activities for Better Mood:**")
        for i, activity in enumerate(top_activities, 1):
            activity_name = activity['activities']
            avg_mood = activity['avg_mood']
            count = activity['count']
            mood_label = {1: "Very Low", 2: "Low", 3: "Okay", 4: "Good", 5: "Great"}.get(round(avg_mood), "Unknown")
            insights.append(f"{i}. **{activity_name}** - Average mood: {mood_label} ({avg_mood:.1f}/5, {count} times)")

        # Add overall insight
        best_activity = top_activities[0]['activities']
        insights.append(f"💡 **{best_activity}** has the strongest positive impact on your mood!")

        # Generate recommendations
        recommendations.append(f"🎯 Try incorporating **{best_activity}** into your routine when you need a mood boost.")
        recommendations.append("📊 Track your activities regularly to discover more mood-boosting patterns.")

    elif len(top_activities) >= 1:
        best_activity = top_activities[0]['activities']
        avg_mood = top_activities[0]['avg_mood']
        count = top_activities[0]['count']
        mood_label = {1: "Very Low", 2: "Low", 3: "Okay", 4: "Good", 5: "Great"}.get(round(avg_mood), "Unknown")

        insights.append(f"🏆 **{best_activity}** appears to improve your mood (avg: {mood_label}, {count} times)")
        recommendations.append(f"🎯 Continue tracking **{best_activity}** to confirm its mood-boosting effects.")

    else:
        insights.append("📊 Need more activity data to analyze mood correlations.")
        recommendations.append("🎯 Track your activities with mood entries to discover patterns.")

    # Create activity-mood correlation chart
    if not activity_stats.empty:
        import plotly.express as px

        # Sort for better visualization
        chart_data = activity_stats.sort_values('avg_mood', ascending=True)

        chart = px.bar(
            chart_data,
            x='avg_mood',
            y='activities',
            orientation='h',
            title='Activity-Mood Correlation',
            labels={'avg_mood': 'Average Mood Score', 'activities': 'Activity'},
            color='count',
            color_continuous_scale='Blues'
        )

        chart.update_layout(
            xaxis=dict(tickmode='array', tickvals=[1, 2, 3, 4, 5],
                      ticktext=['Very Low', 'Low', 'Okay', 'Good', 'Great']),
            height=max(400, len(chart_data) * 30)
        )
    else:
        chart = None

    return {
        "top_activities": top_activities,
        "activity_insights": insights,
        "activity_recommendations": recommendations,
        "activity_chart": chart
    }
