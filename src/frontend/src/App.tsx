import { useEffect } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { Provider } from 'react-redux';
import { store } from './store';
import { useAppDispatch, useAppSelector } from './store/hooks';
import { getProfile } from './store/authSlice';
import { getToken } from './api/client';

import Layout from './components/Layout';
import PrivateRoute from './components/PrivateRoute';
import AdminRoute from './components/AdminRoute';
import SkipNavigation from './components/SkipNavigation';
import Login from './pages/Login';
import Register from './pages/Register';
import LandingPage from './pages/LandingPage';
import EmailGenerator from './pages/EmailGenerator';
import ReportGenerator from './pages/ReportGenerator';
import History from './pages/History';
import AdminDashboard from './pages/AdminDashboard';

function AppContent() {
  const dispatch = useAppDispatch();
  const { isAuthenticated, loading } = useAppSelector((state) => state.auth);

  useEffect(() => {
    const token = getToken();
    if (token && !isAuthenticated) {
      dispatch(getProfile());
    }
  }, [dispatch, isAuthenticated]);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-slate-50">
        <div className="text-center">
          <div className="inline-block animate-spin rounded-full h-12 w-12 border-4 border-primary-500 border-t-transparent"></div>
          <p className="mt-4 text-slate-600">Loading...</p>
        </div>
      </div>
    );
  }

  return (
    <BrowserRouter>
      <SkipNavigation />
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/app" element={<Navigate to="/app/email" replace />} />
        <Route
          path="/app/email"
          element={
            <PrivateRoute>
              <Layout>
                <EmailGenerator />
              </Layout>
            </PrivateRoute>
          }
        />
        <Route
          path="/app/report"
          element={
            <PrivateRoute>
              <Layout>
                <ReportGenerator />
              </Layout>
            </PrivateRoute>
          }
        />
        <Route
          path="/app/history"
          element={
            <PrivateRoute>
              <Layout>
                <History />
              </Layout>
            </PrivateRoute>
          }
        />
        <Route
          path="/app/admin"
          element={
            <AdminRoute>
              <Layout>
                <AdminDashboard />
              </Layout>
            </AdminRoute>
          }
        />
      </Routes>
    </BrowserRouter>
  );
}

function App() {
  return (
    <Provider store={store}>
      <AppContent />
    </Provider>
  );
}

export default App;
