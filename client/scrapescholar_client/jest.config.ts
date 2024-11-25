import type { Config } from 'jest'
import nextJest from 'next/jest.js'

const createJestConfig = nextJest({
  dir: './',
})

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


   setupFilesAfterEnv: ['<rootDir>/jest.setup.ts'],
   testTimeout: 15000, 
}


export default createJestConfig(config)