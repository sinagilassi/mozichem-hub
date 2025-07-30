[![MseeP.ai Security Assessment Badge](https://mseep.net/pr/sinagilassi-mozichem-hub-badge.png)](https://mseep.ai/app/sinagilassi-mozichem-hub)

# MoziChem-Hub

![MoziChem Logo](https://drive.google.com/uc?export=view&id=1G-lxZzOBxX8UtKCvIqSoHfugIOxJw6ft)

![Downloads](https://img.shields.io/pypi/dm/mozichem-hub)
![PyPI Version](https://img.shields.io/pypi/v/mozichem-hub)
![Supported Python Versions](https://img.shields.io/pypi/pyversions/mozichem-hub.svg)
![License](https://img.shields.io/pypi/l/mozichem-hub)
[![FastAPI](https://img.shields.io/badge/FastAPI-Framework-green?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![MCP](https://img.shields.io/badge/Model_Context_Protocol-Compatible-orange)](https://modelcontextprotocol.io)

> 🚀 **A modular Python toolkit for building Model Context Protocol (MCP) modules focused on chemical engineering and chemistry applications.**

MoziChem-Hub empowers researchers, engineers, and developers to seamlessly expose core computational chemistry and process modeling tools as MCP servers, making them accessible through standardized APIs and enabling integration with modern AI workflows.

## 🆕 New Application Under Active Development

**MoziChem-Hub is a newly launched application** currently in active development with continuous improvements and enhancements being made regularly. As an emerging tool in chemical engineering ecosystem.

**Important:** MoziChem-Hub is built on top of **[FastMCP](https://github.com/jlowin/fastmcp)**, a powerful Python package that provides the core MCP (Model Context Protocol) functionality. FastMCP enables the seamless creation and deployment of MCP servers, making it the foundation that powers all MoziChem-Hub modules.

## ✨ What You Can Do

🔬 **Build MCP modules** for a comprehensive range of chemical engineering and chemistry calculations

⚡ **Deploy instantly** as REST APIs using FastAPI for production-ready applications

🌐 **Integrate universally** with any client ecosystem—cloud platforms, VS Code, custom GUIs, and more

## 🎯 Available MCP Modules

### 🧮 **eos-models-mcp**

Advanced thermodynamic property calculations using state-of-the-art equations of state (EOS) models:

- 💨 **Gas & liquid phase fugacity** calculations (gas, liquid, mixture)
- 🔄 **Mixture fugacity** analysis
- 📊 **EOS roots analysis** for components and mixtures

*Backed by: **PyThermoModels***

### ⚗️ **flash-calculations-mcp**

Comprehensive flash calculation suite supporting both ideal and non-ideal thermodynamic models:

- 🌡️ **Bubble & dew point** calculations
- ⚖️ **Flash equilibrium** computations and advanced flash calculations

*Backed by: **PyThermoFlash***

### 📚 **thermodynamic-properties-mcp**

Robust database integration for reliable thermodynamic data management:

- 🔍 **Component property lookup** from multiple data sources
- ✅ **Data availability verification** and validation

*Backed by: **PyThermoDB***

*Each module provides well-defined APIs optimized for LLMs, AI agents, and modern user interfaces.*

## 🚀 Flexible Deployment Options

### 🎯 **Client-Agnostic Design**

Deploy anywhere, integrate everywhere:

- 📝 **Local development** scripts
- ☁️ **Cloud environments** (AWS, Azure, GCP)
- 💻 **IDE integration** (VS Code, PyCharm)
- 🖥️ **Custom applications** and GUIs

## 🌟 Why Choose MoziChem-Hub?

Traditional LLMs and AI agents struggle to deliver **reliable, validated results** in chemistry and engineering without access to domain-specific computational tools.

**MoziChem-Hub bridges this critical gap** by:

✅ **Providing robust, field-tested** Python tools through standardized protocols

✅ **Enabling modern web API integration** for scalable applications

✅ **Supporting the next generation** of intelligent, trustworthy engineering applications


*Transform your chemical engineering workflows with the power of modern AI and reliable computational chemistry.*

## 🗺️ MoziChem-Hub System Architecture

The following diagram illustrates the high-level architecture of MoziChem-Hub and how its components interact:

![MoziChem-Hub Architecture](https://drive.google.com/uc?export=view&id=1BPpVS59ay5jgmZchWa95VCTK1YI8CdUy)

**Explanation:**

- **MoziChem-Hub** acts as the central hub, connecting various MCP modules (e.g., EOS models, flash calculations, property databases) and exposing them as standardized APIs.
- **MCP Modules** (top row) are individual computational tools or servers that implement the Model Context Protocol for specific domains (e.g., thermodynamics, property lookup).
- **PyThermoDB** provides a robust backend for thermodynamic data, which is accessed by MoziChem-Hub and MCP modules.
- **Reference** modules manage and validate data from multiple sources, ensuring reliable property lookups and calculations.
- **Client** applications (bottom right) such as Claude, VS Code, and Claude interact with MoziChem-Hub via MCP APIs, enabling seamless integration into AI workflows, IDEs, and automation tools.
- **External Data** (bottom left) can be incorporated through the Reference system, allowing for custom datasets and advanced data integration.

This architecture enables flexible, modular, and scalable deployment of chemical engineering tools, making them accessible to both humans and AI agents through modern interfaces.

## � MCP Client Integration

MoziChem-Hub modules can be seamlessly integrated with MCP-compatible clients like **Claude Desktop**, **VS Code**, and other AI applications that support the Model Context Protocol.

### 🖥️ **Claude Desktop Integration**

To use MoziChem-Hub modules with Claude Desktop, add the server configuration to your Claude configuration file:

**Windows:** `%APPDATA%\Claude\claude_desktop_config.json`
**macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "mozichem-eos-models": {
      "command": "uv",
      "args": [
        "--directory",
        "C:\\ABSOLUTE\\PATH",
        "run",
        "eos-models-mcp.py"
      ]
    },
    "mozichem-flash-calc": {
      "command": "uv",
      "args": [
        "--directory",
        "C:\\ABSOLUTE\\PATH",
        "run",
        "flash-calculations-mcp.py"
      ]
    },
    "mozichem-thermo-db": {
      "command": "uv",
      "args": [
        "--directory",
        "C:\\ABSOLUTE\\PATH",
        "run",
        "thermodynamic-properties-mcp.py"
      ]
    }
  }
}
```

### 🔧 **VS Code MCP Server Settings**

For VS Code integration, configure your MCP servers in the VS Code settings or workspace configuration:

```json
{
  "mcpServers": {
    "mozichem-hub": {
      "command": "uv",
      "args": [
        "--directory",
        "/absolute/path/",
        "run",
        "eos-models-mcp.py"
      ]
    }
  }
}
```

### ⚙️ **Configuration Options**

#### **Using UV (Recommended)**

The `uv` command provides fast, reliable Python environment management:

- **`--directory`**: Specifies the project directory containing `pyproject.toml`
- **`run`**: Executes the command in the project's virtual environment
- **Benefits**: Automatic dependency resolution, faster execution, isolated environment

#### **Alternative: Direct Python**

For systems without UV, use direct Python execution:

```json
{
  "mcpServers": {
    "mozichem-hub": {
      "command": "python",
      "args": ["/absolute/path/to/mozichem-hub/examples/mcp/eos-models-mcp.py"],
      "env": {
        "PYTHONPATH": "/absolute/path/to/mozichem-hub"
      }
    }
  }
}
```

### 📂 **Path Configuration**

**Important:** Always use **absolute paths** in MCP server configurations:

- ✅ **Windows**: `C:\\Users\\YourName\\Projects\\mozichem-hub`
- ✅ **macOS/Linux**: `/home/username/projects/mozichem-hub`
- ❌ **Relative paths**: `./mozichem-hub` or `~/mozichem-hub`

### 🚀 **Available MCP Modules for Client Integration**

- **`eos-models-mcp`**: Thermodynamic property calculations
  *Script Path*: `examples/mcp/eos-models-mcp.py`

- **`flash-calculations-mcp`**: Flash equilibrium computations
  *Script Path*: `examples/mcp/flash-calculations-mcp.py`

- **`thermodynamic-properties-mcp`**: Component property database
  *Script Path*: `examples/mcp/thermodynamic-properties-mcp.py`

### 🔍 **Verification**

After configuration, restart your MCP client. You should see the MoziChem-Hub tools available for:

- 🧮 **Thermodynamic calculations** (fugacity, phase equilibrium)
- ⚗️ **Flash calculations** (bubble/dew points, flash equilibrium)
- 📊 **Property lookups** (critical properties, molecular data)
- 🔬 **EOS model analysis** (equation of state computations)

*💡 **Tip**: Start with a single module first, then add additional modules as needed for your specific workflow.*

## 📋 Examples

MoziChem-Hub provides extensive examples to help you get started quickly. All examples are located in the `examples/` directory and demonstrate different usage patterns:

### 🚀 Quick Start Examples

#### 1. **Running MCP Servers**

Start an MCP server for thermodynamic calculations:

```python
from mozichem_hub import __version__
from mozichem_hub.prebuilt import create_mozichem_mcp

# Create an EOS models MCP server
eos_models_mcp = create_mozichem_mcp(name="eos-models-mcp")

# Run the server
if __name__ == "__main__":
    eos_models_mcp.run(transport='streamable-http')
```

*📁 See: [`examples/mcp/eos-models-mcp.py`](examples/mcp/eos-models-mcp.py)*

#### 2. **Direct Tool Execution**

Execute thermodynamic calculations directly without MCP server:

```python
from mozichem_hub.executors import ToolExecuter
from mozichem_hub.models import Temperature, Pressure, Component
from mozichem_hub.prebuilt import create_mozichem_mcp

# Create MCP and tool executor
thermo_models_mcp = create_mozichem_mcp(name="eos-models-mcp")
tool_executer = ToolExecuter(mozichem_mcp=thermo_models_mcp)

# Define calculation parameters
temperature = Temperature(value=300.1, unit="K")
pressure = Pressure(value=9.99, unit="bar")
component = Component(name="propane", formula="C3H8", state="g")

# Execute fugacity calculation
result = tool_executer.execute_tool(
    tool_name="calc_gas_component_fugacity",
    temperature=temperature,
    pressure=pressure,
    component=component,
    eos_model="SRK"
)
```

*📁 See: [`examples/execute/fugacity.py`](examples/execute/fugacity.py)*

#### 3. **REST API Deployment**

Deploy multiple MCP modules as a unified REST API:

```python
import uvicorn
from mozichem_hub import create_api, __version__
from mozichem_hub.prebuilt import create_mozichem_mcp

# Create MCP modules
eos_models_mcp = create_mozichem_mcp(name="eos-models-mcp")
flash_calculations_mcp = create_mozichem_mcp(name="flash-calculations-mcp")
thermodynamic_properties_mcp = create_mozichem_mcp(name="thermodynamic-properties-mcp")

# Create unified API
mcp_api = create_api(
    mcps=[eos_models_mcp, flash_calculations_mcp, thermodynamic_properties_mcp],
    title="MoziChem Hub API",
    description="API for MoziChem Hub with multiple MCPs.",
    version=__version__
)

# Run the API server
if __name__ == "__main__":
    uvicorn.run(mcp_api, host="127.0.0.1", port=8000)
```

*📁 See: [`examples/api/create-api.py`](examples/api/create-api.py)*

#### 4. **Creating Custom MCP Tools**

Build your own MCP server with custom functions using the `@app.tool` decorator:

```python
from mozichem_hub import __version__
from mozichem_hub.docs import MoziChemMCP
from rich import print

# Create a custom MCP server
app = MoziChemMCP(name="custom-tools-mcp")

# Define custom functions with @tool decorator
@app.tool(name="multiply")
def multiply(a: int, b: int) -> int:
    """
    Multiply two numbers.

    Parameters
    ----------
    a : int
        The first number.
    b : int
        The second number.

    Returns
    -------
    int
        The product of the two numbers.
    """
    return a * b

@app.tool(name="add")
def add(a: int, b: int) -> int:
    """
    Add two numbers.

    Parameters
    ----------
    a : int
        The first number.
    b : int
        The second number.

    Returns
    -------
    int
        The sum of the two numbers.
    """
    return a + b

# Run the custom MCP server
if __name__ == "__main__":
    app.run(transport="stdio")
    # Or use HTTP transport: app.run(transport="streamable-http", port=8000)
```

*📁 See: [`tests/custom_tools.py`](tests/custom_tools.py)*

This approach allows you to:

- 🛠️ **Define any Python function** as an MCP tool using the `@app.tool()` decorator
- 📝 **Provide detailed documentation** through docstrings that become part of the MCP tool description
- 🔧 **Use standard Python types** for parameters and return values with automatic validation
- 🚀 **Deploy instantly** via multiple transport options (stdio, HTTP, etc.)

### � **Custom References & External Data Integration**

MoziChem-Hub supports advanced integration with external thermodynamic databases using custom reference configurations. This powerful feature allows you to extend the built-in data with your own datasets or integrate with specialized databases.

#### 🔗 **PyThermoDB Integration**

The reference format is fully compatible with **[PyThermoDB](https://github.com/sinagilassi/PyThermoDB)**, a comprehensive Python package for thermodynamic property databases. This integration enables seamless access to extensive thermodynamic data collections.

#### 🛠️ **Adding Custom References**

You can convert your own CSV thermodynamic data (such as vapor pressure, critical constants, etc.) into a custom reference and use it in MoziChem-Hub. The process is as follows:

1. **Prepare your CSV files** with the required columns for each property (e.g., Name, Formula, State, C1, C2, Tmin, Tmax, etc.).

2. **Build a custom databook from CSV:**
   Use the script [`references/create-reference.py`](references/create-reference.py) to read your CSV files and create a PyThermoDB-compatible databook. This script demonstrates how to:
   - Add data tables and equation tables from CSV files using `ThermoDatabook`.
   - Build and save the databook as a YAML file (e.g., `custom-databook.yml`).

3. **Generate and load a custom reference:**
   Use [`references/load-custom-reference.py`](references/load-custom-reference.py) to:
   - Load the databook and build a `ThermoReference`.
   - Save the reference as `custom-references.yml`.
   - Initialize a thermodynamic database with your custom reference and access properties/equations for components.

4. **Integrate with MoziChem-Hub:**
   You can now use your custom reference YAML in MoziChem-Hub for calculations and lookups, either by direct use in your scripts or by updating MCP modules as shown in the examples above.


🔗 Reference Mapping Overview

This module ensures that all thermochemical properties (e.g., critical temperature, vapor pressure, heat capacity) used in calculations are traceable to their original reference sources. Data from `ThermoDB` is processed by `CompBuilder`, mapped to constant symbols (e.g., Tc, Cp_IG, VaPr), and made accessible in the application. These symbols are used consistently in sub-calculations, enabling transparency, validation, and scientific reliability.

![Reference Mapping](https://drive.google.com/uc?export=view&id=1A9qLjWWAYytLXeHeE3kZ3OpP7f7zqo1M)

*See the scripts in [`references/`](references/) for a complete, working example of this workflow.*

You can extend any MCP module with custom thermodynamic data using string-based reference definitions:

```python
from mozichem_hub.prebuilt import create_mozichem_mcp

# Create MCP server
eos_models_mcp = create_mozichem_mcp(name="eos-models-mcp")

# Define custom reference content (PyThermoDB format)
REFERENCE_CONTENT = """
REFERENCES:
    CUSTOM-REF-2:
      DATABOOK-ID: 1
      TABLES:
        vapor-pressure:
          TABLE-ID: 3
          DESCRIPTION:
            This table provides vapor pressure (P) in Pa as a function of temperature (T) in K.
          EQUATIONS:
            EQ-1:
              BODY:
                - res['vapor-pressure | VaPr | Pa'] = math.exp(parms['C1'] + parms['C2']/args['temperature'] + parms['C3']*math.log(args['temperature']))
          STRUCTURE:
            COLUMNS: [No.,Name,Formula,State,C1,C2,C3,Tmin,Tmax,Eq]
            SYMBOL: [None,None,None,None,C1,C2,C3,Tmin,Tmax,VaPr]
            UNIT: [None,None,None,None,1,1,1,K,K,Pa]
          VALUES:
            - [1,'propane','C3H8','g',59.078,-3492.6,-6.0669,85.47,369.83,1]
"""

# Define reference configuration
REFERENCE_CONFIG = """
# Configuration for all components
## ALL

vapor-pressure:
- databook: CUSTOM-REF-2
- table: vapor-pressure
- mode: EQUATIONS
- label: VaPr

general:
- databook: CUSTOM-REF-2
- table: general-data
- mode: DATA
- labels:
  - critical-pressure: Pc
  - critical-temperature: Tc
  - acentric-factor: AcFa
"""

# Apply custom references to MCP server
eos_models_mcp.update_references(
    reference_content=REFERENCE_CONTENT,
    reference_config=REFERENCE_CONFIG
)
```

#### 📋 **Reference Format Features**

- **📊 Multi-table support** - Define multiple data tables within a single reference
- **🧮 Equation-based data** - Support for mathematical correlations and equations
- **📈 Tabular data** - Direct data lookup from structured tables
- **🔄 Mixed modes** - Combine equations and tabular data as needed
- **🏷️ Flexible labeling** - Custom property labels and units
- **⚙️ Component-specific config** - Different references for different components

#### 🎯 **Use Cases**

- **🔬 Research data integration** - Incorporate experimental or literature data
- **📚 Specialized databases** - Connect to industry-specific property databases
- **🧪 Custom correlations** - Implement proprietary thermodynamic models
- **✅ Data validation** - Compare multiple data sources for accuracy verification

*📁 See complete example: [`examples/mcp/eos-models-mcp-with-reference.py`](examples/mcp/eos-models-mcp-with-reference.py)*

*📖 Learn more about PyThermoDB format: [PyThermoDB Documentation](https://github.com/sinagilassi/PyThermoDB)*

### �📚 Available Example Categories

#### 🔧 **Direct Execution Examples** (`examples/execute/`)

- **`fugacity.py`** - Gas and liquid phase fugacity calculations
- **`fugacity_mixture.py`** - Mixture fugacity analysis
- **`bubble-pressure.py`** - Bubble point pressure calculations
- **`bubble-temperature.py`** - Bubble point temperature calculations
- **`dew-pressure.py`** - Dew point pressure calculations
- **`dew-temperature.py`** - Dew point temperature calculations
- **`method-info.py`** - Tool information and metadata

#### 🌐 **MCP Server Examples** (`examples/mcp/`)

- **`eos-models-mcp.py`** - EOS models MCP server
- **`flash-calculations-mcp.py`** - Flash calculations MCP server
- **`thermodynamic-properties-mcp.py`** - Thermodynamic properties MCP server
- **`eos-models-mcp-with-reference.py`** - EOS models with custom references

#### ⚡ **API Deployment Examples** (`examples/api/`)

- **`create-api.py`** - Complete REST API deployment
- **`mcp-api.py`** - Single MCP API deployment
- **`eos-models-mcp.py`** - EOS-specific API

#### 📖 **Reference Configuration Examples** (`examples/references/`)

- **`reference-config.py`** - Custom thermodynamic database configuration
- **`reference-checker.py`** - Database availability verification
- **`doc1.py`** & **`doc2.py`** - Documentation examples

### 🔍 **Running the Examples**

1. **Clone the repository:**

   ```bash
   git clone https://github.com/sinagilassi/mozichem-hub
   cd mozichem-hub
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Run any example:**

   ```bash
   python examples/execute/fugacity.py
   python examples/mcp/eos-models-mcp.py
   python examples/api/create-api.py
   ```

*💡 Each example includes detailed comments and can be customized for your specific needs.*

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request to improve the project.

## 📝 License

This project is licensed under the MIT License. You are free to use, modify, and distribute this software in your own applications or projects. However, if you choose to use this app in another app or software, please ensure that my name, Sina Gilassi, remains credited as the original author. This includes retaining any references to the original repository or documentation where applicable. By doing so, you help acknowledge the effort and time invested in creating this project.

## ❓ FAQ

For any questions, contact me on [LinkedIn](https://www.linkedin.com/in/sina-gilassi/).

## 👨‍💻 Authors

- [@sinagilassi](https://www.github.com/sinagilassi)