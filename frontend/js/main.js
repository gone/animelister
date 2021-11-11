if (import.meta.env.MODE !== 'development') {
  import('vite/modulepreload-polyfill');
}
// Import our CSS
import '/css/app-base.css';
import '/css/app-components.css';
import '/css/app-utilities.css';
