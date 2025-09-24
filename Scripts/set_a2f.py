import requests
import json
import logging
import time
from typing import Optional, Dict, Any

class A2FClient:
    def __init__(self, base_url: str = "http://localhost:8011", timeout: int = 30, players_available: Optional[str] = "/World/audio2face/Player"):
        print("inside A2FClient init")
        """
        Initialize the A2F (Audio2Face) API client
        
        Args:
            base_url (str): Base URL of the Kit services core API
            timeout (int): Request timeout in seconds
            players_available (str): Default player path
        """
        self.players_available=players_available
        self.base_url = base_url.rstrip('/')  # Remove trailing slash
        self.timeout = timeout
        self.headers = {
            'Content-Type': 'application/json'
        }
        
        # Set up logging
        self.logger = logging.getLogger(__name__)
    
    def _make_request(self, method: str, endpoint: str, payload: Optional[Dict[Any, Any]] = None) -> Optional[Dict[Any, Any]]:
        """
        Make a request to the API with common error handling
        
        Args:
            method (str): HTTP method (GET, POST, etc.)
            endpoint (str): API endpoint
            payload (dict, optional): Request payload
            
        Returns:
            dict: Response from the API or None if error
        """
        url = f"{self.base_url}{endpoint}"
        
        try:
            if method.upper() == 'GET':
                response = requests.get(url, headers=self.headers, timeout=self.timeout)
            elif method.upper() == 'POST':
                response = requests.post(
                    url, 
                    headers=self.headers, 
                    data=json.dumps(payload) if payload else None,
                    timeout=self.timeout
                )
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
                
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.Timeout:
            self.logger.error(f"Timeout error for {method} {endpoint}")
            return None
        except requests.exceptions.ConnectionError:
            self.logger.error(f"Connection error for {method} {endpoint}")
            return None
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error with {method} {endpoint}: {e}")
            if hasattr(e, 'response') and e.response is not None:
                self.logger.error(f"Response status: {e.response.status_code}")
                self.logger.error(f"Response text: {e.response.text}")
            return None
    
    def get_status(self) -> Optional[Dict[Any, Any]]:
        """
        Get the current status of the service
        
        Returns:
            dict: Response from the status endpoint
        """
        return self._make_request('GET', '/status')
    
    def load_usd_file(self, file_path: str) -> Optional[Dict[Any, Any]]:
        """
        Load a USD file into the stage
        
        Args:
            file_path (str): Path to the USD file to load
            
        Returns:
            dict: Response from the API
        """
        payload = {
            "file_name": file_path
        }
        return self._make_request('POST', '/A2F/USD/Load', payload)
    
    def set_root_path(self, a2f_player: str, dir_path: str) -> Optional[Dict[Any, Any]]:
        """
        Sets the root folder for the audio files
        
        Args:
            a2f_player (str): The A2F player identifier
            dir_path (str): Path to the directory containing audio files
            
        Returns:
            dict: Response from the API
        """
        payload = {
            "a2f_player": a2f_player,
            "dir_path": dir_path
        }
        print(f"Setting root path with payload: {payload}")
        return self._make_request('POST', '/A2F/Player/SetRootPath', payload)
    
    def get_player_instance(self):
        return self._make_request('GET', '/A2F/Player/GetInstances')
    
    def set_track(self, a2f_player: str, file_name: str, time_range: Optional[list] = [0,-1]) -> Optional[Dict[Any, Any]]:
        """
        Set a track as the active audio track. Expects an audio filename within the root track folder.
        
        Args:
            a2f_player (str): The A2F player identifier
            file_name (str): Audio filename within the root track folder
            time_range (list, optional): Time range as [start, end] in seconds
            
        Returns:
            dict: Response from the API
        """
        payload = {
            "a2f_player": a2f_player,
            "file_name": file_name
        }
        
        if time_range is not None:
            payload["time_range"] = time_range
            
        return self._make_request('POST', '/A2F/Player/SetTrack', payload)
    
    def play_track(self, a2f_player: str) -> Optional[Dict[Any, Any]]:
        """
        Starts playing the current track
        
        Args:
            a2f_player (str): The A2F player identifier
            
        Returns:
            dict: Response from the API
        """
        payload = {
            "a2f_player": a2f_player
        }
        return self._make_request('POST', '/A2F/Player/Play', payload)
    
    def get_stream_livelink_nodes(self) -> Optional[Dict[Any, Any]]:
        """
        Lists the existing StreamLiveLink nodes in the scene
        
        Returns:
            dict: Response from the API containing the list of StreamLiveLink nodes
        """
        return self._make_request('GET', '/A2F/Exporter/GetStreamLivelinkNodes')
    
    def activate_stream_livelink(self, node_path: str, value: bool = True) -> Optional[Dict[Any, Any]]:
        """
        Activate a StreamLiveLink node. The node will try connecting to host:port.
        
        Args:
            node_path (str): Path to the StreamLiveLink node
            value (bool): Whether to activate (True) or deactivate (False) the node
            
        Returns:
            dict: Response from the API
        """
        payload = {
            "node_path": node_path,
            "value": value
        }
        return self._make_request('POST', '/A2F/Exporter/ActivateStreamLivelink', payload)
    
    def is_stream_livelink_connected(self, node_path: str) -> Optional[Dict[Any, Any]]:
        """
        Get if the StreamLiveLink node is connected
        
        Args:
            node_path (str): Path to the StreamLiveLink node
            
        Returns:
            dict: Response from the API indicating connection status
        """
        payload = {
            "node_path": node_path
        }
        return self._make_request('POST', '/A2F/Exporter/IsStreamLivelinkConnected', payload)
    
    def get_stream_livelink_settings(self, node_path: str) -> Optional[Dict[Any, Any]]:
        """
        Get the setting values of the StreamLiveLink node
        
        Args:
            node_path (str): Path to the StreamLiveLink node
            
        Returns:
            dict: Response from the API containing the node settings
        """
        payload = {
            "node_path": node_path
        }
        return self._make_request('POST', '/A2F/Exporter/GetStreamLivelinkSettings', payload)
    
    def set_stream_livelink_settings(self, node_path: str, settings: Dict[str, Any]) -> Optional[Dict[Any, Any]]:
        """
        Set the setting values of the StreamLiveLink node
        
        Args:
            node_path (str): Path to the StreamLiveLink node
            settings (dict): Dictionary of setting-value pairs to configure the node
            
        Returns:
            dict: Response from the API
        """
        payload = {
            "node_path": node_path,
            "values": settings
        }
        return self._make_request('POST', '/A2F/Exporter/SetStreamLivelinkSettings', payload)



def wait_for_a2f(client, retries: int = 10, delay: int = 3) -> bool:
    """
    Wait for A2F service to be ready by retrying status check.

    Args:
        client (A2FClient): The API client
        retries (int): Maximum number of retries
        delay (int): Delay in seconds between retries

    Returns:
        bool: True if A2F is ready, False otherwise
    """
    for attempt in range(retries):
        status = client.get_status()
        print(f"status: {status}    ")
        if status == "OK":   # <-- safer check
            print(f"A2F is running (after {attempt+1} attempt(s))")
            return True
        print(f"A2F not ready yet... retrying ({attempt+1}/{retries})")
        time.sleep(delay)
    return False

    
client = A2FClient()

if __name__ == "__main__":
    if wait_for_a2f(client, retries=15, delay=2):
        
        usd_file_path = r"D:\af\claire_solved_arkit\claire_solved_arkit.usd"
        # Load USD file
        print(f"\nLoading USD file: {usd_file_path}")
        result = client.load_usd_file(usd_file_path)
        # Check if loading was successful
        if result:
            print(f"Success! Response: {result}")
        else:
            print("Failed to load USD file")
            
        
        # Get available players
        client.players_available = client.get_player_instance()['result']['regular'][0]
        print(f"Players available: {client.players_available}")

        # Activate StreamLiveLink node
        stream_node = client.get_stream_livelink_nodes()['result'][0]
        print(f"Response: {stream_node}")
        activate_stream_node = client.activate_stream_livelink(stream_node)
        status = client.is_stream_livelink_connected(stream_node)
        
         # Check connection status
        if status:
            print("Stream node is activated")
        else:
            print("Stream node is not activated")
        print(f"Activate stream node: {activate_stream_node}")
        
        # Get and set StreamNode settings
        current_settings = client.get_stream_livelink_settings(stream_node)
        print(current_settings)
        client.set_stream_livelink_settings(stream_node, {"enable_audio": True})
        print(f'Set StreamNode Settings')
        
        # set root path
        root_path_result = client.set_root_path(client.players_available, "D:/Avatar/audios")
        print(root_path_result)
        
    else:
        print("A2F is not running at all")