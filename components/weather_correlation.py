import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional, Any
import streamlit as st
from datetime import datetime, timedelta
import plotly.graph_objs as go
import plotly.express as px

# Weather data libraries
try:
    from meteostat import Point, Daily
    import timezonefinder
    WEATHER_AVAILABLE = True
except ImportError:
    WEATHER_AVAILABLE = False

def get_weather_data(latitude: float, longitude: float, start_date: datetime, end_date: datetime) -> Optional[pd.DataFrame]:
    """
    Fetch historical weather data for a location and date range
    """
    if not WEATHER_AVAILABLE:
        return None

    try:
        # Create Point for location
        location = Point(latitude, longitude)

        # Get daily weather data
        data = Daily(location, start_date, end_date)
        weather_df = data.fetch()

        if weather_df.empty:
            return None

        # Reset index to have date as column
        weather_df = weather_df.reset_index()

        # Rename columns for clarity
        weather_df = weather_df.rename(columns={
            'tavg': 'temp_avg',
            'tmin': 'temp_min',
            'tmax': 'temp_max',
            'prcp': 'precipitation',
            'wspd': 'wind_speed',
            'pres': 'pressure'
        })

        # Convert temperature from Celsius to Fahrenheit if needed
        # weather_df['temp_avg_f'] = weather_df['temp_avg'] * 9/5 + 32
        # weather_df['temp_min_f'] = weather_df['temp_min'] * 9/5 + 32
        # weather_df['temp_max_f'] = weather_df['temp_max'] * 9/5 + 32

        return weather_df

    except Exception as e:
        print(f"Error fetching weather data: {e}")
        return None

def get_user_location() -> Optional[Tuple[float, float]]:
    """
    Get user's approximate location using IP geolocation
    """
    try:
        import requests

        # Using ipapi.co for free geolocation (no API key required)
        response = requests.get('https://ipapi.co/json/', timeout=5)
        if response.status_code == 200:
            data = response.json()
            lat = data.get('latitude')
            lon = data.get('longitude')
            if lat and lon:
                return float(lat), float(lon)
    except Exception as e:
        print(f"Error getting location: {e}")

    # Fallback to a default location (e.g., New York City)
    return 40.7128, -74.0060

def analyze_weather_mood_correlation(mood_data: pd.DataFrame, weather_data: pd.DataFrame) -> Dict[str, Any]:
    """
    Analyze correlation between weather conditions and mood
    """
    if mood_data.empty or weather_data is None or weather_data.empty:
        return {"correlations": {}, "insights": [], "charts": []}

    try:
        # Prepare mood data
        mood_df = mood_data.copy()
        mood_df['timestamp'] = pd.to_datetime(mood_df['timestamp'])
        mood_df['date'] = mood_df['timestamp'].dt.date
        mood_df['mood_numeric'] = mood_df['mood_level'].map({
            'very_low': 1, 'low': 2, 'okay': 3, 'good': 4, 'great': 5
        })

        # Aggregate mood by date
        daily_mood = mood_df.groupby('date')['mood_numeric'].mean().reset_index()
        daily_mood['date'] = pd.to_datetime(daily_mood['date'])

        # Prepare weather data
        weather_df = weather_data.copy()
        weather_df['time'] = pd.to_datetime(weather_df['time'])
        weather_df['date'] = weather_df['time'].dt.date
        weather_df['date'] = pd.to_datetime(weather_df['date'])

        # Merge mood and weather data
        merged_df = pd.merge(daily_mood, weather_df, on='date', how='inner')

        if merged_df.empty:
            return {"correlations": {}, "insights": [], "charts": []}

        # Calculate correlations
        correlations = {}
        weather_vars = ['temp_avg', 'temp_min', 'temp_max', 'precipitation', 'wind_speed']

        for var in weather_vars:
            if var in merged_df.columns:
                corr = merged_df['mood_numeric'].corr(merged_df[var])
                if not pd.isna(corr):
                    correlations[var] = corr

        # Generate insights
        insights = []

        # Temperature insights
        if 'temp_avg' in correlations:
            temp_corr = correlations['temp_avg']
            if abs(temp_corr) > 0.3:
                direction = "better" if temp_corr > 0 else "worse"
                temp_range = f"{merged_df['temp_avg'].min():.1f}°C - {merged_df['temp_avg'].max():.1f}°C"
                insights.append(f"Your mood tends to be {direction} when temperatures are between {temp_range}")

        # Precipitation insights
        if 'precipitation' in correlations:
            rain_corr = correlations['precipitation']
            if abs(rain_corr) > 0.2:
                direction = "better" if rain_corr > 0 else "worse"
                rainy_days = (merged_df['precipitation'] > 0).sum()
                total_days = len(merged_df)
                rain_percentage = (rainy_days / total_days) * 100
                insights.append(f"You feel {direction} on rainy days ({rain_percentage:.1f}% of tracked days had rain)")

        # Wind insights
        if 'wind_speed' in correlations:
            wind_corr = correlations['wind_speed']
            if abs(wind_corr) > 0.2:
                direction = "better" if wind_corr > 0 else "worse"
                avg_wind = merged_df['wind_speed'].mean()
                insights.append(f"Windy conditions tend to make you feel {direction} (avg wind speed: {avg_wind:.1f} km/h)")

        # Create correlation chart
        corr_data = []
        corr_labels = []

        for var, corr in correlations.items():
            if abs(corr) > 0.1:  # Only show meaningful correlations
                corr_data.append(abs(corr))
                label_map = {
                    'temp_avg': 'Average Temperature',
                    'temp_min': 'Min Temperature',
                    'temp_max': 'Max Temperature',
                    'precipitation': 'Precipitation',
                    'wind_speed': 'Wind Speed'
                }
                corr_labels.append(label_map.get(var, var))

        correlation_chart = None
        if corr_data:
            correlation_chart = go.Figure(data=[
                go.Bar(
                    x=corr_labels,
                    y=corr_data,
                    marker_color=['red' if c > 0.3 else 'orange' if c > 0.2 else 'blue' for c in corr_data]
                )
            ])
            correlation_chart.update_layout(
                title="Weather-Mood Correlation Strength",
                xaxis_title="Weather Factor",
                yaxis_title="Correlation Strength",
                yaxis_range=[0, 1]
            )

        # Create scatter plot for temperature vs mood
        temp_mood_chart = None
        if 'temp_avg' in merged_df.columns and len(merged_df) > 5:
            temp_mood_chart = px.scatter(
                merged_df,
                x='temp_avg',
                y='mood_numeric',
                trendline="ols",
                title="Temperature vs Mood Correlation",
                labels={
                    'temp_avg': 'Average Temperature (°C)',
                    'mood_numeric': 'Mood Level (1-5)'
                }
            )
            temp_mood_chart.update_yaxes(tickvals=[1, 2, 3, 4, 5],
                                        ticktext=['😔 Very Low', '😐 Low', '😊 Okay', '😄 Good', '🌟 Great'])

        return {
            "correlations": correlations,
            "insights": insights,
            "charts": [chart for chart in [correlation_chart, temp_mood_chart] if chart is not None],
            "data_points": len(merged_df)
        }

    except Exception as e:
        print(f"Error in weather-mood correlation analysis: {e}")
        return {"correlations": {}, "insights": [], "charts": []}

def render_weather_mood_analysis(mood_data: pd.DataFrame):
    """
    Render the weather-mood correlation analysis in the dashboard
    """
    st.markdown("### 🌤️ Weather-Mood Correlation Analysis")

    if not WEATHER_AVAILABLE:
        st.warning("Weather analysis requires additional packages. Install meteostat and timezonefinder to enable this feature.")
        return

    # Get user's location
    with st.spinner("Fetching your location..."):
        user_location = get_user_location()

    if not user_location:
        st.error("Unable to determine your location for weather analysis.")
        return

    lat, lon = user_location
    st.info(f"📍 Analyzing weather patterns for your approximate location (Lat: {lat:.2f}, Lon: {lon:.2f})")

    # Date range for analysis
    end_date = datetime.now()
    start_date = end_date - timedelta(days=90)  # Last 90 days

    # Fetch weather data
    with st.spinner("Fetching weather data..."):
        weather_data = get_weather_data(lat, lon, start_date, end_date)

    if weather_data is None or weather_data.empty:
        st.error("Unable to fetch weather data for your location. This could be due to network issues or location restrictions.")
        return

    # Analyze correlation
    with st.spinner("Analyzing weather-mood patterns..."):
        analysis_results = analyze_weather_mood_correlation(mood_data, weather_data)

    if not analysis_results["correlations"]:
        st.info("Not enough overlapping mood and weather data for correlation analysis. Try tracking your mood for a longer period.")
        return

    # Display insights
    if analysis_results["insights"]:
        st.markdown("**🔍 Key Weather-Mood Insights:**")
        for insight in analysis_results["insights"]:
            st.info(f"• {insight}")
    else:
        st.info("No significant weather-mood correlations found in your data.")

    # Display correlation chart
    if analysis_results["charts"]:
        st.markdown("**📊 Weather-Mood Correlations:**")
        for i, chart in enumerate(analysis_results["charts"]):
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
                st.plotly_chart(chart, use_container_width=True)
                st.markdown("</div>")

    # Display raw correlations
    if analysis_results["correlations"]:
        st.markdown("**📈 Detailed Correlations:**")
        corr_df = pd.DataFrame.from_dict(
            analysis_results["correlations"],
            orient='index',
            columns=['Correlation']
        )
        corr_df['Strength'] = corr_df['Correlation'].apply(
            lambda x: 'Strong' if abs(x) > 0.5 else 'Moderate' if abs(x) > 0.3 else 'Weak'
        )
        st.dataframe(corr_df.style.format({'Correlation': '{:.3f}'}))

    # Data summary
    st.markdown(f"**📊 Analysis Summary:** {analysis_results.get('data_points', 0)} days of overlapping mood and weather data analyzed")