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
            grid-template-columns: 300px 1fr 250px;
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
        .style-panel {
            background: rgba(255, 255, 255, 0.95);
            color: #333;
            padding: 20px;
            border-radius: 10px;
            height: fit-content;
            border: 2px solid #ddd;
        }
        .color-grid {
            display: grid;
            grid-template-columns: repeat(6, 1fr);
            gap: 8px;
            margin: 10px 0;
        }
        .color-option {
            width: 30px;
            height: 30px;
            border-radius: 6px;
            cursor: pointer;
            border: 2px solid #333;
            transition: all 0.2s;
        }
        .color-option:hover {
            transform: scale(1.1);
            box-shadow: 0 2px 8px rgba(0,0,0,0.3);
        }
        .color-option.selected {
            border: 3px solid #4CAF50;
            transform: scale(1.15);
        }
        .style-section {
            margin-bottom: 20px;
            padding-bottom: 15px;
            border-bottom: 1px solid #eee;
        }
        .style-section h4 {
            margin: 0 0 10px 0;
            font-size: 14px;
            color: #333;
        }
        .stroke-width-options {
            display: flex;
            gap: 10px;
            margin: 10px 0;
        }
        .stroke-option {
            width: 40px;
            height: 20px;
            background: #333;
            cursor: pointer;
            border-radius: 3px;
            transition: all 0.2s;
        }
        .stroke-option:hover {
            background: #4CAF50;
        }
        .stroke-option.selected {
            background: #4CAF50;
            transform: scale(1.1);
        }
        .stroke-1 { height: 2px; }
        .stroke-2 { height: 4px; }
        .stroke-3 { height: 6px; }
        .pattern-options {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 8px;
            margin: 10px 0;
        }
        .pattern-option {
            width: 40px;
            height: 30px;
            border: 2px solid #333;
            cursor: pointer;
            border-radius: 4px;
            transition: all 0.2s;
        }
        .pattern-option:hover {
            border-color: #4CAF50;
        }
        .pattern-option.selected {
            border-color: #4CAF50;
            background: rgba(76, 175, 80, 0.2);
        }
        .selected-element-info {
            background: rgba(76, 175, 80, 0.1);
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 15px;
            border-left: 4px solid #4CAF50;
        }
        .spacing-control {
            display: flex;
            align-items: center;
            gap: 10px;
            margin: 10px 0;
        }
        .spacing-slider {
            flex: 1;
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
            position: relative;
            display: inline-block;
            white-space: nowrap;
            min-width: auto;
            width: auto;
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

            <div class="style-panel">
                <h3 style="margin-top: 0;">🎨 Style Panel</h3>
                
                <div id="selectedElementInfo" class="selected-element-info" style="display: none;">
                    <strong>Selected:</strong> <span id="selectedElementName">None</span><br>
                    <small>Click on a context or task to customize its appearance</small>
                </div>

                <div class="style-section">
                    <h4>🎯 Stroke Colors</h4>
                    <div class="color-grid" id="strokeColors">
                        <div class="color-option" style="background: #000000" data-color="#000000"></div>
                        <div class="color-option" style="background: #dc3545" data-color="#dc3545"></div>
                        <div class="color-option" style="background: #28a745" data-color="#28a745"></div>
                        <div class="color-option" style="background: #007bff" data-color="#007bff"></div>
                        <div class="color-option" style="background: #ffc107" data-color="#ffc107"></div>
                        <div class="color-option" style="background: #6f42c1" data-color="#6f42c1"></div>
                    </div>
                </div>

                <div class="style-section">
                    <h4>🎨 Background Colors</h4>
                    <div class="color-grid" id="backgroundColors">
                        <div class="color-option" style="background: #ffffff" data-color="#ffffff"></div>
                        <div class="color-option" style="background: #f8d7da" data-color="#f8d7da"></div>
                        <div class="color-option" style="background: #d4edda" data-color="#d4edda"></div>
                        <div class="color-option" style="background: #cce5ff" data-color="#cce5ff"></div>
                        <div class="color-option" style="background: #fff3cd" data-color="#fff3cd"></div>
                        <div class="color-option" style="background: #e2e3e5" data-color="#e2e3e5"></div>
                    </div>
                </div>

                <div class="style-section">
                    <h4>📏 Stroke Width</h4>
                    <div class="stroke-width-options">
                        <div class="stroke-option stroke-1" data-width="2"></div>
                        <div class="stroke-option stroke-2" data-width="4"></div>
                        <div class="stroke-option stroke-3" data-width="6"></div>
                    </div>
                </div>

                <div class="style-section">
                    <h4>📐 Task Spacing</h4>
                    <div class="spacing-control">
                        <label>Gap:</label>
                        <input type="range" id="taskSpacing" class="spacing-slider" min="10" max="50" value="20">
                        <span id="spacingValue">20px</span>
                    </div>
                </div>

                <div class="style-section">
                    <h4>🔧 Quick Actions</h4>
                    <button onclick="applyStyleToSelected()" class="secondary-btn" style="width: 100%; margin-bottom: 10px;">Apply Style</button>
                    <button onclick="resetStyles()" style="width: 100%; background: #6c757d;">Reset Styles</button>
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
        let selectedElement = null;
        let selectedElementType = null;
        let taskSpacing = 20;
        let currentStrokeColor = '#333333';
        let currentBackgroundColor = '#ffffff';
        let currentStrokeWidth = 2;

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
                div.style.backgroundColor = context.color || '#e6f3ff';
                div.style.borderColor = context.strokeColor || '#333333';
                div.style.borderWidth = (context.strokeWidth || 2) + 'px';
                div.dataset.id = context.id;
                div.dataset.type = 'context';
                
                const contextTasks = tasks.filter(t => t.contextId === context.id);
                div.innerHTML = `
                    <div class="context-label">${context.name}</div>
                    <div class="task-area">
                        <!-- Tasks will be positioned here -->
                    </div>
                `;
                
                // Add drag and click functionality
                div.addEventListener('mousedown', startDrag);
                div.addEventListener('click', function(e) {
                    e.stopPropagation();
                    selectElement(context.id, 'context');
                });
                canvas.appendChild(div);
            });

            // Render tasks
            tasks.forEach(task => {
                const div = document.createElement('div');
                div.className = `task-item task-${task.status}`;
                div.style.left = task.x + 'px';
                div.style.top = task.y + 'px';
                div.style.backgroundColor = task.color || getDefaultTaskColor(task.status);
                div.style.borderColor = task.strokeColor || '#333333';
                div.style.borderWidth = (task.strokeWidth || 2) + 'px';
                div.innerHTML = task.name;
                div.dataset.id = task.id;
                div.dataset.type = 'task';
                
                // Add drag and click functionality
                div.addEventListener('mousedown', startDrag);
                div.addEventListener('click', function(e) {
                    e.stopPropagation();
                    selectElement(task.id, 'task');
                });
                canvas.appendChild(div);
            });

            // After rendering, adjust task positions based on actual widths
            setTimeout(() => {
                adjustTaskSpacing();
            }, 10);

            // Add canvas click handler to deselect elements
            canvas.addEventListener('click', function(e) {
                if (e.target === canvas) {
                    selectedElement = null;
                    selectedElementType = null;
                    document.getElementById('selectedElementInfo').style.display = 'none';
                    document.querySelectorAll('.context-box, .task-item').forEach(el => {
                        el.style.outline = 'none';
                    });
                }
            });
        }

        function getDefaultTaskColor(status) {
            const colorMap = {
                'success': '#28a745',
                'failure': '#dc3545',
                'delayed': '#fd7e14',
                'skipped': '#6c757d',
                'default': '#ffffff'
            };
            return colorMap[status] || '#ffffff';
        }

        function adjustTaskSpacing() {
            contexts.forEach(context => {
                const contextTasks = tasks.filter(t => t.contextId === context.id);
                if (contextTasks.length <= 1) return;
                
                // Sort tasks by current x position
                contextTasks.sort((a, b) => a.x - b.x);
                
                let currentX = context.x + 180; // Start position after context label
                
                contextTasks.forEach((task, index) => {
                    const taskElement = document.querySelector(`[data-id="${task.id}"]`);
                    if (taskElement) {
                        task.x = currentX;
                        taskElement.style.left = task.x + 'px';
                        
                        // Get actual rendered width and add custom spacing
                        const actualWidth = taskElement.offsetWidth;
                        currentX += actualWidth + taskSpacing; // Use custom spacing
                    }
                });
            });
            
            // Re-render connections after position adjustment
            renderConnections();
        }

        function renderConnections() {
            // Remove existing connections
            const existingConnections = document.querySelectorAll('.connection-line, .connection-arrow');
            existingConnections.forEach(el => el.remove());
            
            // Re-render connections with updated positions
            connections.forEach(connection => {
                const sourceTask = tasks.find(t => t.id === connection.sourceId);
                const targetTask = tasks.find(t => t.id === connection.targetId);
                
                if (sourceTask && targetTask) {
                    const canvas = document.getElementById('canvas');
                    const sourceContext = contexts.find(c => c.id === sourceTask.contextId);
                    const targetContext = contexts.find(c => c.id === targetTask.contextId);
                    const isInterContext = sourceContext.id !== targetContext.id;
                    
                    const sourceElement = document.querySelector(`[data-id="${sourceTask.id}"]`);
                    const targetElement = document.querySelector(`[data-id="${targetTask.id}"]`);
                    
                    if (sourceElement && targetElement) {
                        const startX = sourceTask.x + (sourceElement.offsetWidth / 2);
                        const startY = sourceTask.y + 20;
                        const endX = targetTask.x;
                        const endY = targetTask.y + 20;
                        
                        if (isInterContext) {
                            // Inter-context connection with L-shape
                            const midY = sourceContext.y + sourceContext.height + 20;
                            
                            // Vertical line down
                            const verticalLine = document.createElement('div');
                            verticalLine.className = 'connection-line inter-context-connection';
                            verticalLine.style.left = startX + 'px';
                            verticalLine.style.top = startY + 'px';
                            verticalLine.style.width = '4px';
                            verticalLine.style.height = (midY - startY) + 'px';
                            canvas.appendChild(verticalLine);
                            
                            // Horizontal line
                            const horizontalLine = document.createElement('div');
                            horizontalLine.className = 'connection-line inter-context-connection';
                            horizontalLine.style.left = Math.min(startX, endX) + 'px';
                            horizontalLine.style.top = midY + 'px';
                            horizontalLine.style.width = Math.abs(endX - startX) + 'px';
                            horizontalLine.style.height = '4px';
                            canvas.appendChild(horizontalLine);
                            
                            // Vertical line up
                            const verticalLine2 = document.createElement('div');
                            verticalLine2.className = 'connection-line inter-context-connection';
                            verticalLine2.style.left = endX + 'px';
                            verticalLine2.style.top = midY + 'px';
                            verticalLine2.style.width = '4px';
                            verticalLine2.style.height = (endY - midY) + 'px';
                            canvas.appendChild(verticalLine2);
                            
                            // Arrow
                            const arrow = document.createElement('div');
                            arrow.className = 'connection-arrow inter-context-arrow';
                            arrow.style.left = (endX - 12) + 'px';
                            arrow.style.top = (endY - 6) + 'px';
                            canvas.appendChild(arrow);
                        } else {
                            // Direct horizontal connection
                            const line = document.createElement('div');
                            line.className = 'connection-line';
                            line.style.left = startX + 'px';
                            line.style.top = (startY - 2) + 'px';
                            line.style.width = Math.abs(endX - startX) + 'px';
                            canvas.appendChild(line);
                            
                            // Arrow
                            const arrow = document.createElement('div');
                            arrow.className = 'connection-arrow';
                            arrow.style.left = (endX - 12) + 'px';
                            arrow.style.top = (endY - 6) + 'px';
                            canvas.appendChild(arrow);
                        }
                    }
                }
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
            initializeStylePanel();
        });

        function initializeStylePanel() {
            // Stroke color selection
            document.querySelectorAll('#strokeColors .color-option').forEach(option => {
                option.addEventListener('click', function() {
                    document.querySelectorAll('#strokeColors .color-option').forEach(o => o.classList.remove('selected'));
                    this.classList.add('selected');
                    currentStrokeColor = this.dataset.color;
                    if (selectedElement) {
                        applyStyleToSelected();
                    }
                });
            });

            // Background color selection
            document.querySelectorAll('#backgroundColors .color-option').forEach(option => {
                option.addEventListener('click', function() {
                    document.querySelectorAll('#backgroundColors .color-option').forEach(o => o.classList.remove('selected'));
                    this.classList.add('selected');
                    currentBackgroundColor = this.dataset.color;
                    if (selectedElement) {
                        applyStyleToSelected();
                    }
                });
            });

            // Stroke width selection
            document.querySelectorAll('.stroke-option').forEach(option => {
                option.addEventListener('click', function() {
                    document.querySelectorAll('.stroke-option').forEach(o => o.classList.remove('selected'));
                    this.classList.add('selected');
                    currentStrokeWidth = parseInt(this.dataset.width);
                    if (selectedElement) {
                        applyStyleToSelected();
                    }
                });
            });

            // Task spacing control
            document.getElementById('taskSpacing').addEventListener('input', function() {
                taskSpacing = parseInt(this.value);
                document.getElementById('spacingValue').textContent = taskSpacing + 'px';
                adjustTaskSpacing();
            });

            // Set default selections
            document.querySelector('#strokeColors .color-option[data-color="#000000"]').classList.add('selected');
            document.querySelector('#backgroundColors .color-option[data-color="#ffffff"]').classList.add('selected');
            document.querySelector('.stroke-option[data-width="2"]').classList.add('selected');
        }

        function selectElement(elementId, elementType) {
            selectedElement = elementId;
            selectedElementType = elementType;
            
            // Update selected element info
            const infoPanel = document.getElementById('selectedElementInfo');
            const nameSpan = document.getElementById('selectedElementName');
            
            if (elementType === 'context') {
                const context = contexts.find(c => c.id === elementId);
                nameSpan.textContent = `Context: ${context.name}`;
            } else if (elementType === 'task') {
                const task = tasks.find(t => t.id === elementId);
                nameSpan.textContent = `Task: ${task.name}`;
            }
            
            infoPanel.style.display = 'block';
            
            // Highlight selected element
            document.querySelectorAll('.context-box, .task-item').forEach(el => {
                el.style.outline = 'none';
            });
            
            const selectedEl = document.querySelector(`[data-id="${elementId}"]`);
            if (selectedEl) {
                selectedEl.style.outline = '3px solid #4CAF50';
            }
        }

        function applyStyleToSelected() {
            if (!selectedElement || !selectedElementType) return;
            
            if (selectedElementType === 'context') {
                const context = contexts.find(c => c.id === selectedElement);
                if (context) {
                    context.color = currentBackgroundColor;
                    context.strokeColor = currentStrokeColor;
                    context.strokeWidth = currentStrokeWidth;
                }
            } else if (selectedElementType === 'task') {
                const task = tasks.find(t => t.id === selectedElement);
                if (task) {
                    task.color = currentBackgroundColor;
                    task.strokeColor = currentStrokeColor;
                    task.strokeWidth = currentStrokeWidth;
                }
            }
            
            renderCanvas();
        }

        function resetStyles() {
            contexts.forEach(context => {
                context.color = '#e6f3ff';
                context.strokeColor = '#333333';
                context.strokeWidth = 2;
            });
            
            tasks.forEach(task => {
                task.color = '#ffffff';
                task.strokeColor = '#333333';
                task.strokeWidth = 2;
            });
            
            renderCanvas();
        }
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