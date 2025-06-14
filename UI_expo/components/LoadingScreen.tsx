import React, { useEffect } from 'react';
import { View, StyleSheet, Platform } from 'react-native';
import Animated, {
  useSharedValue,
  useAnimatedStyle,
  withRepeat,
  withSequence,
  withTiming,
  Easing,
} from 'react-native-reanimated';

export default function LoadingScreen() {
  const glowPosition = useSharedValue(-100);

  useEffect(() => {
    glowPosition.value = withRepeat(
      withTiming(100, {
        duration: 2000,
        easing: Easing.inOut(Easing.ease),
      }),
      -1,
      false
    );
  }, []);

  const animatedTextStyle = useAnimatedStyle(() => ({
    backgroundImage: Platform.select({
      web: `linear-gradient(
        90deg,
        #f4f3ee 0%,
        #f4f3ee 45%,
        #e0afa0 50%,
        #f4f3ee 55%,
        #f4f3ee 100%
      )`,
      default: 'none',
    }),
    backgroundSize: '200% 100%',
    backgroundPosition: `${glowPosition.value}% 0`,
    backgroundClip: 'text',
    WebkitBackgroundClip: 'text',
    color: Platform.OS === 'web' ? 'transparent' : '#f4f3ee',
    textShadow: Platform.select({
      web: '0 0 20px rgba(224, 175, 160, 0.5)',
      default: 'none',
    }),
  }));

  return (
    <View style={styles.container}>
      <Animated.Text style={[styles.text, animatedTextStyle]}>
        SignSpeak
      </Animated.Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    backgroundColor: '#463f3a',
    justifyContent: 'center',
    alignItems: 'center',
    zIndex: 1000,
  },
  text: {
    fontSize: 96,
    fontFamily: Platform.select({
      web: 'Times New Roman',
      default: 'serif',
    }),
    letterSpacing: 4,
    fontWeight: '700',
  },
});