/**
 * Vuetify plugin configuration with Material Design 3 theming
 */
import { createVuetify } from 'vuetify';
import * as components from 'vuetify/components';
import * as directives from 'vuetify/directives';
import '@mdi/font/css/materialdesignicons.css';
import 'vuetify/styles';

const vuetify = createVuetify({
  components,
  directives,
  theme: {
    defaultTheme: 'light',
    themes: {
      light: {
        dark: false,
        colors: {
          // Material Design 3 color tokens
          primary: '#8B4C39', // Rich coffee brown
          secondary: '#A0785A', // Complementary beige
          accent: '#D4A574', // Warm gold accent
          error: '#BA1A1A',
          info: '#00639A',
          success: '#006E1C',
          warning: '#975E00',
          // Surface colors
          surface: '#FFFBFE',
          'surface-bright': '#FFFBFE',
          'surface-variant': '#F3DECE',
          'on-surface': '#1C1B1F',
          'on-surface-variant': '#51443A',
          // Background
          background: '#FFFBFE',
          'on-background': '#1C1B1F',
          // Outline
          outline: '#85736B',
          'outline-variant': '#D9C6B6',
        },
      },
      dark: {
        dark: true,
        colors: {
          // Material Design 3 color tokens for dark theme
          // Improved contrast and readability
          primary: '#FFB79A', // Brighter, more vibrant coffee tone
          secondary: '#C9AA92', // Warm beige
          accent: '#FFC999', // Bright gold accent
          error: '#FEA4A4',
          info: '#70C8FF',
          success: '#6BCF7F',
          warning: '#FFB95F',
          // Surface colors - improved hierarchy
          surface: '#1E1E1E', // Slightly lighter than before for better contrast
          'surface-bright': '#2A2A2A', // For elevated elements
          'surface-variant': '#2D2820', // Warmer brown variant
          'on-surface': '#F5F5F5', // Higher contrast white
          'on-surface-variant': '#D9D9D9', // High contrast light grey
          // Background - warmer and more inviting
          background: '#121212', // True dark background
          'on-background': '#F5F5F5', // High contrast text
          // Outline - subtle but visible
          outline: '#757575', // Neutral grey for borders
          'outline-variant': '#5A5A5A', // Lighter variant
        },
      },
    },
  },
});

export default vuetify;

