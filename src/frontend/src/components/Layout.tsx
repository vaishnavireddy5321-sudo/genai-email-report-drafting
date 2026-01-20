/**
 * Layout component with navigation
 */

import { Link, useLocation } from 'react-router-dom';
import { useAppDispatch, useAppSelector } from '../store/hooks';
import { logout } from '../store/authSlice';

interface LayoutProps {
  children: React.ReactNode;
}

export default function Layout({ children }: LayoutProps) {
  const location = useLocation();
  const dispatch = useAppDispatch();
  const { user } = useAppSelector((state) => state.auth);

  const handleLogout = () => {
    dispatch(logout());
    window.location.href = '/';
  };

  const isActive = (path: string) => location.pathname === path;

  return (
    <div className="min-h-screen bg-slate-50 flex flex-col">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-slate-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center gap-8">
              <Link to="/" className="flex items-center gap-2">
                <div className="w-8 h-8 bg-linear-to-br from-primary-500 to-purple-500 rounded-lg"></div>
                <span className="font-bold text-slate-900 hidden sm:inline">GenAI Drafting</span>
              </Link>

              <nav className="hidden md:flex gap-1">
                <Link
                  to="/app/email"
                  className={`px-4 py-2 rounded-lg font-medium transition ${isActive('/app/email')
                      ? 'bg-primary-50 text-primary-700'
                      : 'text-slate-600 hover:bg-slate-100'
                    }`}
                >
                  Email
                </Link>
                <Link
                  to="/app/report"
                  className={`px-4 py-2 rounded-lg font-medium transition ${isActive('/app/report')
                      ? 'bg-primary-50 text-primary-700'
                      : 'text-slate-600 hover:bg-slate-100'
                    }`}
                >
                  Report
                </Link>
                <Link
                  to="/app/history"
                  className={`px-4 py-2 rounded-lg font-medium transition ${isActive('/app/history')
                      ? 'bg-primary-50 text-primary-700'
                      : 'text-slate-600 hover:bg-slate-100'
                    }`}
                >
                  History
                </Link>
                {user?.role === 'ADMIN' && (
                  <Link
                    to="/app/admin"
                    className={`px-4 py-2 rounded-lg font-medium transition ${isActive('/app/admin')
                        ? 'bg-primary-50 text-primary-700'
                        : 'text-slate-600 hover:bg-slate-100'
                      }`}
                  >
                    Admin
                  </Link>
                )}
              </nav>
            </div>

            <div className="flex items-center gap-4">
              {user && (
                <div className="hidden sm:flex items-center gap-2">
                  <div className="w-8 h-8 bg-linear-to-br from-blue-400 to-indigo-500 rounded-full flex items-center justify-center text-white font-medium text-sm">
                    {user.username.charAt(0).toUpperCase()}
                  </div>
                  <span className="text-sm text-slate-700">{user.username}</span>
                </div>
              )}
              <button
                onClick={handleLogout}
                className="px-4 py-2 bg-slate-200 text-slate-700 rounded-lg font-medium hover:bg-slate-300 transition"
              >
                Logout
              </button>
            </div>
          </div>
        </div>

        {/* Mobile Navigation */}
        <nav className="md:hidden border-t border-slate-200 px-4 py-2 flex gap-1">
          <Link
            to="/app/email"
            className={`flex-1 px-3 py-2 rounded-lg font-medium text-center transition text-sm ${isActive('/app/email')
                ? 'bg-primary-50 text-primary-700'
                : 'text-slate-600 hover:bg-slate-100'
              }`}
          >
            Email
          </Link>
          <Link
            to="/app/report"
            className={`flex-1 px-3 py-2 rounded-lg font-medium text-center transition text-sm ${isActive('/app/report')
                ? 'bg-primary-50 text-primary-700'
                : 'text-slate-600 hover:bg-slate-100'
              }`}
          >
            Report
          </Link>
          <Link
            to="/app/history"
            className={`flex-1 px-3 py-2 rounded-lg font-medium text-center transition text-sm ${isActive('/app/history')
                ? 'bg-primary-50 text-primary-700'
                : 'text-slate-600 hover:bg-slate-100'
              }`}
          >
            History
          </Link>
          {user?.role === 'ADMIN' && (
            <Link
              to="/app/admin"
              className={`flex-1 px-3 py-2 rounded-lg font-medium text-center transition text-sm ${isActive('/app/admin')
                  ? 'bg-primary-50 text-primary-700'
                  : 'text-slate-600 hover:bg-slate-100'
                }`}
            >
              Admin
            </Link>
          )}
        </nav>
      </header>

      {/* Main Content */}
      <main id="main-content" className="flex-1 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 w-full">
        {children}
      </main>

      {/* Footer */}
      <footer className="bg-slate-700 border-t border-slate-600">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 text-center text-sm text-white">
          &copy; {new Date().getFullYear()} GenAI Drafting. All rights reserved.
          <div className="text-xs text-white/80 mt-1">
            Batch 4 — Jyothi, Rishika, Sumasri, Vishnu
          </div>
        </div>
      </footer>
    </div>
  );
}
