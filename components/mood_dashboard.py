import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import os
from collections import Counter, defaultdict
from components.analytics import analyze_mood_trends, analyze_activity_mood_correlation
from components.predictive_analytics import predict_mood_trends
from components.weather_correlation import render_weather_mood_analysis

class MoodTracker:
    def __init__(self):
        self.data_file = "data/mood_data.json"
        self.ensure_data_directory()
        self.load_mood_data()
    
    def ensure_data_directory(self):
        """Ensure the data directory exists"""
        os.makedirs("data", exist_ok=True)
    
    def load_mood_data(self):
        """Load mood data from JSON file"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    st.session_state.mood_data = json.load(f)
                # Migrate existing data to include new fields
                self.migrate_old_data()
            except:
                st.session_state.mood_data = []
        else:
            st.session_state.mood_data = []
    
    def migrate_old_data(self):
        """Migrate old mood data to include new fields"""
        for entry in st.session_state.mood_data:
            # Add context_reason if missing
            if 'context_reason' not in entry:
                entry['context_reason'] = "No specific reason"
            
            # Add activities if missing
            if 'activities' not in entry:
                entry['activities'] = []
            
            # Ensure activities is a list
            if not isinstance(entry['activities'], list):
                entry['activities'] = []
        
        # Save migrated data
        self.save_mood_data()
    
    def save_mood_data(self):
        """Save mood data to JSON file"""
        with open(self.data_file, 'w') as f:
            json.dump(st.session_state.mood_data, f, indent=2)
    
    def add_mood_entry(self, mood_level, notes="", context_reason="", activities=None, timestamp=None):
        """Add a new mood entry with enhanced context"""
        if timestamp is None:
            timestamp = datetime.now().isoformat()
        
        if activities is None:
            activities = []
        
        entry = {
            "timestamp": timestamp,
            "mood_level": mood_level,
            "notes": notes,
            "context_reason": context_reason,
            "activities": activities,
            "date": datetime.fromisoformat(timestamp).strftime("%Y-%m-%d"),
            "time": datetime.fromisoformat(timestamp).strftime("%H:%M"),
            "day_of_week": datetime.fromisoformat(timestamp).strftime("%A")
        }
        
        st.session_state.mood_data.append(entry)
        self.save_mood_data()
    
    def get_mood_dataframe(self, days=30):
        """Get mood data as pandas DataFrame for the last N days"""
        if not st.session_state.mood_data:
            return pd.DataFrame()
        
        cutoff_date = datetime.now() - timedelta(days=days)
        recent_data = [
            entry for entry in st.session_state.mood_data
            if datetime.fromisoformat(entry["timestamp"]) >= cutoff_date
        ]
        
        if not recent_data:
            return pd.DataFrame()
        
        df = pd.DataFrame(recent_data)
        df['datetime'] = pd.to_datetime(df['timestamp'])
        df['date'] = pd.to_datetime(df['date'])
        return df.sort_values('datetime')
    
    def export_mood_data_csv(self, days=None):
        """Export mood data as CSV string for the specified number of days"""
        if days is not None:
            df = self.get_mood_dataframe(days)
        else:
            # Export all data
            if not st.session_state.mood_data:
                return ""
            df = pd.DataFrame(st.session_state.mood_data)
            df['datetime'] = pd.to_datetime(df['timestamp'])
            df['date'] = pd.to_datetime(df['date'])
            df = df.sort_values('datetime')
        
        if df.empty:
            return ""
        
        # Convert activities list to comma-separated string for CSV
        df_export = df.copy()
        df_export['activities'] = df_export['activities'].apply(lambda x: ', '.join(x) if isinstance(x, list) else str(x))
        
        # Select and reorder columns for export
        export_columns = ['date', 'time', 'day_of_week', 'mood_level', 'notes', 'context_reason', 'activities', 'timestamp']
        df_export = df_export[export_columns]
        
        return df_export.to_csv(index=False)
    
    def export_mood_data_json(self, days=None):
        """Export mood data as JSON string for the specified number of days"""
        if days is not None:
            df = self.get_mood_dataframe(days)
            if df.empty:
                return "[]"
            export_data = df.to_dict('records')
        else:
            # Export all data
            if not st.session_state.mood_data:
                return "[]"
            export_data = st.session_state.mood_data
        
        return json.dumps(export_data, indent=2)
    
    def get_mood_numeric(self, mood_level):
        """Convert mood level to numeric value for analysis"""
        mood_mapping = {
            "very_low": 1,
            "low": 2,
            "okay": 3,
            "good": 4,
            "great": 5
        }
        return mood_mapping.get(mood_level, 3)
    
    def get_mood_label(self, mood_level):
        """Convert mood level to display label"""
        mood_labels = {
            "very_low": "😔 Very Low",
            "low": "😐 Low",
            "okay": "😊 Okay",
            "good": "😄 Good",
            "great": "🌟 Great"
        }
        return mood_labels.get(mood_level, mood_level)
    
    def export_mood_data_csv(self, days=None):
        """Export mood data as CSV string for download"""
        if not st.session_state.mood_data:
            return ""
        
        # Filter data if days specified
        data_to_export = st.session_state.mood_data
        if days is not None:
            cutoff_date = datetime.now() - timedelta(days=days)
            data_to_export = [
                entry for entry in st.session_state.mood_data
                if datetime.fromisoformat(entry["timestamp"]) >= cutoff_date
            ]
        
        if not data_to_export:
            return ""
        
        # Convert to DataFrame for easy CSV export
        df = pd.DataFrame(data_to_export)
        
        # Add numeric mood column for analysis
        df['mood_numeric'] = df['mood_level'].apply(self.get_mood_numeric)
        df['mood_label'] = df['mood_level'].apply(self.get_mood_label)
        
        # Convert activities list to string for CSV compatibility
        df['activities'] = df['activities'].apply(lambda x: ', '.join(x) if isinstance(x, list) else str(x))
        
        # Reorder columns for better readability
        columns_order = ['date', 'time', 'day_of_week', 'mood_level', 'mood_label', 'mood_numeric', 
                        'notes', 'context_reason', 'activities', 'timestamp']
        df = df[columns_order]
        
        # Convert to CSV string
        return df.to_csv(index=False)
    
    def export_mood_data_json(self, days=None):
        """Export mood data as JSON string for download"""
        if not st.session_state.mood_data:
            return "[]"
        
        # Filter data if days specified
        data_to_export = st.session_state.mood_data
        if days is not None:
            cutoff_date = datetime.now() - timedelta(days=days)
            data_to_export = [
                entry for entry in st.session_state.mood_data
                if datetime.fromisoformat(entry["timestamp"]) >= cutoff_date
            ]
        
        if not data_to_export:
            return "[]"
        
        # Add additional computed fields for analysis
        enhanced_data = []
        for entry in data_to_export:
            enhanced_entry = entry.copy()
            enhanced_entry['mood_numeric'] = self.get_mood_numeric(entry['mood_level'])
            enhanced_entry['mood_label'] = self.get_mood_label(entry['mood_level'])
            enhanced_data.append(enhanced_entry)
        
        # Sort by timestamp (most recent first)
        enhanced_data.sort(key=lambda x: x['timestamp'], reverse=True)
        
        return json.dumps(enhanced_data, indent=2)
    
    def get_export_summary(self, days=None):
        """Get summary of data being exported"""
        if not st.session_state.mood_data:
            return {"total_entries": 0, "date_range": "No data", "file_size": "0 KB"}
        
        # Filter data if days specified
        data_to_export = st.session_state.mood_data
        if days is not None:
            cutoff_date = datetime.now() - timedelta(days=days)
            data_to_export = [
                entry for entry in st.session_state.mood_data
                if datetime.fromisoformat(entry["timestamp"]) >= cutoff_date
            ]
        
        if not data_to_export:
            return {"total_entries": 0, "date_range": "No data in range", "file_size": "0 KB"}
        
        total_entries = len(data_to_export)
        
        # Get date range
        timestamps = [datetime.fromisoformat(entry["timestamp"]) for entry in data_to_export]
        start_date = min(timestamps).strftime("%Y-%m-%d")
        end_date = max(timestamps).strftime("%Y-%m-%d")
        date_range = f"{start_date} to {end_date}"
        
        # Estimate file size (rough calculation)
        json_size = len(self.export_mood_data_json(days)) / 1024  # KB
        csv_size = len(self.export_mood_data_csv(days)) / 1024    # KB
        
        return {
            "total_entries": total_entries,
            "date_range": date_range,
            "json_size": ".1f",
            "csv_size": ".1f"
        }

def render_mood_dashboard():
    """Render the main mood tracking dashboard"""
    # Add custom CSS for black text
    st.markdown("""
    <style>
    .mood-dashboard-text {
        color: black !important;
    }
    .mood-dashboard-text h1, .mood-dashboard-text h2, .mood-dashboard-text h3, 
    .mood-dashboard-text h4, .mood-dashboard-text h5, .mood-dashboard-text h6 {
        color: black !important;
    }
    .mood-dashboard-text p, .mood-dashboard-text div, .mood-dashboard-text span {
        color: black !important;
    }
    .stMarkdown, .stText, .stInfo, .stSuccess, .stWarning {
        color: black !important;
    }
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, 
    .stMarkdown h4, .stMarkdown h5, .stMarkdown h6 {
        color: black !important;
    }
    .stMarkdown p, .stMarkdown div, .stMarkdown span {
        color: black !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("## 📊 Mood Tracking Insights Dashboard")
    
    # Back to main page button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("⬅️ Back to Main", use_container_width=True):
            st.session_state.show_mood_dashboard = False
            st.rerun()
    
    # Initialize mood tracker
    if "mood_tracker" not in st.session_state:
        st.session_state.mood_tracker = MoodTracker()
    
    tracker = st.session_state.mood_tracker
    
    # Check if there's a new mood entry to save
    if "current_mood_val" in st.session_state and "mood_journal_area" in st.session_state:
        if st.session_state.get("save_mood_entry_clicked", False):
            mood_level = st.session_state.current_mood_val
            notes = st.session_state.get("mood_journal_area", "")
            tracker.add_mood_entry(mood_level, notes)
            st.session_state.save_mood_entry_clicked = False
            st.success("✅ Mood entry saved successfully!")
    
    # Dashboard tabs
    tab1, tab2, tab3 = st.tabs(["📈 Mood History", "📊 Analytics", "💡 Insights"])
    
    with tab1:
        render_mood_history(tracker)
    
    with tab2:
        render_mood_analytics(tracker)
    
    with tab3:
        render_mood_insights(tracker)

def render_mood_history(tracker):
    """Render mood history with charts and filters"""
    st.markdown("### 📈 Mood History View")
    
    # Filter options
    col1, col2, col3 = st.columns(3)
    
    with col1:
        time_period = st.selectbox(
            "Time Period",
            ["Last 7 days", "Last 30 days", "Last 90 days", "All time"],
            index=1
        )
    
    with col2:
        days_map = {"Last 7 days": 7, "Last 30 days": 30, "Last 90 days": 90, "All time": 365}
        days = days_map[time_period]
        df = tracker.get_mood_dataframe(days)
    
    with col3:
        mood_filter = st.selectbox(
            "Filter by Mood",
            ["All moods", "Very Low", "Low", "Okay", "Good", "Great"],
            index=0
        )
    
    if df.empty:
        st.markdown('<div style="color: black;">No mood data available. Start tracking your mood in the sidebar!</div>', unsafe_allow_html=True)
        return
    
    # Apply mood filter
    if mood_filter != "All moods":
        mood_level_map = {"Very Low": "very_low", "Low": "low", "Okay": "okay", "Good": "good", "Great": "great"}
        df = df[df['mood_level'] == mood_level_map[mood_filter]]
    
    if df.empty:
        st.markdown(f'<div style="color: black;">No {mood_filter.lower()} mood entries found for the selected period.</div>', unsafe_allow_html=True)
        return
    
    # Add numeric mood values for charts
    df['mood_numeric'] = df['mood_level'].apply(tracker.get_mood_numeric)
    df['mood_label'] = df['mood_level'].apply(tracker.get_mood_label)
    
    # Line chart for mood over time
    st.markdown("#### 📈 Mood Trend Over Time")
    fig_line = px.line(
        df, 
        x='datetime', 
        y='mood_numeric',
        title="Mood Progression",
        labels={'mood_numeric': 'Mood Level', 'datetime': 'Date'},
        markers=True
    )
    fig_line.update_yaxes(tickvals=[1, 2, 3, 4, 5], 
                         ticktext=['😔 Very Low', '😐 Low', '😊 Okay', '😄 Good', '🌟 Great'],
                         tickfont=dict(color='black'))
    fig_line.update_xaxes(tickfont=dict(color='black'))
    fig_line.update_layout(
        height=400,
        plot_bgcolor='rgba(255, 255, 255, 0.1)',
        paper_bgcolor='rgba(255, 255, 255, 0.05)',
        font=dict(color='black'),
        title=dict(font=dict(size=18, color='black')),
        xaxis=dict(
            gridcolor='rgba(255, 255, 255, 0.1)',
            linecolor='rgba(255, 255, 255, 0.2)',
            showline=True,
            linewidth=1
        ),
        yaxis=dict(
            gridcolor='rgba(255, 255, 255, 0.1)',
            linecolor='rgba(255, 255, 255, 0.2)',
            showline=True,
            linewidth=1
        ),
        margin=dict(l=50, r=50, t=80, b=50)
    )
    
    # Create a box-like container for the chart
    with st.container():
        st.markdown("""
        <div style="
            background: rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 10px;
            padding: 20px;
            margin: 10px 0;
            backdrop-filter: blur(10px);
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        ">
        """, unsafe_allow_html=True)
        st.plotly_chart(fig_line, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Bar chart for mood distribution
    st.markdown("#### 📊 Mood Distribution")
    mood_counts = df['mood_label'].value_counts()
    fig_bar = px.bar(
        x=mood_counts.values,
        y=mood_counts.index,
        orientation='h',
        title="Mood Frequency",
        labels={'x': 'Count', 'y': 'Mood Level'}
    )
    fig_bar.update_xaxes(tickfont=dict(color='black'))
    fig_bar.update_yaxes(tickfont=dict(color='black'))
    fig_bar.update_layout(
        height=300,
        plot_bgcolor='rgba(255, 255, 255, 0.1)',
        paper_bgcolor='rgba(255, 255, 255, 0.05)',
        font=dict(color='black'),
        title=dict(font=dict(size=18, color='black')),
        xaxis=dict(
            gridcolor='rgba(255, 255, 255, 0.1)',
            linecolor='rgba(255, 255, 255, 0.2)',
            showline=True,
            linewidth=1
        ),
        yaxis=dict(
            gridcolor='rgba(255, 255, 255, 0.1)',
            linecolor='rgba(255, 255, 255, 0.2)',
            showline=True,
            linewidth=1
        ),
        margin=dict(l=50, r=50, t=80, b=50)
    )
    
    # Create a box-like container for the chart
    with st.container():
        st.markdown("""
        <div style="
            background: rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 10px;
            padding: 20px;
            margin: 10px 0;
            backdrop-filter: blur(10px);
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        ">
        """, unsafe_allow_html=True)
        st.plotly_chart(fig_bar, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Daily mood summary
    st.markdown("#### 📅 Daily Mood Summary")
    daily_mood = df.groupby('date')['mood_numeric'].mean().reset_index()
    daily_mood['date'] = pd.to_datetime(daily_mood['date'])
    daily_mood['mood_label'] = daily_mood['mood_numeric'].apply(
        lambda x: tracker.get_mood_label({1: "very_low", 2: "low", 3: "okay", 4: "good", 5: "great"}.get(round(x), "okay"))
    )
    
    # Display daily mood in a nice format
    for _, row in daily_mood.iterrows():
        col1, col2, col3 = st.columns([2, 3, 1])
        with col1:
            st.markdown(f'<div style="color: black;"><strong>{row["date"].strftime("%b %d, %Y")}</strong></div>', unsafe_allow_html=True)
        with col2:
            st.markdown(f'<div style="color: black;">{row["mood_label"]}</div>', unsafe_allow_html=True)
        with col3:
            st.markdown(f'<div style="color: black;">({row["mood_numeric"]:.1f}/5)</div>', unsafe_allow_html=True)

    # Enhanced mood entries with context and activities
    st.markdown("#### 📝 Detailed Mood Entries")
    recent_entries = df.tail(10)  # Show last 10 entries
    
    for _, entry in recent_entries.iterrows():
        with st.expander(f"{entry['mood_label']} - {entry['datetime'].strftime('%b %d, %Y at %I:%M %p')}"):
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.markdown(f'<div style="color: black;"><strong>Mood:</strong> {entry["mood_label"]}</div>', unsafe_allow_html=True)
                if 'context_reason' in entry and entry['context_reason'] and entry['context_reason'] != "No specific reason":
                    st.markdown(f'<div style="color: black;"><strong>Reason:</strong> {entry["context_reason"]}</div>', unsafe_allow_html=True)
                if 'notes' in entry and entry['notes']:
                    st.markdown(f'<div style="color: black;"><strong>Notes:</strong> {entry["notes"]}</div>', unsafe_allow_html=True)
            
            with col2:
                if 'activities' in entry and entry['activities']:
                    st.markdown('<div style="color: black;"><strong>Activities:</strong></div>', unsafe_allow_html=True)
                    # Handle both list and other data types
                    activities = entry['activities']
                    if isinstance(activities, list):
                        for activity in activities:
                            st.markdown(f'<div style="color: black;">• {activity}</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div style="color: black;">• {activities}</div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div style="color: black;"><strong>Activities:</strong> None recorded</div>', unsafe_allow_html=True)
    
    # Data Export Section
    st.markdown("---")
    st.markdown("#### 📥 Export Your Mood Data")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        export_format = st.selectbox(
            "Export Format",
            ["CSV", "JSON"],
            help="Choose the format for your exported data"
        )
    
    with col2:
        export_period = st.selectbox(
            "Time Period",
            ["All Data", "Last 7 days", "Last 30 days", "Last 90 days"],
            help="Choose which data to export"
        )
    
    # Export buttons
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        if st.button("📊 Preview Data", use_container_width=True):
            # Show preview of data to be exported
            if export_period == "All Data":
                preview_df = tracker.get_mood_dataframe(365)  # All data
            else:
                days_map = {"Last 7 days": 7, "Last 30 days": 30, "Last 90 days": 90}
                preview_df = tracker.get_mood_dataframe(days_map[export_period])
            
            if not preview_df.empty:
                st.success(f"📊 Ready to export {len(preview_df)} mood entries")
                
                # Show summary
                col_a, col_b, col_c = st.columns(3)
                with col_a:
                    st.metric("Entries", len(preview_df))
                with col_b:
                    date_range = f"{preview_df['date'].min().strftime('%Y-%m-%d')} to {preview_df['date'].max().strftime('%Y-%m-%d')}"
                    st.metric("Date Range", date_range)
                with col_c:
                    avg_mood = preview_df['mood_level'].apply(tracker.get_mood_numeric).mean()
                    st.metric("Avg Mood", f"{avg_mood:.1f}/5")
                
                # Show sample of data
                st.markdown("**Sample Data:**")
                preview_cols = ['date', 'time', 'mood_level', 'notes', 'context_reason']
                st.dataframe(preview_df[preview_cols].head(3), use_container_width=True)
            else:
                st.warning("No data available for the selected period")
    
    with col2:
        export_button_text = f"📥 Export as {export_format}"
        if st.button(export_button_text, use_container_width=True, type="primary"):
            # Get the data to export
            if export_period == "All Data":
                if export_format == "CSV":
                    export_data = tracker.export_mood_data_csv()
                    file_extension = "csv"
                    mime_type = "text/csv"
                else:  # JSON
                    export_data = tracker.export_mood_data_json()
                    file_extension = "json"
                    mime_type = "application/json"
            else:
                days_map = {"Last 7 days": 7, "Last 30 days": 30, "Last 90 days": 90}
                days = days_map[export_period]
                if export_format == "CSV":
                    export_data = tracker.export_mood_data_csv(days)
                    file_extension = "csv"
                    mime_type = "text/csv"
                else:  # JSON
                    export_data = tracker.export_mood_data_json(days)
                    file_extension = "json"
                    mime_type = "application/json"
            
            if export_data:
                # Create filename with timestamp
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"mood_data_{export_period.lower().replace(' ', '_')}_{timestamp}.{file_extension}"
                
                # Create download button
                st.download_button(
                    label=f"⬇️ Download {filename}",
                    data=export_data,
                    file_name=filename,
                    mime=mime_type,
                    use_container_width=True
                )
                
                st.success(f"✅ Ready to download {filename}")
                
                # Show file size estimate
                file_size_kb = len(export_data.encode('utf-8')) / 1024
                st.info(f"📁 File size: {file_size_kb:.1f} KB")
            else:
                st.error("❌ No data available to export")
    
    with col3:
        st.markdown("""
        **💡 Export Tips:**
        - CSV format works well with Excel, Google Sheets
        - JSON format preserves all data structure
        - Use "All Data" for complete backup
        - Exported files include all mood details and activities
        """)

def render_mood_analytics(tracker):
    """Render mood analytics and statistics"""
    st.markdown("### 📊 Mood Analytics")
    
    df = tracker.get_mood_dataframe(30)  # Last 30 days
    
    if df.empty:
        st.info("No mood data available for analytics.")
        return
    
    df['mood_numeric'] = df['mood_level'].apply(tracker.get_mood_numeric)
    
    # Key statistics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        avg_mood = df['mood_numeric'].mean()
        st.metric("Average Mood", f"{avg_mood:.1f}/5", f"{avg_mood:.1f}")
    
    with col2:
        total_entries = len(df)
        st.metric("Total Entries", total_entries)
    
    with col3:
        most_frequent = df['mood_level'].mode().iloc[0] if not df['mood_level'].mode().empty else "N/A"
        st.metric("Most Frequent Mood", tracker.get_mood_label(most_frequent))
    
    with col4:
        mood_range = df['mood_numeric'].max() - df['mood_numeric'].min()
        st.metric("Mood Range", f"{mood_range:.1f}")
    
    st.markdown("---")
    
    # Mood by day of week
    st.markdown("#### 📅 Mood by Day of Week")
    day_mood = df.groupby('day_of_week')['mood_numeric'].mean().reindex([
        'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'
    ]).dropna()
    
    fig_day = px.bar(
        x=day_mood.index,
        y=day_mood.values,
        title="Average Mood by Day of Week",
        labels={'x': 'Day', 'y': 'Average Mood Level'}
    )
    fig_day.update_yaxes(tickvals=[1, 2, 3, 4, 5], 
                        ticktext=['😔 Very Low', '😐 Low', '😊 Okay', '😄 Good', '🌟 Great'],
                        tickfont=dict(color='black'))
    fig_day.update_xaxes(tickfont=dict(color='black'))
    fig_day.update_layout(
        plot_bgcolor='rgba(255, 255, 255, 0.1)',
        paper_bgcolor='rgba(255, 255, 255, 0.05)',
        font=dict(color='black'),
        title=dict(font=dict(size=18, color='black')),
        xaxis=dict(
            gridcolor='rgba(255, 255, 255, 0.1)',
            linecolor='rgba(255, 255, 255, 0.2)',
            showline=True,
            linewidth=1
        ),
        yaxis=dict(
            gridcolor='rgba(255, 255, 255, 0.1)',
            linecolor='rgba(255, 255, 255, 0.2)',
            showline=True,
            linewidth=1
        ),
        margin=dict(l=50, r=50, t=80, b=50)
    )
    
    # Create a box-like container for the chart
    with st.container():
        st.markdown("""
        <div style="
            background: rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 10px;
            padding: 20px;
            margin: 10px 0;
            backdrop-filter: blur(10px);
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        ">
        """, unsafe_allow_html=True)
        st.plotly_chart(fig_day, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Mood heatmap by time
    st.markdown("#### 🕐 Mood by Time of Day")
    df['hour'] = pd.to_datetime(df['time']).dt.hour
    hour_mood = df.groupby('hour')['mood_numeric'].mean()
    
    fig_hour = px.bar(
        x=hour_mood.index,
        y=hour_mood.values,
        title="Average Mood by Hour of Day",
        labels={'x': 'Hour', 'y': 'Average Mood Level'}
    )
    fig_hour.update_yaxes(tickvals=[1, 2, 3, 4, 5],
                         ticktext=['😔 Very Low', '😐 Low', '😊 Okay', '😄 Good', '🌟 Great'],
                         tickfont=dict(color='black'))
    fig_hour.update_xaxes(tickfont=dict(color='black'))
    fig_hour.update_layout(
        plot_bgcolor='rgba(255, 255, 255, 0.1)',
        paper_bgcolor='rgba(255, 255, 255, 0.05)',
        font=dict(color='black'),
        title=dict(font=dict(size=18, color='black')),
        xaxis=dict(
            gridcolor='rgba(255, 255, 255, 0.1)',
            linecolor='rgba(255, 255, 255, 0.2)',
            showline=True,
            linewidth=1
        ),
        yaxis=dict(
            gridcolor='rgba(255, 255, 255, 0.1)',
            linecolor='rgba(255, 255, 255, 0.2)',
            showline=True,
            linewidth=1
        ),
        margin=dict(l=50, r=50, t=80, b=50)
    )
    
    # Create a box-like container for the chart
    with st.container():
        st.markdown("""
        <div style="
            background: rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 10px;
            padding: 20px;
            margin: 10px 0;
            backdrop-filter: blur(10px);
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        ">
        """, unsafe_allow_html=True)
        st.plotly_chart(fig_hour, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # Context and Activity Analytics
    st.markdown("#### 🎯 Context & Activity Analysis")
    
    # Context reason analysis
    if 'context_reason' in df.columns:
        context_counts = df['context_reason'].value_counts()
        if not context_counts.empty:
            st.markdown("**Most Common Reasons for Mood:**")
            for reason, count in context_counts.head(5).items():
                if reason != "No specific reason":
                    percentage = (count / len(df)) * 100
                    st.write(f"• **{reason}**: {count} times ({percentage:.1f}%)")
    
    # Activity analysis
    if 'activities' in df.columns:
        all_activities = []
        for activities_list in df['activities'].dropna():
            if isinstance(activities_list, list):
                all_activities.extend(activities_list)
            elif activities_list:  # Handle non-list activities
                all_activities.append(str(activities_list))
        
        if all_activities:
            activity_counts = pd.Series(all_activities).value_counts()
            st.markdown("**Most Common Activities:**")
            for activity, count in activity_counts.items():
                percentage = (count / len(df)) * 100
                st.write(f"• **{activity}**: {count} times ({percentage:.1f}%)")
    
    # Mood by context
    if 'context_reason' in df.columns:
        st.markdown("#### 📊 Mood by Context")
        context_mood = df.groupby('context_reason')['mood_numeric'].mean().sort_values(ascending=False)
        context_mood = context_mood[context_mood.index != "No specific reason"]
        
        if not context_mood.empty:
            fig_context = px.bar(
                x=context_mood.index,
                y=context_mood.values,
                title="Average Mood by Context",
                labels={'x': 'Context', 'y': 'Average Mood Level'}
            )
            fig_context.update_yaxes(tickvals=[1, 2, 3, 4, 5],
                                   ticktext=['😔 Very Low', '😐 Low', '😊 Okay', '😄 Good', '🌟 Great'],
                                   tickfont=dict(color='black'))
            fig_context.update_xaxes(tickfont=dict(color='black'))
            fig_context.update_layout(
                plot_bgcolor='rgba(255, 255, 255, 0.1)',
                paper_bgcolor='rgba(255, 255, 255, 0.05)',
                font=dict(color='black'),
                title=dict(font=dict(size=18, color='black')),
                xaxis=dict(
                    gridcolor='rgba(255, 255, 255, 0.1)',
                    linecolor='rgba(255, 255, 255, 0.2)',
                    showline=True,
                    linewidth=1
                ),
                yaxis=dict(
                    gridcolor='rgba(255, 255, 255, 0.1)',
                    linecolor='rgba(255, 255, 255, 0.2)',
                    showline=True,
                    linewidth=1
                ),
                margin=dict(l=50, r=50, t=80, b=50)
            )
            
            # Create a box-like container for the chart
            with st.container():
                st.markdown("""
                <div style="
                    background: rgba(255, 255, 255, 0.1);
                    border: 1px solid rgba(255, 255, 255, 0.2);
                    border-radius: 10px;
                    padding: 20px;
                    margin: 10px 0;
                    backdrop-filter: blur(10px);
                    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                ">
                """, unsafe_allow_html=True)
                st.plotly_chart(fig_context, use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)

def render_mood_insights(tracker):
    """Render mood insights and reflections"""
    st.markdown("### 💡 Mood Insights & Reflections")
    
    df = tracker.get_mood_dataframe(30)  # Last 30 days
    
    if df.empty:
        st.info("No mood data available for insights.")
        return
    
    df['mood_numeric'] = df['mood_level'].apply(tracker.get_mood_numeric)
    
    # Advanced Analytics Integration
    st.markdown("#### 🔍 Advanced Mood Analytics")
    
    # Prepare data for analytics module
    analytics_df = df[['timestamp', 'mood_numeric']].copy()
    analytics_df.columns = ['timestamp', 'mood_score']
    
    # Get insights from analytics module
    analytics_results = analyze_mood_trends(analytics_df)
    
    # Display insights
    if analytics_results['insights']:
        st.markdown("**📊 Key Insights:**")
        for insight in analytics_results['insights']:
            st.info(insight)
    
    # Display recommendations
    if analytics_results['recommendations']:
        st.markdown("**💡 Personalized Recommendations:**")
        for rec in analytics_results['recommendations']:
            st.success(rec)
    
    # Display chart
    if analytics_results['charts']:
        st.markdown("**📈 Mood Trend Analysis:**")
        with st.container():
            st.markdown("""
            <div style="
                background: rgba(255, 255, 255, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 10px;
                padding: 20px;
                margin: 10px 0;
                backdrop-filter: blur(10px);
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            ">
            """, unsafe_allow_html=True)
            st.plotly_chart(analytics_results['charts'][0], use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Predictive Analytics Section
    st.markdown("#### 🔮 Mood Predictions & Alerts")
    
    # Get predictive results
    predictive_results = predict_mood_trends(analytics_df, forecast_days=7, alert_threshold=2.8)
    
    if predictive_results['forecast'] is not None:
        # Display alerts
        if predictive_results['alerts']:
            st.markdown("**🚨 Predictive Alerts:**")
            for alert in predictive_results['alerts']:
                if "High Risk" in alert:
                    st.error(alert)
                else:
                    st.warning(alert)
        else:
            st.success("✅ No significant mood dips predicted in the next 7 days!")
        
        # Display forecast chart
        if predictive_results['charts']:
            st.markdown("**📊 7-Day Mood Forecast:**")
            with st.container():
                st.markdown("""
                <div style="
                    background: rgba(255, 255, 255, 0.1);
                    border: 1px solid rgba(255, 255, 255, 0.2);
                    border-radius: 10px;
                    padding: 20px;
                    margin: 10px 0;
                    backdrop-filter: blur(10px);
                    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                ">
                """, unsafe_allow_html=True)
                st.plotly_chart(predictive_results['charts'][0], use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)
        
        # Model information
        st.markdown(f"**🤖 Model Info:** {predictive_results['model_info']}")
        
        # Forecast summary
        forecast_avg = predictive_results['forecast'].mean()
        historical_avg = predictive_results.get('historical_avg', 3.0)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Historical Avg Mood", f"{historical_avg:.1f}/5")
        with col2:
            st.metric("Predicted Avg Mood", f"{forecast_avg:.1f}/5", 
                     f"{forecast_avg - historical_avg:+.1f}")
        with col3:
            dip_count = len(predictive_results['dips'])
            st.metric("Predicted Dips", dip_count)
            
    else:
        st.info(f"🤔 {predictive_results['model_info']}")
    
    st.markdown("---")
    
    # Most frequent mood
    st.markdown("#### 🎯 Most Frequent Mood")
    mood_counts = df['mood_level'].value_counts()
    most_frequent_mood = mood_counts.index[0]
    most_frequent_count = mood_counts.iloc[0]
    total_entries = len(df)
    percentage = (most_frequent_count / total_entries) * 100
    
    st.info(f"**{tracker.get_mood_label(most_frequent_mood)}** appears most often ({most_frequent_count} times, {percentage:.1f}% of entries)")
    
    # Mood trend detection
    st.markdown("#### 📈 Mood Trend Detection")
    
    if len(df) >= 5:
        recent_5 = df.tail(5)['mood_numeric'].mean()
        previous_5 = df.tail(10).head(5)['mood_numeric'].mean()
        
        if recent_5 > previous_5 + 0.5:
            st.success("🎉 **Your mood has improved over the last 5 days!**")
        elif recent_5 < previous_5 - 0.5:
            st.warning("📉 **Your mood has declined over the last 5 days.**")
        else:
            st.info("📊 **Your mood has been relatively stable over the last 5 days.**")
    
    # Weekly mood patterns
    st.markdown("#### 📅 Weekly Patterns")
    day_mood = df.groupby('day_of_week')['mood_numeric'].mean()
    
    best_day = day_mood.idxmax()
    worst_day = day_mood.idxmin()
    
    st.write(f"**Best mood day:** {best_day} ({day_mood[best_day]:.1f}/5)")
    st.write(f"**Challenging mood day:** {worst_day} ({day_mood[worst_day]:.1f}/5)")
    
    # Contextual insights from notes
    st.markdown("#### 📝 Contextual Insights")
    
    # Filter entries with notes
    entries_with_notes = [entry for entry in st.session_state.mood_data if entry.get('notes', '').strip()]
    
    if entries_with_notes:
        # Analyze notes for patterns
        low_mood_entries = [entry for entry in entries_with_notes 
                           if tracker.get_mood_numeric(entry['mood_level']) <= 2]
        high_mood_entries = [entry for entry in entries_with_notes 
                            if tracker.get_mood_numeric(entry['mood_level']) >= 4]
        
        if low_mood_entries:
            st.markdown("**🔍 Low Mood Patterns:**")
            for entry in low_mood_entries[-3:]:  # Show last 3
                st.write(f"• {entry['date']}: {entry['notes'][:100]}...")
        
        if high_mood_entries:
            st.markdown("**🌟 High Mood Patterns:**")
            for entry in high_mood_entries[-3:]:  # Show last 3
                st.write(f"• {entry['date']}: {entry['notes'][:100]}...")
    else:
        st.info("Add notes to your mood entries to get contextual insights!")
    
    # Context and Activity Insights
    st.markdown("#### 🎯 Context & Activity Insights")
    
    # Context insights
    if 'context_reason' in df.columns:
        context_mood_analysis = df.groupby('context_reason')['mood_numeric'].agg(['mean', 'count']).sort_values('mean', ascending=False)
        context_mood_analysis = context_mood_analysis[context_mood_analysis.index != "No specific reason"]
        
        if not context_mood_analysis.empty:
            best_context = context_mood_analysis.index[0]
            worst_context = context_mood_analysis.index[-1]
            
            st.write(f"**Best mood context:** {best_context} ({context_mood_analysis.loc[best_context, 'mean']:.1f}/5)")
            st.write(f"**Challenging mood context:** {worst_context} ({context_mood_analysis.loc[worst_context, 'mean']:.1f}/5)")
    
    # Advanced Activity-Mood Correlation Analysis
    st.markdown("#### 🏃‍♂️ Activity-Mood Correlation Analysis")
    
    # Get activity correlation results
    activity_results = analyze_activity_mood_correlation(df)
    
    # Display activity insights
    if activity_results['activity_insights']:
        for insight in activity_results['activity_insights']:
            if "Top 3" in insight or "strongest positive impact" in insight:
                st.success(insight)
            else:
                st.info(insight)
    
    # Display activity recommendations
    if activity_results['activity_recommendations']:
        st.markdown("**💡 Activity Recommendations:**")
        for rec in activity_results['activity_recommendations']:
            st.success(rec)
    
    # Display activity correlation chart
    if activity_results['activity_chart'] is not None:
        st.markdown("**📊 Activity-Mood Correlation Chart:**")
        with st.container():
            st.markdown("""
            <div style="
                background: rgba(255, 255, 255, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 10px;
                padding: 20px;
                margin: 10px 0;
                backdrop-filter: blur(10px);
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            ">
            """, unsafe_allow_html=True)
            st.plotly_chart(activity_results['activity_chart'], use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
    
    # Weather-Mood Correlation Analysis
    st.markdown("---")
    render_weather_mood_analysis(df)
    
    # Recommendations
    st.markdown("#### 💭 Personalized Recommendations")
    
    avg_mood = df['mood_numeric'].mean()
    
    if avg_mood <= 2:
        st.warning("""
        **Consider reaching out for support:**
        • Talk to a trusted friend or family member
        • Consider professional counseling
        • Practice self-care activities
        • Use the crisis resources in the sidebar if needed
        """)
    elif avg_mood <= 3:
        st.info("""
        **Focus on building positive habits:**
        • Regular exercise and outdoor time
        • Consistent sleep schedule
        • Mindfulness or meditation
        • Social connections
        """)
    else:
        st.success("""
        **Great work maintaining positive mood!**
        • Continue your current positive habits
        • Share your positivity with others
        • Document what's working well
        • Set new wellness goals
        """)

def render_mood_dashboard_button():
    """Render a button to show/hide the mood dashboard"""
    if "show_mood_dashboard" not in st.session_state:
        st.session_state.show_mood_dashboard = False
    
    if st.button("📊 Mood Dashboard", use_container_width=True, type="secondary"):
        st.session_state.show_mood_dashboard = not st.session_state.show_mood_dashboard
        st.rerun()
    
    return st.session_state.show_mood_dashboard