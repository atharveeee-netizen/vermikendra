// @ts-expect-error: no types available for next-pwa
import withPWA from 'next-pwa';

const config = withPWA({
  dest: 'public',
  disable: process.env.NODE_ENV === 'development',
  register: true,
  skipWaiting: true,
})({
  // Next.js config options here
  reactStrictMode: true,
  turbopack: {},
});

export default config;
