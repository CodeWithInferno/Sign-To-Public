import React, { useState, useRef, useEffect } from 'react';
import { StyleSheet, View, Platform, Pressable, Alert } from 'react-native';
import { CameraView, CameraType, useCameraPermissions } from 'expo-camera';
import { useTheme } from '@/hooks/useThemeContext';
import ThemedText from './ThemedText';
import Button from './Button';
import { Camera, SwitchCamera, Megaphone, MegaphoneOff, Circle } from 'lucide-react-native';
import Layout from '@/constants/Layout';
import Animated, { 
  useSharedValue, 
  useAnimatedStyle, 
  withRepeat, 
  withTiming, 
  withSequence,
  Easing,
  cancelAnimation 
} from 'react-native-reanimated';
import { startRecording, stopRecording, processFrame } from '@/services/gestureService';

interface CameraWithOverlayProps {
  onTextRecognized: (text: string) => void;
  isProcessing: boolean;
  isRecording: boolean;
  onRecordingChange: (recording: boolean) => void;
}

// Frame capture interval in milliseconds
const FRAME_CAPTURE_INTERVAL = 500; // 2 frames per second

export default function CameraWithOverlay({ 
  onTextRecognized, 
  isProcessing,
  isRecording,
  onRecordingChange
}: CameraWithOverlayProps) {
  const [permission, requestPermission] = useCameraPermissions();
  const [facing, setFacing] = useState<CameraType>('front');
  const [audioEnabled, setAudioEnabled] = useState<boolean>(true);
  const [captureError, setCaptureError] = useState<string | null>(null);
  
  // Timer state
  const [elapsedTime, setElapsedTime] = useState<number>(0);
  const timerIntervalRef = useRef<NodeJS.Timeout | null>(null);
  
  // Reference to the camera
  const cameraRef = useRef<any>(null);
  
  // Timer for capturing frames
  const frameTimerRef = useRef<NodeJS.Timeout | null>(null);
  
  const recordingPulse = useSharedValue(1);

  // Handle recording state changes
  useEffect(() => {
    if (isRecording) {
      // Start the pulse animation
      recordingPulse.value = withRepeat(
        withSequence(
          withTiming(1.2, { duration: 1000, easing: Easing.inOut(Easing.ease) }),
          withTiming(1, { duration: 1000, easing: Easing.inOut(Easing.ease) })
        ),
        -1,
        true
      );
      
      // Start a new recording session
      startNewRecordingSession();
      
      // Start the timer
      setElapsedTime(0);
      timerIntervalRef.current = setInterval(() => {
        setElapsedTime(prev => prev + 1);
      }, 1000);
    } else {
      // Stop the pulse animation
      cancelAnimation(recordingPulse);
      recordingPulse.value = withTiming(1);
      
      // Stop the current recording session
      stopCurrentRecordingSession();
      
      // Stop the timer
      if (timerIntervalRef.current) {
        clearInterval(timerIntervalRef.current);
        timerIntervalRef.current = null;
      }
    }
    
    // Cleanup function
    return () => {
      if (frameTimerRef.current) {
        clearInterval(frameTimerRef.current);
        frameTimerRef.current = null;
      }
      
      if (timerIntervalRef.current) {
        clearInterval(timerIntervalRef.current);
        timerIntervalRef.current = null;
      }
    };
  }, [isRecording]);

  const animatedRecordingStyle = useAnimatedStyle(() => ({
    transform: [{ scale: recordingPulse.value }],
    opacity: withTiming(isRecording ? 1 : 0, { duration: 300 }),
  }));
  
  // Format seconds into MM:SS format
  const formatTime = (seconds: number): string => {
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;
    return `${minutes.toString().padStart(2, '0')}:${remainingSeconds.toString().padStart(2, '0')}`;
  };

  // Start a new recording session
  const startNewRecordingSession = async () => {
    try {
      // Start the recording on the server
      await startRecording({
        deviceType: Platform.OS,
        cameraFacing: facing,
        timestamp: new Date().toISOString(),
      });
      
      // Start capturing frames at regular intervals
      frameTimerRef.current = setInterval(captureFrame, FRAME_CAPTURE_INTERVAL);
      
      // Notify the user that recording has started
      onTextRecognized("Recording started. Sign language will be processed later.");
    } catch (error) {
      console.error('Failed to start recording:', error);
      setCaptureError('Failed to start recording');
      onRecordingChange(false); // Revert the recording state
    }
  };
  
  // Stop the current recording session
  const stopCurrentRecordingSession = async () => {
    // Clear the frame capture timer
    if (frameTimerRef.current) {
      clearInterval(frameTimerRef.current);
      frameTimerRef.current = null;
    }
    
    try {
      // Stop the recording on the server
      const result = await stopRecording();
      console.log('Recording stopped:', result);
      
      // Notify the user that recording has stopped
      onTextRecognized(`Recording stopped. ${result.frame_count} frames captured.`);
    } catch (error) {
      console.error('Failed to stop recording:', error);
      // Even if stopping fails, we still want to clear the local recording state
    }
  };
  
  // Capture a frame and send it to the server
  const captureFrame = async () => {
    if (!cameraRef.current || !isRecording) return;
    
    try {
      // Take a picture
      const photo = await cameraRef.current.takePictureAsync({ 
        quality: 0.5, // Lower quality to reduce data size
        base64: true,
        exif: false,
        skipProcessing: true
      });
      
      // Send the frame to the server
      await processFrame(photo.base64);
    } catch (error) {
      console.error('Error capturing frame:', error);
      setCaptureError('Error capturing frames');
    }
  };

  if (!permission) {
    return (
      <View style={[styles.container, { backgroundColor: '#463f3a' }]}>
        <ThemedText style={{ color: '#f4f3ee' }}>Requesting camera permission...</ThemedText>
      </View>
    );
  }

  if (!permission.granted) {
    return (
      <View style={[styles.container, { backgroundColor: '#463f3a' }]}>
        <ThemedText 
          variant="h3" 
          style={[styles.permissionText, { color: '#f4f3ee' }]}
        >
          We need your permission to use the camera
        </ThemedText>
        <Button 
          title="Grant Permission" 
          onPress={requestPermission} 
          variant="primary"
          size="large" 
          style={{ backgroundColor: '#e0afa0' }}
        />
      </View>
    );
  }

  const toggleCameraFacing = () => {
    setFacing(current => (current === 'front' ? 'back' : 'front'));
  };
  
  const toggleAudio = () => {
    setAudioEnabled(prev => !prev);
  };

  const toggleRecording = () => {
    // If there's a capture error, clear it when starting a new recording
    if (captureError && !isRecording) {
      setCaptureError(null);
    }
    
    onRecordingChange(!isRecording);
  };

  return (
    <View style={styles.container}>
      <CameraView 
        style={styles.camera} 
        facing={facing}
        ref={cameraRef}
      >
        <View style={styles.overlay}>
          <View style={[styles.header, { justifyContent: 'center' }]}>
            <ThemedText 
              variant="h3" 
              style={[styles.title, { color: '#f4f3ee', textAlign: 'center', width: '100%' }]}
            >
              Sign Language Translator
            </ThemedText>
            {isRecording && (
              <View style={[styles.recordingIndicator, { backgroundColor: '#463f3a' }]}>
                <Animated.View style={[styles.recordingDot, animatedRecordingStyle]} />
                <ThemedText style={[styles.recordingText, { color: '#f4f3ee' }]}>
                  Recording
                </ThemedText>
              </View>
            )}
            
            {/* Timer display */}
            <View style={[styles.timerContainer, { opacity: isRecording ? 1 : 0 }]}>
              <ThemedText style={[styles.timerText, { color: '#f4f3ee' }]}>
                {formatTime(elapsedTime)}
              </ThemedText>
            </View>
            
            {captureError && (
              <View style={[styles.errorIndicator, { backgroundColor: '#e76f51' }]}>
                <ThemedText style={[styles.errorText, { color: '#fff' }]}>
                  {captureError}
                </ThemedText>
              </View>
            )}
          </View>

          <View style={styles.controls}>
            <Pressable
              style={[styles.controlButton, { backgroundColor: '#bcb8b1' }]}
              onPress={toggleAudio}
            >
              {audioEnabled ? 
                <Megaphone size={24} color="#463f3a" /> : 
                <MegaphoneOff size={24} color="#463f3a" />
              }
            </Pressable>
            
            <Pressable
              style={[
                styles.recordButton,
                { borderColor: '#e0afa0' },
                isRecording && { backgroundColor: 'rgba(224, 175, 160, 0.2)' }
              ]}
              onPress={toggleRecording}
            >
              <Circle
                size={24}
                color={isRecording ? '#e0afa0' : '#f4f3ee'}
                fill={isRecording ? '#e0afa0' : 'transparent'}
              />
            </Pressable>
            
            <Pressable
              style={[styles.controlButton, { backgroundColor: '#bcb8b1' }]}
              onPress={toggleCameraFacing}
            >
              <SwitchCamera size={24} color="#463f3a" />
            </Pressable>
          </View>
        </View>
      </CameraView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#000',
    borderRadius: Layout.borderRadius.lg,
    overflow: 'hidden',
  },
  camera: {
    flex: 1,
  },
  overlay: {
    flex: 1,
    backgroundColor: 'rgba(0,0,0,0.4)',
    padding: Layout.spacing.lg,
    justifyContent: 'space-between',
  },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    marginBottom: Layout.spacing.md,
  },
  title: {
    textShadowColor: 'rgba(0,0,0,0.5)',
    textShadowOffset: { width: 0, height: 1 },
    textShadowRadius: 4,
  },
  recordingIndicator: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: Layout.spacing.md,
    paddingVertical: Layout.spacing.sm,
    borderRadius: Layout.borderRadius.full,
    position: 'absolute',
    top: 10 * 5,
    right: Layout.spacing.lg,
  },
  recordingDot: {
    width: 8,
    height: 8,
    borderRadius: 4,
    backgroundColor: '#e0afa0',
    marginRight: Layout.spacing.sm,
  },
  recordingText: {
    fontSize: 14,
    fontWeight: '500',
  },
  // Timer styles
  timerContainer: {
    paddingHorizontal: Layout.spacing.md,
    paddingVertical: Layout.spacing.sm,
    borderRadius: Layout.borderRadius.full,
    backgroundColor: '#463f3a',
    position: 'absolute',
    top: 10 * 5,
    left: Layout.spacing.lg,
  },
  timerText: {
    fontSize: 14,
    fontWeight: '500',
  },
  errorIndicator: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: Layout.spacing.md,
    paddingVertical: Layout.spacing.sm,
    borderRadius: Layout.borderRadius.full,
    position: 'absolute',
    bottom: -Layout.spacing.xl,
    alignSelf: 'center',
  },
  errorText: {
    fontSize: 14,
    fontWeight: '500',
  },
  controls: {
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'center',
    gap: Layout.spacing.xl,
    paddingBottom: Layout.spacing.xl,
  },
  controlButton: {
    width: 48,
    height: 48,
    borderRadius: 24,
    justifyContent: 'center',
    alignItems: 'center',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.25,
    shadowRadius: 3.84,
    elevation: 5,
  },
  recordButton: {
    width: 72,
    height: 72,
    borderRadius: 36,
    backgroundColor: 'rgba(244, 243, 238, 0.2)',
    borderWidth: 3,
    justifyContent: 'center',
    alignItems: 'center',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.25,
    shadowRadius: 3.84,
    elevation: 5,
  },
  permissionText: {
    textAlign: 'center',
    marginBottom: Layout.spacing.xl,
  },
});