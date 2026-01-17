# 🔄 BPM Workflow Designer

A comprehensive **Business Process Management (BPM)** tool built with Python and Gradio that enables you to create, manage, and visualize complex workflows with an intuitive drag-and-drop interface.

![BPM Tool Demo](https://img.shields.io/badge/Status-Ready%20to%20Use-brightgreen)
![Python](https://img.shields.io/badge/Python-3.7%2B-blue)
![Gradio](https://img.shields.io/badge/Gradio-4.0%2B-orange)

## 🌟 Key Features

### 📊 Visual Workflow Design
- **Context Boxes**: Create organizational containers for related tasks
- **Task Management**: Add, edit, and manage individual workflow tasks
- **Visual Connections**: Connect tasks with curved arrows showing workflow dependencies
- **Multiple Connections**: Tasks can have multiple predecessors and successors
- **Auto-positioning**: Smart task placement within contexts

### 🎨 Customization & Styling
- **Color Coding System**:
  - 🟢 **Green**: Success (completed tasks)
  - 🔴 **Red**: Failure (failed tasks)
  - ⚫ **Grey**: Skipped (bypassed tasks)
  - 🟠 **Orange**: Delayed (pending tasks)
  - ⚪ **White**: Default (not started)
- **Custom Colors**: Set custom colors for both contexts and tasks
- **Responsive Design**: Clean, modern interface with visual feedback

### 🔧 Advanced Controls
- **Zoom Functionality**: Zoom in/out with slider control (0.3x to 3.0x)
- **Canvas Management**: Large workspace (1400x900) with grid background
- **Statistics Panel**: Real-time workflow statistics and task status counts
- **Drag & Drop**: Visual positioning of elements (coordinate-based)

### 💾 Data Management
- **Save/Load**: Export workflows to JSON files
- **Import/Export**: Share workflows between users
- **Sample Data**: Comes with example workflows
- **Data Persistence**: Maintains all connections and properties

## 🚀 Quick Start Guide

### Option 1: Automated Setup (Recommended)
1. **Download the project** to your computer
2. **Double-click `setup.bat`** - This will:
   - Create a virtual environment
   - Install all required packages
   - Set up everything automatically
3. **Double-click `run.bat`** to start the application
4. **Open your browser** to the displayed URL (usually `http://localhost:7860`)

### Option 2: Manual Setup
```bash
# 1. Create virtual environment
python -m venv bmp_env

# 2. Activate virtual environment
# On Windows:
bmp_env\Scripts\activate
# On Mac/Linux:
source bmp_env/bin/activate

# 3. Install dependencies
pip install gradio

# 4. Run the application
python enhanced_bpm_tool.py
```

## 📖 How to Use the BPM Tool

### 🏗️ Creating Your First Workflow

#### Step 1: Create Contexts (Process Containers)
1. **Enter Context Name**: e.g., "Data Processing", "Quality Control"
2. **Choose Color**: Select a background color for the context box
3. **Set Position**: Enter X,Y coordinates (or use defaults)
4. **Click "➕ Add Context"**

#### Step 2: Add Tasks to Contexts
1. **Enter Task Name**: e.g., "Validate Input", "Process Data"
2. **Select Parent Context**: Choose which context contains this task
3. **Set Task Status**: Choose from Default, Success, Failure, Skipped, or Delayed
4. **Custom Color** (optional): Override default status colors
5. **Position** (optional): Set specific X,Y coordinates or leave as 0,0 for auto-positioning
6. **Click "➕ Add Task"**

#### Step 3: Connect Tasks (Create Workflow)
1. **Select Source Task**: The task that comes first
2. **Select Target Task**: The task that follows
3. **Click "🔗 Connect"** to create a visual connection
4. **Repeat** to create complex workflows with multiple paths

### 🎛️ Using Advanced Features

#### Canvas Controls
- **🔍 Zoom Slider**: Adjust zoom level from 30% to 300%
- **📐 Fit to Screen**: Auto-adjust zoom to fit all elements
- **🔄 Reset Zoom**: Return to 100% zoom level

#### Task Management
- **Multiple Connections**: Each task can connect to multiple other tasks
- **Status Updates**: Change task status to reflect current state
- **Color Customization**: Override default colors for visual organization
- **Delete Tasks**: Remove tasks and their connections

#### File Operations
- **💾 Save**: Export your workflow to a JSON file
- **📂 Load**: Import a previously saved workflow
- **🗑️ Clear All**: Start fresh with an empty canvas

### 📊 Understanding the Statistics Panel
The stats panel shows real-time information:
- **📦 Contexts**: Number of process containers
- **⚙️ Tasks**: Total number of tasks
- **🔗 Connections**: Number of task relationships
- **Status Breakdown**: Count of tasks by status

## 🎯 Use Cases & Examples

### Business Process Modeling
- **Order Processing**: Model customer order workflows
- **Employee Onboarding**: Design HR processes
- **Quality Assurance**: Map testing and validation procedures
- **Project Management**: Visualize project phases and dependencies

### Software Development
- **CI/CD Pipelines**: Design deployment workflows
- **Code Review Process**: Map review and approval steps
- **Bug Tracking**: Model issue resolution workflows
- **Release Management**: Plan software release processes

### Example Workflow Scenarios

#### 1. E-commerce Order Processing
```
Context: "Order Management"
├── Task: "Receive Order" (Success)
├── Task: "Validate Payment" (Success)
├── Task: "Check Inventory" (Delayed)
└── Task: "Ship Product" (Default)

Context: "Customer Service"
├── Task: "Send Confirmation" (Success)
└── Task: "Handle Issues" (Skipped)
```

#### 2. Software Deployment Pipeline
```
Context: "Development"
├── Task: "Code Review" (Success)
├── Task: "Unit Tests" (Success)
└── Task: "Integration Tests" (Failure)

Context: "Production"
├── Task: "Deploy to Staging" (Skipped)
└── Task: "Deploy to Production" (Default)
```

## 📁 File Structure
```
BPM-Tool/
├── enhanced_bpm_tool.py      # Main application (recommended)
├── bpm_tool.py               # Basic version
├── setup.bat                 # Windows setup script
├── run.bat                   # Windows run script
├── requirements.txt          # Python dependencies
├── sample_workflow.json      # Example workflow
├── README.md                 # This file
└── bmp_env/                  # Virtual environment (created by setup)
```

## 🔧 Technical Details

### System Requirements
- **Python**: 3.7 or higher
- **Operating System**: Windows, macOS, or Linux
- **Memory**: 512MB RAM minimum
- **Browser**: Modern web browser (Chrome, Firefox, Safari, Edge)

### Dependencies
- **Gradio**: Web interface framework
- **JSON**: Data serialization (built-in)
- **UUID**: Unique identifier generation (built-in)
- **Dataclasses**: Data structure management (built-in)

### Architecture
- **Object-Oriented Design**: Clean, maintainable code structure
- **SVG Graphics**: Scalable vector graphics for crisp visuals
- **JSON Storage**: Human-readable data format
- **Web-Based Interface**: Accessible from any browser

## 🎨 Customization Options

### Adding New Task Statuses
```python
class TaskStatus(Enum):
    SUCCESS = "success"
    FAILURE = "failure" 
    SKIPPED = "skipped"
    DELAYED = "delayed"
    DEFAULT = "default"
    # Add your custom status here
    CUSTOM = "custom"
```

### Modifying Colors
```python
def get_status_color(self, status: TaskStatus) -> str:
    color_map = {
        TaskStatus.SUCCESS: "#28a745",  # Green
        TaskStatus.FAILURE: "#dc3545",  # Red
        TaskStatus.SKIPPED: "#6c757d",  # Grey
        TaskStatus.DELAYED: "#fd7e14",  # Orange
        TaskStatus.DEFAULT: "#ffffff",  # White
        # Add custom colors here
    }
    return color_map.get(status, "#ffffff")
```

### Canvas Size Adjustment
```python
def __init__(self):
    self.canvas_width = 1400   # Adjust width
    self.canvas_height = 900   # Adjust height
```

## 🐛 Troubleshooting

### Common Issues

#### "Module not found" Error
**Problem**: Python can't find Gradio
**Solution**: 
1. Make sure virtual environment is activated
2. Run: `pip install gradio`
3. Use the `setup.bat` script for automatic setup

#### Application Won't Start
**Problem**: Port already in use
**Solution**: 
1. Close other applications using port 7860
2. Or modify the launch command: `demo.launch(server_port=7861)`

#### Slow Performance
**Problem**: Large workflows are slow
**Solution**:
1. Reduce zoom level
2. Limit number of tasks per context
3. Use "Fit to Screen" for better overview

#### File Save/Load Issues
**Problem**: Can't save or load workflows
**Solution**:
1. Check file permissions in the directory
2. Ensure filename includes `.json` extension
3. Use full file paths if needed

### Getting Help
1. **Check the Console**: Look for error messages in the terminal
2. **Verify Setup**: Ensure all dependencies are installed
3. **Test with Sample**: Try loading `sample_workflow.json`
4. **Browser Console**: Check for JavaScript errors (F12)

## 🚀 Deployment Options

### Local Development
- Use `python enhanced_bpm_tool.py` for local testing
- Access via `http://localhost:7860`

### Network Sharing
```python
demo.launch(share=True)  # Creates public URL
```

### Docker Deployment
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY . .
RUN pip install gradio
EXPOSE 7860
CMD ["python", "enhanced_bmp_tool.py"]
```

## 🤝 Contributing

### Feature Requests
- Drag-and-drop positioning
- Real-time collaboration
- Export to other formats (PDF, PNG)
- Advanced workflow validation
- Integration with external systems

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- **Gradio Team**: For the excellent web interface framework
- **Python Community**: For the robust ecosystem
- **Contributors**: Everyone who helps improve this tool

---

**Ready to start designing workflows?** Run `setup.bat` and then `run.bat` to get started in minutes! 🚀