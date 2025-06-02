import { useEffect, useState } from 'react';
import { useFonts } from 'expo-font';
import { Inter_400Regular, Inter_500Medium, Inter_600SemiBold, Inter_700Bold } from '@expo-google-fonts/inter';
import * as SplashScreen from 'expo-splash-screen';

export default function useCachedResources() {
  const [isLoadingComplete, setLoadingComplete] = useState(false);
  
  const [fontsLoaded] = useFonts({
    'Radley-Regular': 'https://fonts.gstatic.com/s/radley/v22/LYjDdGzinEIjCN1NpwNFh1gnVA.woff2',
    'Radley-Italic': 'https://fonts.gstatic.com/s/radley/v22/LYjBdGzinEIjCN1NojNHjV8FVtff.woff2',
  });

  // Load any resources or data that we need prior to rendering the app
  useEffect(() => {
    async function loadResourcesAndDataAsync() {
      try {
        // Keep the splash screen visible while we fetch resources
        await SplashScreen.preventAutoHideAsync();

        // Load any data or resources here
        // For example: API calls, local storage, etc.

      } catch (e) {
        // We might want to provide this error information to an error reporting service
        console.warn(e);
      } finally {
        setLoadingComplete(true);
        await SplashScreen.hideAsync();
      }
    }

    if (fontsLoaded) {
      loadResourcesAndDataAsync();
    }
  }, [fontsLoaded]);

  return {
    isLoadingComplete,
    fontsLoaded,
  };
}