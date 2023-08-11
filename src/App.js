import { Outlet } from 'react-router-dom';
import './styles/App.css';

function App() {
  return (
    <>
      {/* Main content area */}
      <div className=''>
        <Outlet />
      </div>
    </>
  );
}

export default App;
