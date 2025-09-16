import json
import os
from datetime import datetime, timedelta
import random

# Create data directory if it doesn't exist
os.makedirs("data", exist_ok=True)

# Generate sample mood data for the last 30 days
mood_data = []
base_date = datetime.now() - timedelta(days=30)

mood_levels = ["very_low", "low", "okay", "good", "great"]
context_reasons = ["Work", "Family", "Health", "Relationships", "Personal goals", "No specific reason"]
activities_options = ["Exercise", "Socialized", "Ate healthy", "Slept well"]

for i in range(30):
    current_date = base_date + timedelta(days=i)

    # Create 1-3 entries per day with some randomness
    entries_per_day = random.randint(1, 3)

    for j in range(entries_per_day):
        # Add some time variation
        hour = random.randint(8, 22)
        minute = random.randint(0, 59)
        entry_time = current_date.replace(hour=hour, minute=minute)

        # Slightly biased towards positive moods
        mood_weights = [0.1, 0.2, 0.4, 0.2, 0.1]  # very_low, low, okay, good, great
        mood_level = random.choices(mood_levels, weights=mood_weights)[0]

        # Generate some sample notes based on mood
        notes_templates = {
            "very_low": ["Feeling overwhelmed today", "Had a tough day at work", "Not feeling my best"],
            "low": ["A bit down today", "Could be better", "Feeling a little off"],
            "okay": ["Just an average day", "Feeling neutral", "Nothing special today"],
            "good": ["Had a productive day", "Feeling positive", "Things went well"],
            "great": ["Amazing day!", "Feeling fantastic", "Everything is going great"]
        }

        note = random.choice(notes_templates[mood_level])

        # Random context and activities
        context_reason = random.choice(context_reasons)
        activities = random.sample(activities_options, random.randint(0, 3))

        entry = {
            "timestamp": entry_time.isoformat(),
            "mood_level": mood_level,
            "notes": note,
            "context_reason": context_reason,
            "activities": activities,
            "date": entry_time.strftime("%Y-%m-%d"),
            "time": entry_time.strftime("%H:%M"),
            "day_of_week": entry_time.strftime("%A")
        }

        mood_data.append(entry)

# Save to JSON file
with open("data/mood_data.json", "w") as f:
    json.dump(mood_data, f, indent=2)

print(f"✅ Generated {len(mood_data)} sample mood entries")
print("📁 Saved to data/mood_data.json")
print("\n📊 Sample entries created:")
for i, entry in enumerate(mood_data[:5]):
    print(f"  {i+1}. {entry['date']} - {entry['mood_level']} - {entry['notes'][:30]}...")