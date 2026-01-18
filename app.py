import gradio as gr
import json
import uuid
from typing import Dict, List
from dataclasses import dataclass
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
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'x': self.x,
            'y': self.y,
            'status': self.status.value,
            'color': self.color,
            'context_id': self.context_id,
            'successors': self.successors
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
        self.canvas_width = 1000
        self.canvas_height = 600
        
    def add_context(self, name: str, x: float = 100, y: float = 100, 
                   width: float = 250, height: float = 180, color: str = "#e6f3ff"):
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
        
        if x == 0 and y == 0 and context_id in self.contexts:
            context = self.contexts[context_id]
            task_count = len(context.tasks)
            x = context.x + 20 + (task_count % 2) * 100
            y = context.y + 40 + (task_count // 2) * 40
        
        task = Task(
            id=task_id,
            name=name,
            x=x, y=y,
            status=status,
            color=color,
            context_id=context_id,
            successors=[]
        )
        self.tasks[task_id] = task
        if context_id in self.contexts:
            self.contexts[context_id].tasks.append(task_id)
        return task_id
    
    def connect_tasks(self, source_id: str, target_id: str):
        if source_id in self.tasks and target_id in self.tasks:
            if target_id not in self.tasks[source_id].successors:
                self.tasks[source_id].successors.append(target_id)
                return True
        return False
    
    def get_status_color(self, status: TaskStatus) -> str:
        color_map = {
            TaskStatus.SUCCESS: "#28a745",
            TaskStatus.FAILURE: "#dc3545",
            TaskStatus.SKIPPED: "#6c757d",
            TaskStatus.DELAYED: "#fd7e14",
            TaskStatus.DEFAULT: "#ffffff"
        }
        return color_map.get(status, "#ffffff")
    
    def generate_svg(self) -> str:
        svg_content = f'''
        <svg width="{int(self.canvas_width * self.zoom_level)}" height="{int(self.canvas_height * self.zoom_level)}" 
             viewBox="0 0 {self.canvas_width} {self.canvas_height}" 
             xmlns="http://www.w3.org/2000/svg"
             style="border: 2px solid #ddd; background: #f9f9f9;">
        
        <defs>
            <marker id="arrowhead" markerWidth="10" markerHeight="7" 
                    refX="9" refY="3.5" orient="auto">
                <polygon points="0 0, 10 3.5, 0 7" fill="#666"/>
            </marker>
        </defs>
        '''
        
        # Draw contexts
        for context in self.contexts.values():
            svg_content += f'''
            <rect x="{context.x}" y="{context.y}" 
                  width="{context.width}" height="{context.height}"
                  fill="{context.color}" stroke="#333" stroke-width="2" rx="5"/>
            <text x="{context.x + 10}" y="{context.y + 20}" 
                  font-family="Arial" font-size="14" font-weight="bold" fill="#333">
                {context.name}
            </text>
            '''
        
        # Draw connections
        for task in self.tasks.values():
            for successor_id in task.successors:
                if successor_id in self.tasks:
                    successor = self.tasks[successor_id]
                    svg_content += f'''
                    <line x1="{task.x + 40}" y1="{task.y + 15}" 
                          x2="{successor.x}" y2="{successor.y + 15}"
                          stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
                    '''
        
        # Draw tasks
        for task in self.tasks.values():
            task_color = task.color if task.color != "#ffffff" else self.get_status_color(task.status)
            svg_content += f'''
            <rect x="{task.x}" y="{task.y}" width="80" height="30"
                  fill="{task_color}" stroke="#333" stroke-width="1" rx="3"/>
            <text x="{task.x + 5}" y="{task.y + 20}" 
                  font-family="Arial" font-size="10" fill="#000">
                {task.name[:8]}{'...' if len(task.name) > 8 else ''}
            </text>
            '''
        
        svg_content += f'''
        <text x="10" y="{self.canvas_height - 10}" 
              font-family="Arial" font-size="12" fill="#666">
            BPM Designer | Zoom: {self.zoom_level:.1f}x
        </text>
        </svg>'''
        return svg_content

# Global instance
bpm_tool = BPMTool()

def create_interface():
    with gr.Blocks(title="BPM Workflow Designer - Vercel", css="""
        .canvas-container { 
            border: 2px solid #ddd; 
            border-radius: 8px;
            overflow: auto; 
            background: #f9f9f9;
        }
    """) as demo:
        
        gr.Markdown("# 🔄 BPM Workflow Designer")
        gr.Markdown("**Deployed on Vercel** - Create and manage business process workflows")
        
        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("### 📦 Context Management")
                context_name = gr.Textbox(label="Context Name", placeholder="e.g., Data Processing")
                context_color = gr.ColorPicker(label="Context Color", value="#e6f3ff")
                add_context_btn = gr.Button("➕ Add Context", variant="primary")
                
                gr.Markdown("### ⚙️ Task Management")
                task_name = gr.Textbox(label="Task Name", placeholder="e.g., Validate Input")
                task_context = gr.Dropdown(label="Parent Context", choices=[], interactive=True)
                task_status = gr.Dropdown(
                    label="Task Status",
                    choices=[
                        ("Default", "default"),
                        ("✅ Success", "success"), 
                        ("❌ Failure", "failure"),
                        ("⏭️ Skipped", "skipped"), 
                        ("⏰ Delayed", "delayed")
                    ],
                    value="default"
                )
                add_task_btn = gr.Button("➕ Add Task", variant="primary")
                
                gr.Markdown("### 🔗 Task Connections")
                source_task = gr.Dropdown(label="Source Task", choices=[], interactive=True)
                target_task = gr.Dropdown(label="Target Task", choices=[], interactive=True)
                connect_btn = gr.Button("🔗 Connect Tasks", variant="secondary")
                
                gr.Markdown("### 🎛️ Canvas Controls")
                zoom_slider = gr.Slider(
                    minimum=0.5, maximum=2.0, value=1.0, step=0.1,
                    label="🔍 Zoom Level"
                )
            
            with gr.Column(scale=2):
                gr.Markdown("## 🎨 Workflow Canvas")
                canvas = gr.HTML(value=bmp_tool.generate_svg(), elem_classes=["canvas-container"])
        
        def update_canvas():
            return bpm_tool.generate_svg()
        
        def update_dropdowns():
            context_choices = [(ctx.name, ctx.id) for ctx in bpm_tool.contexts.values()]
            task_choices = [(task.name, task.id) for task in bpm_tool.tasks.values()]
            return (
                gr.Dropdown.update(choices=context_choices),
                gr.Dropdown.update(choices=task_choices),
                gr.Dropdown.update(choices=task_choices)
            )
        
        def add_context_handler(name, color):
            if name and name.strip():
                bpm_tool.add_context(name.strip(), color=color)
                return update_canvas(), *update_dropdowns()
            return gr.update(), gr.update(), gr.update(), gr.update()
        
        def add_task_handler(name, context_id, status):
            if name and name.strip() and context_id:
                task_status_enum = TaskStatus(status)
                bpm_tool.add_task(name.strip(), context_id, status=task_status_enum)
                return update_canvas(), *update_dropdowns()
            return gr.update(), gr.update(), gr.update(), gr.update()
        
        def connect_tasks_handler(source_id, target_id):
            if source_id and target_id and source_id != target_id:
                bpm_tool.connect_tasks(source_id, target_id)
                return update_canvas()
            return gr.update()
        
        def zoom_handler(zoom_value):
            bpm_tool.zoom_level = zoom_value
            return update_canvas()
        
        # Event handlers
        add_context_btn.click(
            add_context_handler,
            inputs=[context_name, context_color],
            outputs=[canvas, task_context, source_task, target_task]
        )
        
        add_task_btn.click(
            add_task_handler,
            inputs=[task_name, task_context, task_status],
            outputs=[canvas, task_context, source_task, target_task]
        )
        
        connect_btn.click(
            connect_tasks_handler,
            inputs=[source_task, target_task],
            outputs=[canvas]
        )
        
        zoom_slider.change(
            zoom_handler,
            inputs=[zoom_slider],
            outputs=[canvas]
        )
        
        # Initialize display
        demo.load(
            lambda: update_dropdowns(),
            outputs=[task_context, source_task, target_task]
        )
    
    return demo

# Initialize with sample data
try:
    ctx1_id = bpm_tool.add_context("Process Flow", 50, 50, color="#e6f3ff")
    ctx2_id = bpm_tool.add_context("Quality Control", 350, 50, color="#fff2e6")
    
    task1_id = bpm_tool.add_task("Start Process", ctx1_id, status=TaskStatus.SUCCESS)
    task2_id = bpm_tool.add_task("Execute Task", ctx1_id, status=TaskStatus.DEFAULT)
    task3_id = bpm_tool.add_task("Quality Check", ctx2_id, status=TaskStatus.DELAYED)
    
    bpm_tool.connect_tasks(task1_id, task2_id)
    bpm_tool.connect_tasks(task2_id, task3_id)
except Exception as e:
    print(f"Sample data initialization error: {e}")

# Create the app
app = create_interface()

# Export for Vercel
if __name__ == "__main__":
    app.launch(server_name="0.0.0.0", server_port=7860)