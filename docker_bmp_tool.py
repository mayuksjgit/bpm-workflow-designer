import gradio as gr
import json
import uuid
import os
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, asdict
from enum import Enum

class TaskStatus(Enum):
    SUCCESS = "success"
    FAILURE = "failure" 
    SKIPPED = "skipped"
    DELAYED = "delayed"
    DEFAULT = "default"

@dataclass
class Task:
    id: str
    name: str
    x: float
    y: float
    status: TaskStatus
    color: str
    context_id: str
    successors: List[str]
    predecessors: List[str]
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'x': self.x,
            'y': self.y,
            'status': self.status.value,
            'color': self.color,
            'context_id': self.context_id,
            'successors': self.successors,
            'predecessors': self.predecessors
        }

@dataclass
class Context:
    id: str
    name: str
    x: float
    y: float
    width: float
    height: float
    color: str
    tasks: List[str]
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'x': self.x,
            'y': self.y,
            'width': self.width,
            'height': self.height,
            'color': self.color,
            'tasks': self.tasks
        }

class BPMTool:
    def __init__(self):
        self.contexts: Dict[str, Context] = {}
        self.tasks: Dict[str, Task] = {}
        self.zoom_level = 1.0
        self.canvas_width = 1400
        self.canvas_height = 900
        self.data_dir = "/app/data"
        
        # Create data directory if it doesn't exist
        os.makedirs(self.data_dir, exist_ok=True)
        
    def add_context(self, name: str, x: float = 100, y: float = 100, 
                   width: float = 350, height: float = 250, color: str = "#e6f3ff"):
        context_id = str(uuid.uuid4())
        context = Context(
            id=context_id,
            name=name,
            x=x, y=y,
            width=width, height=height,
            color=color,
            tasks=[]
        )
        self.contexts[context_id] = context
        return context_id
    
    def add_task(self, name: str, context_id: str, x: float = 0, y: float = 0,
                status: TaskStatus = TaskStatus.DEFAULT, color: str = "#ffffff"):
        task_id = str(uuid.uuid4())
        
        # Auto-position task within context if coordinates are 0,0
        if x == 0 and y == 0 and context_id in self.contexts:
            context = self.contexts[context_id]
            task_count = len(context.tasks)
            x = context.x + 20 + (task_count % 3) * 110
            y = context.y + 50 + (task_count // 3) * 50
        
        task = Task(
            id=task_id,
            name=name,
            x=x, y=y,
            status=status,
            color=color,
            context_id=context_id,
            successors=[],
            predecessors=[]
        )
        self.tasks[task_id] = task
        if context_id in self.contexts:
            self.contexts[context_id].tasks.append(task_id)
        return task_id
    
    def connect_tasks(self, source_id: str, target_id: str):
        if source_id in self.tasks and target_id in self.tasks:
            if target_id not in self.tasks[source_id].successors:
                self.tasks[source_id].successors.append(target_id)
                self.tasks[target_id].predecessors.append(source_id)
                return True
        return False
    
    def disconnect_tasks(self, source_id: str, target_id: str):
        if source_id in self.tasks and target_id in self.tasks[source_id].successors:
            self.tasks[source_id].successors.remove(target_id)
            self.tasks[target_id].predecessors.remove(source_id)
            return True
        return False
    
    def delete_task(self, task_id: str):
        if task_id in self.tasks:
            task = self.tasks[task_id]
            # Remove from context
            if task.context_id in self.contexts:
                self.contexts[task.context_id].tasks.remove(task_id)
            
            # Remove connections to this task
            for other_task in self.tasks.values():
                if task_id in other_task.successors:
                    other_task.successors.remove(task_id)
                if task_id in other_task.predecessors:
                    other_task.predecessors.remove(task_id)
            
            # Delete the task
            del self.tasks[task_id]
            return True
        return False
    
    def delete_context(self, context_id: str):
        if context_id in self.contexts:
            # Delete all tasks in this context
            context = self.contexts[context_id]
            for task_id in context.tasks.copy():
                self.delete_task(task_id)
            
            # Delete the context
            del self.contexts[context_id]
            return True
        return False
    
    def get_status_color(self, status: TaskStatus) -> str:
        color_map = {
            TaskStatus.SUCCESS: "#28a745",  # Green
            TaskStatus.FAILURE: "#dc3545",  # Red
            TaskStatus.SKIPPED: "#6c757d",  # Grey
            TaskStatus.DELAYED: "#fd7e14",  # Orange
            TaskStatus.DEFAULT: "#ffffff"   # White
        }
        return color_map.get(status, "#ffffff")
    
    def generate_svg(self) -> str:
        svg_content = f'''
        <svg width="{self.canvas_width * self.zoom_level}" height="{self.canvas_height * self.zoom_level}" 
             viewBox="0 0 {self.canvas_width} {self.canvas_height}" 
             xmlns="http://www.w3.org/2000/svg"
             style="border: 2px solid #ddd; background: #f9f9f9;">
        
        <!-- Grid pattern -->
        <defs>
            <pattern id="grid" width="20" height="20" patternUnits="userSpaceOnUse">
                <path d="M 20 0 L 0 0 0 20" fill="none" stroke="#e0e0e0" stroke-width="1"/>
            </pattern>
            <marker id="arrowhead" markerWidth="10" markerHeight="7" 
                    refX="9" refY="3.5" orient="auto">
                <polygon points="0 0, 10 3.5, 0 7" fill="#666"/>
            </marker>
        </defs>
        
        <!-- Grid background -->
        <rect width="100%" height="100%" fill="url(#grid)" />
        '''
        
        # Draw contexts (boxes)
        for context in self.contexts.values():
            svg_content += f'''
            <g class="context" data-id="{context.id}">
                <rect x="{context.x}" y="{context.y}" 
                      width="{context.width}" height="{context.height}"
                      fill="{context.color}" stroke="#333" stroke-width="2" rx="8"
                      style="filter: drop-shadow(2px 2px 4px rgba(0,0,0,0.1));"/>
                <text x="{context.x + 15}" y="{context.y + 25}" 
                      font-family="Arial, sans-serif" font-size="16" font-weight="bold" fill="#333">
                    {context.name}
                </text>
                <text x="{context.x + 15}" y="{context.y + context.height - 10}" 
                      font-family="Arial, sans-serif" font-size="10" fill="#666">
                    {len(context.tasks)} task(s)
                </text>
            </g>
            '''
        
        # Draw task connections (wires) first so they appear behind tasks
        for task in self.tasks.values():
            for successor_id in task.successors:
                if successor_id in self.tasks:
                    successor = self.tasks[successor_id]
                    # Calculate connection points
                    start_x = task.x + 100
                    start_y = task.y + 20
                    end_x = successor.x
                    end_y = successor.y + 20
                    
                    # Create curved connection
                    control_x = start_x + (end_x - start_x) / 2
                    
                    svg_content += f'''
                    <g class="connection">
                        <path d="M {start_x} {start_y} Q {control_x} {start_y} {end_x} {end_y}"
                              stroke="#666" stroke-width="2" fill="none" 
                              marker-end="url(#arrowhead)"
                              style="filter: drop-shadow(1px 1px 2px rgba(0,0,0,0.1));"/>
                    </g>
                    '''
        
        # Draw tasks
        for task in self.tasks.values():
            task_color = task.color if task.color != "#ffffff" else self.get_status_color(task.status)
            text_color = "#000" if task.status != TaskStatus.FAILURE else "#fff"
            
            svg_content += f'''
            <g class="task" data-id="{task.id}">
                <rect x="{task.x}" y="{task.y}" width="100" height="40"
                      fill="{task_color}" stroke="#333" stroke-width="1.5" rx="5"
                      style="filter: drop-shadow(1px 1px 3px rgba(0,0,0,0.2)); cursor: pointer;"/>
                <text x="{task.x + 50}" y="{task.y + 15}" 
                      font-family="Arial, sans-serif" font-size="11" font-weight="bold" 
                      fill="{text_color}" text-anchor="middle">
                    {task.name[:10]}{'...' if len(task.name) > 10 else ''}
                </text>
                <text x="{task.x + 50}" y="{task.y + 30}" 
                      font-family="Arial, sans-serif" font-size="9" 
                      fill="{text_color}" text-anchor="middle">
                    {task.status.value.title()}
                </text>
            </g>
            '''
        
        # Add zoom level indicator
        svg_content += f'''
        <text x="10" y="{self.canvas_height - 10}" 
              font-family="Arial, sans-serif" font-size="12" fill="#666">
            Zoom: {self.zoom_level:.1f}x | Running in Docker 🐳
        </text>
        '''
        
        svg_content += '</svg>'
        return svg_content
    
    def save_to_file(self, filename: str):
        try:
            filepath = os.path.join(self.data_dir, filename)
            data = {
                'contexts': {k: v.to_dict() for k, v in self.contexts.items()},
                'tasks': {k: v.to_dict() for k, v in self.tasks.items()},
                'zoom_level': self.zoom_level,
                'canvas_width': self.canvas_width,
                'canvas_height': self.canvas_height
            }
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)
            return f"✅ Configuration saved to {filename} (Docker volume: /app/data)"
        except Exception as e:
            return f"❌ Error saving file: {str(e)}"
    
    def load_from_file(self, filename: str):
        try:
            filepath = os.path.join(self.data_dir, filename)
            with open(filepath, 'r') as f:
                data = json.load(f)
            
            self.contexts = {}
            self.tasks = {}
            
            # Load contexts
            for context_data in data.get('contexts', {}).values():
                context = Context(
                    id=context_data['id'],
                    name=context_data['name'],
                    x=context_data['x'],
                    y=context_data['y'],
                    width=context_data['width'],
                    height=context_data['height'],
                    color=context_data['color'],
                    tasks=context_data['tasks']
                )
                self.contexts[context.id] = context
            
            # Load tasks
            for task_data in data.get('tasks', {}).values():
                task = Task(
                    id=task_data['id'],
                    name=task_data['name'],
                    x=task_data['x'],
                    y=task_data['y'],
                    status=TaskStatus(task_data['status']),
                    color=task_data['color'],
                    context_id=task_data['context_id'],
                    successors=task_data['successors'],
                    predecessors=task_data.get('predecessors', [])
                )
                self.tasks[task.id] = task
            
            self.zoom_level = data.get('zoom_level', 1.0)
            self.canvas_width = data.get('canvas_width', 1400)
            self.canvas_height = data.get('canvas_height', 900)
            
            return f"✅ Configuration loaded from {filename}"
        except FileNotFoundError:
            return f"❌ File not found: {filename}"
        except Exception as e:
            return f"❌ Error loading file: {str(e)}"
    
    def get_workflow_stats(self):
        total_tasks = len(self.tasks)
        total_contexts = len(self.contexts)
        
        status_counts = {}
        for status in TaskStatus:
            status_counts[status.value] = sum(1 for task in self.tasks.values() if task.status == status)
        
        total_connections = sum(len(task.successors) for task in self.tasks.values())
        
        return {
            'total_contexts': total_contexts,
            'total_tasks': total_tasks,
            'total_connections': total_connections,
            'status_counts': status_counts
        }

# Global BPM tool instance
bpm_tool = BPMTool()

def create_gradio_interface():
    with gr.Blocks(
        title="BPM Workflow Designer - Docker Edition", 
        css="""
        .canvas-container { 
            border: 2px solid #ddd; 
            border-radius: 8px;
            overflow: auto; 
            background: #f9f9f9;
            min-height: 600px;
        }
        .control-panel { 
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); 
            padding: 15px; 
            border-radius: 8px; 
            margin-bottom: 10px;
            border: 1px solid #dee2e6;
        }
        .stats-panel {
            background: #e3f2fd;
            padding: 10px;
            border-radius: 5px;
            border-left: 4px solid #2196f3;
        }
        .docker-badge {
            background: #0db7ed;
            color: white;
            padding: 5px 10px;
            border-radius: 15px;
            font-size: 12px;
            display: inline-block;
            margin: 5px;
        }
        """
    ) as demo:
        
        gr.Markdown("# 🐳 BPM Workflow Designer - Docker Edition")
        gr.HTML('<div class="docker-badge">🐳 Running in Docker Container | Port 80</div>')
        gr.Markdown("Professional Business Process Management tool optimized for containerized deployment")
        
        with gr.Row():
            with gr.Column(scale=1):
                # System Info
                with gr.Group():
                    gr.Markdown("### 🖥️ System Information")
                    system_info = gr.HTML(f"""
                    <div style="background: #f8f9fa; padding: 10px; border-radius: 5px; font-family: monospace;">
                        <strong>Environment:</strong> Docker Container<br>
                        <strong>Port:</strong> 80 (exposed)<br>
                        <strong>Data Volume:</strong> /app/data<br>
                        <strong>Python:</strong> {os.sys.version.split()[0]}<br>
                        <strong>Status:</strong> <span style="color: green;">🟢 Online</span>
                    </div>
                    """)
                
                # Workflow Statistics
                with gr.Group():
                    gr.Markdown("### 📊 Workflow Statistics")
                    stats_display = gr.HTML()
                
                # Context Management
                with gr.Group():
                    gr.Markdown("### 📦 Context Management")
                    context_name = gr.Textbox(label="Context Name", placeholder="e.g., Data Processing")
                    with gr.Row():
                        context_color = gr.ColorPicker(label="Color", value="#e6f3ff")
                        context_x = gr.Number(label="X", value=100, precision=0)
                        context_y = gr.Number(label="Y", value=100, precision=0)
                    with gr.Row():
                        add_context_btn = gr.Button("➕ Add Context", variant="primary")
                        delete_context_btn = gr.Button("🗑️ Delete", variant="secondary")
                    context_list = gr.Dropdown(label="Select Context", choices=[], interactive=True)
                
                # Task Management
                with gr.Group():
                    gr.Markdown("### ⚙️ Task Management")
                    task_name = gr.Textbox(label="Task Name", placeholder="e.g., Validate Input")
                    task_context = gr.Dropdown(label="Parent Context", choices=[], interactive=True)
                    with gr.Row():
                        task_status = gr.Dropdown(
                            label="Status",
                            choices=[
                                ("Default", "default"),
                                ("✅ Success", "success"), 
                                ("❌ Failure", "failure"),
                                ("⏭️ Skipped", "skipped"), 
                                ("⏰ Delayed", "delayed")
                            ],
                            value="default"
                        )
                        task_color = gr.ColorPicker(label="Custom Color", value="#ffffff")
                    with gr.Row():
                        task_x = gr.Number(label="X", value=0, precision=0)
                        task_y = gr.Number(label="Y", value=0, precision=0)
                    with gr.Row():
                        add_task_btn = gr.Button("➕ Add Task", variant="primary")
                        delete_task_btn = gr.Button("🗑️ Delete", variant="secondary")
                    task_list = gr.Dropdown(label="Select Task", choices=[], interactive=True)
                
                # Connection Management
                with gr.Group():
                    gr.Markdown("### 🔗 Task Connections")
                    source_task = gr.Dropdown(label="Source Task", choices=[], interactive=True)
                    target_task = gr.Dropdown(label="Target Task", choices=[], interactive=True)
                    with gr.Row():
                        connect_btn = gr.Button("🔗 Connect", variant="primary")
                        disconnect_btn = gr.Button("✂️ Disconnect", variant="secondary")
                
                # Canvas Controls
                with gr.Group():
                    gr.Markdown("### 🎛️ Canvas Controls")
                    zoom_slider = gr.Slider(
                        minimum=0.3, maximum=3.0, value=1.0, step=0.1,
                        label="🔍 Zoom Level"
                    )
                    with gr.Row():
                        zoom_fit_btn = gr.Button("📐 Fit to Screen")
                        zoom_reset_btn = gr.Button("🔄 Reset Zoom")
                
                # File Operations
                with gr.Group():
                    gr.Markdown("### 💾 File Operations")
                    gr.HTML("<small>Files are stored in Docker volume: /app/data</small>")
                    filename = gr.Textbox(label="Filename", value="workflow.json")
                    with gr.Row():
                        save_btn = gr.Button("💾 Save", variant="primary")
                        load_btn = gr.Button("📂 Load", variant="secondary")
                        clear_btn = gr.Button("🗑️ Clear All", variant="stop")
                    file_status = gr.Textbox(label="Status", interactive=False)
            
            with gr.Column(scale=3):
                gr.Markdown("## 🎨 Workflow Canvas")
                canvas = gr.HTML(value=bpm_tool.generate_svg(), elem_classes=["canvas-container"])
        
        # All the event handlers remain the same as in the original enhanced version
        def update_canvas():
            return bpm_tool.generate_svg()
        
        def update_stats():
            stats = bpm_tool.get_workflow_stats()
            html = f"""
            <div class="stats-panel">
                <strong>📊 Current Workflow:</strong><br>
                📦 Contexts: {stats['total_contexts']}<br>
                ⚙️ Tasks: {stats['total_tasks']}<br>
                🔗 Connections: {stats['total_connections']}<br><br>
                <strong>Task Status:</strong><br>
            """
            
            status_colors = {
                'success': '#28a745',
                'failure': '#dc3545', 
                'skipped': '#6c757d',
                'delayed': '#fd7e14',
                'default': '#ffffff'
            }
            
            for status, count in stats['status_counts'].items():
                color = status_colors.get(status, '#ffffff')
                html += f'<span style="display: inline-block; width: 12px; height: 12px; border-radius: 50%; background-color: {color}; margin-right: 5px;"></span>{status.title()}: {count}<br>'
            
            html += "</div>"
            return html
        
        def update_dropdowns():
            context_choices = [(ctx.name, ctx.id) for ctx in bpm_tool.contexts.values()]
            task_choices = [(task.name, task.id) for task in bpm_tool.tasks.values()]
            return (
                gr.Dropdown.update(choices=context_choices),  # task_context
                gr.Dropdown.update(choices=context_choices),  # context_list
                gr.Dropdown.update(choices=task_choices),     # task_list
                gr.Dropdown.update(choices=task_choices),     # source_task
                gr.Dropdown.update(choices=task_choices)      # target_task
            )
        
        # Event handlers (same as enhanced version)
        def add_context_handler(name, color, x, y):
            if name.strip():
                bpm_tool.add_context(name.strip(), x, y, color=color)
                return (update_canvas(), update_stats(), *update_dropdowns())
            return (gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), gr.update())
        
        def delete_context_handler(context_id):
            if context_id:
                bpm_tool.delete_context(context_id)
                return (update_canvas(), update_stats(), *update_dropdowns())
            return (gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), gr.update())
        
        def add_task_handler(name, context_id, status, color, x, y):
            if name.strip() and context_id:
                task_status_enum = TaskStatus(status)
                bpm_tool.add_task(name.strip(), context_id, x, y, task_status_enum, color)
                return (update_canvas(), update_stats(), *update_dropdowns())
            return (gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), gr.update())
        
        def delete_task_handler(task_id):
            if task_id:
                bpm_tool.delete_task(task_id)
                return (update_canvas(), update_stats(), *update_dropdowns())
            return (gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), gr.update())
        
        def connect_tasks_handler(source_id, target_id):
            if source_id and target_id and source_id != target_id:
                success = bpm_tool.connect_tasks(source_id, target_id)
                if success:
                    return update_canvas(), update_stats()
            return gr.update(), gr.update()
        
        def disconnect_tasks_handler(source_id, target_id):
            if source_id and target_id:
                success = bpm_tool.disconnect_tasks(source_id, target_id)
                if success:
                    return update_canvas(), update_stats()
            return gr.update(), gr.update()
        
        def zoom_handler(zoom_value):
            bpm_tool.zoom_level = zoom_value
            return update_canvas()
        
        def zoom_fit_handler():
            bpm_tool.zoom_level = 0.8
            return update_canvas(), gr.Slider.update(value=0.8)
        
        def zoom_reset_handler():
            bpm_tool.zoom_level = 1.0
            return update_canvas(), gr.Slider.update(value=1.0)
        
        def save_handler(filename):
            if not filename.strip():
                return "❌ Please enter a filename"
            return bpm_tool.save_to_file(filename.strip())
        
        def load_handler(filename):
            if not filename.strip():
                return "❌ Please enter a filename", gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), gr.update()
            status = bpm_tool.load_from_file(filename.strip())
            return (status, update_canvas(), update_stats(), *update_dropdowns())
        
        def clear_all_handler():
            bpm_tool.contexts.clear()
            bpm_tool.tasks.clear()
            return (update_canvas(), update_stats(), *update_dropdowns())
        
        # Bind all event handlers
        add_context_btn.click(add_context_handler, inputs=[context_name, context_color, context_x, context_y], outputs=[canvas, stats_display, task_context, context_list, task_list, source_task, target_task])
        delete_context_btn.click(delete_context_handler, inputs=[context_list], outputs=[canvas, stats_display, task_context, context_list, task_list, source_task, target_task])
        add_task_btn.click(add_task_handler, inputs=[task_name, task_context, task_status, task_color, task_x, task_y], outputs=[canvas, stats_display, task_context, context_list, task_list, source_task, target_task])
        delete_task_btn.click(delete_task_handler, inputs=[task_list], outputs=[canvas, stats_display, task_context, context_list, task_list, source_task, target_task])
        connect_btn.click(connect_tasks_handler, inputs=[source_task, target_task], outputs=[canvas, stats_display])
        disconnect_btn.click(disconnect_tasks_handler, inputs=[source_task, target_task], outputs=[canvas, stats_display])
        zoom_slider.change(zoom_handler, inputs=[zoom_slider], outputs=[canvas])
        zoom_fit_btn.click(zoom_fit_handler, outputs=[canvas, zoom_slider])
        zoom_reset_btn.click(zoom_reset_handler, outputs=[canvas, zoom_slider])
        save_btn.click(save_handler, inputs=[filename], outputs=[file_status])
        load_btn.click(load_handler, inputs=[filename], outputs=[file_status, canvas, stats_display, task_context, context_list, task_list, source_task, target_task])
        clear_btn.click(clear_all_handler, outputs=[canvas, stats_display, task_context, context_list, task_list, source_task, target_task])
        
        # Initialize display
        demo.load(lambda: (update_stats(), *update_dropdowns()), outputs=[stats_display, task_context, context_list, task_list, source_task, target_task])
    
    return demo

if __name__ == "__main__":
    # Initialize with sample data for Docker demo
    print("🐳 Starting BPM Workflow Designer in Docker...")
    print(f"📁 Data directory: {bpm_tool.data_dir}")
    print("🌐 Server will be available on port 80")
    
    # Create sample workflow
    ctx1_id = bpm_tool.add_context("Docker Processing", 50, 50, color="#e6f3ff")
    ctx2_id = bpm_tool.add_context("Container QA", 450, 50, color="#fff2e6")
    ctx3_id = bpm_tool.add_context("Deployment", 850, 50, color="#f0fff0")
    
    # Add tasks
    task1_id = bpm_tool.add_task("Initialize Container", ctx1_id, status=TaskStatus.SUCCESS)
    task2_id = bpm_tool.add_task("Load Configuration", ctx1_id, status=TaskStatus.SUCCESS)
    task3_id = bpm_tool.add_task("Start Services", ctx1_id, status=TaskStatus.DEFAULT)
    
    task4_id = bpm_tool.add_task("Health Check", ctx2_id, status=TaskStatus.DELAYED)
    task5_id = bpm_tool.add_task("Performance Test", ctx2_id, status=TaskStatus.DEFAULT)
    
    task6_id = bpm_tool.add_task("Deploy to Production", ctx3_id, status=TaskStatus.DEFAULT)
    
    # Create connections
    bpm_tool.connect_tasks(task1_id, task2_id)
    bpm_tool.connect_tasks(task2_id, task3_id)
    bpm_tool.connect_tasks(task3_id, task4_id)
    bpm_tool.connect_tasks(task4_id, task5_id)
    bpm_tool.connect_tasks(task5_id, task6_id)
    
    # Launch with Docker-optimized settings
    demo = create_gradio_interface()
    demo.launch(
        server_name="0.0.0.0",  # Listen on all interfaces
        server_port=80,         # Use port 80
        share=False,           # No need for share in Docker
        debug=False,           # Disable debug in production
        show_error=True,       # Show errors for debugging
        quiet=False            # Show startup logs
    )