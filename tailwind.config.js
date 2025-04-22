/** @type {import('tailwindcss').Config} */
export const content = [
  './layouts/**/*.html',
  './content/**/*.md',
];
export const safelist = [
  // Add color variations for prayer cards
  'border-teal-500',
  'border-amber-500',
  'border-blue-500',
  'border-green-500',
  'border-indigo-500',
  'border-purple-500',
  'bg-teal-50',
  'bg-amber-50',
  'bg-blue-50',
  'bg-green-50',
  'bg-indigo-50',
  'bg-purple-50',
  'text-teal-600',
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
        DEFAULT: '#0D9488', // teal-600
        dark: '#0F766E', // teal-700
        light: '#14B8A6', // teal-500
      },
      secondary: {
        DEFAULT: '#EAB308', // yellow-500
        dark: '#CA8A04', // yellow-600
        light: '#FDE047', // yellow-300
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
              backgroundColor: '#0D9488',
            },
          },
          'ol > li': {
            paddingLeft: '1.5em',
            '&::before': {
              color: '#0D9488',
              fontWeight: '600',
            },
          },
          a: {
            color: '#0D9488',
            textDecoration: 'none',
            '&:hover': {
              color: '#0F766E',
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
            borderLeftColor: '#0D9488',
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