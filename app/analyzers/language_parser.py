"""
Multi-language AST parser
"""
import ast
import re
from typing import Optional, Any, Dict, List


class LanguageParser:
    """Parse code into AST for different languages"""
    
    def __init__(self, code: str, language: str):
        """
        Initialize parser
        
        Args:
            code: Code snippet to parse
            language: Programming language
        """
        self.code = code
        self.language = language
        self.tree = None
        self.parse_error = None
    
    def parse(self) -> bool:
        """
        Parse code into AST
        
        Returns:
            True if parsing succeeded, False otherwise
        """
        try:
            if self.language == 'python':
                self.tree = ast.parse(self.code)
                return True
            elif self.language == 'javascript':
                return self._parse_javascript()
            elif self.language == 'java':
                return self._parse_java()
            else:
                self.parse_error = f"Unsupported language: {self.language}"
                return False
        except Exception as e:
            self.parse_error = str(e)
            return False
    
    def _parse_javascript(self) -> bool:
        """Parse JavaScript code"""
        try:
            import esprima
            self.tree = esprima.parseScript(self.code, {'loc': True, 'range': True})
            return True
        except ImportError:
            self.parse_error = "esprima not installed"
            return False
        except Exception as e:
            self.parse_error = f"JavaScript parse error: {str(e)}"
            return False
    
    def _parse_java(self) -> bool:
        """Parse Java code"""
        try:
            import javalang
            self.tree = javalang.parse.parse(self.code)
            return True
        except ImportError:
            self.parse_error = "javalang not installed"
            return False
        except Exception as e:
            self.parse_error = f"Java parse error: {str(e)}"
            return False
    
    def get_functions(self) -> List[Dict[str, Any]]:
        """
        Extract function definitions from AST
        
        Returns:
            List of function info dicts
        """
        functions = []
        
        if self.language == 'python' and self.tree:
            for node in ast.walk(self.tree):
                if isinstance(node, ast.FunctionDef):
                    functions.append({
                        'name': node.name,
                        'line': node.lineno,
                        'args': [arg.arg for arg in node.args.args]
                    })
        
        elif self.language == 'javascript' and self.tree:
            functions = self._extract_js_functions(self.tree)
        
        elif self.language == 'java' and self.tree:
            functions = self._extract_java_methods(self.tree)
        
        return functions
    
    def _extract_js_functions(self, node: Any, functions: Optional[List] = None) -> List[Dict[str, Any]]:
        """Extract JavaScript functions recursively"""
        if functions is None:
            functions = []
        
        if hasattr(node, 'type'):
            if node.type == 'FunctionDeclaration':
                functions.append({
                    'name': node.id.name if hasattr(node, 'id') and node.id else 'anonymous',
                    'line': node.loc.start.line if hasattr(node, 'loc') else 0,
                    'args': [param.name for param in node.params] if hasattr(node, 'params') else []
                })
        
        # Recursively process child nodes
        for key, value in node.__dict__.items():
            if isinstance(value, list):
                for item in value:
                    if hasattr(item, 'type'):
                        self._extract_js_functions(item, functions)
            elif hasattr(value, 'type'):
                self._extract_js_functions(value, functions)
        
        return functions
    
    def _extract_java_methods(self, tree: Any) -> List[Dict[str, Any]]:
        """Extract Java methods"""
        import javalang
        methods = []
        
        for path, node in tree:
            if isinstance(node, javalang.tree.MethodDeclaration):
                methods.append({
                    'name': node.name,
                    'line': node.position.line if hasattr(node, 'position') and node.position else 0,
                    'args': [param.name for param in node.parameters] if node.parameters else []
                })
        
        return methods
    
    def get_variables(self) -> List[Dict[str, Any]]:
        """
        Extract variable assignments from AST
        
        Returns:
            List of variable info dicts
        """
        variables = []
        
        if self.language == 'python' and self.tree:
            for node in ast.walk(self.tree):
                if isinstance(node, ast.Assign):
                    for target in node.targets:
                        if isinstance(target, ast.Name):
                            variables.append({
                                'name': target.id,
                                'line': node.lineno
                            })
        
        elif self.language == 'javascript' and self.tree:
            variables = self._extract_js_variables(self.tree)
        
        elif self.language == 'java' and self.tree:
            variables = self._extract_java_variables(self.tree)
        
        return variables
    
    def _extract_js_variables(self, node: Any, variables: Optional[List] = None) -> List[Dict[str, Any]]:
        """Extract JavaScript variables recursively"""
        if variables is None:
            variables = []
        
        if hasattr(node, 'type'):
            if node.type == 'VariableDeclaration':
                for declarator in node.declarations:
                    if hasattr(declarator, 'id') and hasattr(declarator.id, 'name'):
                        variables.append({
                            'name': declarator.id.name,
                            'line': node.loc.start.line if hasattr(node, 'loc') else 0
                        })
        
        # Recursively process child nodes
        for key, value in node.__dict__.items():
            if isinstance(value, list):
                for item in value:
                    if hasattr(item, 'type'):
                        self._extract_js_variables(item, variables)
            elif hasattr(value, 'type'):
                self._extract_js_variables(value, variables)
        
        return variables
    
    def _extract_java_variables(self, tree: Any) -> List[Dict[str, Any]]:
        """Extract Java variables"""
        import javalang
        variables = []
        
        for path, node in tree:
            if isinstance(node, javalang.tree.VariableDeclarator):
                variables.append({
                    'name': node.name,
                    'line': node.position.line if hasattr(node, 'position') and node.position else 0
                })
        
        return variables
    
    def get_imports(self) -> List[Dict[str, Any]]:
        """
        Extract import statements
        
        Returns:
            List of import info dicts
        """
        imports = []
        
        if self.language == 'python' and self.tree:
            for node in ast.walk(self.tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.append({
                            'name': alias.name,
                            'line': node.lineno
                        })
                elif isinstance(node, ast.ImportFrom):
                    imports.append({
                        'name': node.module or '',
                        'line': node.lineno
                    })
        
        return imports

# Made with Bob
