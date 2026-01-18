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
    <title>BPM Workflow Designer - Drag & Drop</title>
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
            border: 2px solid #333;
            border-radius: 8px;
            background: rgba(230, 243, 255, 0.9);
            padding: 10px;
            cursor: move;
            min-width: 220px;
            min-height: 160px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            transition: box-shadow 0.2s;
            z-index: 10;
        }
        .context-box:hover {
            box-shadow: 0 6px 12px rgba(0,0,0,0.2);
        }
        .context-box.dragging {
            box-shadow: 0 8px 16px rgba(0,0,0,0.3);
            transform: rotate(2deg);
            z-index: 1000;
        }
        .context-header {
            font-weight: bold;
            font-size: 14px;
            color: #333;
            margin-bottom: 8px;
            border-bottom: 1px solid #ccc;
            padding-bottom: 5px;
        }
        .context-stats {
            font-size: 10px;
            color: #666;
            margin-top: 5px;
        }
        .task-item {
            position: absolute;
            background: white;
            border: 2px solid #333;
            border-radius: 5px;
            padding: 8px;
            cursor: move;
            font-size: 11px;
            min-width: 80px;
            text-align: center;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            transition: all 0.2s;
            z-index: 20;
        }
        .task-item:hover {
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
            transform: scale(1.05);
        }
        .task-item.dragging {
            box-shadow: 0 6px 12px rgba(0,0,0,0.3);
            transform: scale(1.1) rotate(3deg);
            z-index: 1001;
        }
        .task-success { background: #28a745; color: white; border-color: #1e7e34; }
        .task-failure { background: #dc3545; color: white; border-color: #c82333; }
        .task-delayed { background: #fd7e14; color: white; border-color: #e55a00; }
        .task-skipped { background: #6c757d; color: white; border-color: #545b62; }
        .task-default { background: #ffffff; color: #333; border-color: #333; }
        .connection-line {
            position: absolute;
            height: 3px;
            background: linear-gradient(90deg, #666, #999);
            transform-origin: left center;
            z-index: 5;
            border-radius: 2px;
        }
        .connection-arrow {
            position: absolute;
            width: 0;
            height: 0;
            border-left: 8px solid #666;
            border-top: 4px solid transparent;
            border-bottom: 4px solid transparent;
            z-index: 6;
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
        .grid-overlay {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            opacity: 0.1;
            pointer-events: none;
            background-image: 
                linear-gradient(to right, #333 1px, transparent 1px),
                linear-gradient(to bottom, #333 1px, transparent 1px);
            background-size: 20px 20px;
        }
        .snap-indicator {
            position: absolute;
            border: 2px dashed #4CAF50;
            background: rgba(76, 175, 80, 0.1);
            pointer-events: none;
            z-index: 999;
            display: none;
        }
        .collision-warning {
            position: absolute;
            background: #ff5722;
            color: white;
            padding: 5px 10px;
            border-radius: 15px;
            font-size: 10px;
            z-index: 1002;
            display: none;
        }
        .auto-arrange-btn {
            background: #9C27B0;
        }
        .auto-arrange-btn:hover {
            background: #7B1FA2;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔄 BPM Workflow Designer</h1>
            <p>Drag & Drop Business Process Management Tool</p>
            <div style="background: rgba(76, 175, 80, 0.2); padding: 8px; border-radius: 5px; margin: 10px 0; font-size: 14px;">
                ✅ <strong>Enhanced with Drag & Drop!</strong> - Move contexts and tasks freely
            </div>
        </div>

        <div class="controls">
            <div class="control-panel">
                <div class="grid-toggle">
                    <label>
                        <input type="checkbox" id="showGrid" checked> Show Grid
                    </label>
                    <label>
                        <input type="checkbox" id="snapToGrid" checked> Snap to Grid
                    </label>
                </div>

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
                <h3 style="color: #333; margin: 0 0 10px 0;">🎨 Workflow Canvas - Drag & Drop Enabled</h3>
                <div id="canvas">
                    <div class="grid-overlay" id="gridOverlay"></div>
                    <div class="snap-indicator" id="snapIndicator"></div>
                    <div class="collision-warning" id="collisionWarning">⚠️ Overlap detected!</div>
                </div>
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
        let gridSize = 20;
        let showGrid = true;
        let snapToGrid = true;

        function generateId() {
            return 'item_' + (nextId++);
        }

        function snapToGridPosition(x, y) {
            if (!snapToGrid) return { x, y };
            return {
                x: Math.round(x / gridSize) * gridSize,
                y: Math.round(y / gridSize) * gridSize
            };
        }

        function checkCollision(element, x, y, width, height) {
            const elementRect = { x, y, width, height };
            
            // Check collision with contexts
            for (let context of contexts) {
                if (context.id === element.id) continue;
                const contextRect = {
                    x: context.x,
                    y: context.y,
                    width: context.width,
                    height: context.height
                };
                if (rectsOverlap(elementRect, contextRect)) {
                    return true;
                }
            }
            
            // Check collision with tasks
            for (let task of tasks) {
                if (task.id === element.id) continue;
                const taskRect = {
                    x: task.x,
                    y: task.y,
                    width: 90,
                    height: 35
                };
                if (rectsOverlap(elementRect, taskRect)) {
                    return true;
                }
            }
            
            return false;
        }

        function rectsOverlap(rect1, rect2) {
            return !(rect1.x + rect1.width <= rect2.x || 
                    rect2.x + rect2.width <= rect1.x || 
                    rect1.y + rect1.height <= rect2.y || 
                    rect2.y + rect2.height <= rect1.y);
        }

        function findNonOverlappingPosition(element, preferredX, preferredY, width, height) {
            let x = preferredX;
            let y = preferredY;
            let attempts = 0;
            const maxAttempts = 100;
            
            while (checkCollision(element, x, y, width, height) && attempts < maxAttempts) {
                x += gridSize;
                if (x + width > 1000) {
                    x = 0;
                    y += gridSize;
                }
                if (y + height > 580) {
                    y = 0;
                }
                attempts++;
            }
            
            return snapToGridPosition(x, y);
        }

        function addContext() {
            const name = document.getElementById('contextName').value;
            const color = document.getElementById('contextColor').value;
            
            if (!name.trim()) {
                alert('Please enter a context name');
                return;
            }

            const width = 220;
            const height = 160;
            const preferredX = Math.random() * 300 + 50;
            const preferredY = Math.random() * 200 + 50;
            
            const context = {
                id: generateId(),
                name: name.trim(),
                color: color,
                width: width,
                height: height,
                x: 0,
                y: 0
            };

            const position = findNonOverlappingPosition(context, preferredX, preferredY, width, height);
            context.x = position.x;
            context.y = position.y;

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

            const width = 90;
            const height = 35;
            const preferredX = context.x + 20;
            const preferredY = context.y + 40;

            const task = {
                id: generateId(),
                name: name.trim(),
                status: status,
                contextId: contextId,
                x: 0,
                y: 0
            };

            const position = findNonOverlappingPosition(task, preferredX, preferredY, width, height);
            task.x = position.x;
            task.y = position.y;

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
            const canvasWidth = 1000;
            const canvasHeight = 580;
            const contextSpacing = 250;
            const taskSpacing = 100;
            
            // Arrange contexts in a grid
            let contextX = 50;
            let contextY = 50;
            let contextsPerRow = Math.floor(canvasWidth / contextSpacing);
            
            contexts.forEach((context, index) => {
                context.x = contextX;
                context.y = contextY;
                
                // Arrange tasks within this context
                const contextTasks = tasks.filter(t => t.contextId === context.id);
                let taskX = context.x + 20;
                let taskY = context.y + 40;
                let tasksPerRow = 2;
                
                contextTasks.forEach((task, taskIndex) => {
                    task.x = taskX;
                    task.y = taskY;
                    
                    taskX += taskSpacing;
                    if ((taskIndex + 1) % tasksPerRow === 0) {
                        taskX = context.x + 20;
                        taskY += 45;
                    }
                });
                
                contextX += contextSpacing;
                if ((index + 1) % contextsPerRow === 0) {
                    contextX = 50;
                    contextY += 200;
                }
            });
            
            renderCanvas();
        }

        function renderCanvas() {
            const canvas = document.getElementById('canvas');
            // Clear only dynamic content, keep grid and indicators
            const dynamicElements = canvas.querySelectorAll('.context-box, .task-item, .connection-line, .connection-arrow');
            dynamicElements.forEach(el => el.remove());

            // Render connections first (behind other elements)
            connections.forEach(connection => {
                const sourceTask = tasks.find(t => t.id === connection.sourceId);
                const targetTask = tasks.find(t => t.id === connection.targetId);
                
                if (sourceTask && targetTask) {
                    const startX = sourceTask.x + 45;
                    const startY = sourceTask.y + 17;
                    const endX = targetTask.x;
                    const endY = targetTask.y + 17;
                    
                    const dx = endX - startX;
                    const dy = endY - startY;
                    const length = Math.sqrt(dx * dx + dy * dy);
                    const angle = Math.atan2(dy, dx) * 180 / Math.PI;
                    
                    // Connection line
                    const line = document.createElement('div');
                    line.className = 'connection-line';
                    line.style.left = startX + 'px';
                    line.style.top = (startY - 1) + 'px';
                    line.style.width = length + 'px';
                    line.style.transform = `rotate(${angle}deg)`;
                    canvas.appendChild(line);
                    
                    // Arrow head
                    const arrow = document.createElement('div');
                    arrow.className = 'connection-arrow';
                    arrow.style.left = (endX - 8) + 'px';
                    arrow.style.top = (endY - 4) + 'px';
                    canvas.appendChild(arrow);
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
                    <div class="context-header">${context.name}</div>
                    <div class="context-stats">${contextTasks.length} task(s)</div>
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
                div.innerHTML = task.name.length > 8 ? task.name.substring(0, 8) + '...' : task.name;
                div.dataset.id = task.id;
                div.dataset.type = 'task';
                
                // Add drag functionality
                div.addEventListener('mousedown', startDrag);
                canvas.appendChild(div);
            });
        }

        function startDrag(e) {
            e.preventDefault();
            draggedElement = e.target;
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
            
            // Snap to grid if enabled
            if (snapToGrid) {
                const snapped = snapToGridPosition(x, y);
                x = snapped.x;
                y = snapped.y;
                
                // Show snap indicator
                const indicator = document.getElementById('snapIndicator');
                indicator.style.left = x + 'px';
                indicator.style.top = y + 'px';
                indicator.style.width = elementWidth + 'px';
                indicator.style.height = elementHeight + 'px';
                indicator.style.display = 'block';
            }
            
            draggedElement.style.left = x + 'px';
            draggedElement.style.top = y + 'px';
            
            // Check for collisions
            const elementId = draggedElement.dataset.id;
            const elementType = draggedElement.dataset.type;
            let element = elementType === 'context' ? 
                contexts.find(c => c.id === elementId) : 
                tasks.find(t => t.id === elementId);
            
            if (element && checkCollision(element, x, y, elementWidth, elementHeight)) {
                const warning = document.getElementById('collisionWarning');
                warning.style.left = (x + elementWidth + 10) + 'px';
                warning.style.top = y + 'px';
                warning.style.display = 'block';
            } else {
                document.getElementById('collisionWarning').style.display = 'none';
            }
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
                    context.x = x;
                    context.y = y;
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
            
            // Hide indicators
            document.getElementById('snapIndicator').style.display = 'none';
            document.getElementById('collisionWarning').style.display = 'none';
            
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
                version: "2.0-drag-drop"
            };
            
            const dataStr = JSON.stringify(workflow, null, 2);
            const dataBlob = new Blob([dataStr], {type: 'application/json'});
            const url = URL.createObjectURL(dataBlob);
            
            const link = document.createElement('a');
            link.href = url;
            link.download = 'bpm_workflow_v2.json';
            link.click();
            
            URL.revokeObjectURL(url);
        }

        // Grid and snap controls
        document.getElementById('showGrid').addEventListener('change', function(e) {
            showGrid = e.target.checked;
            document.getElementById('gridOverlay').style.display = showGrid ? 'block' : 'none';
        });

        document.getElementById('snapToGrid').addEventListener('change', function(e) {
            snapToGrid = e.target.checked;
        });

        // Initialize with sample data
        function initializeSample() {
            // Add sample contexts with proper spacing
            contexts.push({
                id: 'ctx1',
                name: 'Data Processing',
                color: '#e6f3ff',
                x: 60,
                y: 60,
                width: 220,
                height: 160
            });
            
            contexts.push({
                id: 'ctx2',
                name: 'Quality Control',
                color: '#fff2e6',
                x: 320,
                y: 60,
                width: 220,
                height: 160
            });
            
            contexts.push({
                id: 'ctx3',
                name: 'Output Generation',
                color: '#f0fff0',
                x: 580,
                y: 60,
                width: 220,
                height: 160
            });
            
            // Add sample tasks with proper positioning
            tasks.push({
                id: 'task1',
                name: 'Initialize',
                status: 'success',
                contextId: 'ctx1',
                x: 80,
                y: 120
            });
            
            tasks.push({
                id: 'task2',
                name: 'Process Data',
                status: 'default',
                contextId: 'ctx1',
                x: 180,
                y: 120
            });
            
            tasks.push({
                id: 'task3',
                name: 'Validate',
                status: 'success',
                contextId: 'ctx1',
                x: 80,
                y: 170
            });
            
            tasks.push({
                id: 'task4',
                name: 'Quality Check',
                status: 'delayed',
                contextId: 'ctx2',
                x: 340,
                y: 120
            });
            
            tasks.push({
                id: 'task5',
                name: 'Review',
                status: 'default',
                contextId: 'ctx2',
                x: 440,
                y: 120
            });
            
            tasks.push({
                id: 'task6',
                name: 'Generate Report',
                status: 'default',
                contextId: 'ctx3',
                x: 600,
                y: 120
            });
            
            // Add sample connections
            connections.push({
                id: 'conn1',
                sourceId: 'task1',
                targetId: 'task2'
            });
            
            connections.push({
                id: 'conn2',
                sourceId: 'task2',
                targetId: 'task4'
            });
            
            connections.push({
                id: 'conn3',
                sourceId: 'task4',
                targetId: 'task6'
            });
            
            nextId = 20; // Start IDs after sample data
            
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
        
        response = {"status": "success", "message": "BPM Tool with Drag & Drop is working!"}
        self.wfile.write(json.dumps(response).encode())