# Vercel deployment entry point
from enhanced_bpm_tool import create_gradio_interface, bpm_tool

# Initialize with sample data for demo
ctx1_id = bpm_tool.add_context("Data Processing", 50, 50, color="#e6f3ff")
ctx2_id = bpm_tool.add_context("Quality Assurance", 450, 50, color="#fff2e6")
ctx3_id = bpm_tool.add_context("Output Generation", 850, 50, color="#f0fff0")

# Add tasks to contexts
task1_id = bpm_tool.add_task("Initialize", ctx1_id, status=bpm_tool.TaskStatus.SUCCESS)
task2_id = bpm_tool.add_task("Validate Input", ctx1_id, status=bpm_tool.TaskStatus.SUCCESS)
task3_id = bpm_tool.add_task("Process Data", ctx1_id, status=bpm_tool.TaskStatus.DEFAULT)

task4_id = bpm_tool.add_task("Quality Check", ctx2_id, status=bpm_tool.TaskStatus.DELAYED)
task5_id = bpm_tool.add_task("Error Handling", ctx2_id, status=bpm_tool.TaskStatus.SKIPPED)

task6_id = bpm_tool.add_task("Generate Report", ctx3_id, status=bpm_tool.TaskStatus.DEFAULT)
task7_id = bpm_tool.add_task("Send Notification", ctx3_id, status=bpm_tool.TaskStatus.DEFAULT)

# Create connections
bpm_tool.connect_tasks(task1_id, task2_id)
bpm_tool.connect_tasks(task2_id, task3_id)
bpm_tool.connect_tasks(task3_id, task4_id)
bpm_tool.connect_tasks(task4_id, task6_id)
bpm_tool.connect_tasks(task6_id, task7_id)

# Create and export the app
app = create_gradio_interface()

if __name__ == "__main__":
    app.launch()