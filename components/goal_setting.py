import streamlit as st
import json
import os
from datetime import datetime
from core.utils import get_ai_response

class GoalPlanner:
    def __init__(self):
        self.goals_file = "data/user_goals.json"
        self.ensure_data_directory()
        self.load_goals()
    
    def ensure_data_directory(self):
        os.makedirs("data", exist_ok=True)
    
    def load_goals(self):
        if os.path.exists(self.goals_file):
            try:
                with open(self.goals_file, 'r') as f:
                    st.session_state.user_goals = json.load(f)
            except:
                st.session_state.user_goals = []
        else:
            st.session_state.user_goals = []
    
    def save_goals(self):
        with open(self.goals_file, 'w') as f:
            json.dump(st.session_state.user_goals, f, indent=2)
    
    def create_goal(self, prompt, plan_content, goal_type="ai_generated"):
        goal = {
            "id": len(st.session_state.user_goals) + 1,
            "prompt": prompt,
            "goal_type": goal_type, # New field to distinguish AI vs. Manual
            "created_date": datetime.now().isoformat(),
            "completed": False,
            "progress": 0,
            "milestones": [] # Milestones might be used for AI, or adapted for manual
        }
        
        if goal_type == "ai_generated":
            goal["plan"] = plan_content # AI-generated plan is a single string
        elif goal_type == "manual_weekly":
            goal["weekly_tasks"] = plan_content # Manual plan is a dictionary of tasks
        
        st.session_state.user_goals.append(goal)
        self.save_goals()
    
    def delete_goal(self, goal_id):
        st.session_state.user_goals = [g for g in st.session_state.user_goals if g["id"] != goal_id]
        self.save_goals()
    
    def update_progress(self, goal_id, progress):
        for goal in st.session_state.user_goals:
            if goal["id"] == goal_id:
                goal["progress"] = progress
                if progress >= 100:
                    goal["completed"] = True
                self.save_goals()
                break

def generate_ai_goal_plan(prompt):
    """Generate a mental health goal plan using AI"""
    system_prompt = """You are a mental health coach specializing in creating actionable, 
    compassionate goal plans. Create a structured 4-week plan with weekly milestones based 
    on the user's mental health goal. Include specific, measurable actions and emphasize 
    self-compassion. Format with clear sections and bullet points."""
    
    user_prompt = f"Create a mental health goal plan for: {prompt}"
    
    try:
        response = get_ai_response(f"{system_prompt}\n\n{user_prompt}", "openrouter/claude-sonnet-4")
        return response
    except Exception as e:
        return f"I couldn't generate a plan right now. Please try again later. Error: {str(e)}"

def render_goal_creation():
    """Render the goal creation interface"""
    st.markdown("### 🎯 Create New Mental Health Goal")
    
    goal_creation_method = st.radio(
        "How would you like to create your goal?",
        ["✨ Generate Plan with AI", "✍️ Create Manual One-Week Plan"],
        key="goal_creation_method",
        horizontal=True
    )

    if goal_creation_method == "✨ Generate Plan with AI":
        with st.form(key="ai_goal_creation_form"):
            goal_prompt = st.text_area(
                "Describe your mental health goal for AI generation:",
                placeholder="e.g., Reduce stress, Improve sleep, Build better habits, Increase happiness...",
                height=100,
                key="ai_goal_prompt"
            )
            
            submitted = st.form_submit_button("✨ Generate Plan", type="primary")
        
        if submitted and goal_prompt.strip():
            with st.spinner("🧠 Creating your personalized mental health plan..."):
                ai_plan = generate_ai_goal_plan(goal_prompt)
                
                if "Error" not in ai_plan:
                    # Initialize goal planner and save the new goal
                    planner = GoalPlanner()
                    planner.create_goal(goal_prompt, ai_plan, goal_type="ai_generated")
                    
                    st.success("✅ Your AI-generated mental health plan has been created!")
                    st.markdown("---")
                    st.markdown("### 📋 Your Generated Plan")
                    st.markdown(ai_plan)
                    
                    # Option to start a new plan or view all plans
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("➕ Create Another Plan", use_container_width=True):
                            st.session_state.show_goal_creation = True
                            st.rerun()
                    with col2:
                        if st.button("📊 View All Plans", use_container_width=True):
                            st.session_state.show_goal_management = True
                            st.rerun()
                else:
                    st.error(ai_plan)

    elif goal_creation_method == "✍️ Create Manual One-Week Plan":
        st.markdown("---")
        st.markdown("### 📝 Design Your One-Week Goal")
        with st.form(key="manual_goal_creation_form"):
            manual_goal_name = st.text_input(
                "Give your one-week goal a name:",
                placeholder="e.g., My Week of Mindfulness, Stress-Free Week",
                key="manual_goal_name"
            )
            
            st.markdown("#### Daily Tasks (One task per line)")
            daily_tasks = {}
            days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
            for day in days_of_week:
                daily_tasks[day] = st.text_area(
                    f"Tasks for {day}:",
                    placeholder=f"e.g., 1. Meditate for 10 min\n2. Go for a walk",
                    height=80,
                    key=f"manual_task_{day}"
                )
            
            manual_submitted = st.form_submit_button("💾 Save Manual Plan", type="primary")
        
        if manual_submitted and manual_goal_name.strip():
            # Prepare plan content for manual goal
            plan_content = {day: tasks.strip().split('\n') for day, tasks in daily_tasks.items()}
            
            planner = GoalPlanner()
            planner.create_goal(manual_goal_name, plan_content, goal_type="manual_weekly")
            
            st.success("✅ Your manual one-week plan has been created!")
            st.markdown("---")
            st.markdown("### 📋 Your Manual Plan Overview")
            st.markdown(f"**Goal:** {manual_goal_name}")
            for day, tasks in plan_content.items():
                if tasks and tasks[0]: # Check if there are actual tasks
                    st.markdown(f"**{day}:**")
                    for task in tasks:
                        st.markdown(f"- {task}")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("➕ Create Another Plan", use_container_width=True):
                    st.session_state.show_goal_creation = True
                    st.rerun()
            with col2:
                if st.button("📊 View All Plans", use_container_width=True):
                    st.session_state.show_goal_management = True
                    st.rerun()
        elif manual_submitted:
            st.error("Please provide a name for your manual goal.")


def render_goal_management():
    """Render the goal management interface"""
    st.markdown("### 📊 Your Mental Health Goals")
    
    if "user_goals" not in st.session_state or not st.session_state.user_goals:
        st.info("You haven't created any mental health goals yet.")
        if st.button("➕ Create Your First Goal", type="primary"):
            st.session_state.show_goal_creation = True
            st.rerun()
        return
    
    planner = GoalPlanner()
    
    for goal in st.session_state.user_goals:
        with st.expander(f"🎯 {goal['prompt'][:50]}...", expanded=False):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                # Progress tracking
                progress = st.slider(
                    "Progress",
                    0, 100, goal["progress"],
                    key=f"progress_{goal['id']}",
                    help="Track your progress toward this goal"
                )
                
                if progress != goal["progress"]:
                    planner.update_progress(goal["id"], progress)
                    st.rerun()
                
                # Display the plan based on goal_type
                st.markdown("### 📝 Your Plan")
                if goal.get("goal_type") == "ai_generated":
                    st.markdown(goal["plan"])
                elif goal.get("goal_type") == "manual_weekly":
                    st.markdown(f"**Goal Name:** {goal['prompt']}")
                    for day, tasks in goal["weekly_tasks"].items():
                        if tasks and tasks[0]: # Check if there are actual tasks
                            st.markdown(f"**{day}:**")
                            for task in tasks:
                                st.markdown(f"- {task}")
                        else:
                            st.markdown(f"**{day}:** No tasks assigned.")
                else:
                    st.markdown("Plan type not recognized.")
                
            with col2:
                # Goal metadata and actions
                st.metric("Progress", f"{goal['progress']}%")
                status = "✅ Completed" if goal["completed"] else "🟡 In Progress"
                st.write(status)
                
                created_date = datetime.fromisoformat(goal["created_date"]).strftime("%b %d, %Y")
                st.caption(f"Created: {created_date}")
                
                # Delete button
                if st.button("🗑️ Delete", key=f"delete_{goal['id']}", use_container_width=True):
                    planner.delete_goal(goal["id"])
                    st.rerun()
    
    # Add new goal button
    if st.button("➕ Add New Goal", type="primary"):
        st.session_state.show_goal_creation = True
        st.rerun()

def render_goal_planning():
    """Main function to render the goal planning feature"""
    # Initialize session state variables
    if "show_goal_creation" not in st.session_state:
        st.session_state.show_goal_creation = False
    if "show_goal_management" not in st.session_state:
        st.session_state.show_goal_management = True
       
    # Back button to home
    if st.button("← Back to Home", type="primary"):
        st.session_state.show_goal_planning = False
        st.session_state.active_page = "TalkHeal" # This will trigger the main page rendering
        st.rerun()
    # Main header
    st.markdown("""
    <div class="main-header">
        <h1>🎯 Mental Health Goal Planning</h1>
        <p>Set goals, create actionable plans, and track your progress</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation tabs
    tab1, tab2 = st.tabs(["📋 Manage Goals", "➕ Create New Goal"])
    
    with tab1:
        render_goal_management()
    
    with tab2:
        render_goal_creation()

