import React from 'react';
import { Text, TextProps, StyleSheet } from 'react-native';
import { useTheme } from '@/hooks/useThemeContext';
import { typography } from '@/constants/Layout';

interface ThemedTextProps extends TextProps {
  variant?: 'h1' | 'h2' | 'h3' | 'h4' | 'body' | 'caption' | 'small';
  weight?: 'regular' | 'italic';
  color?: keyof typeof variantColors | string;
}

const variantColors = {
  primary: 'text',
  secondary: 'textSecondary',
  tint: 'tint',
  error: 'error',
  success: 'success',
};

export default function ThemedText({
  variant = 'body',
  weight = 'regular',
  color = 'primary',
  style,
  ...props
}: ThemedTextProps) {
  const { colors } = useTheme();
  
  const fontFamily = `Radley-${weight.charAt(0).toUpperCase() + weight.slice(1)}`;
  
  const getColorValue = () => {
    if (color in variantColors) {
      return colors[variantColors[color as keyof typeof variantColors]];
    }
    return color;
  };

  return (
    <Text
      style={[
        styles.baseText,
        styles[variant],
        { fontFamily, color: getColorValue() },
        style,
      ]}
      {...props}
    />
  );
}

const styles = StyleSheet.create({
  baseText: {
    fontSize: typography.size.md,
    lineHeight: typography.lineHeight.md,
  },
  h1: {
    fontSize: typography.size.xxxl,
    lineHeight: typography.lineHeight.xxxl,
    marginBottom: 16,
  },
  h2: {
    fontSize: typography.size.xxl,
    lineHeight: typography.lineHeight.xxl,
    marginBottom: 12,
  },
  h3: {
    fontSize: typography.size.xl,
    lineHeight: typography.lineHeight.xl,
    marginBottom: 8,
  },
  h4: {
    fontSize: typography.size.lg,
    lineHeight: typography.lineHeight.lg,
    marginBottom: 8,
  },
  body: {
    fontSize: typography.size.md,
    lineHeight: typography.lineHeight.md,
  },
  caption: {
    fontSize: typography.size.sm,
    lineHeight: typography.lineHeight.sm,
  },
  small: {
    fontSize: typography.size.xs,
    lineHeight: typography.lineHeight.xs,
  },
});