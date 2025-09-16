import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional, Any
import warnings
warnings.filterwarnings('ignore')

# ARIMA and auto ARIMA
try:
    from statsmodels.tsa.arima.model import ARIMA
    from statsmodels.tsa.stattools import adfuller
    ARIMA_AVAILABLE = True
except ImportError:
    ARIMA_AVAILABLE = False

# Facebook Prophet
try:
    from prophet import Prophet
    PROPHET_AVAILABLE = True
except ImportError:
    PROPHET_AVAILABLE = False

# Plotly for visualizations
import plotly.graph_objs as go

def check_stationarity(timeseries: pd.Series) -> bool:
    """Check if time series is stationary using Augmented Dickey-Fuller test"""
    try:
        result = adfuller(timeseries.dropna())
        return result[1] < 0.05  # p-value < 0.05 means stationary
    except:
        return False

def prepare_time_series_data(mood_log: pd.DataFrame, freq: str = 'D') -> pd.DataFrame:
    """Prepare mood data for time series forecasting"""
    if mood_log.empty:
        return pd.DataFrame()

    df = mood_log.copy()
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df = df.set_index('timestamp').sort_index()

    # Resample to daily frequency and take mean mood for each day
    daily_mood = df.resample(freq)['mood_score'].mean().dropna()

    # Require minimum data points for forecasting
    if len(daily_mood) < 7:
        return pd.DataFrame()

    return daily_mood

def forecast_arima(mood_series: pd.Series, forecast_days: int = 7) -> Dict[str, Any]:
    """Forecast mood using ARIMA model"""
    if not ARIMA_AVAILABLE:
        return {}
        
    try:
        # Use simple ARIMA(1,1,1) model
        model_fit = ARIMA(mood_series, order=(1, 1, 1)).fit()
        order = (1, 1, 1)
        seasonal_order = (0, 0, 0, 0)

        # Make predictions
        forecast = model_fit.predict(start=len(mood_series), end=len(mood_series)+forecast_days-1)

        # Get confidence intervals if possible
        try:
            pred_conf = model_fit.get_forecast(steps=forecast_days).conf_int()
            conf_int = pred_conf.values
        except:
            conf_int = None

        # Create forecast index
        last_date = mood_series.index[-1]
        forecast_index = pd.date_range(start=last_date + pd.Timedelta(days=1),
                                     periods=forecast_days, freq='D')

        return {
            'forecast': pd.Series(forecast, index=forecast_index),
            'confidence_intervals': conf_int,
            'model_type': 'ARIMA',
            'order': order,
            'seasonal_order': seasonal_order
        }

    except Exception as e:
        print(f"ARIMA forecasting failed: {e}")
        return {}

def forecast_prophet(mood_series: pd.Series, forecast_days: int = 7) -> Dict[str, Any]:
    """Forecast mood using Facebook Prophet"""
    if not PROPHET_AVAILABLE:
        return {}
        
    try:
        # Prepare data for Prophet
        prophet_df = pd.DataFrame({
            'ds': mood_series.index,
            'y': mood_series.values
        })

        # Create and fit model
        model = Prophet(
            daily_seasonality=True,
            weekly_seasonality=True,
            yearly_seasonality=False,
            changepoint_prior_scale=0.05
        )

        model.fit(prophet_df)

        # Make future dataframe
        future = model.make_future_dataframe(periods=forecast_days, freq='D')

        # Forecast
        forecast = model.predict(future)

        # Extract predictions for future dates only
        future_predictions = forecast[forecast['ds'] > mood_series.index[-1]]

        return {
            'forecast': pd.Series(future_predictions['yhat'].values,
                                index=future_predictions['ds']),
            'confidence_intervals': future_predictions[['yhat_lower', 'yhat_upper']].values,
            'model_type': 'Prophet',
            'model': model
        }

    except Exception as e:
        print(f"Prophet forecasting failed: {e}")
        return {}

def detect_mood_dips(forecast: pd.Series, confidence_intervals: Optional[np.ndarray] = None,
                    threshold: float = 2.5) -> List[Dict[str, Any]]:
    """Detect potential mood dips from forecast"""
    dips = []

    for date, predicted_mood in forecast.items():
        # Check if predicted mood is below threshold
        if predicted_mood < threshold:
            dip_info = {
                'date': date,
                'predicted_mood': predicted_mood,
                'severity': 'severe' if predicted_mood < 2.0 else 'moderate',
                'confidence': None
            }

            # Add confidence information if available
            if confidence_intervals is not None:
                try:
                    idx = forecast.index.get_loc(date)
                    if idx < len(confidence_intervals):
                        lower_bound = confidence_intervals[idx][0] if isinstance(confidence_intervals[idx], (list, np.ndarray)) else confidence_intervals[idx]
                        upper_bound = confidence_intervals[idx][1] if isinstance(confidence_intervals[idx], (list, np.ndarray)) else confidence_intervals[idx]
                        dip_info['confidence'] = {
                            'lower': lower_bound,
                            'upper': upper_bound
                        }
                except:
                    pass

            dips.append(dip_info)

    return dips

def generate_predictive_alerts(dips: List[Dict[str, Any]], historical_avg: float) -> List[str]:
    """Generate personalized alerts based on predicted mood dips"""
    alerts = []

    for dip in dips:
        date_str = dip['date'].strftime('%A, %B %d')
        mood_level = dip['predicted_mood']

        if dip['severity'] == 'severe':
            alerts.append(f"🚨 **High Risk Alert**: Your mood may drop significantly on {date_str} "
                         f"(predicted: {mood_level:.1f}/5). Consider reaching out for support.")
        else:
            alerts.append(f"⚠️ **Mood Dip Alert**: Your mood may be lower on {date_str} "
                         f"(predicted: {mood_level:.1f}/5). Try a Focus Session or Breathing Exercise.")

        # Add confidence information if available
        if dip.get('confidence'):
            confidence_range = f"{dip['confidence']['lower']:.1f} - {dip['confidence']['upper']:.1f}"
            alerts.append(f"   *Confidence range: {confidence_range}*")

    return alerts

def create_forecast_chart(historical_data: pd.Series, forecast: pd.Series,
                         confidence_intervals: Optional[np.ndarray] = None,
                         dips: List[Dict[str, Any]] = None) -> go.Figure:
    """Create interactive forecast visualization"""
    fig = go.Figure()

    # Historical data
    fig.add_trace(go.Scatter(
        x=historical_data.index,
        y=historical_data.values,
        mode='lines+markers',
        name='Historical Mood',
        line=dict(color='blue', width=2)
    ))

    # Forecast
    fig.add_trace(go.Scatter(
        x=forecast.index,
        y=forecast.values,
        mode='lines+markers',
        name='Forecast',
        line=dict(color='red', width=2, dash='dash')
    ))

    # Confidence intervals
    if confidence_intervals is not None:
        try:
            lower_bounds = []
            upper_bounds = []

            for i, ci in enumerate(confidence_intervals):
                if isinstance(ci, (list, np.ndarray)) and len(ci) >= 2:
                    lower_bounds.append(ci[0])
                    upper_bounds.append(ci[1])
                else:
                    lower_bounds.append(forecast.iloc[i] - 0.5)
                    upper_bounds.append(forecast.iloc[i] + 0.5)

            fig.add_trace(go.Scatter(
                x=forecast.index.tolist() + forecast.index.tolist()[::-1],
                y=upper_bounds + lower_bounds[::-1],
                fill='toself',
                fillcolor='rgba(255, 0, 0, 0.2)',
                line=dict(color='rgba(255, 255, 255, 0)'),
                name='Confidence Interval'
            ))
        except:
            pass

    # Mood dip markers
    if dips:
        dip_dates = [d['date'] for d in dips]
        dip_moods = [d['predicted_mood'] for d in dips]

        colors = ['red' if d['severity'] == 'severe' else 'orange' for d in dips]

        fig.add_trace(go.Scatter(
            x=dip_dates,
            y=dip_moods,
            mode='markers',
            name='Predicted Dips',
            marker=dict(size=12, color=colors, symbol='triangle-down')
        ))

    # Update layout
    fig.update_layout(
        title='Mood Forecast with Predicted Dips',
        xaxis_title='Date',
        yaxis_title='Mood Score',
        yaxis=dict(range=[0.5, 5.5], tickvals=[1, 2, 3, 4, 5],
                  ticktext=['😔 Very Low', '😐 Low', '😊 Okay', '😄 Good', '🌟 Great']),
        showlegend=True
    )

    return fig

def predict_mood_trends(mood_log: pd.DataFrame, forecast_days: int = 7,
                       alert_threshold: float = 2.5) -> Dict[str, Any]:
    """
    Main function to predict mood trends and generate alerts
    """
    if mood_log.empty:
        return {
            'forecast': None,
            'alerts': [],
            'dips': [],
            'charts': [],
            'model_info': 'Insufficient data for forecasting'
        }

    # Prepare data
    mood_series = prepare_time_series_data(mood_log)
    if mood_series.empty:
        return {
            'forecast': None,
            'alerts': [],
            'dips': [],
            'charts': [],
            'model_info': 'Need at least 7 days of mood data for forecasting'
        }

    historical_avg = mood_series.mean()

    # Try ARIMA first, fallback to Prophet
    forecast_result = forecast_arima(mood_series, forecast_days)

    if not forecast_result:
        forecast_result = forecast_prophet(mood_series, forecast_days)

    if not forecast_result:
        return {
            'forecast': None,
            'alerts': [],
            'dips': [],
            'charts': [],
            'model_info': 'Forecasting models failed to fit the data'
        }

    forecast = forecast_result['forecast']
    confidence_intervals = forecast_result.get('confidence_intervals')

    # Detect mood dips
    dips = detect_mood_dips(forecast, confidence_intervals, alert_threshold)

    # Generate alerts
    alerts = generate_predictive_alerts(dips, historical_avg)

    # Create visualization
    chart = create_forecast_chart(mood_series, forecast, confidence_intervals, dips)

    return {
        'forecast': forecast,
        'alerts': alerts,
        'dips': dips,
        'charts': [chart],
        'model_info': f"Using {forecast_result['model_type']} model",
        'historical_avg': historical_avg
    }