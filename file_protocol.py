import json
import logging
import shlex
import base64
from file_interface import FileInterface

class FileProtocol:
    def __init__(self):
        self.file = FileInterface()
        self.valid_commands = {
            'list': self.file.list,
            'get': self.file.get,
            'upload': self.file.upload,
            'delete': self.file.delete
        }

    def proses_string(self, command_str=''):
        logging.info(f"Received command: {command_str}")
        try:
            args = shlex.split(command_str)
            if not args:
                raise ValueError("Empty command string")
            
            command = args[0].strip().lower()
            if command not in self.valid_commands:
                raise ValueError(f"Unknown command: {command}")

            params = args[1:]
            result = self.valid_commands[command](params)

            return json.dumps(result)
        
        except ValueError as ve:
            logging.error(f"Invalid command: {str(ve)}")
            return json.dumps({'status': 'ERROR', 'data': f'Invalid command: {str(ve)}'})
        
        except Exception as e:
            logging.error(f"Error processing command: {str(e)}")
            return json.dumps({'status': 'ERROR', 'data': str(e)})

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    fp = FileProtocol()
    
    # Example commands
    print(fp.proses_string("list"))
    print(fp.proses_string("get pokijan.jpg"))
    print(fp.proses_string(f"upload test_upload.jpg {base64.b64encode(b'test content').decode()}"))
    print(fp.proses_string("delete test_upload.jpg"))
