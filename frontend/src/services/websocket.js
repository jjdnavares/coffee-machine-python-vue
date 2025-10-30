/**
 * WebSocket service for real-time updates from the coffee machine API.
 */
class WebSocketService {
  constructor() {
    this.ws = null;
    this.reconnectAttempts = 0;
    this.maxReconnectAttempts = 5;
    this.reconnectDelay = 3000;
    this.listeners = new Map();
    this.isConnecting = false;
    this.heartbeatInterval = null;
  }

  connect(url = null) {
    if (this.ws?.readyState === WebSocket.OPEN) {
      console.log('WebSocket already connected');
      return;
    }

    if (this.isConnecting) {
      console.log('WebSocket connection already in progress');
      return;
    }

    this.isConnecting = true;
    
    // Determine WebSocket URL from API URL environment variable
    console.log('VITE_API_URL in frontend =', import.meta.env.VITE_API_URL); // Added for live debug
    let wsUrl = url;
    if (!wsUrl) {
      const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';
      // Convert HTTP URL to WebSocket URL
      const apiUrlObj = new URL(apiUrl);
      const wsProtocol = apiUrlObj.protocol === 'https:' ? 'wss:' : 'ws:';
      // Replace /api with /api/v1/ws
      const basePath = apiUrlObj.pathname.replace(/\/api\/?$/, '/api/v1/ws');
      wsUrl = `${wsProtocol}//${apiUrlObj.host}${basePath}`;
    }

    console.log('Connecting to WebSocket:', wsUrl);

    try {
      this.ws = new WebSocket(wsUrl);

      this.ws.onopen = () => {
        console.log('WebSocket connected');
        this.isConnecting = false;
        this.reconnectAttempts = 0;
        this.emit('connected');
        
        // Start heartbeat
        this.startHeartbeat();
      };

      this.ws.onmessage = (event) => {
        try {
          const message = JSON.parse(event.data);
          console.log('WebSocket message:', message);
          
          // Emit message to listeners based on type
          this.emit(message.type, message);
          this.emit('message', message);
        } catch (error) {
          console.error('Error parsing WebSocket message:', error);
        }
      };

      this.ws.onerror = (error) => {
        console.error('WebSocket error:', error);
        this.isConnecting = false;
        this.emit('error', error);
      };

      this.ws.onclose = (event) => {
        console.log('WebSocket closed:', event.code, event.reason);
        this.isConnecting = false;
        this.stopHeartbeat();
        this.emit('disconnected');
        
        // Attempt to reconnect
        if (this.reconnectAttempts < this.maxReconnectAttempts) {
          this.reconnectAttempts++;
          console.log(`Reconnecting... Attempt ${this.reconnectAttempts}`);
          setTimeout(() => this.connect(), this.reconnectDelay);
        } else {
          console.error('Max reconnection attempts reached');
          this.emit('max_reconnect_attempts');
        }
      };
    } catch (error) {
      console.error('Error creating WebSocket:', error);
      this.isConnecting = false;
    }
  }

  disconnect() {
    if (this.ws) {
      this.reconnectAttempts = this.maxReconnectAttempts; // Prevent reconnect
      this.stopHeartbeat();
      this.ws.close();
      this.ws = null;
    }
  }

  send(message) {
    if (this.ws?.readyState === WebSocket.OPEN) {
      if (typeof message === 'string') {
        this.ws.send(message);
      } else {
        this.ws.send(JSON.stringify(message));
      }
    } else {
      console.error('WebSocket not connected');
    }
  }

  on(event, callback) {
    if (!this.listeners.has(event)) {
      this.listeners.set(event, []);
    }
    this.listeners.get(event).push(callback);
  }

  off(event, callback) {
    if (!this.listeners.has(event)) return;
    
    const callbacks = this.listeners.get(event);
    const index = callbacks.indexOf(callback);
    if (index > -1) {
      callbacks.splice(index, 1);
    }
  }

  emit(event, data) {
    if (!this.listeners.has(event)) return;
    
    this.listeners.get(event).forEach(callback => {
      try {
        callback(data);
      } catch (error) {
        console.error(`Error in listener for ${event}:`, error);
      }
    });
  }

  startHeartbeat() {
    this.heartbeatInterval = setInterval(() => {
      if (this.ws?.readyState === WebSocket.OPEN) {
        this.send('ping');
      }
    }, 30000); // Every 30 seconds
  }

  stopHeartbeat() {
    if (this.heartbeatInterval) {
      clearInterval(this.heartbeatInterval);
      this.heartbeatInterval = null;
    }
  }

  requestStatus() {
    this.send('request_status');
  }

  isConnected() {
    return this.ws?.readyState === WebSocket.OPEN;
  }
}

// Export singleton instance
export default new WebSocketService();

