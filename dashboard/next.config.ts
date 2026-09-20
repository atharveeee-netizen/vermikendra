import withPWA from 'next-pwa';

const config = withPWA({
  dest: 'public',
  disable: process.env.NODE_ENV === 'development',
  register: true,
  skipWaiting: true,
})({
  // Next.js config options here
  reactStrictMode: true,
});

export default config;
