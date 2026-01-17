import gradio as gr
import json
import uuid
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
        self.canvas_width = 1200
        self.canvas_height = 800
        
    def add_context(self, name: str, x: float = 100, y: float = 100, 
                   width: float = 300, height: float = 200, color: str = "#e6f3ff"):
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
             xmlns="http://www.w3.org/2000/svg">
        '''
        
        # Draw contexts (boxes)
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
        
        # Draw task connections (wires)
        for task in self.tasks.values():
            for successor_id in task.successors:
                if successor_id in self.tasks:
                    successor = self.tasks[successor_id]
                    # Draw arrow line
                    svg_content += f'''
                    <line x1="{task.x + 50}" y1="{task.y + 15}" 
                          x2="{successor.x}" y2="{successor.y + 15}"
                          stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
                    '''
        
        # Arrow marker definition
        svg_content += '''
        <defs>
            <marker id="arrowhead" markerWidth="10" markerHeight="7" 
                    refX="9" refY="3.5" orient="auto">
                <polygon points="0 0, 10 3.5, 0 7" fill="#666"/>
            </marker>
        </defs>
        '''
        
        # Draw tasks
        for task in self.tasks.values():
            task_color = task.color if task.color != "#ffffff" else self.get_status_color(task.status)
            svg_content += f'''
            <rect x="{task.x}" y="{task.y}" width="100" height="30"
                  fill="{task_color}" stroke="#333" stroke-width="1" rx="3"/>
            <text x="{task.x + 5}" y="{task.y + 20}" 
                  font-family="Arial" font-size="12" fill="#000">
                {task.name[:12]}{'...' if len(task.name) > 12 else ''}
            </text>
            '''
        
        svg_content += '</svg>'
        return svg_content
    
    def save_to_file(self, filename: str):
        data = {
            'contexts': {k: v.to_dict() for k, v in self.contexts.items()},
            'tasks': {k: v.to_dict() for k, v in self.tasks.items()},
            'zoom_level': self.zoom_level
        }
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        return f"Configuration saved to {filename}"
    
    def load_from_file(self, filename: str):
        try:
            with open(filename, 'r') as f:
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
                    successors=task_data['successors']
                )
                self.tasks[task.id] = task
            
            self.zoom_level = data.get('zoom_level', 1.0)
            return f"Configuration loaded from {filename}"
        except Exception as e:
            return f"Error loading file: {str(e)}"

# Global BPM tool instance
bpm_tool = BPMTool()

def create_gradio_interface():
    with gr.Blocks(title="BPM Workflow Designer", css="""
        .canvas-container { border: 1px solid #ccc; overflow: auto; }
        .control-panel { background: #f8f9fa; padding: 10px; border-radius: 5px; }
    """) as demo:
        
        gr.Markdown("# BPM Workflow Designer")
        gr.Markdown("Design and manage business process workflows with drag-and-drop functionality")
        
        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("## Controls")
                
                # Context controls
                with gr.Group():
                    gr.Markdown("### Context Management")
                    context_name = gr.Textbox(label="Context Name", placeholder="Enter context name")
                    context_color = gr.ColorPicker(label="Context Color", value="#e6f3ff")
                    context_x = gr.Number(label="X Position", value=100)
                    context_y = gr.Number(label="Y Position", value=100)
                    add_context_btn = gr.Button("Add Context", variant="primary")
                
                # Task controls
                with gr.Group():
                    gr.Markdown("### Task Management")
                    task_name = gr.Textbox(label="Task Name", placeholder="Enter task name")
                    task_context = gr.Dropdown(label="Context", choices=[], interactive=True)
                    task_status = gr.Dropdown(
                        label="Task Status",
                        choices=["default", "success", "failure", "skipped", "delayed"],
                        value="default"
                    )
                    task_color = gr.ColorPicker(label="Task Color", value="#ffffff")
                    task_x = gr.Number(label="X Position", value=0)
                    task_y = gr.Number(label="Y Position", value=0)
                    add_task_btn = gr.Button("Add Task", variant="primary")
                
                # Connection controls
                with gr.Group():
                    gr.Markdown("### Task Connections")
                    source_task = gr.Dropdown(label="Source Task", choices=[], interactive=True)
                    target_task = gr.Dropdown(label="Target Task", choices=[], interactive=True)
                    connect_btn = gr.Button("Connect Tasks", variant="secondary")
                
                # Zoom controls
                with gr.Group():
                    gr.Markdown("### Canvas Controls")
                    zoom_slider = gr.Slider(
                        minimum=0.5, maximum=3.0, value=1.0, step=0.1,
                        label="Zoom Level"
                    )
                
                # File operations
                with gr.Group():
                    gr.Markdown("### File Operations")
                    filename = gr.Textbox(label="Filename", value="workflow.json")
                    with gr.Row():
                        save_btn = gr.Button("Save", variant="primary")
                        load_btn = gr.Button("Load", variant="secondary")
                    file_status = gr.Textbox(label="Status", interactive=False)
            
            with gr.Column(scale=3):
                gr.Markdown("## Canvas")
                canvas = gr.HTML(value=bpm_tool.generate_svg(), elem_classes=["canvas-container"])
        
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
        
        def add_context_handler(name, color, x, y):
            if name:
                bpm_tool.add_context(name, x, y, color=color)
                return update_canvas(), *update_dropdowns()
            return gr.update(), gr.update(), gr.update(), gr.update()
        
        def add_task_handler(name, context_id, status, color, x, y):
            if name and context_id:
                task_status_enum = TaskStatus(status)
                bpm_tool.add_task(name, context_id, x, y, task_status_enum, color)
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
        
        def save_handler(filename):
            return bpm_tool.save_to_file(filename)
        
        def load_handler(filename):
            status = bpm_tool.load_from_file(filename)
            return status, update_canvas(), *update_dropdowns()
        
        # Event handlers
        add_context_btn.click(
            add_context_handler,
            inputs=[context_name, context_color, context_x, context_y],
            outputs=[canvas, task_context, source_task, target_task]
        )
        
        add_task_btn.click(
            add_task_handler,
            inputs=[task_name, task_context, task_status, task_color, task_x, task_y],
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
        
        save_btn.click(
            save_handler,
            inputs=[filename],
            outputs=[file_status]
        )
        
        load_btn.click(
            load_handler,
            inputs=[filename],
            outputs=[file_status, canvas, task_context, source_task, target_task]
        )
    
    return demo

if __name__ == "__main__":
    # Initialize with sample data
    ctx1_id = bpm_tool.add_context("Process Context", 50, 50, color="#e6f3ff")
    ctx2_id = bpm_tool.add_context("Review Context", 400, 50, color="#fff2e6")
    
    task1_id = bpm_tool.add_task("Start Task", ctx1_id, 70, 100, TaskStatus.SUCCESS)
    task2_id = bpm_tool.add_task("Process Data", ctx1_id, 70, 150, TaskStatus.DEFAULT)
    task3_id = bpm_tool.add_task("Review", ctx2_id, 420, 100, TaskStatus.DELAYED)
    
    bpm_tool.connect_tasks(task1_id, task2_id)
    bpm_tool.connect_tasks(task2_id, task3_id)
    
    demo = create_gradio_interface()
    demo.launch(share=True, debug=True)