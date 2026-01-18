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
    <title>BPM Workflow Designer</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            min-height: 100vh;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: rgba(255, 255, 255, 0.1);
            padding: 30px;
            border-radius: 15px;
            backdrop-filter: blur(10px);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        }
        .header {
            text-align: center;
            margin-bottom: 30px;
        }
        .controls {
            display: grid;
            grid-template-columns: 1fr 2fr;
            gap: 30px;
            margin-bottom: 30px;
        }
        .control-panel {
            background: rgba(255, 255, 255, 0.1);
            padding: 20px;
            border-radius: 10px;
        }
        .canvas-area {
            background: rgba(255, 255, 255, 0.9);
            border-radius: 10px;
            padding: 20px;
            min-height: 500px;
            position: relative;
        }
        .input-group {
            margin-bottom: 15px;
        }
        label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
        }
        input, select, button {
            width: 100%;
            padding: 10px;
            border: none;
            border-radius: 5px;
            margin-bottom: 10px;
            font-size: 14px;
        }
        button {
            background: #4CAF50;
            color: white;
            cursor: pointer;
            font-weight: bold;
            transition: background 0.3s;
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
        #canvas {
            width: 100%;
            height: 500px;
            border: 2px solid #ddd;
            border-radius: 8px;
            background: #f9f9f9;
            position: relative;
            overflow: hidden;
        }
        .context-box {
            position: absolute;
            border: 2px solid #333;
            border-radius: 8px;
            background: rgba(230, 243, 255, 0.8);
            padding: 10px;
            cursor: move;
            min-width: 200px;
            min-height: 150px;
        }
        .task-item {
            position: absolute;
            background: white;
            border: 1px solid #333;
            border-radius: 5px;
            padding: 8px;
            cursor: move;
            font-size: 12px;
            min-width: 80px;
            text-align: center;
        }
        .task-success { background: #28a745; color: white; }
        .task-failure { background: #dc3545; color: white; }
        .task-delayed { background: #fd7e14; color: white; }
        .task-skipped { background: #6c757d; color: white; }
        .connection-line {
            position: absolute;
            height: 2px;
            background: #666;
            transform-origin: left center;
        }
        .stats {
            background: rgba(255, 255, 255, 0.1);
            padding: 15px;
            border-radius: 8px;
            margin-top: 20px;
        }
        .feature-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-top: 20px;
        }
        .feature {
            background: rgba(255, 255, 255, 0.1);
            padding: 15px;
            border-radius: 8px;
            text-align: center;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔄 BPM Workflow Designer</h1>
            <p>Create and manage business process workflows with visual tools</p>
            <div style="background: rgba(76, 175, 80, 0.2); padding: 10px; border-radius: 5px; margin: 10px 0;">
                ✅ <strong>Successfully deployed on Vercel!</strong> - Serverless-optimized version
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
                <button onclick="clearCanvas()" style="background: #f44336;">🗑️ Clear All</button>
                <button onclick="saveWorkflow()" class="secondary-btn">💾 Save Workflow</button>
            </div>

            <div class="canvas-area">
                <h3 style="color: #333; margin-top: 0;">🎨 Workflow Canvas</h3>
                <div id="canvas"></div>
            </div>
        </div>

        <div class="stats">
            <h3>📊 Workflow Statistics</h3>
            <div id="stats">
                <p>📦 Contexts: <span id="contextCount">0</span></p>
                <p>⚙️ Tasks: <span id="taskCount">0</span></p>
                <p>🔗 Connections: <span id="connectionCount">0</span></p>
            </div>
        </div>

        <div class="feature-grid">
            <div class="feature">
                <h4>🎨 Visual Design</h4>
                <p>Drag-and-drop workflow creation</p>
            </div>
            <div class="feature">
                <h4>📦 Context Boxes</h4>
                <p>Organize related processes</p>
            </div>
            <div class="feature">
                <h4>🔗 Task Flow</h4>
                <p>Connect tasks with visual arrows</p>
            </div>
            <div class="feature">
                <h4>📊 Real-time Stats</h4>
                <p>Monitor workflow metrics</p>
            </div>
        </div>
    </div>

    <script>
        let contexts = [];
        let tasks = [];
        let connections = [];
        let nextId = 1;

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

            const context = {
                id: generateId(),
                name: name.trim(),
                color: color,
                x: Math.random() * 300 + 50,
                y: Math.random() * 200 + 50,
                width: 200,
                height: 150
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

            const task = {
                id: generateId(),
                name: name.trim(),
                status: status,
                contextId: contextId,
                x: context.x + 20 + (Math.random() * 100),
                y: context.y + 40 + (Math.random() * 60)
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

            const connection = {
                id: generateId(),
                sourceId: sourceId,
                targetId: targetId
            };

            connections.push(connection);
            renderCanvas();
            updateStats();
        }

        function renderCanvas() {
            const canvas = document.getElementById('canvas');
            canvas.innerHTML = '';

            // Render contexts
            contexts.forEach(context => {
                const div = document.createElement('div');
                div.className = 'context-box';
                div.style.left = context.x + 'px';
                div.style.top = context.y + 'px';
                div.style.width = context.width + 'px';
                div.style.height = context.height + 'px';
                div.style.backgroundColor = context.color;
                div.innerHTML = `<strong>${context.name}</strong>`;
                canvas.appendChild(div);
            });

            // Render connections
            connections.forEach(connection => {
                const sourceTask = tasks.find(t => t.id === connection.sourceId);
                const targetTask = tasks.find(t => t.id === connection.targetId);
                
                if (sourceTask && targetTask) {
                    const line = document.createElement('div');
                    line.className = 'connection-line';
                    
                    const dx = targetTask.x - (sourceTask.x + 40);
                    const dy = targetTask.y - sourceTask.y;
                    const length = Math.sqrt(dx * dx + dy * dy);
                    const angle = Math.atan2(dy, dx) * 180 / Math.PI;
                    
                    line.style.left = (sourceTask.x + 40) + 'px';
                    line.style.top = (sourceTask.y + 15) + 'px';
                    line.style.width = length + 'px';
                    line.style.transform = `rotate(${angle}deg)`;
                    
                    canvas.appendChild(line);
                }
            });

            // Render tasks
            tasks.forEach(task => {
                const div = document.createElement('div');
                div.className = `task-item task-${task.status}`;
                div.style.left = task.x + 'px';
                div.style.top = task.y + 'px';
                div.innerHTML = task.name;
                canvas.appendChild(div);
            });
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
                timestamp: new Date().toISOString()
            };
            
            const dataStr = JSON.stringify(workflow, null, 2);
            const dataBlob = new Blob([dataStr], {type: 'application/json'});
            const url = URL.createObjectURL(dataBlob);
            
            const link = document.createElement('a');
            link.href = url;
            link.download = 'bpm_workflow.json';
            link.click();
            
            URL.revokeObjectURL(url);
        }

        // Initialize with sample data
        function initializeSample() {
            // Add sample contexts
            contexts.push({
                id: 'ctx1',
                name: 'Data Processing',
                color: '#e6f3ff',
                x: 50,
                y: 50,
                width: 200,
                height: 150
            });
            
            contexts.push({
                id: 'ctx2',
                name: 'Quality Control',
                color: '#fff2e6',
                x: 300,
                y: 50,
                width: 200,
                height: 150
            });
            
            // Add sample tasks
            tasks.push({
                id: 'task1',
                name: 'Start Process',
                status: 'success',
                contextId: 'ctx1',
                x: 70,
                y: 90
            });
            
            tasks.push({
                id: 'task2',
                name: 'Process Data',
                status: 'default',
                contextId: 'ctx1',
                x: 170,
                y: 90
            });
            
            tasks.push({
                id: 'task3',
                name: 'Quality Check',
                status: 'delayed',
                contextId: 'ctx2',
                x: 320,
                y: 90
            });
            
            // Add sample connection
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
            
            nextId = 10; // Start IDs after sample data
            
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
        
        response = {"status": "success", "message": "BPM Tool is working!"}
        self.wfile.write(json.dumps(response).encode())