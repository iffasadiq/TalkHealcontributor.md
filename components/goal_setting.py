# FileName:goal_setting.py
# FileContents:
import streamlit as st
from datetime import datetime, timedelta
import json
import os
import google.generativeai as genai
from google.generativeai import types as genai_types
#from google.generativeai.types import GenerationError
from core import config # Assuming config.py is in the core directory and has the configure function
def generate_1_week_plan(user_goal):
    """
    Uses the Gemini API to generate a 1-week daily plan based on user goal.
    """
    model = config.configure_gemini()
    if model is None:
        st.error("Gemini API is not configured. Cannot generate plan.")
        return ["Could not generate a plan. Please check API configuration."]

    system_prompt = """
    You are an AI assistant specialized in mental health and wellness goal setting.
    Your task is to create a personalized 1-week daily plan (7 days) for a user based on their mental health goal.
    Each day should have a specific, actionable step related to the goal.
    The plan should be encouraging, realistic, and focus on small, manageable steps.
    Provide only the plan as a list of daily actions, without any introductory or concluding remarks.
    Each item in the list should start with the day of the week, followed by a colon and the action.
    Example format:
    Monday: Practice 10 minutes of deep breathing.
    Tuesday: Take a 20-minute walk outdoors.
    Wednesday: Write down 3 things you are grateful for.
    ...
    """

    try:
        response = model.generate_content([
            {"role": "system", "parts": [system_prompt]},
            {"role": "user", "parts": [f"Generate a 1-week plan for the goal: '{user_goal}'"]}
        ])
        
        # Assuming the response text is a string with each day's plan on a new line
        plan_text = response.text.strip()
        if plan_text:
            # Split the response into individual plan steps
            generated_plan = [step.strip() for step in plan_text.split('\n') if step.strip()]
            return generated_plan
        else:
            return ["Could not generate a plan. The AI returned an empty response."]

    except ValueError as e:
        st.error(f"Invalid input or model configuration issue: {e}")
        return ["Could not generate a plan due to an internal error."]
    except genai_types.BlockedPromptException:
        st.error("Content policy violation. Please rephrase your goal.")
        return ["Could not generate a plan due to content policy. Please try a different goal."]
    #except GenerationError as e: # Add this specific exception handler
       # st.error(f"Failed to generate response from AI: {e}")
       # return ["Could not generate a plan. Please try again later."]
    except Exception as e:
        st.error(f"An unexpected error occurred with the AI: {e}")
        return ["An unexpected error occurred while generating the plan."]
class GoalTracker:
    def __init__(self):
        self.data_file = "data/goals_data.json"
        self.ensure_data_directory()
        self.load_goals_data()
    
    def ensure_data_directory(self):
        os.makedirs("data", exist_ok=True)
    
    def load_goals_data(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    st.session_state.goals_data = json.load(f)
            except json.JSONDecodeError:
                st.session_state.goals_data = []
        else:
            st.session_state.goals_data = []
    
    def save_goals_data(self):
        with open(self.data_file, 'w') as f:
            json.dump(st.session_state.goals_data, f, indent=2)
            
    def add_goal(self, goal_statement, plan):
        start_date = datetime.now()
        end_date = start_date + timedelta(weeks=1)
        new_goal = {
            "id": str(datetime.now().timestamp()),
            "goal_statement": goal_statement,
            "plan": plan,
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
            "progress": ["pending"] * len(plan),
            "status": "active",
            "created_at": datetime.now().isoformat()
        }
        st.session_state.goals_data.append(new_goal)
        self.save_goals_data()
        return new_goal

    def update_progress(self, goal_id, step_index, status):
        for goal in st.session_state.goals_data:
            if goal["id"] == goal_id:
                if 0 <= step_index < len(goal["progress"]):
                    goal["progress"][step_index] = status
                    if all(s == "completed" for s in goal["progress"]):
                        goal["status"] = "completed"
                    elif any(s == "completed" for s in goal["progress"]):
                        goal["status"] = "active"
                    self.save_goals_data()
                    return True
        return False

    def update_goal_status(self, goal_id, status):
        for goal in st.session_state.goals_data:
            if goal["id"] == goal_id:
                goal["status"] = status
                self.save_goals_data()
                return True
        return False

def render_goal():
    st.markdown("## 🎯AI Based Mental Health Planner")
    st.markdown("Enter your mental health goal below, and get a personalized 1-week plan.")

    if "goal_tracker" not in st.session_state:
        st.session_state.goal_tracker = GoalTracker()

    tracker = st.session_state.goal_tracker

    if "goal_input_cleared" not in st.session_state:
        st.session_state.goal_input_cleared = False

    if st.button("← Back to Chat", type="primary"):
        st.session_state.show_goal_setting = False
        st.session_state.goal_input_cleared = False
        st.experimental_rerun()

    st.markdown("---")

    goal_input_value = "" if st.session_state.goal_input_cleared else st.session_state.get("new_goal_input", "")

    goal_statement = st.text_input(
        "Your mental health goal (e.g., 'reduce stress', 'make me happy', 'improve mental health','mental health exercise'):",
        value=goal_input_value,
        key="new_goal_input"
    )

    if st.button("Generate 1-Week Plan", type="secondary"):
        if goal_statement.strip():
            with st.spinner("Generating your personalized 1-week plan..."):
                plan = generate_1_week_plan(goal_statement)
                if plan and "Could not generate a plan" not in plan[0]: # Check if plan generation was successful
                    tracker.add_goal(goal_statement, plan)
                    st.success("✅ Your 1-week plan has been generated and added!")
                    st.session_state.goal_input_cleared = True
                    st.experimental_rerun()
                else:
                    st.error("Failed to generate a plan. Please try again or rephrase your goal.")
        else:
            st.warning("Please enter your goal.")

    st.markdown("---")

    # Show active goals with progress tracking (similar to previous example)
    st.subheader("🚀 Your Active Goals")
    active_goals = [g for g in st.session_state.goals_data if g["status"] == "active"]

    if not active_goals:
        st.info("No active goals yet. Create one above!")
    else:
        for goal in active_goals:
            current_date = datetime.now()
            start_dt = datetime.fromisoformat(goal["start_date"])
            end_dt = datetime.fromisoformat(goal["end_date"])
            days_left = (end_dt - current_date).days
            progress_percentage = (goal["progress"].count("completed") / len(goal["plan"])) * 100 if goal["plan"] else 0

            with st.expander(f"🎯 **{goal['goal_statement']}** (Ends: {end_dt.strftime('%b %d')}, {days_left} days left)", expanded=True):
                st.progress(progress_percentage / 100, text=f"Progress: {progress_percentage:.0f}%")
                st.markdown(f"**Plan Start Date:** {start_dt.strftime('%B %d, %Y')}")
                st.markdown(f"**Plan End Date:** {end_dt.strftime('%B %d, %Y')}")
                
                st.markdown("#### Your 1-Week Step-by-Step Plan:")
                for step_idx, step in enumerate(goal["plan"]):
                    col1, col2 = st.columns([0.8, 0.2])
                    with col1:
                        st.markdown(f"- {step}")
                    with col2:
                        current_status = goal["progress"][step_idx]
                        new_status = st.selectbox(
                            "Status",
                            ["pending", "completed", "skipped"],
                            index=["pending", "completed", "skipped"].index(current_status),
                            key=f"progress_select_{goal['id']}_{step_idx}",
                            label_visibility="collapsed"
                        )
                        if new_status != current_status:
                            tracker.update_progress(goal["id"], step_idx, new_status)
                            st.experimental_rerun()
                
                st.markdown("---")
                col_actions = st.columns(3)
                with col_actions[0]:
                    if st.button("Mark as Completed", key=f"complete_goal_{goal['id']}", type="success"):
                        tracker.update_goal_status(goal["id"], "completed")
                        st.success(f"Goal '{goal['goal_statement']}' marked as completed!")
                        st.experimental_rerun()
                with col_actions[1]:
                    if st.button("Abandon Goal", key=f"abandon_goal_{goal['id']}", type="warning"):
                        tracker.update_goal_status(goal["id"], "abandoned")
                        st.warning(f"Goal '{goal['goal_statement']}' marked as abandoned.")
                        st.experimental_rerun()
                with col_actions[2]:
                    if st.button("Delete Goal", key=f"delete_goal_{goal['id']}", type="danger"):
                        st.session_state.goals_data = [g for g in st.session_state.goals_data if g["id"] != goal["id"]]
                        tracker.save_goals_data()
                        st.error(f"Goal '{goal['goal_statement']}' deleted.")
                        st.experimental_rerun()

    st.markdown("---")

    # Completed & Abandoned Goals
    st.subheader("Archive: Completed & Abandoned Goals")
    completed_abandoned_goals = [g for g in st.session_state.goals_data if g["status"] in ["completed", "abandoned"]]

    if not completed_abandoned_goals:
        st.info("No completed or abandoned goals yet.")
    else:
        for goal in completed_abandoned_goals:
            status_emoji = "✅" if goal["status"] == "completed" else "❌"
            with st.expander(f"{status_emoji} **{goal['goal_statement']}** ({goal['status'].capitalize()})"):
                st.markdown(f"**Created On:** {datetime.fromisoformat(goal['created_at']).strftime('%B %d, %Y')}")
                st.markdown(f"**Status:** {goal['status'].capitalize()}")
                st.markdown("#### Original Plan:")
                for step in goal["plan"]:
                    st.markdown(f"- {step}")
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Reactivate Goal", key=f"reactivate_goal_{goal['id']}", type="secondary"):
                        tracker.update_goal_status(goal["id"], "active")
                        st.info(f"Goal '{goal['goal_statement']}' reactivated.")
                        st.experimental_rerun()
                with col2:
                    if st.button("Delete Goal", key=f"delete_archived_goal_{goal['id']}", type="danger"):
                        st.session_state.goals_data = [g for g in st.session_state.goals_data if g["id"] != goal["id"]]
                        tracker.save_goals_data()
                        st.error(f"Goal '{goal['goal_statement']}' deleted.")
                        st.experimental_rerun()
