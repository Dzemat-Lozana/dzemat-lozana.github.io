/** @type {import('tailwindcss').Config} */
export const content = [
  './layouts/**/*.html',
  './content/**/*.md',
];
export const safelist = [
  // Add color variations for prayer cards
  'border-primary',
  'border-amber-500',
  'border-blue-500',
  'border-green-500',
  'border-indigo-500',
  'border-purple-500',
  'bg-primary/10',
  'bg-amber-50',
  'bg-blue-50',
  'bg-green-50',
  'bg-indigo-50',
  'bg-purple-50',
  'text-primary',
  'text-amber-600',
  'text-blue-600',
  'text-green-600',
  'text-indigo-600',
  'text-purple-600',
];
export const theme = {
  extend: {
    colors: {
      primary: {
        DEFAULT: '#2e74b5', // Blue from logo
        dark: '#235c92', // Darker blue
        light: '#4389c8', // Lighter blue
      },
      secondary: {
        DEFAULT: '#b99c6b', // Gold/tan from logo
        dark: '#9a8158', // Darker gold
        light: '#d1b98e', // Lighter gold
      },
      neutral: {
        50: '#F8FAFC',
        100: '#F1F5F9',
        200: '#E2E8F0',
        800: '#1E293B',
        900: '#0F172A',
      }
    },
    fontFamily: {
      sans: ['Inter', 'system-ui', 'sans-serif'],
      heading: ['Montserrat', 'sans-serif'],
    },
    container: {
      center: true,
      padding: {
        DEFAULT: '1rem',
        sm: '2rem',
        lg: '4rem',
        xl: '5rem',
      },
    },
    typography: {
      DEFAULT: {
        css: {
          'max-width': 'none',
          color: '#334155',
          h2: {
            fontWeight: '700',
            fontFamily: 'Montserrat, sans-serif',
            marginTop: '2em',
            marginBottom: '1em',
          },
          h3: {
            fontWeight: '600',
            fontFamily: 'Montserrat, sans-serif',
            marginTop: '1.5em',
            marginBottom: '0.75em',
          },
          'ul > li': {
            paddingLeft: '1.5em',
            '&::before': {
              backgroundColor: '#2e74b5', // Updated to match new primary color
            },
          },
          'ol > li': {
            paddingLeft: '1.5em',
            '&::before': {
              color: '#2e74b5', // Updated to match new primary color
              fontWeight: '600',
            },
          },
          a: {
            color: '#2e74b5', // Updated to match new primary color
            textDecoration: 'none',
            '&:hover': {
              color: '#235c92', // Updated to match new primary dark color
              textDecoration: 'underline',
            },
          },
          strong: {
            color: '#1E293B',
            fontWeight: '600',
          },
          hr: {
            borderColor: '#E2E8F0',
            marginTop: '2em',
            marginBottom: '2em',
          },
          blockquote: {
            fontStyle: 'normal',
            fontWeight: '500',
            color: '#1E293B',
            borderLeftColor: '#2e74b5', // Updated to match new primary color
            borderLeftWidth: '0.25rem',
            marginTop: '1.5em',
            marginBottom: '1.5em',
            paddingLeft: '1em',
          },
          'blockquote p:first-of-type::before': {
            content: 'none',
          },
          'blockquote p:last-of-type::after': {
            content: 'none',
          },
        },
      },
    },
  },
};
export const plugins = [
  require('@tailwindcss/typography'),
];