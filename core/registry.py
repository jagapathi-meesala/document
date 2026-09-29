import os
import yaml
import importlib.util
import inspect
from typing import Dict, Any, Type, Optional
from contracts.tool_contract import ToolContract
from core.result import Result

class DynamicToolRegistry:
    def __init__(self, tools_dir: str = "tools"):
        self.tools_dir = tools_dir
        self.tools: Dict[str, ToolContract] = {}
        self.tool_definitions: Dict[str, Dict[str, Any]] = {}
        self.errors = []
        
    def discover(self):
        """Scans the tools directory for YAML definitions and Python implementations."""
        if not os.path.exists(self.tools_dir):
            self.errors.append(f"Tools directory '{self.tools_dir}' not found.")
            return

        for filename in os.listdir(self.tools_dir):
            if filename.endswith(".yaml"):
                tool_name = filename[:-5]
                yaml_path = os.path.join(self.tools_dir, filename)
                py_path = os.path.join(self.tools_dir, f"{tool_name}.py")
                
                if not os.path.exists(py_path):
                    self.errors.append(f"Implementation {py_path} missing for {filename}")
                    continue
                    
                self._register_tool(tool_name, yaml_path, py_path)

    def _register_tool(self, tool_name: str, yaml_path: str, py_path: str):
        try:
            with open(yaml_path, 'r', encoding='utf-8') as f:
                definition = yaml.safe_load(f)
                
            if not definition or "name" not in definition:
                self.errors.append(f"Invalid YAML schema in {yaml_path}")
                return
                
            if definition["name"] != tool_name:
                self.errors.append(f"Name mismatch in {yaml_path}: {definition['name']} != {tool_name}")
                return
                
            # Load the Python module
            spec = importlib.util.spec_from_file_location(f"tools.{tool_name}", py_path)
            if spec is None or spec.loader is None:
                self.errors.append(f"Failed to load module spec for {py_path}")
                return
                
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Find the ToolContract implementation
            tool_class = None
            for name, obj in inspect.getmembers(module, inspect.isclass):
                if issubclass(obj, ToolContract) and obj != ToolContract:
                    tool_class = obj
                    break
                    
            if not tool_class:
                self.errors.append(f"No ToolContract implementation found in {py_path}")
                return
                
            tool_instance = tool_class()
            if tool_instance.name() != tool_name:
                self.errors.append(f"Tool implementation name '{tool_instance.name()}' does not match '{tool_name}'")
                return
                
            self.tools[tool_name] = tool_instance
            self.tool_definitions[tool_name] = definition
            
        except Exception as e:
            self.errors.append(f"Error registering {tool_name}: {str(e)}")

    def get_tool(self, tool_name: str) -> Optional[ToolContract]:
        return self.tools.get(tool_name)
        
    def list_tools(self) -> list:
        return list(self.tools.keys())
        
    def execute_tool(self, tool_name: str, input_data: Dict[str, Any]) -> Result:
        tool = self.get_tool(tool_name)
        if not tool:
            return Result.fail(tool_name, "UNKNOWN_TOOL", f"Tool '{tool_name}' is not registered.")
            
        try:
            result_data = tool.execute(input_data)
            return Result.ok(tool_name, result_data)
        except ValueError as ve:
            return Result.fail(tool_name, "INVALID_INPUT", str(ve))
        except Exception as e:
            return Result.fail(tool_name, "TOOL_EXECUTION_ERROR", str(e))
