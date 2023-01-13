import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

import { UserConfig } from 'vite'

export default defineConfig<UserConfig>({
  plugins: [react()],
  watch: ['src/**/*.txs', 'src/**/*.css']
})



