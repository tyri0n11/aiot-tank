import type { RouteObject } from 'react-router-dom'
import HomePage from '../../pages/HomePage'
import LoginPage from '../../pages/LoginPage'
import SignupPage from '../../pages/SignupPage'
import MainPage from '../../pages/MainPage'
import NotFoundPage from '../../pages/NotFoundPage'
import ProtectedRoute from '../../src/components/ProtectedRoute'
import MainLayout from '../../layouts/MainLayout'
import AuthLayout from '../../layouts/AuthLayout'
const routes: RouteObject[] = [
  {
    element: <AuthLayout />,
    children: [
      { path: '/', element: <HomePage /> },
      { path: '/login', element: <LoginPage /> },
      { path: '/signup', element: <SignupPage /> },
    ],
  },
  {
    element: <MainLayout />,
    children: [
      {
        path: '/main',
        element: (
          <ProtectedRoute>
            <MainPage />
          </ProtectedRoute>
        ),
      },
    ],
  },
  { path: '*', element: <NotFoundPage /> },
]

export default routes
