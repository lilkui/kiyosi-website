import DefaultTheme from 'vitepress/theme-without-fonts'
import '@fontsource-variable/geist'
import Layout from './Layout.vue'
import './style.css'

export default {
  extends: DefaultTheme,
  Layout,
}
