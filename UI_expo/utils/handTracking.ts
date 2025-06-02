import * as mp from '@mediapipe/hands';
import { Camera } from '@mediapipe/camera_utils';

interface HandLandmark {
  x: number;
  y: number;
  z: number;
}

interface HandTrackingResult {
  landmarks: HandLandmark[];
  handedness: 'Left' | 'Right';
  confidence: number;
}

class HandTracker {
  private hands: mp.Hands;
  private camera: Camera | null = null;
  private onResultsCallback: ((results: HandTrackingResult[]) => void) | null = null;

  constructor() {
    this.hands = new mp.Hands({
      locateFile: (file) => {
        return `https://cdn.jsdelivr.net/npm/@mediapipe/hands/${file}`;
      }
    });

    this.hands.setOptions({
      maxNumHands: 2,
      modelComplexity: 1,
      minDetectionConfidence: 0.5,
      minTrackingConfidence: 0.5
    });

    this.hands.onResults(this.onResults.bind(this));
  }

  private onResults(results: mp.Results): void {
    if (!this.onResultsCallback) return;

    const handResults: HandTrackingResult[] = [];

    if (results.multiHandLandmarks) {
      for (let i = 0; i < results.multiHandLandmarks.length; i++) {
        const landmarks = results.multiHandLandmarks[i];
        const handedness = results.multiHandedness[i].label;
        const confidence = results.multiHandedness[i].score;

        handResults.push({
          landmarks: landmarks.map(landmark => ({
            x: landmark.x,
            y: landmark.y,
            z: landmark.z
          })),
          handedness: handedness as 'Left' | 'Right',
          confidence
        });
      }
    }

    this.onResultsCallback(handResults);
  }

  public startTracking(videoElement: HTMLVideoElement, callback: (results: HandTrackingResult[]) => void): void {
    this.onResultsCallback = callback;
    this.camera = new Camera(videoElement, {
      onFrame: async () => {
        await this.hands.send({ image: videoElement });
      },
      width: 1280,
      height: 720
    });
    this.camera.start();
  }

  public stopTracking(): void {
    if (this.camera) {
      this.camera.stop();
      this.camera = null;
    }
    this.onResultsCallback = null;
  }
}

export default HandTracker;
export type { HandLandmark, HandTrackingResult };