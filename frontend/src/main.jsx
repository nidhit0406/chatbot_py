import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'
import { BrowserRouter } from 'react-router-dom'

const host = new URLSearchParams(window.location.search).get('host');

const config = {
  apiKey: import.meta.env.VITE_SHOPIFY_API_KEY,
  host,
  forceRedirect: true,
};
console.log('Shopify config:', config);
console.log(`${import.meta.env.VITE_APP_API_URL}/create-session`, "API URL");



createRoot(document.getElementById('root')).render(
  <StrictMode>
    <BrowserRouter config={config}><App /></BrowserRouter>
  </StrictMode>,
)
