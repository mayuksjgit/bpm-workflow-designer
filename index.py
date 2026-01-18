from http.server import BaseHTTPRequestHandler
import json
import uuid
from urllib.parse import parse_qs, urlparse

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        html_content = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BPM Workflow Designer - Organized Layout</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            min-height: 100vh;
            user-select: none;
        }
        .container {
            max-width: 1400px;
            margin: 0 auto;
            background: rgba(255, 255, 255, 0.1);
            padding: 20px;
            border-radius: 15px;
            backdrop-filter: blur(10px);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        }
        .header {
            text-align: center;
            margin-bottom: 20px;
        }
        .controls {
            display: grid;
            grid-template-columns: 300px 1fr;
            gap: 20px;
            margin-bottom: 20px;
        }
        .control-panel {
            background: rgba(255, 255, 255, 0.1);
            padding: 20px;
            border-radius: 10px;
            height: fit-content;
        }
        .canvas-area {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 10px;
            padding: 10px;
            position: relative;
        }
        .input-group {
            margin-bottom: 15px;
        }
        label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
            font-size: 12px;
        }
        input, select, button {
            width: 100%;
            padding: 8px;
            border: none;
            border-radius: 5px;
            margin-bottom: 8px;
            font-size: 12px;
            box-sizing: border-box;
        }
        button {
            background: #4CAF50;
            color: white;
            cursor: pointer;
            font-weight: bold;
            transition: background 0.3s;
            padding: 10px;
        }
        button:hover {
            background: #45a049;
        }
        .secondary-btn {
            background: #2196F3;
        }
        .secondary-btn:hover {
            background: #1976D2;
        }
        .danger-btn {
            background: #f44336;
        }
        .danger-btn:hover {
            background: #d32f2f;
        }
        .auto-arrange-btn {
            background: #9C27B0;
        }
        .auto-arrange-btn:hover {
            background: #7B1FA2;
        }
        #canvas {
            width: 100%;
            height: 600px;
            border: 2px solid #ddd;
            border-radius: 8px;
            background: #f9f9f9;
            position: relative;
            overflow: hidden;
            cursor: default;
        }
        .context-box {
            position: absolute;
            border: 3px solid #333;
            border-radius: 12px;
            background: rgba(230, 243, 255, 0.9);
            padding: 15px;
            cursor: move;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            transition: all 0.2s;
            z-index: 10;
        }
        .context-box:hover {
            box-shadow: 0 6px 16px rgba(0,0,0,0.25);
            transform: translateY(-2px);
        }
        .context-box.dragging {
            box-shadow: 0 8px 20px rgba(0,0,0,0.35);
            transform: rotate(1deg) scale(1.02);
            z-index: 1000;
        }
        .context-header {
            font-weight: bold;
            font-size: 16px;
            color: #333;
            margin-bottom: 10px;
            border-bottom: 2px solid #ccc;
            padding-bottom: 8px;
            background: rgba(255, 255, 255, 0.8);
            padding: 8px;
            border-radius: 6px;
            text-align: center;
        }
        .context-label {
            position: absolute;
            left: 15px;
            top: 15px;
            width: 100px;
            height: 80px;
            background: rgba(0, 0, 0, 0.1);
            border: 2px solid #666;
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            font-size: 14px;
            color: #333;
        }
        .task-area {
            margin-left: 130px;
            padding: 20px 0;
            min-height: 60px;
            display: flex;
            align-items: center;
            gap: 20px;
        }
        .task-item {
            background: white;
            border: 2px solid #333;
            border-radius: 8px;
            padding: 12px 16px;
            cursor: move;
            font-size: 12px;
            font-weight: bold;
            text-align: center;
            box-shadow: 0 3px 6px rgba(0,0,0,0.15);
            transition: all 0.2s;
            z-index: 20;
            min-width: 80px;
            position: relative;
        }
        .task-item:hover {
            box-shadow: 0 5px 10px rgba(0,0,0,0.25);
            transform: translateY(-2px) scale(1.05);
        }
        .task-item.dragging {
            box-shadow: 0 8px 16px rgba(0,0,0,0.35);
            transform: scale(1.1) rotate(2deg);
            z-index: 1001;
        }
        .task-success { 
            background: linear-gradient(135deg, #28a745, #20c997); 
            color: white; 
            border-color: #1e7e34; 
        }
        .task-failure { 
            background: linear-gradient(135deg, #dc3545, #e74c3c); 
            color: white; 
            border-color: #c82333; 
        }
        .task-delayed { 
            background: linear-gradient(135deg, #fd7e14, #ff9500); 
            color: white; 
            border-color: #e55a00; 
        }
        .task-skipped { 
            background: linear-gradient(135deg, #6c757d, #868e96); 
            color: white; 
            border-color: #545b62; 
        }
        .task-default { 
            background: linear-gradient(135deg, #ffffff, #f8f9fa); 
            color: #333; 
            border-color: #333; 
        }
        .connection-line {
            position: absolute;
            height: 4px;
            background: linear-gradient(90deg, #4CAF50, #45a049);
            border-radius: 2px;
            z-index: 5;
            box-shadow: 0 2px 4px rgba(0,0,0,0.2);
        }
        .connection-arrow {
            position: absolute;
            width: 0;
            height: 0;
            border-left: 12px solid #4CAF50;
            border-top: 6px solid transparent;
            border-bottom: 6px solid transparent;
            z-index: 6;
            filter: drop-shadow(0 2px 4px rgba(0,0,0,0.2));
        }
        .inter-context-connection {
            background: linear-gradient(90deg, #2196F3, #1976D2);
        }
        .inter-context-arrow {
            border-left-color: #2196F3;
        }
        .stats {
            background: rgba(255, 255, 255, 0.1);
            padding: 15px;
            border-radius: 8px;
            margin-top: 15px;
        }
        .grid-toggle {
            background: rgba(255, 255, 255, 0.1);
            padding: 10px;
            border-radius: 5px;
            margin-bottom: 15px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔄 BPM Workflow Designer</h1>
            <p>Organized Layout - Contexts Stacked Vertically, Tasks Flow Horizontally</p>
            <div style="background: rgba(76, 175, 80, 0.2); padding: 8px; border-radius: 5px; margin: 10px 0; font-size: 14px;">
                ✅ <strong>Enhanced Layout!</strong> - Contexts arranged vertically, tasks flow horizontally within each context
            </div>
        </div>

        <div class="controls">
            <div class="control-panel">
                <h3>📦 Context Management</h3>
                <div class="input-group">
                    <label>Context Name:</label>
                    <input type="text" id="contextName" placeholder="e.g., Data Processing">
                </div>
                <div class="input-group">
                    <label>Context Color:</label>
                    <input type="color" id="contextColor" value="#e6f3ff">
                </div>
                <button onclick="addContext()">➕ Add Context</button>

                <h3>⚙️ Task Management</h3>
                <div class="input-group">
                    <label>Task Name:</label>
                    <input type="text" id="taskName" placeholder="e.g., Validate Input">
                </div>
                <div class="input-group">
                    <label>Task Status:</label>
                    <select id="taskStatus">
                        <option value="default">Default</option>
                        <option value="success">✅ Success</option>
                        <option value="failure">❌ Failure</option>
                        <option value="delayed">⏰ Delayed</option>
                        <option value="skipped">⏭️ Skipped</option>
                    </select>
                </div>
                <div class="input-group">
                    <label>Parent Context:</label>
                    <select id="taskContext">
                        <option value="">Select Context</option>
                    </select>
                </div>
                <button onclick="addTask()">➕ Add Task</button>

                <h3>🔗 Connections</h3>
                <div class="input-group">
                    <label>Source Task:</label>
                    <select id="sourceTask">
                        <option value="">Select Source</option>
                    </select>
                </div>
                <div class="input-group">
                    <label>Target Task:</label>
                    <select id="targetTask">
                        <option value="">Select Target</option>
                    </select>
                </div>
                <button onclick="connectTasks()" class="secondary-btn">🔗 Connect Tasks</button>

                <h3>🎛️ Canvas Controls</h3>
                <button onclick="autoArrange()" class="auto-arrange-btn">🎯 Auto Arrange</button>
                <button onclick="clearCanvas()" class="danger-btn">🗑️ Clear All</button>
                <button onclick="saveWorkflow()" class="secondary-btn">💾 Save Workflow</button>

                <div class="stats">
                    <h4>📊 Statistics</h4>
                    <p>📦 Contexts: <span id="contextCount">0</span></p>
                    <p>⚙️ Tasks: <span id="taskCount">0</span></p>
                    <p>🔗 Connections: <span id="connectionCount">0</span></p>
                </div>
            </div>

            <div class="canvas-area">
                <h3 style="color: #333; margin: 0 0 10px 0;">🎨 Workflow Canvas - Organized Layout</h3>
                <div id="canvas"></div>
            </div>
        </div>
    </div>

    <script>
        let contexts = [];
        let tasks = [];
        let connections = [];
        let nextId = 1;
        let draggedElement = null;
        let dragOffset = { x: 0, y: 0 };

        function generateId() {
            return 'item_' + (nextId++);
        }

        function addContext() {
            const name = document.getElementById('contextName').value;
            const color = document.getElementById('contextColor').value;
            
            if (!name.trim()) {
                alert('Please enter a context name');
                return;
            }

            const contextIndex = contexts.length;
            const context = {
                id: generateId(),
                name: name.trim(),
                color: color,
                width: 800,
                height: 120,
                x: 50,
                y: 50 + (contextIndex * 150) // Stack contexts vertically
            };

            contexts.push(context);
            renderCanvas();
            updateDropdowns();
            updateStats();
            
            document.getElementById('contextName').value = '';
        }

        function addTask() {
            const name = document.getElementById('taskName').value;
            const status = document.getElementById('taskStatus').value;
            const contextId = document.getElementById('taskContext').value;
            
            if (!name.trim()) {
                alert('Please enter a task name');
                return;
            }
            
            if (!contextId) {
                alert('Please select a parent context');
                return;
            }

            const context = contexts.find(c => c.id === contextId);
            if (!context) return;

            // Position task horizontally within context
            const contextTasks = tasks.filter(t => t.contextId === contextId);
            const taskIndex = contextTasks.length;

            const task = {
                id: generateId(),
                name: name.trim(),
                status: status,
                contextId: contextId,
                x: context.x + 180 + (taskIndex * 140), // Horizontal flow
                y: context.y + 40 // Center vertically in context
            };

            tasks.push(task);
            renderCanvas();
            updateDropdowns();
            updateStats();
            
            document.getElementById('taskName').value = '';
        }

        function connectTasks() {
            const sourceId = document.getElementById('sourceTask').value;
            const targetId = document.getElementById('targetTask').value;
            
            if (!sourceId || !targetId) {
                alert('Please select both source and target tasks');
                return;
            }
            
            if (sourceId === targetId) {
                alert('Cannot connect a task to itself');
                return;
            }

            // Check if connection already exists
            const existingConnection = connections.find(c => 
                c.sourceId === sourceId && c.targetId === targetId
            );
            
            if (existingConnection) {
                alert('Connection already exists');
                return;
            }

            const connection = {
                id: generateId(),
                sourceId: sourceId,
                targetId: targetId
            };

            connections.push(connection);
            renderCanvas();
            updateStats();
        }

        function autoArrange() {
            // Arrange contexts vertically
            contexts.forEach((context, index) => {
                context.x = 50;
                context.y = 50 + (index * 150);
                context.width = 800;
                context.height = 120;
                
                // Arrange tasks horizontally within context
                const contextTasks = tasks.filter(t => t.contextId === context.id);
                contextTasks.forEach((task, taskIndex) => {
                    task.x = context.x + 180 + (taskIndex * 140);
                    task.y = context.y + 40;
                });
            });
            
            renderCanvas();
        }

        function renderCanvas() {
            const canvas = document.getElementById('canvas');
            canvas.innerHTML = '';

            // Render connections first (behind other elements)
            connections.forEach(connection => {
                const sourceTask = tasks.find(t => t.id === connection.sourceId);
                const targetTask = tasks.find(t => t.id === connection.targetId);
                
                if (sourceTask && targetTask) {
                    const sourceContext = contexts.find(c => c.id === sourceTask.contextId);
                    const targetContext = contexts.find(c => c.id === targetTask.contextId);
                    const isInterContext = sourceContext.id !== targetContext.id;
                    
                    const startX = sourceTask.x + 50; // Center of source task
                    const startY = sourceTask.y + 20;
                    const endX = targetTask.x;
                    const endY = targetTask.y + 20;
                    
                    // Create connection line
                    const line = document.createElement('div');
                    line.className = isInterContext ? 'connection-line inter-context-connection' : 'connection-line';
                    
                    if (isInterContext) {
                        // Vertical then horizontal connection for inter-context
                        const midY = sourceContext.y + sourceContext.height + 20;
                        
                        // Vertical line down from source
                        const verticalLine = document.createElement('div');
                        verticalLine.className = 'connection-line inter-context-connection';
                        verticalLine.style.left = startX + 'px';
                        verticalLine.style.top = startY + 'px';
                        verticalLine.style.width = '4px';
                        verticalLine.style.height = (midY - startY) + 'px';
                        canvas.appendChild(verticalLine);
                        
                        // Horizontal line across
                        const horizontalLine = document.createElement('div');
                        horizontalLine.className = 'connection-line inter-context-connection';
                        horizontalLine.style.left = Math.min(startX, endX) + 'px';
                        horizontalLine.style.top = midY + 'px';
                        horizontalLine.style.width = Math.abs(endX - startX) + 'px';
                        horizontalLine.style.height = '4px';
                        canvas.appendChild(horizontalLine);
                        
                        // Vertical line up to target
                        const verticalLine2 = document.createElement('div');
                        verticalLine2.className = 'connection-line inter-context-connection';
                        verticalLine2.style.left = endX + 'px';
                        verticalLine2.style.top = midY + 'px';
                        verticalLine2.style.width = '4px';
                        verticalLine2.style.height = (endY - midY) + 'px';
                        canvas.appendChild(verticalLine2);
                        
                        // Arrow at target
                        const arrow = document.createElement('div');
                        arrow.className = 'connection-arrow inter-context-arrow';
                        arrow.style.left = (endX - 12) + 'px';
                        arrow.style.top = (endY - 6) + 'px';
                        canvas.appendChild(arrow);
                    } else {
                        // Direct horizontal connection within context
                        const dx = endX - startX;
                        const length = Math.abs(dx);
                        
                        line.style.left = startX + 'px';
                        line.style.top = (startY - 2) + 'px';
                        line.style.width = length + 'px';
                        canvas.appendChild(line);
                        
                        // Arrow head
                        const arrow = document.createElement('div');
                        arrow.className = 'connection-arrow';
                        arrow.style.left = (endX - 12) + 'px';
                        arrow.style.top = (endY - 6) + 'px';
                        canvas.appendChild(arrow);
                    }
                }
            });

            // Render contexts
            contexts.forEach(context => {
                const div = document.createElement('div');
                div.className = 'context-box';
                div.style.left = context.x + 'px';
                div.style.top = context.y + 'px';
                div.style.width = context.width + 'px';
                div.style.height = context.height + 'px';
                div.style.backgroundColor = context.color;
                div.dataset.id = context.id;
                div.dataset.type = 'context';
                
                const contextTasks = tasks.filter(t => t.contextId === context.id);
                div.innerHTML = `
                    <div class="context-label">${context.name}</div>
                    <div class="task-area">
                        <!-- Tasks will be positioned here -->
                    </div>
                `;
                
                // Add drag functionality
                div.addEventListener('mousedown', startDrag);
                canvas.appendChild(div);
            });

            // Render tasks
            tasks.forEach(task => {
                const div = document.createElement('div');
                div.className = `task-item task-${task.status}`;
                div.style.left = task.x + 'px';
                div.style.top = task.y + 'px';
                div.innerHTML = task.name.length > 10 ? task.name.substring(0, 10) + '...' : task.name;
                div.dataset.id = task.id;
                div.dataset.type = 'task';
                
                // Add drag functionality
                div.addEventListener('mousedown', startDrag);
                canvas.appendChild(div);
            });
        }

        function startDrag(e) {
            e.preventDefault();
            draggedElement = e.target.closest('.context-box, .task-item');
            if (!draggedElement) return;
            
            draggedElement.classList.add('dragging');
            
            const rect = draggedElement.getBoundingClientRect();
            const canvasRect = document.getElementById('canvas').getBoundingClientRect();
            
            dragOffset.x = e.clientX - rect.left;
            dragOffset.y = e.clientY - rect.top;
            
            document.addEventListener('mousemove', drag);
            document.addEventListener('mouseup', stopDrag);
        }

        function drag(e) {
            if (!draggedElement) return;
            
            const canvas = document.getElementById('canvas');
            const canvasRect = canvas.getBoundingClientRect();
            
            let x = e.clientX - canvasRect.left - dragOffset.x;
            let y = e.clientY - canvasRect.top - dragOffset.y;
            
            // Constrain to canvas bounds
            const elementWidth = draggedElement.offsetWidth;
            const elementHeight = draggedElement.offsetHeight;
            
            x = Math.max(0, Math.min(x, canvas.offsetWidth - elementWidth));
            y = Math.max(0, Math.min(y, canvas.offsetHeight - elementHeight));
            
            draggedElement.style.left = x + 'px';
            draggedElement.style.top = y + 'px';
        }

        function stopDrag(e) {
            if (!draggedElement) return;
            
            const elementId = draggedElement.dataset.id;
            const elementType = draggedElement.dataset.type;
            
            const x = parseInt(draggedElement.style.left);
            const y = parseInt(draggedElement.style.top);
            
            // Update data model
            if (elementType === 'context') {
                const context = contexts.find(c => c.id === elementId);
                if (context) {
                    const deltaX = x - context.x;
                    const deltaY = y - context.y;
                    context.x = x;
                    context.y = y;
                    
                    // Move all tasks in this context
                    tasks.filter(t => t.contextId === context.id).forEach(task => {
                        task.x += deltaX;
                        task.y += deltaY;
                    });
                }
            } else if (elementType === 'task') {
                const task = tasks.find(t => t.id === elementId);
                if (task) {
                    task.x = x;
                    task.y = y;
                }
            }
            
            draggedElement.classList.remove('dragging');
            draggedElement = null;
            
            document.removeEventListener('mousemove', drag);
            document.removeEventListener('mouseup', stopDrag);
            
            // Re-render to update connections
            renderCanvas();
        }

        function updateDropdowns() {
            const contextSelect = document.getElementById('taskContext');
            const sourceSelect = document.getElementById('sourceTask');
            const targetSelect = document.getElementById('targetTask');
            
            // Update context dropdown
            contextSelect.innerHTML = '<option value="">Select Context</option>';
            contexts.forEach(context => {
                const option = document.createElement('option');
                option.value = context.id;
                option.textContent = context.name;
                contextSelect.appendChild(option);
            });
            
            // Update task dropdowns
            const taskOptions = '<option value="">Select Task</option>' + 
                tasks.map(task => `<option value="${task.id}">${task.name}</option>`).join('');
            
            sourceSelect.innerHTML = taskOptions;
            targetSelect.innerHTML = taskOptions;
        }

        function updateStats() {
            document.getElementById('contextCount').textContent = contexts.length;
            document.getElementById('taskCount').textContent = tasks.length;
            document.getElementById('connectionCount').textContent = connections.length;
        }

        function clearCanvas() {
            if (confirm('Are you sure you want to clear all workflows?')) {
                contexts = [];
                tasks = [];
                connections = [];
                renderCanvas();
                updateDropdowns();
                updateStats();
            }
        }

        function saveWorkflow() {
            const workflow = {
                contexts: contexts,
                tasks: tasks,
                connections: connections,
                timestamp: new Date().toISOString(),
                version: "3.0-organized-layout"
            };
            
            const dataStr = JSON.stringify(workflow, null, 2);
            const dataBlob = new Blob([dataStr], {type: 'application/json'});
            const url = URL.createObjectURL(dataBlob);
            
            const link = document.createElement('a');
            link.href = url;
            link.download = 'bpm_workflow_organized.json';
            link.click();
            
            URL.revokeObjectURL(url);
        }

        // Initialize with sample data matching your expected layout
        function initializeSample() {
            // Add contexts vertically stacked
            contexts.push({
                id: 'ctx1',
                name: 'Context1',
                color: '#e6f3ff',
                x: 50,
                y: 50,
                width: 800,
                height: 120
            });
            
            contexts.push({
                id: 'ctx2',
                name: 'Context2',
                color: '#fff2e6',
                x: 50,
                y: 200,
                width: 800,
                height: 120
            });
            
            // Add tasks horizontally within contexts
            tasks.push({
                id: 'task1',
                name: 'Task 1',
                status: 'success',
                contextId: 'ctx1',
                x: 230,
                y: 90
            });
            
            tasks.push({
                id: 'task2',
                name: 'Task 2',
                status: 'success',
                contextId: 'ctx1',
                x: 370,
                y: 90
            });
            
            tasks.push({
                id: 'task3',
                name: 'Task 1',
                status: 'success',
                contextId: 'ctx2',
                x: 230,
                y: 240
            });
            
            tasks.push({
                id: 'task4',
                name: 'Task 2',
                status: 'default',
                contextId: 'ctx2',
                x: 370,
                y: 240
            });
            
            // Add connections
            connections.push({
                id: 'conn1',
                sourceId: 'task1',
                targetId: 'task2'
            });
            
            connections.push({
                id: 'conn2',
                sourceId: 'task2',
                targetId: 'task3'
            });
            
            connections.push({
                id: 'conn3',
                sourceId: 'task3',
                targetId: 'task4'
            });
            
            nextId = 20;
            
            renderCanvas();
            updateDropdowns();
            updateStats();
        }

        // Initialize the application
        document.addEventListener('DOMContentLoaded', function() {
            initializeSample();
        });
    </script>
</body>
</html>
        '''
        
        self.wfile.write(html_content.encode())

    def do_POST(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        response = {"status": "success", "message": "BPM Tool with Organized Layout is working!"}
        self.wfile.write(json.dumps(response).encode())