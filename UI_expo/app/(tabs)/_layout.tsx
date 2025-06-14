import React from 'react';
import { Tabs } from 'expo-router';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { useTheme } from '@/hooks/useThemeContext';
import { Camera, History, Settings, Info } from 'lucide-react-native';
import useCachedResources from '@/hooks/useCachedResources';
import { ThemeProvider } from '@/hooks/useThemeContext';
import { View, ActivityIndicator } from 'react-native';

export default function TabLayout() {
  const { colors, theme } = useTheme();
  const insets = useSafeAreaInsets();
  const { isLoadingComplete } = useCachedResources();

  if (!isLoadingComplete) {
    return (
      <View style={{ flex: 1, alignItems: 'center', justifyContent: 'center' }}>
        <ActivityIndicator color={colors.tint} size="large" />
      </View>
    );
  }

  return (
    <Tabs
      screenOptions={{
        tabBarActiveTintColor: colors.tint,
        tabBarInactiveTintColor: colors.tabIconDefault,
        tabBarStyle: {
          backgroundColor: colors.card,
          borderTopColor: colors.border,
          height: 70 + insets.bottom,
          paddingBottom: insets.bottom,
          paddingTop: 10,
        },
        tabBarLabelStyle: {
          fontFamily: 'Radley-Regular',
          fontSize: 14,
        },
        tabBarIconStyle: {
          width: 30,
          height: 30,
        },
        headerStyle: {
          backgroundColor: colors.card,
          shadowColor: 'transparent',
          borderBottomWidth: 1,
          borderBottomColor: colors.border,
        },
        headerTitleStyle: {
          fontFamily: 'Radley-Regular',
          color: colors.text,
          fontSize: 16,
        },
      }}
    >
      <Tabs.Screen
        name="index"
        options={{
          title: 'Translate',
          headerShown: false,
          tabBarIcon: ({ color }) => (
            <Camera size={28} color={color} />
          ),
        }}
      />
      <Tabs.Screen
        name="history"
        options={{
          title: 'History',
          headerShown: true,
          headerTitle: 'Translation History',
          tabBarIcon: ({ color }) => (
            <History size={28} color={color} />
          ),
        }}
      />
      <Tabs.Screen
        name="settings"
        options={{
          title: 'Settings',
          headerTitle: 'Settings',
          tabBarIcon: ({ color }) => (
            <Settings size={28} color={color} />
          ),
        }}
      />
    </Tabs>
  );
}

// Wrap the tab layout with the theme provider
export function RootLayoutNav() {
  return (
    <ThemeProvider>
      <TabLayout />
    </ThemeProvider>
  );
}