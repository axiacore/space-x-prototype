const plugin = require('tailwindcss/plugin');

module.exports = {
    content: ['../../app/static/js/**/*.js', '../../templates/**/*.html'],
    theme: {
        container: {
            center: true,
        },
        fontFamily: {
            roboto: ['Roboto Flex', 'sans-serif'],
        },
        extend: {
            fontSize: {
                xs: ['0.625rem', '1.125rem'],
                sm: ['0.833rem', '1.25rem'],
                base: ['1rem', '1.7rem'],
                lg: ['1.2rem', '2rem'],
                xl: ['1.44rem', '2.125rem'],
                '2xl': ['1.728rem', '2.5rem'],
                '3xl': ['2.074rem', '2.813rem'],
                '4xl': ['2.488rem', '3.063rem'],
            },
            colors: {
                transparent: 'transparent',
                current: 'currentColor',
                black: '#000000',
                white: '#ffffff',
                spacex: {
                    primary: {
                        50: '#FFF5EF',
                        100: '#FEEADF',
                        200: '#FDD5BE',
                        300: '#FCB48C',
                        400: '#FA945B',
                        500: '#F97429',
                        600: '#E85807',
                        700: '#B74505',
                        800: '#853204',
                        900: '#542002',
                        950: '#220D01',
                    },
                    gray: {
                        50: '#FDFDFD',
                        100: '#F5F5F5',
                        200: '#DBDBDB',
                        300: '#C2C2C2',
                        400: '#A8A8A8',
                        500: '#8F8F8F',
                        600: '#757575',
                        700: '#5C5C5C',
                        800: '#424242',
                        900: '#292929',
                        950: '#0F0F0F',
                    },
                },
            },
            spacing: {
                'screen-px': 'var(--vh-in-px, 100vh)',
                '-1-px': '-1px',
                'px-2': '2px',
                'px-4': '4px',
                'px-6': '6px',
                'px-8': '8px',
            },
            gridTemplateRows: {
                16: 'repeat(16, minmax(0, 1fr))',
            },
            minHeight: {
                'screen-px': 'var(--vh-in-px, 100vh)',
            },
            zIndex: {
                1000: '1000',
                '-1': '-1',
            },
        },
    },
    plugins: [
        plugin(({ addUtilities, theme }) => {
            const newUtilities = {
                '.lazyload': { backgroundColor: theme('colors.gray.100') },
                '.lazyload-img': { transition: 'opacity .5s ease-in-out' },
                '.lazyload-hidden': { opacity: '0' },
                '.no-scroll': { height: '100vh' },
                '.no-scroll body': {
                    left: '0',
                    position: 'fixed',
                    width: '100%',
                    overflow: 'hidden',
                },
                '[x-cloak]': { display: 'none !important' },
            };
            addUtilities(newUtilities);
        }),
    ],
};
