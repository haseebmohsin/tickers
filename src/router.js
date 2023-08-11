import { createBrowserRouter } from 'react-router-dom';
import App from './App';
import ErrorPage from './features/ErrorPage';
import { Counter } from './features/counter/Counter';
import Login from './features/auth/Login';
import Register from './features/auth/Register';
import Home from './features/home/Home';

export const router = createBrowserRouter([
  {
    path: '/',
    element: <App />,
    errorElement: <ErrorPage />,
    children: [
      {
        index: true,
        element: <Home />,
      },
      {
        path: '/login',
        element: <Login />,
      },
      {
        path: '/register',
        element: <Register />,
      },

      // to be removed later
      {
        path: '/counter',
        element: <Counter />,
      },
    ],
  },
]);
