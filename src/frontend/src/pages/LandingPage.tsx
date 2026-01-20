/**
 * Landing page component
 */

import { Link } from 'react-router-dom';
import { useAppSelector } from '../store/hooks';
import Layout from '../components/Layout';

export default function LandingPage() {
  const { isAuthenticated } = useAppSelector((state) => state.auth);

  const content = (
    <div className="space-y-16">
      <section className="text-center space-y-6">
        <h1 className="text-4xl sm:text-5xl font-bold text-slate-900">
          GenAI Email &amp; Report Drafting System
        </h1>
        <p className="text-slate-600 max-w-3xl mx-auto text-lg">
          An enterprise-grade application for generating professional emails and reports using Generative AI.
        </p>
      </section>

      <section className="max-w-4xl mx-auto text-center">
        <h2 className="text-2xl font-semibold text-slate-900">Problem Statement</h2>
        <p className="mt-4 text-slate-600">
          Professional communication is time-consuming, repetitive, and inconsistent. This system uses Generative AI to
          automate email and report drafting while maintaining security, auditability, and enterprise architecture principles.
        </p>
      </section>

      <section id="features" className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        {[
          'AI-powered Email & Report Generation',
          'N-Tier Architecture',
          'JWT Authentication & RBAC',
          'Prompt Engineering Strategy',
          'Document History & Audit Logs',
          'Secure, Scalable REST API',
        ].map((feature) => (
          <div key={feature} className="bg-white rounded-xl shadow-md p-6">
            <h3 className="text-lg font-semibold text-slate-900">{feature}</h3>
          </div>
        ))}
      </section>

      <section className="max-w-4xl mx-auto text-center">
        <h2 className="text-2xl font-semibold text-slate-900">Technology Stack</h2>
        <div className="mt-4 text-slate-600 space-y-2">
          <p>Frontend: React.js + TypeScript + Tailwind CSS</p>
          <p>Backend: Python (Flask) REST API</p>
          <p>Database: PostgreSQL</p>
          <p>AI Model: Google Gemini</p>
          <p>Security: JWT, Role-Based Access Control</p>
          <p>Architecture: N-Tier</p>
        </div>
      </section>

      <section className="max-w-4xl mx-auto text-center">
        <h2 className="text-2xl font-semibold text-slate-900">Architecture Overview</h2>
        <p className="mt-4 text-slate-600">
          Presentation Layer → Application Layer → Data Layer → AI Service Layer
        </p>
      </section>
    </div>
  );

  if (isAuthenticated) {
    return <Layout>{content}</Layout>;
  }

  return (
    <div className="min-h-screen bg-linear-to-br from-blue-50 via-indigo-50 to-purple-50">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-16 space-y-16">
        <header className="flex items-center justify-between">
          <Link to="/" className="flex items-center gap-3">
            <div className="w-8 h-8 bg-linear-to-br from-primary-500 to-purple-500 rounded-lg" />
            <span className="font-semibold text-slate-900">GenAI Drafting</span>
          </Link>
          <div className="flex items-center gap-3">
            <Link
              to="/login"
              className="bg-slate-200 text-slate-700 py-2 px-5 rounded-lg font-medium border border-slate-300 hover:bg-slate-300 hover:border-slate-400 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-slate-400 transition"
            >
              Login
            </Link>
            <Link
              to="/register"
              className="bg-white text-slate-700 py-2 px-5 rounded-lg font-medium border border-slate-300 hover:bg-slate-100 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-slate-400 transition"
            >
              Register
            </Link>
          </div>
        </header>

        {content}
      </div>
    </div>
  );
}
