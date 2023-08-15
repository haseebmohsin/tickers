import { Outlet } from 'react-router-dom';
import './styles/App.css';
import ToastProvider from './providers/ToastProvider';

function App() {
  return (
    <>
      {/* Main content area */}
      <div className=''>
        <ToastProvider />

        <Outlet />
      </div>
    </>
  );
}

export default App;
