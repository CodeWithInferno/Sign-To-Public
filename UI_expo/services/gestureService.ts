import * as FileSystem from 'expo-file-system';
import { Platform, Alert } from 'react-native';

// Use different URLs for iOS simulator and Android emulator
const SERVER_URL = Platform.select({
  ios: 'http://localhost:5001',
  android: 'http://10.0.2.2:5001', // Special IP for Android emulator to access host machine
  default: 'http://localhost:5001'
});

// For debugging - log the server URL
console.log('Using server URL:', SERVER_URL);

// Interface for recording session
interface RecordingSession {
  sessionId: string;
  frameCount: number;
  isActive: boolean;
  metadata?: Record<string, any>;
}

// Current recording session
let currentSession: RecordingSession | null = null;

/**
 * Start a new recording session
 * @param metadata Optional metadata to associate with the recording
 * @returns Promise with the session information
 */
export async function startRecording(metadata: Record<string, any> = {}): Promise<RecordingSession> {
  try {
    console.log('Starting recording with metadata:', metadata);
    console.log('Connecting to server at:', SERVER_URL);
    
    // Check if we can reach the server
    try {
      const testResponse = await fetch(`${SERVER_URL}/recordings`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });
      
      if (!testResponse.ok) {
        throw new Error(`Server test failed with status: ${testResponse.status}`);
      }
      
      console.log('Server connection test successful');
    } catch (testError) {
      console.error('Server connection test failed:', testError);
      Alert.alert(
        'Server Connection Error',
        `Could not connect to the server at ${SERVER_URL}. Please check that the server is running and accessible.`,
        [{ text: 'OK' }]
      );
      throw new Error(`Server connection failed: ${testError.message}`);
    }
    
    const response = await fetch(`${SERVER_URL}/start-recording`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ metadata }),
    });

    if (!response.ok) {
      const errorText = await response.text();
      console.error('Server response error:', errorText);
      throw new Error(`Failed to start recording session: ${response.status} ${errorText}`);
    }

    const data = await response.json();
    console.log('Recording started successfully:', data);
    
    currentSession = {
      sessionId: data.session_id,
      frameCount: 0,
      isActive: true,
      metadata
    };

    return currentSession;
  } catch (error) {
    console.error('Error starting recording:', error);
    Alert.alert(
      'Recording Error',
      `Failed to start recording: ${error.message}`,
      [{ text: 'OK' }]
    );
    throw error;
  }
}

/**
 * Process a frame and send it to the server
 * @param frame Base64 encoded image data
 * @returns Promise with the processing results
 */
export async function processFrame(frame: string): Promise<any> {
  try {
    // If we have an active session, include the session ID
    const sessionData = currentSession ? { session_id: currentSession.sessionId } : {};
    
    const response = await fetch(`${SERVER_URL}/process-frame`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ 
        frame,
        ...sessionData
      }),
    });

    if (!response.ok) {
      const errorText = await response.text();
      console.error('Server response error:', errorText);
      throw new Error(`Server response was not ok: ${response.status} ${errorText}`);
    }

    const result = await response.json();
    
    // If this is part of a recording session, update the frame count
    if (currentSession && result.session_id === currentSession.sessionId) {
      currentSession.frameCount = result.frame_number + 1;
    }

    return result;
  } catch (error) {
    console.error('Error processing frame:', error);
    throw error;
  }
}

/**
 * Stop the current recording session
 * @returns Promise with the recording summary
 */
export async function stopRecording(): Promise<any> {
  if (!currentSession) {
    throw new Error('No active recording session');
  }

  try {
    const response = await fetch(`${SERVER_URL}/stop-recording`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ 
        session_id: currentSession.sessionId 
      }),
    });

    if (!response.ok) {
      const errorText = await response.text();
      console.error('Server response error:', errorText);
      throw new Error(`Failed to stop recording session: ${response.status} ${errorText}`);
    }

    const result = await response.json();
    console.log('Recording stopped successfully:', result);
    
    // Clear the current session
    const completedSession = { ...currentSession, isActive: false };
    currentSession = null;
    
    return {
      ...result,
      session: completedSession
    };
  } catch (error) {
    console.error('Error stopping recording:', error);
    Alert.alert(
      'Recording Error',
      `Failed to stop recording: ${error.message}`,
      [{ text: 'OK' }]
    );
    throw error;
  }
}

/**
 * Get the current recording session if one exists
 * @returns The current recording session or null
 */
export function getCurrentSession(): RecordingSession | null {
  return currentSession;
}

/**
 * List all available recordings
 * @returns Promise with the list of recordings
 */
export async function listRecordings(): Promise<any> {
  try {
    const response = await fetch(`${SERVER_URL}/recordings`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      const errorText = await response.text();
      console.error('Server response error:', errorText);
      throw new Error(`Failed to fetch recordings: ${response.status} ${errorText}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Error fetching recordings:', error);
    throw error;
  }
}