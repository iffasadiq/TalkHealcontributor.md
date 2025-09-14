import pandas as pd
from components.analytics import analyze_mood_trends

# Create more realistic sample mood data with varied times and patterns
timestamps = []
mood_scores = []

# Simulate 2 weeks of data with varied times
base_date = pd.Timestamp('2023-01-01')
for day in range(14):
    for hour in [9, 12, 18, 21]:  # Morning, noon, evening, night
        timestamps.append(base_date + pd.Timedelta(days=day, hours=hour))
        
        # Create patterns: lower mood on weekends, dips in evening
        day_of_week = (base_date + pd.Timedelta(days=day)).dayofweek
        is_weekend = day_of_week >= 5
        is_evening = hour >= 18
        
        base_mood = 3
        if is_weekend:
            base_mood -= 0.5
        if is_evening:
            base_mood -= 0.3
        
        # Add some randomness
        import random
        mood = max(1, min(5, base_mood + random.uniform(-0.5, 0.5)))
        mood_scores.append(round(mood, 1))

sample_data = pd.DataFrame({
    'timestamp': timestamps,
    'mood_score': mood_scores
})

# Run analytics
results = analyze_mood_trends(sample_data)

print("=== Analytics Results ===")
print("\nInsights:")
for insight in results['insights']:
    print(f"- {insight}")

print("\nRecommendations:")
for rec in results['recommendations']:
    print(f"- {rec}")

print(f"\nCharts generated: {len(results['charts'])}")
print(f"Sample data shape: {sample_data.shape}")
print(f"Mood score range: {sample_data['mood_score'].min()} - {sample_data['mood_score'].max()}")
print(f"Average mood: {sample_data['mood_score'].mean():.2f}")