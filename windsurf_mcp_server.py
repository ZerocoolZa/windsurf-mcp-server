#!/usr/bin/env python3
import sys
import os
import json
import logging
from typing import Dict, Any

# Add system-wide site-packages to Python path
sys.path.append('/opt/homebrew/lib/python3.11/site-packages')
sys.path.append('/usr/local/lib/python3.11/site-packages')
sys.path.append(os.path.expanduser('~/.local/lib/python3.11/site-packages'))

# Add Cascade Tools directory to Python path
cascade_tools_path = '/Users/wws/pdf-ollama/CascadeProjects/windsurf-project/AI_GUI_PYQT6/M K Tender System/Cascade_Tools'
if cascade_tools_path not in sys.path:
    sys.path.insert(0, cascade_tools_path)

# Import Cascade core tools
from wayne_cascade_cli import CascadeCLI
from cascade_memory_injector import MemoryInjector
from cascade_quantum_db_intelligence_v2 import QuantumDatabaseIntelligence
from cascade_context_manager import ContextManager
from cascade_resource_manager import ResourceManager
from cascade_security_manager import SecurityManager

class WindsurfMCPServer:
    def __init__(self, config_path='/Users/wws/.codeium/windsurf/mcp_config.json'):
        # Load configuration
        with open(config_path, 'r') as config_file:
            self.config = json.load(config_file)
        
        # Robust logging configuration
        logging_config = self.config.get('logging', {})
        log_file = logging_config.get('file', '/Users/wws/.codeium/windsurf/mcp_server.log')
        log_level = logging_config.get('level', 'INFO')
        
        # Configure logging
        logging.basicConfig(
            level=getattr(logging, log_level.upper()),
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        
        # Initialize Cascade tools
        self.cascade_cli = CascadeCLI()
        self.memory_injector = MemoryInjector()
        self.quantum_db = QuantumDatabaseIntelligence()
        
        # Update context directory to match actual project structure
        context_directory = self.config.get('resources', {}).get(
            'context_directory', 
            '/Users/wws/pdf-ollama/CascadeProjects/windsurf-project/AI_GUI_PYQT6/M K Tender System/context'
        )
        
        # Initialize new tools
        self.context_manager = ContextManager(
            context_directory=context_directory
        )
        
        self.resource_manager = ResourceManager(self.config)
        
        self.security_manager = SecurityManager(
            config=self.config.get('security', {})
        )
        
        # Command registry
        self.command_registry = {
            'execute_cli': self._execute_cli_command,
            'inject_memory': self._inject_memory,
            'query_database': self._query_database,
            'retrieve_memories': self._retrieve_memories,
            'load_context': self._load_context,
            'save_context': self._save_context,
            'check_resources': self._check_resources,
            'allocate_resources': self._allocate_resources,
            'register_user': self._register_user,
            'authenticate_user': self._authenticate_user
        }
    
    def _execute_cli_command(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute CLI commands via Cascade CLI"""
        try:
            command = params.get('command', '')
            args = params.get('args', [])
            
            # For 'ls' command, use read_file for directory contents
            if command == 'ls':
                directory = args[0] if args else '.'
                files = os.listdir(directory)
                return {'status': 'success', 'result': files}
            
            # For 'read_file' command
            elif command == 'read_file':
                file_path = args[0] if args else None
                if not file_path:
                    return {'status': 'error', 'message': 'No file path provided'}
                content = self.cascade_cli.read_file(file_path)
                return {'status': 'success', 'result': content}
            
            # Default error for unsupported commands
            else:
                return {
                    'status': 'error', 
                    'message': f'Unsupported command: {command}'
                }
        except Exception as e:
            self.logger.error(f"CLI command error: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def _inject_memory(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Inject a memory into the Cascade memory system
        
        Args:
            params (Dict[str, Any]): Memory injection parameters
                - context (str): Context or name of the memory
                - data (Any): Memory content
                - tags (List[str], optional): Tags for memory categorization
        
        Returns:
            Dict[str, Any]: Injection result
        """
        try:
            context = params.get('context')
            data = params.get('data')
            tags = params.get('tags', [])
            
            if not context or data is None:
                return {
                    'status': 'error', 
                    'message': 'Context and data are required for memory injection'
                }
            
            # Inject memory
            self.memory_injector.inject_memory(
                context=context, 
                data=data, 
                tags=tags
            )
            
            return {
                'status': 'success', 
                'message': f'Memory injected for context: {context}',
                'details': {
                    'context': context,
                    'tags': tags
                }
            }
        except Exception as e:
            self.logger.error(f"Memory injection error: {e}")
            return {
                'status': 'error', 
                'message': str(e)
            }

    def _retrieve_memories(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Retrieve memories from the Cascade memory system
        
        Args:
            params (Dict[str, Any]): Memory retrieval parameters
                - tag (str, optional): Tag to filter memories
        
        Returns:
            Dict[str, Any]: Retrieved memories
        """
        try:
            tag = params.get('tag')
            memories = self.memory_injector.retrieve_memories(tag)
            
            return {
                'status': 'success',
                'memories': memories,
                'count': len(memories)
            }
        except Exception as e:
            self.logger.error(f"Memory retrieval error: {e}")
            return {
                'status': 'error', 
                'message': str(e)
            }

    def _query_database(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute quantum database query"""
        try:
            result = self.quantum_db.execute_query(
                params.get('query', {})
            )
            return {'status': 'success', 'result': result}
        except Exception as e:
            self.logger.error(f"Database query error: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def _load_context(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Load a context file
        
        Args:
            params (Dict[str, Any]): Context loading parameters
        
        Returns:
            Dict[str, Any]: Loaded context
        """
        try:
            context_name = params.get('context_name', 'default_context.json')
            context = self.context_manager.load_context(context_name)
            
            return {
                'status': 'success',
                'context': context
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def _save_context(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Save a context file
        
        Args:
            params (Dict[str, Any]): Context saving parameters
        
        Returns:
            Dict[str, Any]: Save operation result
        """
        try:
            context_data = params.get('context_data')
            context_name = params.get('context_name', 'custom_context.json')
            
            if not context_data:
                return {
                    'status': 'error',
                    'message': 'No context data provided'
                }
            
            self.context_manager.save_context(context_data, context_name)
            
            return {
                'status': 'success',
                'message': f'Context saved as {context_name}'
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def _check_resources(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Check current system resources
        
        Returns:
            Dict[str, Any]: System resource information
        """
        try:
            resources = self.resource_manager.check_system_resources()
            
            return {
                'status': 'success',
                'resources': resources
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def _allocate_resources(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Allocate resources based on requirements
        
        Args:
            params (Dict[str, Any]): Resource allocation requirements
        
        Returns:
            Dict[str, Any]: Resource allocation status
        """
        try:
            requirements = params.get('requirements', {})
            allocation_status = self.resource_manager.allocate_resources(requirements)
            
            return {
                'status': 'success',
                'allocation': allocation_status
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def _register_user(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Register a new user
        
        Args:
            params (Dict[str, Any]): User registration parameters
        
        Returns:
            Dict[str, Any]: User registration result
        """
        try:
            username = params.get('username')
            password = params.get('password')
            roles = params.get('roles', ['user'])
            
            if not username or not password:
                return {
                    'status': 'error',
                    'message': 'Username and password are required'
                }
            
            registration_result = self.security_manager.register_user(
                username, password, roles
            )
            
            return {
                'status': 'success' if registration_result else 'error',
                'message': 'User registered successfully' if registration_result else 'User registration failed'
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def _authenticate_user(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Authenticate a user
        
        Args:
            params (Dict[str, Any]): User authentication parameters
        
        Returns:
            Dict[str, Any]: User authentication result
        """
        try:
            username = params.get('username')
            password = params.get('password')
            
            if not username or not password:
                return {
                    'status': 'error',
                    'message': 'Username and password are required'
                }
            
            authentication_result = self.security_manager.authenticate_user(
                username, password
            )
            
            return {
                'status': 'success' if authentication_result else 'error',
                'message': 'Authentication successful' if authentication_result else 'Authentication failed'
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def execute(self, operation: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Central execution method"""
        if operation not in self.command_registry:
            error_msg = f"Unknown operation: {operation}"
            self.logger.error(error_msg)
            return {'status': 'error', 'message': error_msg}
        
        return self.command_registry[operation](params)

# HTTP Server Integration
from flask import Flask, request, jsonify
import threading

def create_http_server(mcp_server):
    app = Flask(__name__)
    
    @app.route('/execute', methods=['POST'])
    def execute_operation():
        data = request.json
        operation = data.get('operation')
        params = data.get('params', {})
        
        result = mcp_server.execute(operation, params)
        return jsonify(result)
    
    @app.route('/status', methods=['GET'])
    def server_status():
        return jsonify({
            'status': 'running',
            'server': 'Windsurf MCP Server',
            'version': '1.0.0'
        })
    
    return app

def run_server(mcp_server):
    app = create_http_server(mcp_server)
    host = 'localhost'
    port = 8001
    app.run(host=host, port=port)

if __name__ == "__main__":
    server = WindsurfMCPServer()
    run_server(server)
