import type { Config } from 'jest'
import nextJest from 'next/jest.js'

const createJestConfig = nextJest({
  // Provide the path to your Next.js app to load next.config.js and .env files in your test environment
  dir: './',
})

// Add any custom config to be passed to Jest
const config: Config = {
  coverageProvider: 'v8',
  testEnvironment: 'jsdom',
  moduleNameMapper: {
    'd3': '<rootDir>/node_modules/d3/dist/d3.min.js',
  },
  testMatch: [
    "**/__tests__/unit/**/*.test.tsx",
    "**/__tests__/integration/**/*.test.tsx"
  ],

  // Add more setup options before each test is run
   setupFilesAfterEnv: ['<rootDir>/jest.setup.ts'],
   testTimeout: 15000, 
}

// createJestConfig is exported this way to ensure that next/jest can load the Next.js config which is async
export default createJestConfig(config)