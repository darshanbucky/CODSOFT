import streamlit as st
import pandas as pd
import os

TASKS_FILE = "tasks.csv"

def load_tasks():
    if os.path.exists(TASKS_FILE):
        return pd.read_csv(TASKS_FILE)
    else:
        return pd.DataFrame(columns=["Task", "Status"])

def save_tasks(tasks_df):
    tasks_df.to_csv(TASKS_FILE, index=False)

def main():
    st.set_page_config(page_title="To-Do List", page_icon="📝", layout="centered")
    st.title("📝 To-Do List Manager")
    
    
    if 'show_done_toast' not in st.session_state:
        st.session_state.show_done_toast = False
    if 'done_task_name' not in st.session_state:
        st.session_state.done_task_name = ""
    
    tasks_df = load_tasks()
    
    with st.form("add_task_form"):
        st.subheader("Add New Task")
        new_task = st.text_input("Task Description", placeholder="Enter your task here...")
        submitted = st.form_submit_button("➕ Add Task")
        if submitted and new_task.strip():
            tasks_df = pd.concat([tasks_df, pd.DataFrame([{"Task": new_task, "Status": "Pending"}])], ignore_index=True)
            save_tasks(tasks_df)
            st.toast("🎉 Task added successfully!", icon="✅")
    
    st.subheader("Your Tasks")
    if not tasks_df.empty:
        for index, row in tasks_df.iterrows():
            col1, col2, col3 = st.columns([6, 2, 2])
            status_icon = "✅" if row['Status'] == "Completed" else "⏳"
            col1.markdown(f"{status_icon} **{row['Task']}** - {row['Status']}")
            
            if row['Status'] != "Completed":
                if col2.button("✔ Done", key=f"done{index}"):
                    tasks_df.at[index, "Status"] = "Completed"
                    save_tasks(tasks_df)
                    st.session_state.show_done_toast = True
                    st.session_state.done_task_name = row['Task']
                    st.rerun()
            
            if col3.button("❌ Delete", key=f"delete{index}"):
                deleted_task = row['Task']
                tasks_df = tasks_df.drop(index).reset_index(drop=True)
                save_tasks(tasks_df)
                st.rerun()
    else:
        st.info("No tasks added yet! Add your first task above.")
    if st.session_state.show_done_toast:
        st.toast(f"🎉 {st.session_state.done_task_name} : Task completed")
        st.session_state.show_done_toast = False
        st.session_state.done_task_name = ""

    if not tasks_df.empty:
        completed_count = len(tasks_df[tasks_df['Status'] == "Completed"])
        st.caption(f"📊 Total tasks: {len(tasks_df)} | ✅ Completed: {completed_count} | ⏳ Pending: {len(tasks_df)-completed_count}")

if __name__ == "__main__":
    main()